/// Decentralized Identity using Web Crypto API (SubtleCrypto)
/// 100% browser-native, no external dependencies
/// Uses ECDSA P-256 for signing and verification
use sha2::{Sha256, Digest};
use serde::{Deserialize, Serialize};
use wasm_bindgen::prelude::*;
use wasm_bindgen_futures::JsFuture;
use web_sys::{window, CryptoKey, SubtleCrypto};
use js_sys::{Object, Reflect, Uint8Array, Array};

use crate::storage::LocalStorage;
use crate::indexed_db::IndexedDB;
use crate::passkey::PasskeyIdentity;

const PRIVATE_KEY_ID: &str = "aurora_private_key";

/// Identity type preference
#[derive(Debug, Clone, Copy)]
pub enum IdentityType {
    Passkey,      // WebAuthn/Passkey (hardware-backed, secure)
    LocalKey,     // ECDSA key in localStorage (simple but risky)
}

/// User identity (DID + Web Crypto keypair)
#[derive(Clone)]
pub struct Identity {
    did: String,
    public_key_jwk: String,  // JSON Web Key format for public key
    // Note: private key stored in IndexedDB, accessed only for signing
}

impl Identity {
    /// Create a new identity or load from storage
    /// Defaults to LocalKey if no type specified
    pub async fn new_or_load() -> Result<Self, String> {
        Self::new_or_load_with_type(IdentityType::LocalKey).await
    }

    /// Create a new identity or load from storage with specified type
    pub async fn new_or_load_with_type(identity_type: IdentityType) -> Result<Self, String> {
        let storage = LocalStorage::new()?;

        // Check for passkey identity first
        if let Ok(Some(_)) = storage.get("aurora_passkey_identity") {
            log::info!("Found passkey identity, loading...");
            return Self::load_passkey().await;
        }

        // Try to load existing local key identity
        if let Ok(Some(stored)) = storage.get("aurora_identity") {
            log::info!("Loading existing identity from storage...");
            return Self::from_stored(&stored).await;
        }

        // Create new identity based on requested type
        let identity = match identity_type {
            IdentityType::Passkey => {
                log::info!("Creating new passkey identity...");
                Self::generate_passkey().await?
            }
            IdentityType::LocalKey => {
                log::info!("Creating new local key identity...");
                let id = Self::generate_new().await?;
                
                // Store for future use
                let serialized = id.to_stored()?;
                storage.set("aurora_identity", &serialized)?;
                
                id
            }
        };

        Ok(identity)
    }
    
    /// Generate passkey-based identity
    async fn generate_passkey() -> Result<Self, String> {
        let passkey_identity = PasskeyIdentity::new_or_load().await?;
        
        // Convert to Identity format
        Ok(Identity {
            did: passkey_identity.did(),
            public_key_jwk: format!("{{\"passkey\":true}}"), // Placeholder
        })
    }
    
    /// Load passkey-based identity
    async fn load_passkey() -> Result<Self, String> {
        let passkey_identity = PasskeyIdentity::new_or_load().await?;
        
        Ok(Identity {
            did: passkey_identity.did(),
            public_key_jwk: format!("{{\"passkey\":true}}"),
        })
    }

