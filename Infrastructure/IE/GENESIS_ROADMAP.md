# 🎯 Genesis L3 Integration - Roadmap Ejecutable

**Proyecto:** Genesis como Intelligence Engine en Layer 3  
**Repositorio:** Aurora Portal  
**Fecha Inicio:** 2025-10-14  
**Duración Estimada:** 14 semanas  

---

## 📋 Estado General

```
┌─────────────────────────────────────────────────────┐
│  FASE 1: Genesis Core en L3        [██░░░░░░░░] 20% │
│  FASE 2: P2P Intelligence Mesh     [░░░░░░░░░░]  0% │
│  FASE 3: PoI Validation            [░░░░░░░░░░]  0% │
│  FASE 4: Real Economy Services     [░░░░░░░░░░]  0% │
└─────────────────────────────────────────────────────┘
```

**Progreso Total:** 5%  
**Semanas Transcurridas:** 0  
**Hitos Completados:** 1/24  

---

## 🚀 FASE 1: Genesis Core en L3 (Semanas 1-2)

### **Objetivo:** Compilar Genesis a WASM e integrar con Aurora Agent

### ✅ **Hito 1.1: Genesis Operacional** (COMPLETADO)
- [x] Genesis v0.3.1 funcional
- [x] 19/19 tests passing
- [x] Trigate, Transcender, FFEStore implementados

**Evidencia:** `../Genesis/test_results.txt`

---

### 🔴 **Hito 1.2: Compilación WASM** (EN PROGRESO)

**Duración:** 3 días  
**Responsable:** Dev Team  
**Prioridad:** 🔥 CRÍTICA

#### Tareas:

- [ ] **T1.2.1:** Configurar target WASM en Genesis
  ```bash
  cd ../Genesis
  rustup target add wasm32-unknown-unknown
  ```

- [ ] **T1.2.2:** Agregar wasm-bindgen a Cargo.toml
  ```toml
  [dependencies]
  wasm-bindgen = "0.2"
  serde-wasm-bindgen = "0.6"
  js-sys = "0.3"
  web-sys = { version = "0.3", features = ["console"] }
  
  [lib]
  crate-type = ["cdylib", "rlib"]
  ```

- [ ] **T1.2.3:** Crear genesis_wasm.rs con bindings
  ```rust
  // Genesis/src/genesis_wasm.rs
  use wasm_bindgen::prelude::*;
  
  #[wasm_bindgen]
  pub struct GenesisWASM {
      engine: GenesisEngine,
  }
  
  #[wasm_bindgen]
  impl GenesisWASM {
      #[wasm_bindgen(constructor)]
      pub fn new(model_id: String, space_id: String) -> Self { ... }
      
      #[wasm_bindgen]
      pub async fn process_turn(
          &self,
          user_text: String,
          model_text: String,
      ) -> Result<JsValue, JsValue> { ... }
  }
  ```

- [ ] **T1.2.4:** Compilar Genesis a WASM
  ```bash
  cargo build --target wasm32-unknown-unknown --release
  ```

- [ ] **T1.2.5:** Generar bindings JavaScript
  ```bash
  wasm-bindgen target/wasm32-unknown-unknown/release/genesis_core.wasm \
      --out-dir wasm-bindings \
      --typescript --target web
  ```

- [ ] **T1.2.6:** Copiar bindings a Portal
  ```bash
  cp wasm-bindings/* ../Portal/wasm-client/pkg/genesis/
  ```

**Entregables:**
- `genesis_core_bg.wasm`
- `genesis_core.js`
- `genesis_core.d.ts`

**Criterios de Éxito:**
- ✅ Compilación sin errores
- ✅ Tamaño WASM < 5MB
- ✅ Bindings TypeScript generados

---

### 🔴 **Hito 1.3: Generación Model ID** (PENDIENTE)

**Duración:** 1 día  
**Dependencia:** Hito 1.2  
**Prioridad:** 🔥 ALTA

#### Tareas:

