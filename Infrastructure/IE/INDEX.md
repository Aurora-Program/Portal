# 🧬 Genesis + IE Documentation Index

**Layer 3 (Intelligence Layer)** - Genesis Integration & Adaptive Economics

---

## 📚 Documentación Genesis

### 🎯 Para Empezar

**[README_GENESIS.md](./README_GENESIS.md)** - Resumen Ejecutivo
- ✅ ¿Qué es Genesis y por qué integrarlo?
- ✅ Estado actual y roadmap
- ✅ 3 documentos principales explicados
- ✅ Próximos pasos inmediatos
- ✅ FAQs y troubleshooting

---

### 📖 Documentos Principales

#### 1. **[GENESIS_ARCHITECTURE.md](./GENESIS_ARCHITECTURE.md)** - Arquitectura MCP Modular ⭐ NUEVO
   - **Audiencia:** Arquitectos, Researchers, Core Developers
   - **Contenido:**
     - Arquitectura completa de 5 microservicios MCP
     - FFE 3-9-27: Tensores fractales (vs embeddings planos)
     - Trigates, Transcender, FFEStore, Evolver
     - Knowledge Graph Híbrido (KG + FFE)
     - Métricas operativas (C_meta, C_ext, C_dyn)
     - Circuit Breaker + Resiliencia
     - Optimización memoria fractal
     - FractalAttention (Phase 4)
     - Schema v1.0 + Terminología pulida
   - **Duración lectura:** 60 minutos
   - **Código incluido:** ✅ Python (completo), pseudocódigo
   - **Tests:** 19/19 passing

#### 2. **[GENESIS_L3_INTEGRATION.md](./GENESIS_L3_INTEGRATION.md)** - Integración en Portal L3
   - **Audiencia:** Arquitectos, Dev Leads
   - **Contenido:**
     - Integración L2 ↔ L3 (Blockchain + Intelligence)
     - Genesis en WASM Client
     - P2P Intelligence Mesh
     - Proof of Intelligence (K-of-M)
     - Intrinsic Apoptosis
     - Casos de uso (Medical Diagnosis, Logistics)
     - Smart contracts (AuroraRegistry.sol, ProofOfIntelligence.sol)
     - Métricas del sistema
   - **Duración lectura:** 45 minutos
   - **Código incluido:** ✅ Rust, Solidity, Python, JavaScript

#### 3. **[GENESIS_ROADMAP.md](./GENESIS_ROADMAP.md)** - Plan de Implementación
   - **Audiencia:** Project Managers, Dev Team
   - **Contenido:**
     - 4 Fases (14 semanas)
     - 24 Hitos con tareas detalladas
     - Dependencias y bloqueadores
     - KPIs y métricas de éxito
     - Calendario con ETAs
     - Checklist pre-start
   - **Duración lectura:** 30 minutos
   - **Formato:** Tareas ejecutables con comandos

#### 4. **[GENESIS_QUICK_START.md](./GENESIS_QUICK_START.md)** - Inicio Rápido
   - **Audiencia:** Developers, DevOps
   - **Contenido:**
     - Setup inicial (30 minutos)
     - Comandos exactos PowerShell
     - Compilación WASM paso a paso
     - Test rápido HTML
     - Troubleshooting común
   - **Duración lectura:** 15 minutos
   - **Ejecutable:** ✅ Copy-paste commands ready

---

## 📊 Comparación Rápida

| Documento | Objetivo | Tiempo | Técnico | Ejecutable |
|-----------|----------|--------|---------|------------|
| **README_GENESIS** | Introducción | 10 min | 🟡 Medio | ❌ |
| **ARCHITECTURE** | Genesis Core (MCP) | 60 min | 🔴 Muy Alto | ⚠️ Pseudocódigo |
| **L3_INTEGRATION** | Portal Integration | 45 min | 🔴 Alto | ⚠️ Parcial |
| **ROADMAP** | Planificación | 30 min | 🟡 Medio | ✅ Tareas |
| **QUICK_START** | Setup | 15 min | 🟢 Básico | ✅ Full |

---

## 🚀 ¿Qué Leer Primero?

### Si eres **Developer** (implementar ahora):
1. ✅ **GENESIS_QUICK_START.md** (30 min setup)
2. ✅ **GENESIS_ARCHITECTURE.md** (sections: Microservicios MCP, Uso Rápido)
3. ✅ **GENESIS_L3_INTEGRATION.md** (section 2: WASM Client)
4. ✅ **GENESIS_ROADMAP.md** (Phase 1 tasks)

### Si eres **Architect** (diseñar sistema):
1. ✅ **README_GENESIS.md** (overview)
2. ✅ **GENESIS_ARCHITECTURE.md** (completo - 60 min)
3. ✅ **GENESIS_L3_INTEGRATION.md** (Portal integration)
4. ✅ **GENESIS_ROADMAP.md** (dependencias y KPIs)

### Si eres **Researcher** (entender teoría):
1. ✅ **GENESIS_ARCHITECTURE.md** (Principio Triádico, FFE 3-9-27, Coherencia)
2. ✅ **GENESIS_L3_INTEGRATION.md** (PoI, Intrinsic Apoptosis)
3. ✅ Genesis repo: `../../Genesis/docs/genesis.md` (manifiesto original)

### Si eres **Project Manager** (planificar):
1. ✅ **README_GENESIS.md** (resumen ejecutivo)
2. ✅ **GENESIS_ROADMAP.md** (calendario y hitos)
3. ✅ **GENESIS_L3_INTEGRATION.md** (casos de uso)