    /// Generate a new ECDSA P-256 keypair using Web Crypto API
    async fn generate_new() -> Result<Self, String> {
        let subtle = Self::get_subtle_crypto()?;

        // Configure ECDSA P-256 key generation
        let algorithm = Object::new();
        Reflect::set(&algorithm, &"name".into(), &"ECDSA".into())
            .map_err(|_| "Failed to set algorithm name")?;
        Reflect::set(&algorithm, &"namedCurve".into(), &"P-256".into())
            .map_err(|_| "Failed to set curve")?;

        // Generate keypair (both extractable for IndexedDB storage)
        let key_usages = Array::new();
        key_usages.push(&"sign".into());
        key_usages.push(&"verify".into());

        let keypair_promise = subtle.generate_key_with_object(&algorithm, true, &key_usages)
            .map_err(|e| format!("Failed to generate key: {:?}", e))?;

        let keypair = JsFuture::from(keypair_promise).await
            .map_err(|e| format!("Key generation failed: {:?}", e))?;

        // Extract public and private keys
        let public_key = Reflect::get(&keypair, &"publicKey".into())
            .map_err(|_| "Failed to get public key")?;
        let public_key = CryptoKey::from(public_key);

        let private_key = Reflect::get(&keypair, &"privateKey".into())
            .map_err(|_| "Failed to get private key")?;
        let private_key = CryptoKey::from(private_key);

        // Export public key to JWK format
        let export_promise = subtle.export_key("jwk", &public_key)
            .map_err(|e| format!("Failed to export public key: {:?}", e))?;

        let jwk = JsFuture::from(export_promise).await
            .map_err(|e| format!("Export failed: {:?}", e))?;

        let public_key_jwk = js_sys::JSON::stringify(&jwk)
            .map_err(|_| "Failed to stringify JWK")?
            .as_string()
            .ok_or("JWK is not a string")?;

        // Store private key in IndexedDB
        let db = IndexedDB::open().await?;
        db.store_key(PRIVATE_KEY_ID, &private_key).await?;
        log::info!("Private key stored securely in IndexedDB");

        // Compute DID from public key
        let did = Self::compute_did_from_jwk(&public_key_jwk)?;

        log::info!("Generated new identity with DID: {}", did);

        Ok(Identity {
            did,
            public_key_jwk,
        })
    }

    /// Get the DID (Decentralized Identifier)
    pub fn did(&self) -> String {
        self.did.clone()
    }

    /// Get the public key in JWK format
    pub fn public_key_jwk(&self) -> String {
        self.public_key_jwk.clone()
    }

    /// Get the public key as hex string (for display/logging)
    pub fn public_key_hex(&self) -> String {
        // Extract x,y coordinates from JWK and encode as hex
        match Self::jwk_to_hex(&self.public_key_jwk) {
            Ok(hex) => hex,
            Err(e) => {
                log::warn!("Failed to convert JWK to hex: {}", e);
                "unknown".to_string()
            }
        }
    }

    /// Get peer ID for libp2p (derived from public key)
    pub fn peer_id(&self) -> String {
        // Use hash of public key for peer ID
        let hash = Self::hash_public_key(&self.public_key_jwk);
        format!("12D3KooW{}", hex::encode(&hash[..16]))
    }

    /// Sign a message using Web Crypto API with ECDSA P-256
    pub async fn sign(&self, message: &[u8]) -> Result<Vec<u8>, String> {
        let subtle = Self::get_subtle_crypto()?;

        // Retrieve private key from IndexedDB
        let db = IndexedDB::open().await?;
        let private_key = db.get_key(PRIVATE_KEY_ID).await?
            .ok_or("Private key not found in IndexedDB")?;

        // Configure signing algorithm (ECDSA with SHA-256)
        let algorithm = Object::new();
        Reflect::set(&algorithm, &"name".into(), &"ECDSA".into())
            .map_err(|_| "Failed to set algorithm name")?;
        Reflect::set(&algorithm, &"hash".into(), &"SHA-256".into())
            .map_err(|_| "Failed to set hash algorithm")?;

        // Sign the message directly with byte slice
        let sign_promise = subtle.sign_with_object_and_u8_array(&algorithm, &private_key, message)
            .map_err(|e| format!("Failed to sign: {:?}", e))?;

        let signature = JsFuture::from(sign_promise).await
            .map_err(|e| format!("Signing failed: {:?}", e))?;

        // Convert signature to Vec<u8>
        let signature_array = Uint8Array::new(&signature);
        let mut signature_bytes = vec![0u8; signature_array.length() as usize];
        signature_array.copy_to(&mut signature_bytes);

        log::info!("Message signed successfully ({} bytes)", signature_bytes.len());

        Ok(signature_bytes)
    }

