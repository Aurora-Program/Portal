# Contributing to Aurora Portal

Thank you for your interest in contributing to Aurora Portal! This document provides guidelines and instructions for contributing to the project.

## 🌟 Ways to Contribute

### 1. Infrastructure Contribution
Run infrastructure and earn tokens:
- **Domains**: Provide access domains
- **DNS Servers**: Run community DNS nodes
- **Web Portals**: Host the Aurora Portal web app
- **P2P Relays/Gateways**: Enable connectivity for users behind NAT

### 2. Model Contribution
- Create new AI models (operational, service, management)
- Improve existing models
- Host models for the network
- Earn royalties for model usage

### 3. Code Contribution
- Fix bugs
- Add features
- Improve performance
- Enhance documentation
- Write tests

### 4. Documentation
- Improve README files
- Write tutorials and guides
- Translate documentation
- Create video tutorials

### 5. Community Participation
- Help users in discussions
- Report bugs and issues
- Suggest improvements
- Participate in governance

## 🔧 Development Setup

### Prerequisites
```powershell
# Install Rust
# Visit: https://rustup.rs/

# Install wasm-pack
cargo install wasm-pack

# Install Python (for local server)
# Or Node.js for alternative server
```

### Clone and Build
```powershell
# Clone repository
git clone https://github.com/Aurora-Program/Portal.git
cd Portal

# Build WASM client
cd wasm-client
.\build.ps1 -BuildType dev

# Run locally
cd ..
python -m http.server 8000
```

## 📝 Code Guidelines

### Rust Code
- Follow [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/)
- Run `cargo fmt` before committing
- Run `cargo clippy` and fix warnings
- Add tests for new features
- Document public APIs with doc comments

### JavaScript Code
- Use ES6+ features
- Follow [Airbnb Style Guide](https://github.com/airbnb/javascript)
- Add JSDoc comments for functions
- Test in multiple browsers

### Commit Messages
Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add P2P relay discovery
fix: resolve WASM initialization race condition
docs: update WASM client README
test: add integration tests for blockchain interface
refactor: simplify identity storage logic
```

## 🧪 Testing

### Run Rust Tests
```bash
cd wasm-client
cargo test
```

### Run WASM Tests
```bash
cd wasm-client
wasm-pack test --headless --firefox
wasm-pack test --headless --chrome
```

### Manual Testing
1. Build WASM client
2. Run local server
3. Open browser console
4. Check for errors
5. Test all features

## 📋 Pull Request Process

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Make** your changes
4. **Test** thoroughly
5. **Commit** with descriptive messages
6. **Push** to your fork (`git push origin feature/amazing-feature`)
7. **Open** a Pull Request

### PR Checklist
- [ ] Code follows project style guidelines
- [ ] Tests pass (`cargo test`)
- [ ] New features have tests
- [ ] Documentation is updated
- [ ] Commit messages follow conventions
- [ ] No merge conflicts
- [ ] PR description explains changes

## 🐛 Bug Reports

When reporting bugs, include:

1. **Environment**: OS, browser, Rust version
2. **Steps to Reproduce**: Clear, minimal steps
3. **Expected Behavior**: What should happen
4. **Actual Behavior**: What actually happens
5. **Logs**: Console errors, stack traces
6. **Screenshots**: If applicable

## 💡 Feature Requests

When suggesting features:

1. **Problem**: What problem does it solve?
2. **Solution**: Proposed implementation
3. **Alternatives**: Other solutions considered
4. **Impact**: Who benefits from this?
5. **Alignment**: How does it align with Aurora's values?

## 🔒 Security

**Do not** report security vulnerabilities in public issues.

Email: security@auroraprogram.org

We will respond within 48 hours and work with you to address the issue.

## 📜 Code of Conduct

### Our Pledge
Aurora Portal is committed to providing a welcoming, inclusive, and harassment-free experience for everyone.

### Our Standards
- **Be respectful**: Treat everyone with respect
- **Be constructive**: Provide helpful feedback
- **Be collaborative**: Work together toward common goals
- **Be ethical**: Align with Aurora's founding principles

### Unacceptable Behavior
- Harassment or discrimination
- Trolling or insulting comments
- Spam or off-topic content
- Unethical or malicious code

### Enforcement
Violations may result in:
1. Warning
2. Temporary ban
3. Permanent ban

Report violations to: conduct@auroraprogram.org

## 🏆 Recognition

Contributors are recognized in:
- **README.md**: Contributors section
- **On-chain**: Contribution tokens and reputation
- **Community**: Public acknowledgment

## 📚 Resources

- [Aurora Program Website](https://www.auroraprogram.org)
- [Aurora Portal Specification](Docs/AuroraPortal.md)
- [WASM Client README](wasm-client/README.md)
- [Rust Book](https://doc.rust-lang.org/book/)
- [WebAssembly](https://webassembly.org/)
- [libp2p Documentation](https://docs.libp2p.io/)

## 🤝 Community

Join the Aurora community:
- GitHub Discussions
- Discord (coming soon)
- Twitter: @AuroraProgram

## 📄 License

By contributing to Aurora Portal, you agree that your contributions will be licensed under the Apache License 2.0.

---

Thank you for contributing to Aurora Portal! Together, we're building the future through ethical intelligence and decentralized collaboration.
