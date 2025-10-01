// Temporarily using stub implementation until getrandom WASM issues are resolved
// TODO: Re-enable ed25519-dalek and rand once libp2p WASM support improves
// use ed25519_dalek::{Keypair, PublicKey, SecretKey, Signature, Signer, Verifier};
// use rand::rngs::OsRng;
use sha2::{Sha256, Digest};
use serde::{Deserialize, Serialize};
use web_sys::window;

use crate::storage::LocalStorage;

/// User identity (DID + keypair) - Stub implementation
#[derive(Clone)]
pub struct Identity {
    // keypair: Keypair,  // Temporarily disabled
    did: String,
    public_key_stub: Vec<u8>,
}

impl Identity {
    /// Create a new identity or load from storage
    pub async fn new_or_load() -> Result<Self, String> {
        let storage = LocalStorage::new()?;

        // Try to load existing identity
        if let Ok(Some(stored)) = storage.get("aurora_identity") {
            log::info!("Loading existing identity...");
            return Self::from_stored(&stored);
        }

        // Create new identity
        log::info!("Creating new identity...");
        let identity = Self::new();

        // Store for future use
        let serialized = identity.to_stored()?;
        storage.set("aurora_identity", &serialized)?;

        Ok(identity)
    }

    /// Create a new random identity (stub implementation using browser crypto)
    pub fn new() -> Self {
        // Generate random bytes using browser's crypto API
        let public_key_stub = Self::generate_random_key();
        let did = Self::compute_did_from_bytes(&public_key_stub);

        Identity { did, public_key_stub }
    }
    
    fn generate_random_key() -> Vec<u8> {
        // Use browser's crypto.getRandomValues for now
        let window = window().expect("no global `window` exists");
        let crypto = window.crypto().expect("crypto not available");
        let mut bytes = vec![0u8; 32];
        crypto.get_random_values_with_u8_array(&mut bytes).expect("failed to generate random");
        bytes
    }

    /// Get the DID (Decentralized Identifier)
    pub fn did(&self) -> String {
        self.did.clone()
    }

    /// Get the public key as hex string
    pub fn public_key_hex(&self) -> String {
        hex::encode(&self.public_key_stub)
    }

    /// Get peer ID for libp2p (derived from public key)
    pub fn peer_id(&self) -> String {
        // Stub implementation - will use proper libp2p PeerId in Phase 1
        format!("12D3KooW{}", &hex::encode(&self.public_key_stub[..16]))
    }

    /// Sign a message (stub - returns placeholder)
    pub fn sign(&self, message: &[u8]) -> Vec<u8> {
        // Stub implementation - will use proper Ed25519 signing in Phase 1
        let mut hasher = Sha256::new();
        hasher.update(message);
        hasher.update(&self.public_key_stub);
        hasher.finalize().to_vec()
    }

    /// Verify a signature (stub - always returns Ok for now)
    pub fn verify(_public_key: &[u8], _message: &[u8], _signature: &[u8]) -> Result<(), String> {
        // Stub implementation - will use proper Ed25519 verification in Phase 1
        log::warn!("Signature verification is stubbed - not secure yet!");
        Ok(())
    }

    /// Compute DID from public key bytes
    fn compute_did_from_bytes(public_key: &[u8]) -> String {
        let mut hasher = Sha256::new();
        hasher.update(public_key);
        let hash = hasher.finalize();
        
        format!("did:aurora:{}", hex::encode(&hash[..20]))
    }

    /// Serialize identity for storage (encrypted in production)
    fn to_stored(&self) -> Result<String, String> {
        let data = StoredIdentity {
            public_key: hex::encode(&self.public_key_stub),
            did: self.did.clone(),
        };

        serde_json::to_string(&data)
            .map_err(|e| format!("Failed to serialize identity: {}", e))
    }

    /// Deserialize identity from storage
    fn from_stored(stored: &str) -> Result<Self, String> {
        let data: StoredIdentity = serde_json::from_str(stored)
            .map_err(|e| format!("Failed to deserialize identity: {}", e))?;
        
        let public_key_stub = hex::decode(&data.public_key)
            .map_err(|e| format!("Invalid public key hex: {}", e))?;

        Ok(Identity {
            public_key_stub,
            did: data.did,
        })
    }
}

#[derive(Debug, Serialize, Deserialize)]
struct StoredIdentity {
    public_key: String,
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
