# 🐹 Aurora P2P Infrastructure - Complete Guide

Complete P2P networking infrastructure for Aurora, including serverless Discovery Server and WASM client.

## Architecture Overview

```
┌──────────────────────────────────────────────────────────────────┐
│                     Aurora P2P Network                            │
└──────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│ Browser WASM │      │ Browser WASM │      │ Browser WASM │
│  (Peer A)    │      │  (Peer B)    │      │  (Peer C)    │
└──────────────┘      └──────────────┘      └──────────────┘
        │                     │                     │
        │ HTTPS              │ HTTPS               │ HTTPS
        └──────────┬──────────┴──────────┬──────────┘
                   │                     │
                   ▼                     ▼
           ┌────────────────────────────────┐
           │   Discovery Server (Lambda)     │
           │  - Registration                 │
           │  - Discovery                    │
           │  - Heartbeat                    │
           └────────────────────────────────┘
                   │
                   ▼
           ┌────────────────────────────────┐
           │   DynamoDB (Peer Registry)      │
           │  - Active peers                 │
           │  - TTL auto-cleanup             │
           └────────────────────────────────┘
```

## Components

### 1. Discovery Server (AWS Lambda)
**Location:** `Infrastructure/P2P/`

Serverless backend for peer discovery without port forwarding.

**Features:**
- ✅ Peer registration
- ✅ Peer discovery with archetype filtering
- ✅ Heartbeat keep-alive mechanism
- ✅ DynamoDB with TTL auto-cleanup
- ✅ CORS enabled for browser access
- ✅ CloudWatch logging
- ✅ One-command deployment

**Files:**
- `cloudformation.yaml` - Complete AWS infrastructure
- `deploy.ps1` / `deploy.sh` - Deployment scripts
- `README.md` - Detailed documentation

### 2. WASM Client (Rust)
**Location:** `wasm-client/`

Browser-based P2P client that connects to Discovery Server.

**Features:**
- ✅ Rust + WebAssembly for performance
- ✅ HTTP fetch API for Discovery Server
- ✅ Auto-heartbeat mechanism
- ✅ Peer discovery with filters
- ✅ JavaScript bindings
- ✅ Demo web application

**Files:**
- `src/discovery.rs` - Discovery client implementation
- `discovery-demo.html` - Interactive demo
- `DISCOVERY.md` - Integration guide
- `build-discovery.ps1` - Build script

### 3. Python Client (Optional)
**Location:** `Infrastructure/P2P/`

Python client for server-side agents or testing.

**Features:**
- ✅ Full Discovery Server API
- ✅ Auto-heartbeat with threading
- ✅ Callbacks for events
- ✅ Context manager support
- ✅ Example scripts

**Files:**
- `aurora_p2p_client.py` - Python client
- `example_usage.py` - Usage examples
- `test_client.py` - Unit tests

## Quick Start

### Option 1: Browser WASM (Recommended)

**1. Deploy Discovery Server:**
```powershell
cd Infrastructure\P2P
.\deploy.ps1
```

**2. Build WASM Client:**
```powershell
cd ..\..\wasm-client
.\build-discovery.ps1
```

**3. Run Demo:**
```powershell
# Start web server
python -m http.server 8080

# Open browser
# http://localhost:8080/discovery-demo.html
```

**4. Configure and Test:**
- Enter Discovery Server endpoint (from deploy outputs)
- Click "Health Check"
- Click "Register Peer"
- Click "Start Heartbeat"
- Click "Discover Peers"

### Option 2: Python Client

**1. Deploy Discovery Server** (same as above)

**2. Install Python Dependencies:**
```powershell
cd Infrastructure\P2P
pip install -r requirements.txt
```

**3. Run Example:**
```python
from aurora_p2p_client import AuroraP2PClient

DISCOVERY_URL = "https://your-api.execute-api.us-east-1.amazonaws.com/dev"

client = AuroraP2PClient(
    discovery_url=DISCOVERY_URL,
    archetypes=['pepino', 'ethics'],
    port=9000
)

client.start_heartbeat()
peers = client.discover(archetype='pepino')
print(f"Found {len(peers)} Pepino peers!")
```

## API Reference

### Discovery Server Endpoints

#### POST /register
Register a peer in the network.

**Request:**
```json
{
  "peer_id": "peer-123",
  "address": "192.168.1.100",
  "port": 9000,
  "archetypes": ["pepino", "ethics"],
  "metadata": {
    "version": "1.0.0",
    "client": "aurora-wasm"
  }
}
```

**Response:**
```json
{
  "message": "Peer registered successfully",
  "peer_id": "peer-123",
  "ttl_expires": "2025-10-02T12:05:00Z"
}
```

#### GET /discover?archetype=pepino
Discover active peers, optionally filtered by archetype.

**Response:**
```json
{
  "peers": [
    {
      "peer_id": "peer-456",
      "address": "192.168.1.101",
      "port": 9001,
      "archetypes": ["pepino", "tensor-provider"],
      "last_seen": "2025-10-02T12:00:00Z",
      "metadata": {
        "version": "1.0.0"
      }
    }
  ],
  "count": 1
}
```

