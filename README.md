# Aurora Portal 🚀

**Building the future through ethical intelligence and decentralized collaboration.**

> *"What took 10 engineers and 5 years in 2014 (IPFS), we're building with 1 developer + AI in 18 months (2025)."*

Aurora Portal is the web entry point to the Aurora Network - a decentralized ecosystem for **verifiable AI model execution** with **Proof of Intelligence** at its core.

![Aurora Portal](assets/aurora-portal-logo.png)

## 🌟 What Makes Aurora Different?

### The Problem
- Centralized AI (OpenAI, Anthropic): "Trust us, our models are good"
- Existing decentralized compute (Golem, iExec): No AI verification
- AI + Blockchain projects (Fetch.ai): Vague promises, no real tech

### Aurora's Solution
1. **Proof of Intelligence (PoI)**: Every model = verifiable hash on-chain
2. **Browser-native**: WASM client, no setup, 1-click start
3. **Earn-by-contribution**: Run relays, host models, operate DNS → earn tokens
4. **Trinity_3 Engine**: Ternary logic + fractal tensors (3-5 year moat)

## 🎯 Core Features

- **Decentralized Identity** (DID): Ed25519 cryptographic identity
- **P2P Connectivity**: libp2p with WebSocket/WebRTC (no open ports needed)
- **Blockchain Integration**: Aurora L2 for model registry & settlements
- **Model Execution**: ONNX Runtime in WASM with hash verification
- **Ethical AI**: Computational honesty (NULL values instead of hallucinations)

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Aurora Ecosystem                          │
├─────────────────────────────────────────────────────────────┤
│  L7: Culture & Governance (Ethici, InnovaLab, Cooperative) │
│  L6: Real Economy (Mobility, Housing, Education, Energy)    │
│  L5: Service Layer (Unified API & Digital Services)         │
│  L4: Orchestration (The Ethical Cloud)                      │
│  L3: Intelligence (Collaborative Models Network)            │
│  L2: Trust (Blockchain & Integrity)                         │
│  L1: Physical (GPUs, CPUs, Storage, Bandwidth)              │
└─────────────────────────────────────────────────────────────┘

Aurora Portal = Web entry point that delivers the WASM client
```

## 📁 Project Structure

```
Portal/
├── index.html              # Main portal page
├── assets/                 # Static assets (logo, images)
│   └── aurora-portal-logo.png
├── js/                     # JavaScript integration
│   └── aurora-portal.js    # WASM client integration
├── wasm-client/            # Rust WASM client
│   ├── src/
│   │   ├── lib.rs          # WASM entry point
│   │   ├── agent.rs        # Aurora Agent
│   │   ├── p2p.rs          # P2P networking (libp2p)
│   │   ├── blockchain.rs   # Blockchain interface
│   │   ├── models.rs       # Model registry
│   │   ├── crypto.rs       # Identity & cryptography
│   │   └── storage.rs      # LocalStorage wrapper
│   ├── Cargo.toml          # Rust dependencies
│   ├── build.ps1           # Build script (PowerShell)
│   └── README.md           # WASM client docs
├── Infrastructure/         # CloudFormation templates
│   └── main.yml            # S3 + CloudFront setup
├── Docs/                   # Documentation
│   └── AuroraPortal.md     # Complete specification
└── README.md               # This file
```

## ⚡ The AI Advantage

**Why Aurora is achievable in 18 months** (vs 3-5 years for similar projects in 2014-2020):

| Task | 2017 (Solo) | 2025 (Solo + Copilot) | Speedup |
|------|-------------|----------------------|---------|
| P2P networking | 3 weeks | 4 days | 5x |
| Smart contracts | 2 weeks | 3 days | 4x |
| WASM integration | 4 weeks | 1 week | 4x |
| Documentation | 1 week | 1 day | 5x |
| **Overall** | - | - | **~4x** |

**In this project**:
- 8 Rust modules (1,300 lines): 2 hours vs 2 weeks
- 7 docs (5,100 lines): 3 hours vs 1 week
- Trinity_3 analysis (2,206 lines): 20 mins vs 2 days

**Read more**: [Why Aurora Will Succeed](WHY_AURORA_WILL_SUCCEED.md)

---

## 🚀 Quick Start

### Prerequisites

- **Rust** (stable) - [Install](https://rustup.rs/)
- **wasm-pack** - `cargo install wasm-pack`
- **Python 3** (for local server) or **Node.js**
- **GitHub Copilot** (recommended for development)

### Build the WASM Client

```powershell
# Navigate to wasm-client directory
cd wasm-client

# Development build
.\build.ps1 -BuildType dev

# Production build (optimized)
.\build.ps1 -BuildType release
```

### Run Locally

```powershell
# From project root
python -m http.server 8000

