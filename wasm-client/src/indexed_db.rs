/// Simplified key storage using localStorage with JWK format
/// Stores CryptoKey as JWK JSON string for easier persistence
use wasm_bindgen::prelude::*;
use wasm_bindgen_futures::JsFuture;
use web_sys::{window, CryptoKey};
use js_sys::{Object, Reflect, Array};

use crate::storage::LocalStorage;

const PRIVATE_KEY_JWK_STORAGE_KEY: &str = "aurora_private_key_jwk";

pub struct IndexedDB {
    storage: LocalStorage,
}

impl IndexedDB {
    /// Open or create storage
    pub async fn open() -> Result<Self, String> {
        let storage = LocalStorage::new()?;
        Ok(IndexedDB { storage })
    }

    /// Store a CryptoKey by exporting it as JWK
    pub async fn store_key(&self, _key_id: &str, key: &CryptoKey) -> Result<(), String> {
        // Export key to JWK
        let window = window().ok_or("No window")?;
        let crypto = window.crypto().map_err(|_| "Crypto not available")?;
        let subtle = crypto.subtle();

        let export_promise = subtle.export_key("jwk", key)
            .map_err(|e| format!("Failed to export private key: {:?}", e))?;

        let jwk = JsFuture::from(export_promise).await
            .map_err(|e| format!("Export failed: {:?}", e))?;

        let jwk_str = js_sys::JSON::stringify(&jwk)
            .map_err(|_| "Failed to stringify JWK")?
            .as_string()
            .ok_or("JWK is not a string")?;

        // Store as string in localStorage
        self.storage.set(PRIVATE_KEY_JWK_STORAGE_KEY, &jwk_str)?;

        log::info!("Private key stored as JWK");

        Ok(())
    }

    /// Retrieve a CryptoKey by importing from JWK
    pub async fn get_key(&self, _key_id: &str) -> Result<Option<CryptoKey>, String> {
        // Get JWK string from storage
        let jwk_str = match self.storage.get(PRIVATE_KEY_JWK_STORAGE_KEY)? {
            Some(s) => s,
            None => return Ok(None),
        };

        // Parse JWK
        let jwk_value = js_sys::JSON::parse(&jwk_str)
            .map_err(|_| "Failed to parse JWK")?;
        let jwk_obj: Object = jwk_value.dyn_into()
            .map_err(|_| "JWK is not an object")?;

        // Configure algorithm for import
        let algorithm = Object::new();
        Reflect::set(&algorithm, &"name".into(), &"ECDSA".into())
            .map_err(|_| "Failed to set algorithm name")?;
        Reflect::set(&algorithm, &"namedCurve".into(), &"P-256".into())
            .map_err(|_| "Failed to set curve")?;

        // Import key
        let window = window().ok_or("No window")?;
        let crypto = window.crypto().map_err(|_| "Crypto not available")?;
        let subtle = crypto.subtle();

        let key_usages = Array::new();
        key_usages.push(&"sign".into());

        let import_promise = subtle.import_key_with_object("jwk", &jwk_obj, &algorithm, true, &key_usages)
            .map_err(|e| format!("Failed to import key: {:?}", e))?;

        let key = JsFuture::from(import_promise).await
            .map_err(|e| format!("Import failed: {:?}", e))?;

        let crypto_key: CryptoKey = key.dyn_into()
            .map_err(|_| "Failed to convert to CryptoKey")?;

        Ok(Some(crypto_key))
    }

    /// Check if a key exists
    pub async fn has_key(&self, _key_id: &str) -> Result<bool, String> {
        Ok(self.storage.has(PRIVATE_KEY_JWK_STORAGE_KEY))
    }

    /// Delete a key
    pub async fn delete_key(&self, _key_id: &str) -> Result<(), String> {
        self.storage.remove(PRIVATE_KEY_JWK_STORAGE_KEY)
    }

    /// Clear all keys
    pub async fn clear(&self) -> Result<(), String> {
        self.storage.remove(PRIVATE_KEY_JWK_STORAGE_KEY)
    }
}