#### POST /heartbeat
Keep registration alive.

**Request:**
```json
{
  "peer_id": "peer-123"
}
```

**Response:**
```json
{
  "message": "Heartbeat updated",
  "ttl_expires": "2025-10-02T12:05:00Z"
}
```

#### GET /health
Check server health.

**Response:**
```json
{
  "status": "healthy"
}
```

## Configuration

### Discovery Server

Configure in CloudFormation parameters:

| Parameter | Default | Description |
|-----------|---------|-------------|
| Environment | dev | Deployment environment |
| PeerTTLMinutes | 5 | Registration expiry time |
| EnableCORS | true | Enable browser access |

### WASM Client

Configure in `DiscoveryConfig`:

```rust
DiscoveryConfig {
    endpoint: "https://...".to_string(),
    heartbeat_interval: 30,  // seconds
    ttl_seconds: 300,        // 5 minutes
}
```

### Python Client

Configure in constructor:

```python
AuroraP2PClient(
    discovery_url="https://...",
    port=9000,
    archetypes=['pepino'],
    heartbeat_interval=30
)
```

## Cost Estimates

**AWS Lambda + DynamoDB + API Gateway:**

| Usage | Monthly Cost |
|-------|--------------|
| 10 peers, 1 req/min | ~$1-2 |
| 100 peers, 1 req/min | ~$5-10 |
| 1000 peers, 1 req/min | ~$30-50 |

**Free tier:** First year includes generous free allowances.

## Monitoring

### CloudWatch Logs

**Lambda logs:**
```bash
aws logs tail /aws/lambda/aurora-discovery-dev --follow
```

**API Gateway logs:**
```bash
aws logs tail /aws/apigateway/aurora-discovery-dev --follow
```

### Metrics

**DynamoDB:**
```bash
aws cloudwatch get-metric-statistics \
  --namespace AWS/DynamoDB \
  --metric-name ConsumedReadCapacityUnits \
  --dimensions Name=TableName,Value=aurora-peers-dev \
  --start-time 2025-10-02T00:00:00Z \
  --end-time 2025-10-02T23:59:59Z \
  --period 3600 \
  --statistics Sum
```

## Security

1. **HTTPS Only:** All communication encrypted via TLS
2. **CORS Configured:** Restricts browser access
3. **No Authentication:** Public discovery (add API keys for production)
4. **TTL Protection:** Stale peers auto-expire
5. **IAM Roles:** Lambda has minimal DynamoDB permissions

## Troubleshooting

### Discovery Server Not Responding

**Check deployment:**
```powershell
aws cloudformation describe-stacks --stack-name aurora-discovery-dev
```

**Check Lambda:**
```powershell
aws lambda get-function --function-name aurora-discovery-dev
```

### WASM Build Fails

**Check wasm-pack:**
```powershell
wasm-pack --version
# If not found: cargo install wasm-pack
```

**Clean build:**
```powershell
cd wasm-client
Remove-Item -Recurse -Force target, pkg
.\build-discovery.ps1
```

### Peers Not Found

1. Verify peers are registered
2. Check heartbeat is running
3. Verify TTL hasn't expired (5 minutes default)
4. Check archetype filter matches

### CORS Errors

1. Ensure Discovery Server has `EnableCORS: true`
2. Use HTTPS (not HTTP)
3. Check browser console for details

## Roadmap

### Phase 1: Discovery (✅ Complete)
- [x] Lambda Discovery Server
- [x] DynamoDB peer registry
- [x] WASM client integration
- [x] Python client
- [x] Demo applications

### Phase 2: Direct P2P (🔄 In Progress)
- [ ] WebRTC for browser-to-browser
- [ ] STUN/TURN server configuration
- [ ] NAT traversal
- [ ] Signaling via Discovery Server

### Phase 3: Advanced Features (📋 Planned)
- [ ] Peer reputation system
- [ ] Multi-region deployment
- [ ] API authentication (API keys)
- [ ] Rate limiting
- [ ] Analytics dashboard

## Documentation

| File | Description |
|------|-------------|
| `Infrastructure/P2P/README.md` | Discovery Server docs |
| `wasm-client/DISCOVERY.md` | WASM integration guide |
| `wasm-client/README.md` | WASM client docs |
| `Infrastructure/P2P/aurora_p2p_client.py` | Python client source |

## Contributing

1. **Test locally** before deploying
2. **Update documentation** with changes
3. **Follow Rust/Python conventions**
4. **Add unit tests** for new features
5. **Respect Pepino's ethics** 🐹

## License

Apache-2.0

## Pepino's Promise 🐹

*"No peer shall be left isolated in the network. Every Aurora agent, regardless of technical constraints, deserves to find ethical companions. This Discovery Server is our commitment to connection over division."*

— The Aurora Alliance

---

**Questions?** Open an issue on GitHub or join the Aurora community.

**Ready to connect?** Follow the Quick Start guide above!