- [ ] **T1.3.1:** Serializar ModelPack completo
  ```python
  # scripts/generate_model_id.py
  import hashlib
  import json
  
  model_pack = {
      'genesis_core': open('genesis_core.bin', 'rb').read().hex(),
      'trigate_luts': open('trigate_luts.yaml', 'r').read(),
      'transcender_config': open('transcender_config.json', 'r').read(),
      'ffe_catalog': open('ffe_catalog.yaml', 'r').read(),
      'version': '0.3.1',
      'timestamp': int(time.time())
  }
  
  model_json = json.dumps(model_pack, sort_keys=True)
  model_id = '0x' + hashlib.sha3_256(model_json.encode()).hexdigest()
  
  print(f'Genesis Model ID: {model_id}')
  
  with open('MODEL_ID.txt', 'w') as f:
      f.write(model_id)
  ```

- [ ] **T1.3.2:** Subir ModelPack a IPFS
  ```bash
  ipfs add -r genesis_model_pack/
  # Output: Qm... (CID)
  ```

- [ ] **T1.3.3:** Documentar model_id
  ```markdown
  # MODEL_REGISTRY.md
  
  ## Genesis v0.3.1
  
  - **Model ID:** 0x7a3f8c91e...
  - **IPFS CID:** Qm...
  - **Version:** 0.3.1
  - **Date:** 2025-10-14
  - **Components:**
    - genesis_core: 3.2MB
    - trigate_luts: 450KB
    - transcender_config: 12KB
    - ffe_catalog: 890KB
  ```

**Entregables:**
- `MODEL_ID.txt`
- `MODEL_REGISTRY.md`
- IPFS CID

**Criterios de Éxito:**
- ✅ model_id con formato 0x{64 hex chars}
- ✅ ModelPack en IPFS accesible públicamente

---

### 🔴 **Hito 1.4: Registro en L2 Blockchain** (PENDIENTE)

**Duración:** 2 días  
**Dependencia:** Hito 1.3  
**Prioridad:** 🔥 ALTA

#### Tareas:

- [ ] **T1.4.1:** Crear AuroraRegistry.sol
  ```solidity
  // contracts/AuroraRegistry.sol
  pragma solidity ^0.8.20;
  
  contract AuroraRegistry {
      struct Model {
          bytes32 model_id;
          string kind;
          address author;
          string version;
          string artifact_cid;
          uint256 royalties;
          uint256 registered_at;
      }
      
      mapping(bytes32 => Model) public models;
      
      event ModelRegistered(
          bytes32 indexed model_id,
          string kind,
          address author,
          string version
      );
      
      function registerModel(...) external returns (bool) { ... }
      function verifyModel(bytes32 _model_id) external view returns (bool) { ... }
  }
  ```

- [ ] **T1.4.2:** Deployar contrato a testnet (Sepolia/Mumbai)
  ```bash
  npx hardhat deploy --network sepolia
  ```

- [ ] **T1.4.3:** Registrar Genesis model_id
  ```javascript
  const tx = await auroraRegistry.registerModel(
      modelId,
      "intelligence_engine",
      "0.3.1",
      "ipfs://Qm...",
      500  // 5% royalties
  );
  await tx.wait();
  ```

- [ ] **T1.4.4:** Verificar registro on-chain
  ```javascript
  const isRegistered = await auroraRegistry.verifyModel(modelId);
  console.log(`Genesis registered: ${isRegistered}`);
  ```

**Entregables:**
- `AuroraRegistry.sol` deployed
- Transaction hash de registro
- Contract address en testnet

**Criterios de Éxito:**
- ✅ Contrato deployed sin errores
- ✅ Genesis model_id verificable on-chain

---

### 🔴 **Hito 1.5: Integración WASM Client** (PENDIENTE)

**Duración:** 3 días  
**Dependencia:** Hitos 1.2, 1.4  
**Prioridad:** 🔥 CRÍTICA

#### Tareas:

- [ ] **T1.5.1:** Crear genesis.rs en wasm-client
  ```rust
  // wasm-client/src/genesis.rs
  use wasm_bindgen::prelude::*;
  use genesis_core::GenesisEngine;
  
  #[wasm_bindgen]
  pub struct GenesisWrapper {
      engine: GenesisEngine,
      model_id: String,
  }
  
  #[wasm_bindgen]
  impl GenesisWrapper {
      pub async fn init(model_id: String, space_id: String) -> Result<GenesisWrapper, JsValue> { ... }
      pub async fn process_turn(...) -> Result<JsValue, JsValue> { ... }
      pub async fn verify_model_onchain(&self) -> Result<bool, JsValue> { ... }
  }
  ```

