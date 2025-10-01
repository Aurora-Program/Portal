use wasm_bindgen::prelude::*;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;

use crate::p2p::P2PNetwork;
use crate::blockchain::BlockchainInterface;
use crate::models::ModelRegistry;
use crate::crypto::Identity;
use crate::storage::LocalStorage;

/// Configuration for the Aurora Agent
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AgentConfig {
    /// Relay nodes for P2P connectivity
    pub relay_nodes: Vec<String>,
    /// Blockchain RPC endpoint
    pub blockchain_rpc: String,
    /// Bootstrap models to load
    pub bootstrap_models: Vec<String>,
    /// User DID (Decentralized Identifier)
    pub user_did: Option<String>,
}

/// The main Aurora Intelligence System agent
#[wasm_bindgen]
pub struct AuroraAgent {
    identity: Identity,
    p2p: P2PNetwork,
    blockchain: BlockchainInterface,
    models: ModelRegistry,
    storage: LocalStorage,
    state: AgentState,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AgentState {
    pub connected: bool,
    pub authenticated: bool,
    pub peer_count: usize,
    pub active_sessions: HashMap<String, SessionInfo>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SessionInfo {
    pub session_id: String,
    pub peer_id: String,
    pub model_id: String,
    pub started_at: u64,
}

#[wasm_bindgen]
impl AuroraAgent {
    /// Create a new Aurora Agent
    pub async fn new(config_json: &str) -> Result<AuroraAgent, String> {
        log::info!("Initializing Aurora Agent...");
        
        let config: AgentConfig = serde_json::from_str(config_json)
            .map_err(|e| format!("Failed to parse config: {}", e))?;

        // Initialize identity (DID/wallet)
        let identity = Identity::new_or_load()
            .await
            .map_err(|e| format!("Failed to initialize identity: {}", e))?;

        log::info!("Identity loaded: {}", identity.did());

        // Initialize local storage
        let storage = LocalStorage::new()
            .map_err(|e| format!("Failed to initialize storage: {}", e))?;

        // Initialize P2P network
        let p2p = P2PNetwork::new(&config.relay_nodes, &identity)
            .await
            .map_err(|e| format!("Failed to initialize P2P: {}", e))?;

        // Initialize blockchain interface
        let blockchain = BlockchainInterface::new(&config.blockchain_rpc)
            .await
            .map_err(|e| format!("Failed to initialize blockchain: {}", e))?;

        // Initialize model registry
        let mut models = ModelRegistry::new();
        
        // Load bootstrap models
        for model_hash in config.bootstrap_models {
            log::info!("Loading bootstrap model: {}", model_hash);
            models.register_model(&model_hash)
                .await
                .map_err(|e| format!("Failed to load model {}: {}", model_hash, e))?;
        }

        let state = AgentState {
            connected: false,
            authenticated: false,
            peer_count: 0,
            active_sessions: HashMap::new(),
        };

        Ok(AuroraAgent {
            identity,
            p2p,
            blockchain,
            models,
            storage,
            state,
        })
    }

    /// Start the agent (connect to P2P network and blockchain)
    pub async fn start(&mut self) -> Result<(), JsValue> {
        log::info!("Starting Aurora Agent...");

        // Connect to P2P network
        self.p2p.connect()
            .await
            .map_err(|e| JsValue::from_str(&format!("P2P connection failed: {}", e)))?;

        self.state.connected = true;
        log::info!("Connected to P2P network");

        // Authenticate with blockchain
        self.blockchain.authenticate(&self.identity)
            .await
            .map_err(|e| JsValue::from_str(&format!("Blockchain auth failed: {}", e)))?;

        self.state.authenticated = true;
        log::info!("Authenticated with blockchain");

        Ok(())
    }

    /// Process a user prompt
    pub async fn process_prompt(&mut self, prompt: String) -> Result<String, JsValue> {
        log::info!("Processing prompt: {}", prompt);

        // 1. Parse user intent
        let intent = self.parse_intent(&prompt)?;

        // 2. Discover suitable nodes/models
        let candidates = self.discover_candidates(&intent)
            .await
            .map_err(|e| JsValue::from_str(&e))?;

        // 3. Negotiate and open session
        let session = self.negotiate_session(&intent, &candidates)
            .await
            .map_err(|e| JsValue::from_str(&e))?;

        // 4. Execute with SLO tracking
        let result = self.execute_session(&session)
            .await
            .map_err(|e| JsValue::from_str(&e))?;

        // 5. Settle on-chain
        self.settle_session(&session, &result)
            .await
            .map_err(|e| JsValue::from_str(&e))?;

        Ok(result)
    }

    /// Get current agent state
    pub fn get_state(&self) -> JsValue {
        serde_wasm_bindgen::to_value(&self.state).unwrap()
    }

    /// Get user DID
    pub fn get_did(&self) -> String {
        self.identity.did()
    }

    /// Get connected peer count
    pub fn get_peer_count(&self) -> usize {
        self.p2p.peer_count()
    }

    /// Get public key in JWK format
    pub fn get_public_key(&self) -> String {
        self.identity.public_key_jwk()
    }

    /// Sign a message using the user's private key
    /// Returns the signature as a hex-encoded string
    pub async fn sign_message(&self, message: String) -> Result<String, JsValue> {
        log::info!("Signing message: {}", message);
        
        let signature = self.identity.sign(message.as_bytes())
            .await
            .map_err(|e| JsValue::from_str(&format!("Signing failed: {}", e)))?;

        // Convert to hex for easy transport
        let hex_signature = signature.iter()
            .map(|b| format!("{:02x}", b))
            .collect::<String>();

        log::info!("Signature generated: {}...", &hex_signature[..16]);
        
        Ok(hex_signature)
    }

    /// Verify a signature (static method)
    /// This can be called by other peers to verify messages
    pub async fn verify_signature(
        public_key_jwk: String,
        message: String,
        hex_signature: String,
    ) -> Result<bool, JsValue> {
        log::info!("Verifying signature...");

        // Convert hex signature back to bytes
        let signature = (0..hex_signature.len())
            .step_by(2)
            .map(|i| u8::from_str_radix(&hex_signature[i..i + 2], 16))
            .collect::<Result<Vec<u8>, _>>()
            .map_err(|e| JsValue::from_str(&format!("Invalid hex: {}", e)))?;

        let valid = Identity::verify(&public_key_jwk, message.as_bytes(), &signature)
            .await
            .map_err(|e| JsValue::from_str(&format!("Verification failed: {}", e)))?;

        log::info!("Signature valid: {}", valid);
        
        Ok(valid)
    }

    /// Shutdown the agent
    pub async fn shutdown(&mut self) -> Result<(), JsValue> {
        log::info!("Shutting down Aurora Agent...");
        
        self.p2p.disconnect().await
            .map_err(|e| JsValue::from_str(&format!("P2P disconnect failed: {}", e)))?;
        
        self.state.connected = false;
        Ok(())
    }
}

// Private implementation methods
impl AuroraAgent {
    fn parse_intent(&self, prompt: &str) -> Result<Intent, JsValue> {
        // TODO: Implement intent parsing logic
        Ok(Intent {
            action: "query".to_string(),
            parameters: HashMap::new(),
        })
    }

    async fn discover_candidates(&self, intent: &Intent) -> Result<Vec<Candidate>, String> {
        // TODO: Implement P2P discovery using Kademlia DHT
        Ok(vec![])
    }

    async fn negotiate_session(&mut self, intent: &Intent, candidates: &[Candidate]) -> Result<Session, String> {
        // TODO: Implement bid/offer negotiation
        Ok(Session {
            id: "session_123".to_string(),
            peer: "peer_456".to_string(),
            model: "model_789".to_string(),
        })
    }

    async fn execute_session(&self, session: &Session) -> Result<String, String> {
        // TODO: Implement P2P execution with SLO tracking
        Ok("Result from execution".to_string())
    }

    async fn settle_session(&self, session: &Session, result: &str) -> Result<(), String> {
        // TODO: Implement on-chain settlement
        Ok(())
    }
}

// Supporting types
#[derive(Debug, Clone)]
struct Intent {
    action: String,
    parameters: HashMap<String, String>,
}

#[derive(Debug, Clone)]
struct Candidate {
    peer_id: String,
    model_id: String,
    reputation: f64,
}

#[derive(Debug, Clone)]
struct Session {
    id: String,
    peer: String,
    model: String,
}
