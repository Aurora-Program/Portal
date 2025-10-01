/// WebAuthn/Passkey integration for secure key storage
/// Uses browser's credential manager and hardware security
use wasm_bindgen::prelude::*;
use wasm_bindgen_futures::JsFuture;
use web_sys::{window, CredentialsContainer, PublicKeyCredentialCreationOptions, PublicKeyCredentialRequestOptions};
use js_sys::{Object, Reflect, Uint8Array, Array};
use serde::{Deserialize, Serialize};

use crate::storage::LocalStorage;

/// Passkey-based identity using WebAuthn
pub struct PasskeyIdentity {
    did: String,
    credential_id: Vec<u8>,
    public_key: Vec<u8>,
}

impl PasskeyIdentity {
    /// Create or load a passkey-based identity
    pub async fn new_or_load() -> Result<Self, String> {
        let storage = LocalStorage::new()?;

        // Check if passkey exists
        if let Ok(Some(stored)) = storage.get("aurora_passkey_identity") {
            log::info!("Loading existing passkey identity...");
            return Self::from_stored(&stored).await;
        }

        // Create new passkey
        log::info!("Creating new passkey identity...");
        Self::create_new().await
    }

    /// Create a new passkey using WebAuthn
    async fn create_new() -> Result<Self, String> {
        let window = window().ok_or("No window")?;
        let navigator = window.navigator();
        let credentials = navigator.credentials();

        // Configure WebAuthn registration
        let challenge = Self::generate_challenge();
        
        let rp = Object::new();
        Reflect::set(&rp, &"name".into(), &"Aurora Portal".into())
            .map_err(|_| "Failed to set RP name")?;
        Reflect::set(&rp, &"id".into(), &window.location().hostname()?.into())
            .map_err(|_| "Failed to set RP id")?;

        let user = Object::new();
        let user_id = Self::generate_user_id();
        Reflect::set(&user, &"id".into(), &Uint8Array::from(&user_id[..]).into())
            .map_err(|_| "Failed to set user id")?;
        Reflect::set(&user, &"name".into(), &"Aurora User".into())
            .map_err(|_| "Failed to set user name")?;
        Reflect::set(&user, &"displayName".into(), &"Aurora Portal User".into())
            .map_err(|_| "Failed to set display name")?;

        let pub_key_cred_params = Array::new();
        let es256 = Object::new();
        Reflect::set(&es256, &"type".into(), &"public-key".into())
            .map_err(|_| "Failed to set type")?;
        Reflect::set(&es256, &"alg".into(), &(-7).into()) // ES256 (ECDSA P-256)
            .map_err(|_| "Failed to set alg")?;
        pub_key_cred_params.push(&es256);

        let authenticator_selection = Object::new();
        Reflect::set(&authenticator_selection, &"authenticatorAttachment".into(), &"platform".into())
            .map_err(|_| "Failed to set authenticator attachment")?;
        Reflect::set(&authenticator_selection, &"userVerification".into(), &"required".into())
            .map_err(|_| "Failed to set user verification")?;

        let options = Object::new();
        Reflect::set(&options, &"challenge".into(), &Uint8Array::from(&challenge[..]).into())
            .map_err(|_| "Failed to set challenge")?;
        Reflect::set(&options, &"rp".into(), &rp)
            .map_err(|_| "Failed to set rp")?;
        Reflect::set(&options, &"user".into(), &user)
            .map_err(|_| "Failed to set user")?;
        Reflect::set(&options, &"pubKeyCredParams".into(), &pub_key_cred_params)
            .map_err(|_| "Failed to set pubKeyCredParams")?;
        Reflect::set(&options, &"authenticatorSelection".into(), &authenticator_selection)
            .map_err(|_| "Failed to set authenticatorSelection")?;
        Reflect::set(&options, &"timeout".into(), &60000.into())
            .map_err(|_| "Failed to set timeout")?;
        Reflect::set(&options, &"attestation".into(), &"none".into())
            .map_err(|_| "Failed to set attestation")?;

        let credential_options = Object::new();
        Reflect::set(&credential_options, &"publicKey".into(), &options)
            .map_err(|_| "Failed to set publicKey")?;

        // Create credential
        log::info!("🔐 Requesting passkey creation (you may see a system prompt)...");
        let create_promise = credentials.create_with_options(&credential_options)
            .map_err(|e| format!("Failed to create credential: {:?}", e))?;

        let credential = JsFuture::from(create_promise).await
            .map_err(|e| format!("Credential creation failed: {:?}", e))?;

        if credential.is_null() || credential.is_undefined() {
            return Err("User cancelled passkey creation".to_string());
        }

        // Extract credential ID and public key
        let raw_id = Reflect::get(&credential, &"rawId".into())
            .map_err(|_| "Failed to get rawId")?;
        let credential_id_array = Uint8Array::new(&raw_id);
        let mut credential_id = vec![0u8; credential_id_array.length() as usize];
        credential_id_array.copy_to(&mut credential_id);

        let response = Reflect::get(&credential, &"response".into())
            .map_err(|_| "Failed to get response")?;
        let attestation_object = Reflect::get(&response, &"attestationObject".into())
            .map_err(|_| "Failed to get attestationObject")?;
        
        // For simplicity, we'll derive the public key from credential_id
        // In production, parse attestationObject properly
        let public_key = Self::derive_public_key_from_credential(&credential_id);

        // Compute DID
        let did = Self::compute_did(&public_key);

        log::info!("✅ Passkey created with DID: {}", did);

        let identity = PasskeyIdentity {
            did: did.clone(),
            credential_id: credential_id.clone(),
            public_key: public_key.clone(),
        };

        // Store metadata (not the actual key - that's in system)
        let storage = LocalStorage::new()?;
        let stored = StoredPasskeyIdentity {
            did,
            credential_id: hex::encode(&credential_id),
            public_key: hex::encode(&public_key),
        };
        storage.set("aurora_passkey_identity", &serde_json::to_string(&stored)
            .map_err(|e| format!("Failed to serialize: {}", e))?)?;

        Ok(identity)
    }

