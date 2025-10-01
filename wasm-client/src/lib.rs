use wasm_bindgen::prelude::*;
use web_sys::console;

mod agent;
mod p2p;
mod blockchain;
mod models;
mod crypto;
mod storage;

pub use agent::AuroraAgent;
pub use p2p::P2PNetwork;
pub use blockchain::BlockchainInterface;
pub use models::{Model, ModelRegistry};

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