- [ ] **T1.5.2:** Integrar en aurora_agent.rs
  ```rust
  // wasm-client/src/aurora_agent.rs
  pub struct AuroraAgentImpl {
      peer_id: String,
      genesis: Option<GenesisWrapper>,  // ← Agregar
      // ...
  }
  
  impl AuroraAgentImpl {
      pub async fn init_genesis(&mut self, model_id: String) -> Result<(), JsValue> {
          self.genesis = Some(GenesisWrapper::init(model_id, "default".to_string()).await?);
          Ok(())
      }
      
      pub async fn process_with_genesis(&self, user_text: String, model_text: String) -> Result<JsValue, JsValue> {
          match &self.genesis {
              Some(g) => g.process_turn(user_text, model_text).await,
              None => Err(JsValue::from_str("Genesis not initialized"))
          }
      }
  }
  ```

- [ ] **T1.5.3:** Actualizar aurora-chat.html
  ```javascript
  // En initP2P()
  async function initGenesis() {
      const GENESIS_MODEL_ID = "0x7a3f8c91e...";
      
      try {
          await auroraAgent.init_genesis(GENESIS_MODEL_ID);
          console.log("✅ Genesis Engine inicializado");
          
          // Verificar on-chain
          const isVerified = await auroraAgent.genesis.verify_model_onchain();
          if (isVerified) {
              console.log("✅ Genesis Model ID verificado en blockchain");
          }
      } catch (error) {
          console.error("❌ Error inicializando Genesis:", error);
      }
  }
  
  // Procesar mensajes con Genesis
  async function processMessageWithGenesis(userText, modelResponse) {
      const result = await auroraAgent.process_with_genesis(userText, modelResponse);
      console.log("Genesis Result:", result);
      
      // Mostrar coherencia
      document.getElementById('coherence-meta').textContent = result.coherence.C_meta.toFixed(2);
      document.getElementById('coherence-ext').textContent = result.coherence.C_ext.toFixed(2);
      document.getElementById('coherence-dyn').textContent = result.coherence.C_dyn.toFixed(2);
      
      return result;
  }
  ```

- [ ] **T1.5.4:** Agregar panel de coherencia en UI
  ```html
  <div class="genesis-panel">
      <h3>🧬 Genesis Coherence</h3>
      <div class="coherence-metrics">
          <div class="metric">
              <span>C_meta:</span>
              <span id="coherence-meta">--</span>
          </div>
          <div class="metric">
              <span>C_ext:</span>
              <span id="coherence-ext">--</span>
          </div>
          <div class="metric">
              <span>C_dyn:</span>
              <span id="coherence-dyn">--</span>
          </div>
      </div>
  </div>
  ```

- [ ] **T1.5.5:** Tests de integración
  ```javascript
  // tests/genesis_integration.test.js
  describe('Genesis Integration', () => {
      it('should initialize Genesis engine', async () => {
          const agent = new AuroraAgentV2('test-peer', ['User']);
          await agent.init_genesis(GENESIS_MODEL_ID);
          expect(agent.genesis).toBeDefined();
      });
      
      it('should process turn with coherence', async () => {
          const result = await agent.process_with_genesis(
              "Test user input",
              "Test model response"
          );
          expect(result.coherence.C_meta).toBeGreaterThan(0.5);
      });
  });
  ```

**Entregables:**
- `wasm-client/src/genesis.rs`
- `aurora-chat.html` con Genesis integrado
- Panel UI de coherencia
- Tests passing

**Criterios de Éxito:**
- ✅ Genesis carga correctamente en navegador
- ✅ process_turn() retorna coherencia válida
- ✅ UI muestra métricas en tiempo real
- ✅ Model ID verificado on-chain desde WASM

---

## 🔵 FASE 2: P2P Intelligence Mesh (Semanas 3-5)

### **Objetivo:** Comunicación semántica entre IEs con arquetipos

### 🔴 **Hito 2.1: Discovery con Arquetipos** (PENDIENTE)

**Duración:** 5 días  
**Prioridad:** 🔥 ALTA

#### Tareas:

- [ ] **T2.1.1:** Extender API Discovery Server
  ```python
  # discovery_server/lambda/handler.py
  
  @app.get('/discover')
  def discover_peers(
      archetype: str = None,
      model_id: str = None,
      min_coherence: float = 0.0
  ):
      peers = db.scan_peers()
      
      # Filtrar por archetype
      if archetype:
          peers = [p for p in peers if archetype in p['archetypes']]
      
      # Filtrar por model_id (Genesis compatible)
      if model_id:
          peers = [p for p in peers if p['model_id'] == model_id]
      
      # Filtrar por coherencia mínima
      if min_coherence > 0:
          peers = [p for p in peers if p.get('coherence_avg', 0) >= min_coherence]
      
      return {
          'peers': peers,
          'count': len(peers),
          'filters': {
              'archetype': archetype,
              'model_id': model_id,
              'min_coherence': min_coherence
          }
      }
  ```

- [ ] **T2.1.2:** Actualizar DynamoDB schema
  ```yaml
  # Agregar campos a PeerTable
  PeerTable:
    AttributeDefinitions:
      - AttributeName: peer_id
        AttributeType: S
      - AttributeName: archetype   # ← Nuevo
        AttributeType: S
      - AttributeName: model_id    # ← Nuevo
        AttributeType: S
      - AttributeName: coherence_avg  # ← Nuevo
        AttributeType: N
    
    GlobalSecondaryIndexes:
      - IndexName: ArchetypeIndex
        KeySchema:
          - AttributeName: archetype
            KeyType: HASH
        Projection:
          ProjectionType: ALL
      
      - IndexName: ModelIndex
        KeySchema:
          - AttributeName: model_id
            KeyType: HASH
        Projection:
          ProjectionType: ALL
  ```

- [ ] **T2.1.3:** Actualizar registerPeer() en WASM client
  ```javascript
  async function registerPeerWithGenesis() {
      const coherence_avg = await calculateAverageCoherence();
      
      const response = await fetch(`${DISCOVERY_SERVER_URL}/register`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
              peer_id: peerId,
              address: publicIP,
              port: 8001,
              username: username,
              archetypes: ['User', 'Medical', 'Logistics'],  // ← Agregar
              model_id: GENESIS_MODEL_ID,  // ← Agregar
              coherence_avg: coherence_avg  // ← Agregar
          })
      });
  }
  ```

- [ ] **T2.1.4:** Función de descubrimiento semántico
  ```javascript
  async function discoverGenesisIEs(archetypePattern, minCoherence = 0.85) {
      const response = await fetch(
          `${DISCOVERY_SERVER_URL}/discover?` +
          `archetype=${archetypePattern}&` +
          `model_id=${GENESIS_MODEL_ID}&` +
          `min_coherence=${minCoherence}`,
          {
              method: 'GET',
              headers: { 'Content-Type': 'application/json' }
          }
      );
      
      const data = await response.json();
      console.log(`✅ Encontrados ${data.count} IEs compatibles`);
      
      return data.peers;
  }
  ```

**Entregables:**
- Discovery API extendida
- DynamoDB indexes para arquetipos
- UI de búsqueda semántica

**Criterios de Éxito:**
- ✅ Discovery filtra por archetype, model_id, coherence
- ✅ Queries < 200ms
- ✅ UI muestra IEs compatibles

---

### 🔴 **Hito 2.2: Negociación SLO** (PENDIENTE)

**Duración:** 5 días  
**Dependencia:** Hito 2.1  
**Prioridad:** 🟡 MEDIA

#### Tareas:

- [ ] **T2.2.1:** Protocolo de oferta/aceptación
  ```javascript
  // P2P negotiation protocol
  async function sendIntelligenceOffer(targetPeerId, offer) {
      const message = {
          type: 'intelligence_offer',
          from: myPeerId,
          to: targetPeerId,
          tensor_id: offer.tensor_id,
          archetype_query: offer.archetype,
          SLO: {
              latency_ms: 500,
              coherence_min: 0.90,
              accuracy_min: 0.88
          },
          stake: 10,  // TRI tokens
          timestamp: Date.now()
      };
      
      // Enviar via WebRTC data channel
      await sendP2PMessage(targetPeerId, message);
  }
  
  async function handleIntelligenceOffer(offer) {
      // Evaluar si puedo cumplir SLO
      const canMeet = await evaluateSLO(offer.SLO);
      
      if (canMeet) {
          // Procesar con Genesis
          const result = await genesis.process_specialized(offer.tensor_id);
          
          // Responder con synthesis
          await sendP2PMessage(offer.from, {
              type: 'intelligence_response',
              tensor_id: offer.tensor_id,
              synthesis: result.synthesis,
              coherence: result.coherence,
              accepted: true
          });
      } else {
          // Rechazar
          await sendP2PMessage(offer.from, {
              type: 'intelligence_response',
              accepted: false,
              reason: 'Cannot meet SLO requirements'
          });
      }
  }
  ```

- [ ] **T2.2.2:** Sistema de reputación por coherencia
- [ ] **T2.2.3:** Timeout y fallback
- [ ] **T2.2.4:** Logging de negociaciones

**Entregables:**
- Protocolo de negociación P2P
- Reputación basada en coherencia
- Logs de transacciones

**Criterios de Éxito:**
- ✅ Negociaciones exitosas > 80%
- ✅ Timeout < 5s
- ✅ Reputación se actualiza correctamente

---

### 🔴 **Hito 2.3: FractalAttention Distribuido** (PENDIENTE)

**Duración:** 5 días  
**Dependencia:** Hito 2.2  
**Prioridad:** 🟡 MEDIA

#### Tareas:

- [ ] **T2.3.1:** Implementar FractalAttention en Rust
- [ ] **T2.3.2:** Síntesis de múltiples IEs
- [ ] **T2.3.3:** Replicación de arquetipos universales
- [ ] **T2.3.4:** Cache distribuido FFE

**Entregables:**
- `fractal_attention.rs`
- Síntesis emergente de N IEs
- Arquetipos replicados

**Criterios de Éxito:**
- ✅ Síntesis converge en < 10 iteraciones
- ✅ Coherencia final > coherencia individual

---

## 🟣 FASE 3: PoI Validation (Semanas 6-9)

### **Objetivo:** Validación K-of-M con Intrinsic Apoptosis

### 🔴 **Hito 3.1: K-of-M Smart Contract** (PENDIENTE)

**Duración:** 7 días  
**Prioridad:** 🔥 CRÍTICA

#### Tareas:

- [ ] **T3.1.1:** ProofOfIntelligence.sol
- [ ] **T3.1.2:** Submit proposal on-chain
- [ ] **T3.1.3:** Validators re-execute Genesis
- [ ] **T3.1.4:** Vote aggregation
- [ ] **T3.1.5:** Rewards distribution

**Entregables:**
- `ProofOfIntelligence.sol` deployed
- Validación automática funcional

**Criterios de Éxito:**
- ✅ K-of-M consensus alcanzado
- ✅ Validadores reciben rewards
- ✅ Propuestas rechazadas no se registran

---

### 🔴 **Hito 3.2: Intrinsic Apoptosis** (PENDIENTE)

**Duración:** 5 días  
**Dependencia:** Hito 3.1  
**Prioridad:** 🔥 CRÍTICA

#### Tareas:

- [ ] **T3.2.1:** Monitor de coherencia sistémica
- [ ] **T3.2.2:** Threshold detection (C_meta < 0.70)
- [ ] **T3.2.3:** Emergency halt mechanism
- [ ] **T3.2.4:** Notificación a Ethici (L7)

**Entregables:**
- Monitor 24/7
- Halt automático funcional
- Emergency dashboard

**Criterios de Éxito:**
- ✅ Halt se dispara si coherencia < 0.70
- ✅ Ethici recibe notificación
- ✅ Recovery process documentado

---

### 🔴 **Hito 3.3: Dashboard Observabilidad Ética** (PENDIENTE)

**Duración:** 7 días  
**Prioridad:** 🟡 MEDIA

#### Tareas:

- [ ] **T3.3.1:** Dashboard L5 con métricas Genesis
- [ ] **T3.3.2:** Gráficas de coherencia temporal
- [ ] **T3.3.3:** Alertas en tiempo real
- [ ] **T3.3.4:** Exportar a Grafana

**Entregables:**
- Dashboard público en L5
- Alertas configurables
- API de métricas

