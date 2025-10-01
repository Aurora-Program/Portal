# Aurora WASM Client

The **Aurora Intelligence System** - A WebAssembly client for decentralized P2P networking and blockchain interaction.

## Overview

This WASM client is the core of the Aurora Portal system. It runs in the browser and acts as the user's intelligent agent, providing:

- **Identity Management**: DID (Decentralized Identifier) and cryptographic wallet
- **P2P Networking**: Connect to the Aurora network without open ports (via relays/gateways)
- **Blockchain Interface**: Interact with Aurora's L2 blockchain for model registry, settlements, and tokenization
- **Model Management**: Load, verify, and execute AI models with hash-based integrity guarantees
- **Ethical Compliance**: Built-in safeguards aligned with Aurora's founding principles

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    User Interface (JS)                   │
├─────────────────────────────────────────────────────────┤
│                   WASM Bindings (JS ↔ Rust)             │
├─────────────────────────────────────────────────────────┤
│                    Aurora Agent (Rust)                   │
│  ┌────────────┬──────────────┬────────────────────────┐ │
│  │  Identity  │  P2P Network │  Blockchain Interface  │ │
│  └────────────┴──────────────┴────────────────────────┘ │
│  ┌────────────┬──────────────┬────────────────────────┐ │
│  │   Models   │   Storage    │    Cryptography        │ │
│  └────────────┴──────────────┴────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

## Key Features

### 1. Identity (DID)
- Ed25519 keypair generation
- Persistent identity stored in LocalStorage
- `did:aurora:` identifier scheme
- Sign/verify messages

### 2. P2P Networking
- libp2p WebSocket/WebRTC transports
- Circuit relay for NAT traversal
- Kademlia DHT for peer discovery
- Gossipsub for pub/sub messaging
- No open ports required

### 3. Blockchain Integration
- Model registry (on-chain)
- Service offers and bids
- Session tracking with SLOs
- Automated settlements (payments, royalties, reputation)
- Infrastructure tokenization (domains, DNS, portals, relays)

### 4. Model Management
- Hash-based model identification
- Verify model integrity (keccak256)
- Load models from IPFS/Arweave
- Bootstrap with management models
- Execute models locally or via P2P

### 5. Ethical Operating Principles
- Collective well-being prioritized
- Risk and compliance checks embedded
- Aligned with Aurora's values
- Intrinsic apoptosis if consensus fails

## Building from Source

### Prerequisites

