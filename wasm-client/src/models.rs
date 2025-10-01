use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use sha2::{Sha256, Digest};

/// Model registry for managing AI models
pub struct ModelRegistry {
    models: HashMap<String, Model>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Model {
    pub model_id: String,
    pub kind: ModelKind,
    pub version: String,
    pub artifact_cid: String,
    pub author_did: String,
    pub license: String,
    pub royalties_percent: u8,
    pub hash: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum ModelKind {
    Operational,
    Service,
    Management,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ModelPack {
    pub architecture: String,
    pub weights: Vec<u8>,
    pub normalization: Vec<f32>,
    pub metadata: HashMap<String, String>,
}

impl ModelRegistry {
    /// Create a new model registry
    pub fn new() -> Self {
        ModelRegistry {
            models: HashMap::new(),
        }
    }

    /// Register a model by its hash
    pub async fn register_model(&mut self, model_hash: &str) -> Result<(), String> {
        log::info!("Registering model: {}", model_hash);
        
        // TODO: Fetch model metadata from blockchain
        // TODO: Download model artifacts from IPFS/Arweave using artifact_cid
        
        let model = Model {
            model_id: model_hash.to_string(),
            kind: ModelKind::Management,
            version: "0.1.0".to_string(),
            artifact_cid: "QmExample123".to_string(),
            author_did: "did:aurora:example".to_string(),
            license: "Apache-2.0".to_string(),
            royalties_percent: 5,
            hash: model_hash.to_string(),
        };

        self.models.insert(model_hash.to_string(), model);
        Ok(())
    }

    /// Get a model by its hash
    pub fn get_model(&self, model_hash: &str) -> Option<&Model> {
        self.models.get(model_hash)
    }

    /// Verify model integrity by checking hash
    pub fn verify_model(&self, model_pack: &ModelPack) -> Result<String, String> {
        log::info!("Verifying model integrity...");
        
        let hash = Self::compute_model_hash(model_pack);
        
        if self.models.contains_key(&hash) {
            Ok(hash)
        } else {
            Err(format!("Model hash {} not registered", hash))
        }
    }

    /// Compute the hash of a model pack
    pub fn compute_model_hash(model_pack: &ModelPack) -> String {
        let mut hasher = Sha256::new();
        
        // Hash architecture
        hasher.update(model_pack.architecture.as_bytes());
        
        // Hash weights
        hasher.update(&model_pack.weights);
        
        // Hash normalization
        for val in &model_pack.normalization {
            hasher.update(&val.to_le_bytes());
        }
        
        // Hash metadata (sorted keys for determinism)
        let mut keys: Vec<_> = model_pack.metadata.keys().collect();
        keys.sort();
        for key in keys {
            hasher.update(key.as_bytes());
            hasher.update(model_pack.metadata[key].as_bytes());
        }
        
        let result = hasher.finalize();
        format!("0x{}", hex::encode(result))
    }

    /// List all registered models
    pub fn list_models(&self) -> Vec<String> {
        self.models.keys().cloned().collect()
    }

    /// Get model count
    pub fn model_count(&self) -> usize {
        self.models.len()
    }

    /// Execute a model (stub - actual execution would involve WASM runtime or inference)
    pub async fn execute_model(&self, model_id: &str, input: &[u8]) -> Result<Vec<u8>, String> {
        log::info!("Executing model: {}", model_id);
        
        let model = self.get_model(model_id)
            .ok_or_else(|| format!("Model {} not found", model_id))?;

        // TODO: Load model artifacts
        // TODO: Run inference
        // TODO: Return output

        Ok(vec![])
    }
}

impl Default for ModelRegistry {
    fn default() -> Self {
        Self::new()
    }
}

// Helper module for hex encoding (simple implementation)
mod hex {
    pub fn encode(bytes: impl AsRef<[u8]>) -> String {
        bytes
            .as_ref()
            .iter()
            .map(|b| format!("{:02x}", b))
            .collect()
    }
}
