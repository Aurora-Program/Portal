use web_sys::{window, Storage};

/// Local storage wrapper for WASM
pub struct LocalStorage {
    storage: Storage,
}

impl LocalStorage {
    /// Create a new LocalStorage instance
    pub fn new() -> Result<Self, String> {
        let window = window()
            .ok_or_else(|| "No window object available".to_string())?;
        
        let storage = window.local_storage()
            .map_err(|_| "Failed to access localStorage".to_string())?
            .ok_or_else(|| "localStorage not available".to_string())?;

        Ok(LocalStorage { storage })
    }

    /// Get a value from storage
    pub fn get(&self, key: &str) -> Result<Option<String>, String> {
        self.storage.get_item(key)
            .map_err(|_| format!("Failed to get item: {}", key))
    }

    /// Set a value in storage
    pub fn set(&self, key: &str, value: &str) -> Result<(), String> {
        self.storage.set_item(key, value)
            .map_err(|_| format!("Failed to set item: {}", key))
    }

    /// Remove a value from storage
    pub fn remove(&self, key: &str) -> Result<(), String> {
        self.storage.remove_item(key)
            .map_err(|_| format!("Failed to remove item: {}", key))
    }

    /// Clear all storage
    pub fn clear(&self) -> Result<(), String> {
        self.storage.clear()
            .map_err(|_| "Failed to clear storage".to_string())
    }

    /// Check if a key exists
    pub fn has(&self, key: &str) -> bool {
        self.get(key).ok().flatten().is_some()
    }

    /// Get storage size (number of keys)
    pub fn len(&self) -> Result<usize, String> {
        self.storage.length()
            .map(|l| l as usize)
            .map_err(|_| "Failed to get storage length".to_string())
    }

    /// Check if storage is empty
    pub fn is_empty(&self) -> Result<bool, String> {
        Ok(self.len()? == 0)
    }
}