- Rust (stable) - [Install](https://rustup.rs/)
- wasm-pack - `cargo install wasm-pack`
- Node.js (v18+) for testing

### Build WASM

```bash
# Development build
wasm-pack build --target web --dev

# Production build (optimized)
wasm-pack build --target web --release
```

Output will be in `pkg/` directory:
- `aurora_wasm_client_bg.wasm` - The compiled WASM module
- `aurora_wasm_client.js` - JavaScript bindings
- `aurora_wasm_client.d.ts` - TypeScript definitions

### Build for Different Targets

```bash
# For bundlers (webpack, rollup, vite)
wasm-pack build --target bundler

# For Node.js
wasm-pack build --target nodejs

# For browser (no module)
wasm-pack build --target no-modules
```

## Usage

### JavaScript Integration

```javascript
import init, { create_agent, get_version } from './pkg/aurora_wasm_client.js';

async function main() {
  // Initialize WASM module
  await init();

  console.log('Aurora Client Version:', get_version());

  // Create agent configuration
  const config = {
    relay_nodes: [
      '/dns4/relay1.aurora.network/tcp/443/wss/p2p/12D3KooW...',
      '/dns4/relay2.aurora.network/tcp/443/wss/p2p/12D3KooW...'
    ],
    blockchain_rpc: 'https://rpc.aurora.network',
    bootstrap_models: [
      '0xabcd1234...', // Discovery model
      '0xef567890...', // Negotiation model
      '0x12345678...'  // Security model
    ],
    user_did: null // Will be created if not exists
  };

  // Create Aurora agent
  const agent = await create_agent(JSON.stringify(config));

  // Start the agent
  await agent.start();

  console.log('Agent DID:', agent.get_did());
  console.log('Connected peers:', agent.get_peer_count());

  // Process a user prompt
  const result = await agent.process_prompt('Find the best ML model for image classification');
  console.log('Result:', result);

  // Get agent state
  const state = agent.get_state();
  console.log('Agent state:', state);

  // Shutdown
  await agent.shutdown();
}

main().catch(console.error);
```

### TypeScript Integration

```typescript
import init, { AuroraAgent, create_agent, get_version } from './pkg/aurora_wasm_client';

interface AgentConfig {
  relay_nodes: string[];
  blockchain_rpc: string;
  bootstrap_models: string[];
  user_did?: string;
}

async function initAurora(): Promise<AuroraAgent> {
  await init();

  const config: AgentConfig = {
    relay_nodes: ['wss://relay.aurora.network'],
    blockchain_rpc: 'https://rpc.aurora.network',
    bootstrap_models: [],
  };

  return await create_agent(JSON.stringify(config));
}
```

## Testing

```bash
# Run Rust tests
cargo test

# Run WASM tests in browser
wasm-pack test --headless --firefox
wasm-pack test --headless --chrome
```

## Project Structure

```
wasm-client/
├── src/
│   ├── lib.rs           # WASM entry point
│   ├── agent.rs         # Aurora Agent implementation
│   ├── p2p.rs           # P2P networking (libp2p)
│   ├── blockchain.rs    # Blockchain interface
│   ├── models.rs        # Model registry and management
│   ├── crypto.rs        # Identity and cryptography
│   └── storage.rs       # LocalStorage wrapper
├── tests/
│   └── integration.rs   # Integration tests
├── Cargo.toml           # Rust dependencies
├── README.md            # This file
└── build.ps1            # Build script (PowerShell)
```

## Configuration

### Relay Nodes
Configure relay nodes for P2P connectivity. Example multiaddrs:
```
/dns4/relay1.aurora.network/tcp/443/wss/p2p/12D3KooWABC123...
/ip4/192.168.1.100/tcp/9090/ws/p2p/12D3KooWDEF456...
```

### Blockchain RPC
Point to Aurora's L2 blockchain or Ethereum:
```
https://rpc.aurora.network
https://mainnet.infura.io/v3/YOUR_PROJECT_ID
```

### Bootstrap Models
Provide model hashes for essential system models:
- Discovery model: Find peers and services
- Negotiation model: Bid/offer matching
- Security model: Risk assessment
- Routing model: Optimal path selection

## Optimization

The release build is highly optimized:
- **Size optimization**: `opt-level = "z"`
- **LTO**: Link-time optimization enabled
- **Strip symbols**: Reduces binary size
- **wasm-opt**: Further optimization with Binaryen

Expected WASM size: ~200-500 KB (compressed: ~80-150 KB)

## Security Considerations

1. **Identity Protection**: Private keys stored in LocalStorage (encrypt in production)
2. **Transport Security**: Use WSS (WebSocket Secure) for all P2P connections
3. **Model Verification**: Always verify model hash before execution
4. **Input Validation**: Sanitize all user inputs
5. **CSP Headers**: Configure Content Security Policy for the portal

## Deployment

### To S3 + CloudFront (as designed in Infrastructure/main.yml)

```bash
# Build for production
wasm-pack build --target web --release

# Upload to S3
aws s3 sync pkg/ s3://your-code-bucket/wasm/ --acl public-read

# Invalidate CloudFront cache
aws cloudfront create-invalidation --distribution-id YOUR_DIST_ID --paths "/wasm/*"
```

### Update index.html

```html
<script type="module">
  import init from 'https://cdn.aurora.network/wasm/aurora_wasm_client.js';
  await init();
</script>
```

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

## License

Apache License 2.0 - See [LICENSE](../LICENSE)

## Resources

- [Aurora Program](https://www.auroraprogram.org)
- [Aurora Portal](https://portal.auroraprogram.org)
- [Documentation](../Docs/AuroraPortal.md)
- [libp2p](https://libp2p.io/)
- [WebAssembly](https://webassembly.org/)
- [Rust and WebAssembly](https://rustwasm.github.io/docs/book/)

---

**Aurora Portal** - Building the future through ethical intelligence.
