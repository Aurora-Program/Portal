#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_version() {
        let version = crate::get_version();
        assert!(!version.is_empty());
        assert_eq!(version, env!("CARGO_PKG_VERSION"));
    }

    #[test]
    fn test_health_check() {
        assert!(crate::health_check());
    }
}