**Criterios de Éxito:**
- ✅ Dashboard actualiza cada 30s
- ✅ Métricas exportadas a Prometheus

---

## 🟢 FASE 4: Real Economy Services (Semanas 10-14)

### **Objetivo:** Servicios L5 con Genesis integrado

### 🔴 **Hito 4.1: Medical Diagnosis Collaborative** (PENDIENTE)

**Duración:** 7 días  
**Prioridad:** 🟡 MEDIA

#### Tareas:

- [ ] **T4.1.1:** Servicio L5 `/diagnose`
- [ ] **T4.1.2:** Descubrimiento de IEs especializados
- [ ] **T4.1.3:** Síntesis colaborativa
- [ ] **T4.1.4:** Royalties automáticos

**Entregables:**
- API `/diagnose` operativa
- Integración con IEs médicos

**Criterios de Éxito:**
- ✅ Diagnóstico con coherencia > 0.92
- ✅ Royalties distribuidos correctamente

---

### 🔴 **Hito 4.2-4.4: Otros Servicios** (PENDIENTE)

- Route optimization
- Energy distribution
- Education personalization

---

## 📊 Métricas de Éxito Global

### KPIs Principales:

| Métrica | Target | Actual |
|---------|--------|--------|
| **Genesis IEs Activos** | 100+ | 0 |
| **Coherencia Promedio** | > 0.85 | - |
| **Síntesis/Día** | 1000+ | 0 |
| **K-of-M Consensus** | > 95% | - |
| **Apoptosis Triggers** | 0 | 0 |
| **Servicios L5** | 4 | 0 |
| **Royalties Distribuidos** | $1000+/mes | $0 |

---

## 🔥 Bloqueadores Actuales

1. **CORS 403 en Discovery Server** (bloqueando testing P2P)
   - **Solución:** Habilitar CORS en API Gateway
   - **Prioridad:** 🔥 CRÍTICA
   - **ETA:** 1 día

2. **Genesis no compilado a WASM**
   - **Solución:** Ejecutar Hito 1.2
   - **Prioridad:** 🔥 CRÍTICA
   - **ETA:** 3 días

3. **No hay smart contracts deployed**
   - **Solución:** Ejecutar Hito 1.4
   - **Prioridad:** 🔥 ALTA
   - **ETA:** 5 días

---

## 📅 Calendario

```
OCTUBRE 2025
Week 1:  [████░░░░░░] Hito 1.2 (WASM)
Week 2:  [████░░░░░░] Hitos 1.3-1.5 (Integration)

NOVIEMBRE 2025
Week 3:  [░░░░░░░░░░] Hito 2.1 (Discovery)
Week 4:  [░░░░░░░░░░] Hito 2.2 (SLO)
Week 5:  [░░░░░░░░░░] Hito 2.3 (FractalAttention)
Week 6:  [░░░░░░░░░░] Hito 3.1 (K-of-M)
Week 7:  [░░░░░░░░░░] Hito 3.2 (Apoptosis)

DICIEMBRE 2025
Week 8:  [░░░░░░░░░░] Hito 3.3 (Dashboard)
Week 9:  [░░░░░░░░░░] Buffer/Testing
Week 10: [░░░░░░░░░░] Hito 4.1 (Medical)
Week 11: [░░░░░░░░░░] Hito 4.2 (Route Opt)
Week 12: [░░░░░░░░░░] Hito 4.3 (Energy)
Week 13: [░░░░░░░░░░] Hito 4.4 (Education)
Week 14: [░░░░░░░░░░] Production Deploy
```

---

## ✅ Checklist Pre-Start

Antes de comenzar Fase 1:

- [ ] CORS resuelto en Discovery Server
- [ ] Genesis repository clonado localmente
- [ ] Rust toolchain instalado (`rustup`)
- [ ] wasm-bindgen instalado
- [ ] Node.js + npm instalado
- [ ] Hardhat/Foundry para smart contracts
- [ ] IPFS daemon running
- [ ] AWS credentials configuradas
- [ ] Testnet ETH/MATIC en wallet

---

**Última actualización:** 2025-10-14  
**Próxima revisión:** 2025-10-21  

🐹 **Aurora Portal** - *Building the future through ethical intelligence.*