    /// Sign a message using the passkey
    pub async fn sign(&self, message: &[u8]) -> Result<Vec<u8>, String> {
        let window = window().ok_or("No window")?;
        let navigator = window.navigator();
        let credentials = navigator.credentials();

        // Configure WebAuthn authentication
        let challenge = message.to_vec(); // Use message as challenge

        let allow_credentials = Array::new();
        let allowed = Object::new();
        Reflect::set(&allowed, &"type".into(), &"public-key".into())
            .map_err(|_| "Failed to set type")?;
        Reflect::set(&allowed, &"id".into(), &Uint8Array::from(&self.credential_id[..]).into())
            .map_err(|_| "Failed to set id")?;
        allow_credentials.push(&allowed);

        let options = Object::new();
        Reflect::set(&options, &"challenge".into(), &Uint8Array::from(&challenge[..]).into())
            .map_err(|_| "Failed to set challenge")?;
        Reflect::set(&options, &"allowCredentials".into(), &allow_credentials)
            .map_err(|_| "Failed to set allowCredentials")?;
        Reflect::set(&options, &"timeout".into(), &60000.into())
            .map_err(|_| "Failed to set timeout")?;
        Reflect::set(&options, &"userVerification".into(), &"required".into())
            .map_err(|_| "Failed to set userVerification")?;

        let credential_options = Object::new();
        Reflect::set(&credential_options, &"publicKey".into(), &options)
            .map_err(|_| "Failed to set publicKey")?;

        // Get assertion (sign)
        log::info!("🔐 Requesting signature (you may see a system prompt)...");
        let get_promise = credentials.get_with_options(&credential_options)
            .map_err(|e| format!("Failed to get credential: {:?}", e))?;

        let assertion = JsFuture::from(get_promise).await
            .map_err(|e| format!("Authentication failed: {:?}", e))?;

        if assertion.is_null() || assertion.is_undefined() {
            return Err("User cancelled signing".to_string());
        }

        // Extract signature
        let response = Reflect::get(&assertion, &"response".into())
            .map_err(|_| "Failed to get response")?;
        let signature = Reflect::get(&response, &"signature".into())
            .map_err(|_| "Failed to get signature")?;
        
        let signature_array = Uint8Array::new(&signature);
        let mut signature_bytes = vec![0u8; signature_array.length() as usize];
        signature_array.copy_to(&mut signature_bytes);

        log::info!("✅ Message signed ({} bytes)", signature_bytes.len());

        Ok(signature_bytes)
    }

    pub fn did(&self) -> String {
        self.did.clone()
    }

    pub fn public_key(&self) -> Vec<u8> {
        self.public_key.clone()
    }

    fn generate_challenge() -> Vec<u8> {
        let window = window().unwrap();
        let crypto = window.crypto().unwrap();
        let mut challenge = vec![0u8; 32];
        crypto.get_random_values_with_u8_array(&mut challenge).unwrap();
        challenge
    }

    fn generate_user_id() -> Vec<u8> {
        Self::generate_challenge()
    }

    fn derive_public_key_from_credential(credential_id: &[u8]) -> Vec<u8> {
        // Simplified: hash credential_id to get a deterministic public key
        // In production, extract from attestationObject
        use sha2::{Sha256, Digest};
        let mut hasher = Sha256::new();
        hasher.update(credential_id);
        hasher.finalize().to_vec()
    }

    fn compute_did(public_key: &[u8]) -> String {
        use sha2::{Sha256, Digest};
        let mut hasher = Sha256::new();
        hasher.update(public_key);
        let hash = hasher.finalize();
        format!("did:aurora:passkey:{}", hex::encode(&hash[..20]))
    }

    async fn from_stored(stored: &str) -> Result<Self, String> {
        let data: StoredPasskeyIdentity = serde_json::from_str(stored)
            .map_err(|e| format!("Failed to parse stored identity: {}", e))?;

        let credential_id = hex::decode(&data.credential_id)
            .map_err(|e| format!("Invalid credential_id: {}", e))?;
        let public_key = hex::decode(&data.public_key)
            .map_err(|e| format!("Invalid public_key: {}", e))?;

        log::info!("✅ Passkey identity loaded: {}", data.did);

        Ok(PasskeyIdentity {
            did: data.did,
            credential_id,
            public_key,
        })
    }
}

#[derive(Debug, Serialize, Deserialize)]
struct StoredPasskeyIdentity {
    did: String,
    credential_id: String,
    public_key: String,
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
