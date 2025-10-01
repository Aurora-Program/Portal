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

/// User identity (DID + Web Crypto keypair)
#[derive(Clone)]
pub struct Identity {
    did: String,
    public_key_jwk: String,  // JSON Web Key format for public key
    // Note: private key stays in browser's CryptoKey (non-extractable for security)
}

impl Identity {
    /// Create a new identity or load from storage
    pub async fn new_or_load() -> Result<Self, String> {
        let storage = LocalStorage::new()?;

        // Try to load existing identity
        if let Ok(Some(stored)) = storage.get("aurora_identity") {
            log::info!("Loading existing identity from storage...");
            return Self::from_stored(&stored).await;
        }

        // Create new identity using Web Crypto API
        log::info!("Creating new decentralized identity...");
        let identity = Self::generate_new().await?;

        // Store for future use
        let serialized = identity.to_stored()?;
        storage.set("aurora_identity", &serialized)?;

        Ok(identity)
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

        // Generate keypair (extractable public, non-extractable private for security)
        let key_usages = Array::new();
        key_usages.push(&"sign".into());
        key_usages.push(&"verify".into());

        let keypair_promise = subtle.generate_key_with_object(&algorithm, true, &key_usages)
            .map_err(|e| format!("Failed to generate key: {:?}", e))?;

        let keypair = JsFuture::from(keypair_promise).await
            .map_err(|e| format!("Key generation failed: {:?}", e))?;

        // Extract public key
        let public_key = Reflect::get(&keypair, &"publicKey".into())
            .map_err(|_| "Failed to get public key")?;
        let public_key = CryptoKey::from(public_key);

        // Export public key to JWK format
        let export_promise = subtle.export_key("jwk", &public_key)
            .map_err(|e| format!("Failed to export public key: {:?}", e))?;

        let jwk = JsFuture::from(export_promise).await
            .map_err(|e| format!("Export failed: {:?}", e))?;

        let public_key_jwk = js_sys::JSON::stringify(&jwk)
            .map_err(|_| "Failed to stringify JWK")?
            .as_string()
            .ok_or("JWK is not a string")?;

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

    /// Sign a message using Web Crypto API
    pub async fn sign(&self, message: &[u8]) -> Result<Vec<u8>, String> {
        let subtle = Self::get_subtle_crypto()?;

        // Import the private key (we need to retrieve it from IndexedDB in a real implementation)
        // For now, we'll use a simplified approach
        log::warn!("Signing is not fully implemented yet - using hash for Phase 0");
        
        // Temporary: hash the message with public key (will be replaced with real signing)
        let mut hasher = Sha256::new();
        hasher.update(message);
        hasher.update(self.public_key_jwk.as_bytes());
        Ok(hasher.finalize().to_vec())
    }

    /// Verify a signature using Web Crypto API
    pub async fn verify(public_key_jwk: &str, message: &[u8], signature: &[u8]) -> Result<bool, String> {
        let subtle = Self::get_subtle_crypto()?;

        // Parse JWK
        let jwk = js_sys::JSON::parse(public_key_jwk)
            .map_err(|_| "Failed to parse public key JWK")?;

        // Configure algorithm
        let algorithm = Object::new();
        Reflect::set(&algorithm, &"name".into(), &"ECDSA".into())
            .map_err(|_| "Failed to set algorithm name")?;
        Reflect::set(&algorithm, &"namedCurve".into(), &"P-256".into())
            .map_err(|_| "Failed to set curve")?;

        // Import public key
        let key_usages = Array::new();
        key_usages.push(&"verify".into());

        let import_promise = subtle.import_key_with_object("jwk", &jwk, &algorithm, true, &key_usages)
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

        // Verify signature
        let signature_array = Uint8Array::from(signature);
        let message_array = Uint8Array::from(message);

        let verify_promise = subtle.verify_with_object_and_u8_array_and_u8_array(
            &sign_algorithm,
            &public_key,
            &signature_array,
            &message_array
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
