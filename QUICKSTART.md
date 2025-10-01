# Aurora Portal - Quick Start Guide

Get Aurora Portal running in **5 minutes**!

## ⚡ Prerequisites

Install these tools:

```powershell
# 1. Install Rust
# Visit: https://rustup.rs/
# Or on Windows with winget:
winget install Rustlang.Rustup

# 2. Install wasm-pack
cargo install wasm-pack

# 3. Python (for local server) - likely already installed
python --version
```

## 🚀 Build & Run

### Step 1: Clone Repository

```powershell
git clone https://github.com/Aurora-Program/Portal.git
cd Portal
```

### Step 2: Build WASM Client

```powershell
cd wasm-client
.\build.ps1 -BuildType dev
```

**Expected output:**
```
Building Aurora WASM Client...
Build type: dev
Target: web

[INFO]: Checking for the Wasm target...
[INFO]: Compiling to Wasm...
   Compiling aurora-wasm-client v0.1.0
    Finished dev [unoptimized + debuginfo] target(s)
[INFO]: Installing wasm-bindgen...
[INFO]: Optimizing wasm binaries with `wasm-opt`...
[INFO]: Done in 45.23s

Build successful!
Output directory: wasm-client\pkg

Generated files:
  aurora_wasm_client_bg.wasm - 234.56 KB
  aurora_wasm_client.js - 12.34 KB
  aurora_wasm_client.d.ts - 3.45 KB
```

### Step 3: Run Local Server

```powershell
cd ..
python -m http.server 8000
```

**Alternative (Node.js):**
```powershell
npx http-server -p 8000
```

### Step 4: Open Browser

Navigate to: **http://localhost:8000/index.html**

You should see:
- ✅ Aurora Portal logo
- ✅ "Building the future." tagline
- ✅ Status: "Initializing Aurora Intelligence System..."
- ✅ Browser console shows WASM loading logs

## 🔍 Verify Installation

Open browser DevTools (F12) and check console:

```
Aurora Portal loading...
Initializing Aurora Portal...
WASM module loaded successfully
Aurora Client Version: 0.1.0
Health check: true
Aurora Agent created
Identity loaded: did:aurora:1234abcd...
Connected to P2P network
Authenticated with blockchain
Aurora Portal ready!
```

## 🎨 What You See

The portal displays:

1. **Aurora Logo** (centered)
2. **Title**: "Aurora Portal"
3. **Tagline**: "Building the future."
4. **Status Indicator**: Real-time connection status
5. **Info Row**:
   - P2P: 0 peers (will update when connected)
   - DID: Your decentralized identifier
6. **Footer**: Copyright Aurora Program

## 🐛 Troubleshooting

### Build Fails

**Problem**: `wasm-pack: command not found`
```powershell
cargo install wasm-pack
```

**Problem**: Rust not installed
```powershell
# Visit: https://rustup.rs/
# Follow installation instructions
```

**Problem**: `error: linker 'link.exe' not found`
```powershell
# Install Visual Studio Build Tools
# Visit: https://visualstudio.microsoft.com/downloads/
# Select "Desktop development with C++"
```

### WASM Not Loading

**Problem**: 404 on `aurora_wasm_client.wasm`

**Solution**: Check file paths:
```powershell
# Verify pkg/ exists
ls wasm-client\pkg

# Should see:
# - aurora_wasm_client_bg.wasm
# - aurora_wasm_client.js
# - aurora_wasm_client.d.ts
```

**Problem**: CORS errors

**Solution**: Use a proper server (not file://)
```powershell
python -m http.server 8000
```

### Console Errors

**Problem**: `Failed to initialize identity`

**Solution**: Check LocalStorage is enabled in browser

**Problem**: `P2P connection failed`

**Solution**: This is expected! Relay nodes need to be configured.
See [WASM Client README](wasm-client/README.md) for relay setup.

## 📝 Configuration

### Edit Relay Nodes

**File**: `js/aurora-portal.js`

```javascript
this.config = {
  relay_nodes: [
    '/dns4/your-relay1.example.com/tcp/443/wss/p2p/12D3KooW...',
    '/dns4/your-relay2.example.com/tcp/443/wss/p2p/12D3KooW...'
  ],
  blockchain_rpc: 'https://your-rpc.example.com',
  bootstrap_models: [
    '0xYourModelHash1...',
    '0xYourModelHash2...'
  ]
};
```

### Production Build

For deployment:

```powershell
cd wasm-client
.\build.ps1 -BuildType release

# Output will be optimized (smaller size)
# Expected: ~150-200 KB compressed
```

## 🚢 Deploy to Production

### AWS (S3 + CloudFormation)

```powershell
# 1. Deploy infrastructure
aws cloudformation create-stack \
  --stack-name aurora-portal \
  --template-body file://Infrastructure/main.yml

# 2. Build for production
cd wasm-client
.\build.ps1 -BuildType release

# 3. Upload to S3
cd ..
aws s3 sync . s3://your-bucket-name/ `
  --exclude ".git/*" `
  --exclude "wasm-client/target/*" `
  --exclude "*.md"

# 4. Invalidate CloudFront cache
aws cloudfront create-invalidation `
  --distribution-id YOUR_DIST_ID `
  --paths "/*"
```

## 📚 Next Steps

1. **Read Documentation**:
   - [Main README](README.md)
   - [WASM Client README](wasm-client/README.md)
   - [Implementation Summary](IMPLEMENTATION_SUMMARY.md)

2. **Customize**:
   - Update logo (`assets/aurora-portal-logo.png`)
   - Edit colors in `index.html` CSS
   - Configure relay nodes

3. **Develop**:
   - Add features to WASM client
   - Implement P2P connections
   - Integrate blockchain

4. **Contribute**:
   - See [CONTRIBUTING.md](CONTRIBUTING.md)
   - Join community discussions

## 💡 Tips

### Fast Iteration

Use `--dev` builds during development (faster):
```powershell
.\build.ps1 -BuildType dev
```

Use `--release` only for production:
```powershell
.\build.ps1 -BuildType release
```

### Watch Mode

Install cargo-watch for auto-rebuild:
```powershell
cargo install cargo-watch

# In wasm-client/ directory:
cargo watch -s "wasm-pack build --target web --dev"
```

### Browser DevTools

- **Console**: See logs and errors
- **Network**: Check WASM file size and load time
- **Application → Storage → Local Storage**: See stored identity
- **Performance**: Profile WASM execution

## 🎓 Learning Resources

- [Rust Book](https://doc.rust-lang.org/book/)
- [Rust and WebAssembly Book](https://rustwasm.github.io/docs/book/)
- [wasm-bindgen Guide](https://rustwasm.github.io/docs/wasm-bindgen/)
- [libp2p Docs](https://docs.libp2p.io/)
- [Aurora Portal Spec](Docs/AuroraPortal.md)

## 🆘 Get Help

- **Documentation**: Check README files
- **GitHub Issues**: Report bugs or ask questions
- **Community**: Join discussions (coming soon)
- **Email**: contact@auroraprogram.org

## ✅ Success Checklist

- [ ] Rust installed
- [ ] wasm-pack installed
- [ ] Repository cloned
- [ ] WASM built successfully
- [ ] Local server running
- [ ] Portal loads in browser
- [ ] No console errors (except P2P connection - expected)
- [ ] DID displayed in UI

If all checked, you're ready to develop! 🎉

---

**Aurora Portal** - *Building the future through ethical intelligence.*

**Time to complete**: ~5 minutes  
**Difficulty**: Easy  
**Next**: [Read the full README](README.md)