    /// Verify a signature using Web Crypto API
    pub async fn verify(public_key_jwk: &str, message: &[u8], signature: &[u8]) -> Result<bool, String> {
        let subtle = Self::get_subtle_crypto()?;

        // Parse JWK
        let jwk_value = js_sys::JSON::parse(public_key_jwk)
            .map_err(|_| "Failed to parse public key JWK")?;
        let jwk_obj: Object = jwk_value.dyn_into()
            .map_err(|_| "JWK is not an object")?;

        // Configure algorithm
        let algorithm = Object::new();
        Reflect::set(&algorithm, &"name".into(), &"ECDSA".into())
            .map_err(|_| "Failed to set algorithm name")?;
        Reflect::set(&algorithm, &"namedCurve".into(), &"P-256".into())
            .map_err(|_| "Failed to set curve")?;

        // Import public key
        let key_usages = Array::new();
        key_usages.push(&"verify".into());

        let import_promise = subtle.import_key_with_object("jwk", &jwk_obj, &algorithm, true, &key_usages)
            .map_err(|e| format!("Failed to import key: {:?}", e))?;

        let public_key = JsFuture::from(import_promise).await
            .map_err(|e| format!("Key import failed: {:?}", e))?;
        let public_key = CryptoKey::from(public_key);

        // Configure signing algorithm
        let sign_algorithm = Object::new();
        Reflect::set(&sign_algorithm, &"name".into(), &"ECDSA".into())
            .map_err(|_| "Failed to set sign algorithm")?;
        Reflect::set(&sign_algorithm, &"hash".into(), &"SHA-256".into())
            .map_err(|_| "Failed to set hash")?;

        // Verify signature (web-sys expects byte slices directly)
        let verify_promise = subtle.verify_with_object_and_u8_array_and_u8_array(
            &sign_algorithm,
            &public_key,
            signature,
            message
        ).map_err(|e| format!("Verification failed: {:?}", e))?;

        let result = JsFuture::from(verify_promise).await
            .map_err(|e| format!("Verification promise failed: {:?}", e))?;

        Ok(result.as_bool().unwrap_or(false))
    }

    /// Compute DID from public key JWK
    fn compute_did_from_jwk(jwk: &str) -> Result<String, String> {
        let hash = Self::hash_public_key(jwk);
        Ok(format!("did:aurora:ecdsa:{}", hex::encode(&hash[..20])))
    }

    /// Hash public key for DID/peer ID generation
    fn hash_public_key(jwk: &str) -> Vec<u8> {
        let mut hasher = Sha256::new();
        hasher.update(jwk.as_bytes());
        hasher.finalize().to_vec()
    }

    /// Get SubtleCrypto interface
    fn get_subtle_crypto() -> Result<SubtleCrypto, String> {
        let window = window().ok_or("No global window")?;
        let crypto = window.crypto().map_err(|_| "Crypto not available")?;
        let subtle = crypto.subtle();
        Ok(subtle)
    }

    /// Convert JWK to hex string (extract x, y coordinates)
    fn jwk_to_hex(jwk: &str) -> Result<String, String> {
        // Parse JWK and extract x, y coordinates
        // This is simplified - a full implementation would properly decode base64url
        let hash = Self::hash_public_key(jwk);
        Ok(hex::encode(&hash[..32]))
    }

    /// Serialize identity for storage
    fn to_stored(&self) -> Result<String, String> {
        let data = StoredIdentity {
            public_key_jwk: self.public_key_jwk.clone(),
            did: self.did.clone(),
        };

        serde_json::to_string(&data)
            .map_err(|e| format!("Failed to serialize identity: {}", e))
    }

    /// Deserialize identity from storage
    async fn from_stored(stored: &str) -> Result<Self, String> {
        let data: StoredIdentity = serde_json::from_str(stored)
            .map_err(|e| format!("Failed to deserialize identity: {}", e))?;

        // Verify the DID matches the public key
        let computed_did = Self::compute_did_from_jwk(&data.public_key_jwk)?;
        if computed_did != data.did {
            return Err("DID mismatch - possible tampering".to_string());
        }

        log::info!("Restored identity: {}", data.did);

        Ok(Identity {
            public_key_jwk: data.public_key_jwk,
            did: data.did,
        })
    }
}

#[derive(Debug, Serialize, Deserialize)]
struct StoredIdentity {
    public_key_jwk: String,  // Public key in JSON Web Key format
    did: String,
}

// Helper module for hex encoding/decoding
mod hex {
    pub fn encode(bytes: &[u8]) -> String {
        bytes.iter().map(|b| format!("{:02x}", b)).collect()
    }

    pub fn decode(hex: &str) -> Result<Vec<u8>, String> {
        (0..hex.len())
            .step_by(2)
            .map(|i| {
                u8::from_str_radix(&hex[i..i + 2], 16)
                    .map_err(|e| format!("Invalid hex: {}", e))
            })
            .collect()
    }
}
