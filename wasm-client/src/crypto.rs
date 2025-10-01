use ed25519_dalek::{Keypair, PublicKey, SecretKey, Signature, Signer, Verifier};
use rand::rngs::OsRng;
use sha2::{Sha256, Digest};
use serde::{Deserialize, Serialize};

use crate::storage::LocalStorage;

/// User identity (DID + keypair)
#[derive(Clone)]
pub struct Identity {
    keypair: Keypair,
    did: String,
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

    /// Create a new random identity
    pub fn new() -> Self {
        let mut csprng = OsRng{};
        let keypair = Keypair::generate(&mut csprng);
        
        let did = Self::compute_did(&keypair.public);

        Identity { keypair, did }
    }

    /// Get the DID (Decentralized Identifier)
    pub fn did(&self) -> String {
        self.did.clone()
    }

    /// Get the public key as hex string
    pub fn public_key_hex(&self) -> String {
        hex::encode(self.keypair.public.as_bytes())
    }

    /// Get peer ID for libp2p (derived from public key)
    pub fn peer_id(&self) -> String {
        // In a full implementation, this would use libp2p's PeerId derivation
        format!("12D3KooW{}", &hex::encode(&self.keypair.public.as_bytes()[..16]))
    }

    /// Sign a message
    pub fn sign(&self, message: &[u8]) -> Vec<u8> {
        let signature = self.keypair.sign(message);
        signature.to_bytes().to_vec()
    }

    /// Verify a signature
    pub fn verify(public_key: &[u8], message: &[u8], signature: &[u8]) -> Result<(), String> {
        let public = PublicKey::from_bytes(public_key)
            .map_err(|e| format!("Invalid public key: {}", e))?;
        
        let sig = Signature::from_bytes(signature)
            .map_err(|e| format!("Invalid signature: {}", e))?;

        public.verify(message, &sig)
            .map_err(|e| format!("Signature verification failed: {}", e))
    }

    /// Compute DID from public key
    fn compute_did(public_key: &PublicKey) -> String {
        let mut hasher = Sha256::new();
        hasher.update(public_key.as_bytes());
        let hash = hasher.finalize();
        
        format!("did:aurora:{}", hex::encode(&hash[..20]))
    }

    /// Serialize identity for storage (encrypted in production)
    fn to_stored(&self) -> Result<String, String> {
        let data = StoredIdentity {
            secret_key: hex::encode(self.keypair.secret.as_bytes()),
            public_key: hex::encode(self.keypair.public.as_bytes()),
            did: self.did.clone(),
        };

        serde_json::to_string(&data)
            .map_err(|e| format!("Failed to serialize identity: {}", e))
    }

    /// Deserialize identity from storage
    fn from_stored(stored: &str) -> Result<Self, String> {
        let data: StoredIdentity = serde_json::from_str(stored)
            .map_err(|e| format!("Failed to deserialize identity: {}", e))?;

        let secret_bytes = hex::decode(&data.secret_key)
            .map_err(|e| format!("Invalid secret key hex: {}", e))?;
        
        let public_bytes = hex::decode(&data.public_key)
            .map_err(|e| format!("Invalid public key hex: {}", e))?;

        let secret = SecretKey::from_bytes(&secret_bytes)
            .map_err(|e| format!("Invalid secret key: {}", e))?;
        
        let public = PublicKey::from_bytes(&public_bytes)
            .map_err(|e| format!("Invalid public key: {}", e))?;

        let keypair = Keypair { secret, public };

        Ok(Identity {
            keypair,
            did: data.did,
        })
    }
}

#[derive(Debug, Serialize, Deserialize)]
struct StoredIdentity {
    secret_key: String,
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