# Open browser
# http://localhost:8000/index.html
```

## 🔧 Development

### Build WASM for Different Targets

```powershell
# For web (default)
.\build.ps1 -Target web

# For bundlers (webpack, vite, rollup)
.\build.ps1 -Target bundler

# For Node.js
.\build.ps1 -Target nodejs
```

### Test

```bash
# Run Rust tests
cd wasm-client
cargo test

# Run WASM tests in browser
wasm-pack test --headless --firefox
```

## 📦 Deployment

### Deploy to AWS (S3 + CloudFront)

The `Infrastructure/main.yml` CloudFormation template creates:
- S3 bucket with encryption and versioning
- Bucket policy allowing CloudFront access
- Outputs for bucket name and ARN

```powershell
# Deploy CloudFormation stack
aws cloudformation create-stack \
  --stack-name aurora-portal \
  --template-body file://Infrastructure/main.yml \
  --parameters ParameterKey=BucketName,ParameterValue=aurora-portal-code \
               ParameterKey=CloudFrontOriginAccessIdentity,ParameterValue=<OAI-ID>

# Build WASM for production
cd wasm-client
.\build.ps1 -BuildType release

# Upload to S3
aws s3 sync . s3://aurora-portal-code/ --exclude "wasm-client/target/*" --exclude ".git/*"

# Invalidate CloudFront cache
aws cloudfront create-invalidation --distribution-id <DIST-ID> --paths "/*"
```

## 🌐 Key Features

### 1. Decentralized Identity (DID)
- Ed25519 keypair generation
- Persistent identity in browser LocalStorage
- `did:aurora:` identifier scheme

### 2. P2P Networking
- libp2p with WebSocket/WebRTC transports
- Circuit relay for NAT traversal (no open ports needed)
- Kademlia DHT for peer discovery
- Gossipsub for pub/sub messaging

### 3. Blockchain Integration
- Model registry (on-chain)
- Service offers and bids
- Session tracking with SLOs
- Automated settlements (payments, royalties, reputation)

### 4. Model Management
- Hash-based model identification (keccak256)
- Verify model integrity
- Load models from IPFS/Arweave
- Execute models with SLO tracking

### 5. Ethical Operating Principles
- Collective well-being prioritized
- Risk and compliance checks embedded
- Intrinsic apoptosis if consensus fails

## 🤝 Contributing

Aurora Portal is open source (Apache 2.0 license) and welcomes contributions!

### How to contribute:

1. **Infrastructure**: Run domains, DNS, portals, relays → earn tokens
2. **Models**: Create, share, and improve AI models → earn royalties
3. **Code**: Submit PRs to improve the portal and WASM client
4. **Documentation**: Help others understand and use Aurora
5. **Community**: Participate in governance and ethical discussions

## 📚 Documentation

### Core Docs
- [Complete Specification](Docs/AuroraPortal.md) - Full Aurora Portal spec (v0.2)
- [Trinity_3 Engine](Docs/trinity_3.md) - Ternary logic + fractal tensors (2,206 lines)
- [WASM Client README](wasm-client/README.md) - Detailed WASM client docs

### Project Planning
- [Roadmap](ROADMAP.md) - 10-phase development plan (18 months)
- [Execution Strategy](EXECUTION_STRATEGY.md) - 18-month plan with AI acceleration
- [Why Aurora Will Succeed](WHY_AURORA_WILL_SUCCEED.md) - Historical comparison
- [Contributing Guide](CONTRIBUTING.md) - How to contribute

### Quick References
- [Quick Start](QUICKSTART.md) - 5-minute getting started guide
- [Implementation Summary](IMPLEMENTATION_SUMMARY.md) - Technical overview
- [Project Structure](STRUCTURE.md) - File organization

### External Links
- [Aurora Program](https://www.auroraprogram.org) - Main website
- [Community Foundation Articles](https://docs.auroraprogram.org) - Ethical principles

## 🔐 Security

- **Identity**: Private keys stored in LocalStorage (encrypt in production)
- **Transport**: Use WSS (WebSocket Secure) for all P2P connections
- **Model Verification**: Always verify model hash before execution
- **CSP**: Configure Content Security Policy headers

Report security vulnerabilities to: security@auroraprogram.org

## 📄 License

Apache License 2.0

This license ensures that Aurora Portal is free to use, modify, and distribute, both in personal and commercial contexts, while preserving proper attribution to the community.

No single entity owns the network — it belongs to all who help it grow.

## 🌍 Community

- **Website**: [aurora program.org](https://www.auroraprogram.org)
- **Portal**: [portal.auroraprogram.org](https://portal.auroraprogram.org)
- **GitHub**: [github.com/Aurora-Program](https://github.com/Aurora-Program)

---

**Aurora Portal** - Where ethical intelligence meets decentralized collaboration.

*"The agent is designed to reinforce and protect the stability of the network, placing collective well-being above its own operations."*
