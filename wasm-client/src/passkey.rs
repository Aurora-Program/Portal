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
    /// Note: This is a stub implementation
    async fn create_new() -> Result<Self, String> {
        // TODO: Implement proper WebAuthn credential creation
        // This requires proper web-sys bindings for:
        // - CredentialsContainer.create()
        // - PublicKeyCredentialCreationOptions
        // - Parsing AttestationObject
        
        Err("Passkey creation not yet implemented - use LocalKey for now".to_string())
    }

    /// Sign a message using the passkey
    /// Note: This is a placeholder - actual WebAuthn signing is complex
    /// and requires proper JS interop. For now, we return an error.
    pub async fn sign(&self, _message: &[u8]) -> Result<Vec<u8>, String> {
        // TODO: Implement proper WebAuthn signing
        // This requires:
        // 1. Proper CredentialRequestOptions setup
        // 2. navigator.credentials.get() call
        // 3. Signature extraction from AuthenticatorAssertionResponse
        
        Err("Passkey signing not yet implemented - use LocalKey for now".to_string())
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