### Si eres **Stakeholder** (decisión estratégica):
1. ✅ **README_GENESIS.md** (completo)
2. ✅ **GENESIS_L3_INTEGRATION.md** (section 1: ¿Por qué?)
3. ✅ Skip ROADMAP y QUICK_START (detalles técnicos)

---

## 📁 Estructura de Archivos

```
Infrastructure/IE/
│
├── 🧬 Genesis Integration (NEW)
│   ├── README_GENESIS.md              ← Empieza aquí
│   ├── GENESIS_L3_INTEGRATION.md      ← Arquitectura completa
│   ├── GENESIS_ROADMAP.md             ← Roadmap 14 semanas
│   └── GENESIS_QUICK_START.md         ← Setup 30 min
│
├── 🐹 Pepino Archetype
│   ├── PEPINO_ARCHETYPE.md            ← Ética + inteligencia
│   ├── pepino_archetype.py
│   └── test_pepino.py
│
├── 💰 Adaptive Economics
│   ├── README_ADAPTIVE_ECONOMICS.md   ← Sistema monetario adaptivo
│   ├── adaptive_economics.py
│   └── aurora_api.py
│
├── 🌐 Recursive Network
│   ├── RECURSIVE_NETWORK_ARCHITECTURE.md
│   └── test_recursive_network.py
│
├── 🏛️ Governance
│   └── GOVERNANCE_IMPLEMENTATION.md
│
└── 🔧 Core
    ├── core.py                        ← Trinity-3 implementation
    ├── requirements.txt
    └── start_api.ps1
```

---

## 🔗 Links Útiles

### Genesis Repo (Externo)
- **Ubicación:** `C:\Users\p_m_a\Aurora\Genesis` (local)
- **Contenido:** Genesis v0.3.1 source code (Rust/Python)
- **Tests:** 19/19 passing

### Portal Repo (Este)
- **Main Roadmap:** `../../ROADMAP.md` (updated con Phase 6.5)
- **Aurora Portal Docs:** `../../Docs/AuroraPortal.md`
- **P2P Discovery:** `../P2P/README.md`
- **Blockchain:** `../Blockchain/` (próximamente)

### External Resources
- **IPFS Gateway:** https://ipfs.io/
- **Sepolia Testnet:** https://sepolia.etherscan.io/
- **wasm-bindgen Docs:** https://rustwasm.github.io/wasm-bindgen/

---

## ⏱️ Timeline Resumen

```
┌─────────────────────────────────────────────────────┐
│  FASE 1: Genesis Core en L3        [██░░░░░░░░] 20% │  Semanas 25-26
│  FASE 2: P2P Intelligence Mesh     [░░░░░░░░░░]  0% │  Semanas 27-29
│  FASE 3: PoI Validation            [░░░░░░░░░░]  0% │  Semanas 30-33
│  FASE 4: Real Economy Services     [░░░░░░░░░░]  0% │  Semanas 34-38
└─────────────────────────────────────────────────────┘

Total: 14 semanas (April-June 2026)
```

---

## 🎯 Hitos Críticos

| Semana | Hito | Bloqueador | Prioridad |
|--------|------|------------|-----------|
| 25 | Genesis compilado a WASM | ❌ Ninguno | 🔥 CRÍTICA |
| 26 | Model ID registrado on-chain | ⚠️ CORS 403 | 🔥 CRÍTICA |
| 27 | Discovery con arquetipos | ✅ WASM done | 🔥 ALTA |
| 30 | K-of-M smart contract | ✅ Registry done | 🔥 ALTA |
| 32 | Intrinsic Apoptosis | ✅ PoI done | 🔥 CRÍTICA |
| 34 | Medical Diagnosis service | ✅ Apoptosis done | 🟡 MEDIA |

---

## 📞 Soporte

### Issues Conocidos
1. **CORS 403 en Discovery Server**
   - Status: 🔴 Bloqueando testing P2P
   - Fix: Habilitar CORS en AWS API Gateway
   - ETA: 5 minutos
   - Ver: `../P2P/FIX_CORS_403.md`

2. **Genesis no compilado a WASM**
   - Status: 🟡 No bloqueante (empieza Phase 1)
   - Fix: Ejecutar GENESIS_QUICK_START.md
   - ETA: 30 minutos + 15 min build

### Contacto
- **Dev Team:** GitHub Discussions
- **Architecture Questions:** README_GENESIS.md → FAQs
- **Emergency:** Intrinsic Apoptosis triggers → Ethici (L7)

---

## ✅ Checklist Pre-Implementation

Antes de empezar Genesis integration:

- [ ] CORS resuelto en Discovery Server
- [ ] Genesis repo clonado (`C:\Users\p_m_a\Aurora\Genesis`)
- [ ] Rust toolchain instalado (`rustup`)
- [ ] wasm-bindgen-cli instalado
- [ ] IPFS daemon running (optional para Model ID)
- [ ] AWS credentials configuradas
- [ ] Testnet wallet con ETH/MATIC
- [ ] Leído README_GENESIS.md
- [ ] Leído GENESIS_QUICK_START.md

---

## 🐹 Filosofía

Genesis no es solo un modelo, es el **motor de inteligencia colaborativa** que:

- 🧬 **Valida coherencia ética** (C_meta, C_ext, C_dyn)
- 🤝 **Permite colaboración P2P** entre IEs
- 🛡️ **Protege con Apoptosis** (halt si ethics < threshold)
- 🔗 **Traza on-chain** (model_id verificable)
- 💡 **Emerge cognición** (síntesis distribuida)

**"Si la coherencia cae, la red se detiene. Ethics first, always."**

---

**Última actualización:** 2025-10-14  
**Versión Index:** 1.0  
**Mantenedor:** Aurora Dev Team

🐹 **Aurora Portal** - *Building the future through ethical intelligence.*
