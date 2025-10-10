use wasm_bindgen::prelude::*;
use web_sys::console;

mod agent;
mod p2p;
mod discovery; // Discovery Server client
mod blockchain;
mod models;
mod crypto;
mod storage;
mod indexed_db;
mod passkey;

// 🐹 Aurora P2P + Agent modules
mod p2p_client;
mod aurora_agent;

pub use agent::AuroraAgent;
pub use p2p::P2PNetwork;
pub use discovery::{DiscoveryClient, DiscoveryConfig, DiscoveredPeer};
pub use blockchain::BlockchainInterface;
pub use models::{Model, ModelRegistry};

// 🐹 Aurora P2P exports
pub use p2p_client::{AuroraP2PClient, P2PConfig, PeerInfo, WebRTCManager};
pub use aurora_agent::{
    AuroraAgentImpl as AuroraAgentV2,
    FractalTensor,
    TernaryVector,
    Trigate,
};

/// Initialize the Aurora WASM client
/// This is the entry point called from JavaScript
#[wasm_bindgen(start)]
pub fn main() {
    // Set up panic hook for better error messages
    #[cfg(feature = "console_error_panic_hook")]
    console_error_panic_hook::set_once();

    // Initialize logger
    wasm_logger::init(wasm_logger::Config::default());
    
    log::info!("Aurora Intelligence System initializing...");
    console::log_1(&"Aurora WASM client loaded successfully".into());
}

/// Create a new Aurora Agent instance
#[wasm_bindgen]
pub async fn create_agent(config: JsValue) -> Result<AuroraAgent, JsValue> {
    let config_str = config
        .as_string()
        .ok_or_else(|| JsValue::from_str("Invalid configuration"))?;
    
    let agent = AuroraAgent::new(&config_str)
        .await
        .map_err(|e| JsValue::from_str(&e.to_string()))?;
    
    Ok(agent)
}

/// Get the version of the Aurora client
#[wasm_bindgen]
pub fn get_version() -> String {
    env!("CARGO_PKG_VERSION").to_string()
}

/// Health check function
#[wasm_bindgen]
pub fn health_check() -> bool {
    true
}

/// Sign a message with the agent's private key
#[wasm_bindgen]
pub async fn sign_message(agent: &AuroraAgent, message: String) -> Result<String, JsValue> {
    agent.sign_message(message).await
}

/// Verify a signature
#[wasm_bindgen]
pub async fn verify_signature(
    public_key_jwk: String,
    message: String,
    signature: String,
) -> Result<bool, JsValue> {
    AuroraAgent::verify_signature(public_key_jwk, message, signature).await
}

// ============================================================================
// DISCOVERY SERVER API
// ============================================================================

/// Create a Discovery Client
#[wasm_bindgen]
pub fn create_discovery_client(
    endpoint: String,
    peer_id: String,
    archetypes: JsValue,
) -> Result<JsValue, JsValue> {
    let archetypes_vec: Vec<String> = serde_wasm_bindgen::from_value(archetypes)
        .map_err(|e| JsValue::from_str(&format!("Invalid archetypes: {:?}", e)))?;
    
    let config = DiscoveryConfig {
        endpoint,
        heartbeat_interval: 30,
        ttl_seconds: 300,
    };
    
    let client = DiscoveryClient::new(config, peer_id, archetypes_vec);
    
    serde_wasm_bindgen::to_value(&client)
        .map_err(|e| JsValue::from_str(&format!("Serialization error: {:?}", e)))
}

/// Register peer with Discovery Server
#[wasm_bindgen]
pub async fn discovery_register(
    endpoint: String,
    peer_id: String,
    archetypes: JsValue,
    address: String,
    port: u16,
) -> Result<JsValue, JsValue> {
    let archetypes_vec: Vec<String> = serde_wasm_bindgen::from_value(archetypes)
        .map_err(|e| JsValue::from_str(&format!("Invalid archetypes: {:?}", e)))?;
    
    let config = DiscoveryConfig {
        endpoint,
        heartbeat_interval: 30,
        ttl_seconds: 300,
    };
    
    let mut client = DiscoveryClient::new(config, peer_id, archetypes_vec);
    
    client.register(address, port)
        .await
        .map_err(|e| JsValue::from_str(&e))?;
    
    Ok(JsValue::from_str("{\"status\":\"registered\"}"))
}

/// Discover peers from Discovery Server
#[wasm_bindgen]
pub async fn discovery_find_peers(
    endpoint: String,
    peer_id: String,
    archetypes: JsValue,
    archetype_filter: Option<String>,
) -> Result<JsValue, JsValue> {
    let archetypes_vec: Vec<String> = serde_wasm_bindgen::from_value(archetypes)
        .map_err(|e| JsValue::from_str(&format!("Invalid archetypes: {:?}", e)))?;
    
    let config = DiscoveryConfig {
        endpoint,
        heartbeat_interval: 30,
        ttl_seconds: 300,
    };
    
    let client = DiscoveryClient::new(config, peer_id, archetypes_vec);
    
    let peers = client.discover(archetype_filter.as_deref())
        .await
        .map_err(|e| JsValue::from_str(&e))?;
    
    serde_wasm_bindgen::to_value(&peers)
        .map_err(|e| JsValue::from_str(&format!("Serialization error: {:?}", e)))
}

/// Send heartbeat to Discovery Server
#[wasm_bindgen]
pub async fn discovery_heartbeat(
    endpoint: String,
    peer_id: String,
) -> Result<JsValue, JsValue> {
    let config = DiscoveryConfig {
        endpoint: endpoint.clone(),
        heartbeat_interval: 30,
        ttl_seconds: 300,
    };
    
    // Create temporary client for heartbeat
    let mut client = DiscoveryClient::new(config, peer_id.clone(), vec![]);
    client.registered = true; // Mark as registered for heartbeat
    
    client.heartbeat()
        .await
        .map_err(|e| JsValue::from_str(&e))?;
    
    Ok(JsValue::from_str("{\"status\":\"ok\"}"))
}

/// Check Discovery Server health
#[wasm_bindgen]
pub async fn discovery_health(endpoint: String) -> Result<bool, JsValue> {
    let config = DiscoveryConfig {
        endpoint,
        heartbeat_interval: 30,
        ttl_seconds: 300,
    };
    
    let client = DiscoveryClient::new(config, "health-check".to_string(), vec![]);
    
    client.health_check()
        .await
        .map_err(|e| JsValue::from_str(&e))
}
