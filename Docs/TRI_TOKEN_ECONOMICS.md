# Aurora Tri-Token Economics: Guía Visual

## 🎯 Los Tres Pilares de Aurora

```
        AURORA ECOSYSTEM
              ▲
              │
     ┌────────┴────────┐
     │                 │
     │   EQUILIBRIO    │
     │                 │
     └────────┬────────┘
              │
    ┌─────────┴─────────┐
    │         │         │
    ▼         ▼         ▼
┌───────┐ ┌───────┐ ┌───────┐
│△MERIT │ │○ MIND │ │U TRUST│
│       │ │       │ │       │
│ Infra │ │ Intel │ │ Human │
└───────┘ └───────┘ └───────┘
```

---

## 1. △ MERIT - La Columna Vertebral

### 🏗️ Propósito
**"La infraestructura confiable es la base de todo"**

```
Usuario necesita ejecutar IA
    ↓
Busca en red P2P
    ↓
Encuentra nodos con MERIT alto
    ↓
Conexión confiable garantizada
```

### 📊 Características

| Propiedad | Valor |
|-----------|-------|
| **Max Supply** | 1,000,000,000 (1B) |
| **Genesis Supply** | 500,000,000 (50%) |
| **Emisión** | 10 MERIT/bloque (halving cada 2 años) |
| **Burn Rate** | 20% de fees de red |
| **Tiempo a Max** | ~10 años |

### 💎 Cómo Ganar MERIT

```rust
// Opción 1: Ser validator
fn become_validator() {
    stake(10_000 MERIT);
    maintain_uptime(99%);
    earn(10 MERIT per block);
}

// Opción 2: Proporcionar relay
fn provide_relay() {
    bandwidth(1 Gbps);
    uptime(99.5%);
    earn(5 MERIT per block);
}

// Opción 3: Early adopter
fn genesis_allocation() {
    be_in_first_100_nodes();
    receive(2_000_000 MERIT);
}
```

### 🎮 Ejemplo Real

**María quiere ser validator:**

```
Día 0:
- Compra 10,000 MERIT en DEX
- Stakea todo en validator contract
- Configura su nodo con uptime monitoring

Día 1-365:
- Gana ~10 MERIT/bloque = ~3,650 MERIT/año
- Recibe 20% de fees = ~500 MERIT/año adicional
- Uptime bonus (99.7%) = +10% = ~400 MERIT/año
Total Año 1: ~4,550 MERIT (~45% ROI)

Año 2 (después de halving):
- Gana ~5 MERIT/bloque = ~1,825 MERIT/año
- Fees aumentan por más usuarios = ~1,000 MERIT/año
- Uptime bonus = +200 MERIT/año
Total Año 2: ~3,025 MERIT (~30% ROI)

Después de 5 años:
- MERIT original: 10,000
- MERIT ganado: ~15,000
- Valor aumentado por deflación
- Total: 25,000 MERIT staked
```

---

## 2. ○ MIND - El Combustible Intelectual

### 🧠 Propósito
**"La inteligencia debe fluir libremente y ser recompensada justamente"**

```
Developer publica modelo GPT-style
    ↓
Users pagan en MIND por inferencias
    ↓
Developer gana MIND
    ↓
30% se quema (deflación)
    ↓
Valor de MIND aumenta
```

### 📊 Características

| Propiedad | Valor |
|-----------|-------|
| **Max Supply** | 2,000,000,000 (2B) |
| **Genesis Supply** | 300,000,000 (15%) |
| **Emisión** | Dinámica (basada en demanda) |
| **Burn Rate** | 30% de pagos por inferencia |
| **Tiempo a Max** | ~15-20 años |

### 💎 Cómo Ganar MIND

```javascript
// Opción 1: Ejecutar inferencias
const executeInference = async (model, input) => {
    const cost = calculateCost(model, input); // ej: 10 MIND
    const result = await runModel(model, input);
    const reward = cost * 0.7; // 70% para provider
    
    earn(reward); // 7 MIND
    burn(cost * 0.3); // 3 MIND quemados
};

// Opción 2: Publicar modelo
const publishModel = async (modelFile) => {
    await registry.register(modelFile);
    receive(500_000 MIND); // One-time reward
    
    // Plus: royalties perpetuas
    onEachInference(() => earn(fee * 0.05)); // 5% de cada uso
};

// Opción 3: Contribuir datasets
const contributeData = async (dataset) => {
    const quality = await validate(dataset);
    if (quality > 0.9) {
        receive(10_000 MIND);
        recurringReward(100 MIND per day); // Mientras se use
    }
};
```

### 🎮 Ejemplo Real

**Carlos es desarrollador de IA:**

```
Mes 0:
- Publica modelo de traducción
- Recibe 500,000 MIND de incentivo inicial
- Stakea 100,000 MIND para descuentos

Mes 1:
- Modelo usado 1,000 veces
- Precio promedio: 50 MIND por inferencia
- Total facturado: 50,000 MIND
- Carlos recibe: 35,000 MIND (70%)
- Quemados: 15,000 MIND (30%)
- Royalty (5%): +2,500 MIND

Mes 6:
- Modelo popular: 10,000 usos/mes
- Facturación: 500,000 MIND/mes
- Carlos recibe: 350,000 MIND
- Royalty: +25,000 MIND
- Total: 375,000 MIND/mes

Año 1:
- MIND ganado: ~4M
- Valor aumentado por burn: +20%
- Equivalente real: ~4.8M MIND valor inicial
```

**Ana es usuaria de IA:**

```
Ana necesita procesar 100 documentos:

Opción A (sin MIND):
- Usa ChatGPT/Claude: $20 USD
- Centralizado, sin control

Opción B (con MIND):
- Compra 1,000 MIND en DEX: ~$15 USD
- Usa modelo en Aurora: 800 MIND consumidos
- 200 MIND sobran para siguiente mes
- Descentralizado, privado, más barato
- Plus: puede ganar TRUST ayudando a otros
```

---

## 3. U TRUST - El Alma Social

### 🤝 Propósito
**"La confianza no se compra, se gana a través de relaciones genuinas"**

```
Usuario A ayuda a Usuario B (mentoría)
    ↓
Ambos validan la interacción
    ↓
Smart contract verifica autenticidad
    ↓
Ambos reciben TRUST
    ↓
Reputación on-chain permanente
```

### 📊 Características

| Propiedad | Valor |
|-----------|-------|
| **Max Supply** | 100,000,000 (100M) |
| **Genesis Supply** | 0 (¡CERO!) |
| **Emisión** | Solo por interacciones validadas |
| **Burn Rate** | Opcional (burn para boost) |
| **Transferibilidad** | Limitada (max 10% balance) |

### 💎 Cómo Ganar TRUST

```solidity
// Opción 1: Mentorship
function completeMentorship(
    address mentor,
    address mentee,
    uint256 duration,
    uint8 rating
) external onlyOracle {
    require(rating >= 4, "Rating too low");
    
    uint256 baseReward = 10 * 10**18; // 10 TRUST
    uint256 durationBonus = duration / 30 days; // +1 por mes
    uint256 totalReward = baseReward + durationBonus;
    
    trust.mint(mentor, totalReward);
    trust.mint(mentee, totalReward);
    
    emit TrustEarned(mentor, mentee, totalReward);
}

// Opción 2: Collaboration
function validateCollaboration(
    address[] contributors,
    string projectHash,
    uint8 impact
) external {
    require(impact >= 3, "Impact too low");
    
    uint256 reward = impact * 5 * 10**18;
    
    for (uint i = 0; i < contributors.length; i++) {
        trust.mint(contributors[i], reward);
    }
}

// Opción 3: Dispute Resolution
function resolveDispute(
    bytes32 disputeId,
    address arbiter,
    bool successful
) external {
    if (successful) {
        trust.mint(arbiter, 15 * 10**18); // 15 TRUST (más valioso)
    }
}
```

### 🎮 Ejemplo Real

**Laura quiere ser parte de la comunidad:**

```
Semana 1:
- Se registra en Aurora
- TRUST balance: 0
- Acceso: limitado a features básicas

Mes 1:
- Completa mentorship con desarrollador senior
- Rating: 5/5, duración: 8 semanas
- Gana: 10 + 2 (bonus) = 12 TRUST
- TRUST balance: 12

Mes 3:
- Colabora en 3 proyectos open source
- Gana: 5 TRUST por proyecto = 15 TRUST
- Ayuda a resolver 1 dispute
- Gana: 15 TRUST
- TRUST balance: 42 TRUST

Mes 6:
- TRUST balance: 100+
- Desbloquea: mentorship program (puede ser mentora)
- Nueva mentoría: +10 TRUST/mes
- Code reviews: +3 TRUST cada uno

Año 1:
- TRUST balance: ~500
- Status: "Trusted Contributor"
- Benefits:
  * Puede arbitrar disputes (earn 15 TRUST cada uno)
  * Priority en collaborations
  * Access a premium features
  * Network effect: más gente quiere trabajar con ella
```

**¿Por qué TRUST es diferente?**

```javascript
// TRUST NO se puede comprar en exchange
const buyTrust = () => {
    throw new Error("TRUST cannot be purchased!");
};

// Solo se puede transferir limitadamente
const transferTrust = (amount) => {
    if (amount > balance * 0.1) {
        throw new Error("Max 10% of balance per transfer");
    }
    // Requiere validación de receptor
    if (!isWhitelisted(recipient)) {
        throw new Error("Recipient not validated");
    }
};

// Esto hace que TRUST sea:
// 1. Soulbound (ligado a la persona)
// 2. No especulativo (no hay pump & dump)
// 3. Verdadero indicador de reputación
// 4. El más valioso a largo plazo
```

---

## 4. Casos de Uso Combinados

### 🎯 Caso 1: Provider Completo

**Pedro quiere ser provider de élite:**

```
Setup:
├── Stakea 50,000 MERIT → Validator status
├── Publica 3 modelos → 1.5M MIND reward
└── Completa 5 mentorships → 60 TRUST

Mes 1 earnings:
├── MERIT: 3,650 (validating) + 500 (fees) = 4,150 MERIT
├── MIND: 200,000 (inferencias) + 10,000 (royalties) = 210,000 MIND
└── TRUST: +20 (nuevas colaboraciones)

Beneficios combinados:
├── Alto MERIT → Prioridad en discovery
├── Alto MIND → Más users eligen sus modelos
└── Alto TRUST → +15% premium pricing

Resultado:
- Earnings normales: 214,150 tokens/mes
- Con bonuses: 246,272 tokens/mes (+15%)
- ROI: Recupera inversión inicial en 3-4 meses
```

### 🎯 Caso 2: Usuario Power

**Sofía usa Aurora intensivamente:**

```
Profile:
├── 1,000 MERIT staked (descuentos en fees)
├── 50,000 MIND (para inferencias)
└── 200 TRUST (comunidad activa)

Uso mensual:
├── 100 inferencias complejas → Gasta 40,000 MIND
│   └── Descuento por MERIT stake: -10% → 36,000 MIND
├── Colabora en 2 proyectos → Gana 10 TRUST
└── Da feedback a providers → Gana 100 MIND en rewards

Balance después de 1 mes:
├── MERIT: 1,000 + 50 (staking rewards) = 1,050
├── MIND: 50,000 - 36,000 + 100 = 14,100
└── TRUST: 200 + 10 = 210

Sofía es "power user": usa mucho pero también contribuye.
```

### 🎯 Caso 3: Cooperativa

**Un equipo de 10 personas crea cooperativa:**

```
Cooperativa "AuroraAI-COOP":

Estructura:
├── 3 validators (30,000 MERIT cada uno)
├── 5 developers (200,000 MIND cada uno)
└── 2 community managers (500 TRUST cada uno)

Funcionamiento:
1. Validators mantienen infraestructura
2. Developers publican modelos bajo marca cooperativa
3. Community managers atraen usuarios

Revenue sharing:
├── MERIT rewards → Reinvertir en infraestructura
├── MIND earnings → Distribuir 70% a miembros, 30% fondo común
└── TRUST → Crecer reputación colectiva

Después de 6 meses:
├── Pool MERIT: 90,000 → 120,000 (+33%)
├── Pool MIND: 1,000,000 → 2,500,000 (+150% por uso)
├── Pool TRUST: 1,000 → 3,000 (+200% por colaboraciones)

Nuevos miembros:
- Pueden entrar comprando share de pool
- O contribuyendo trabajo (ganan tokens gradualmente)
- Votación proporcional a holdings
```

---

## 5. Economía Deflacionaria

### 📉 Mecanismos de Burn

```
△ MERIT Burn:
├── 20% de network fees → quemados
├── Slashing penalties → quemados
└── Voluntary burn para voting boost

○ MIND Burn:
├── 30% de payments por inferencias → quemados
├── Failed transactions → quemados
└── Optional burn para priority access

U TRUST Burn:
├── Burn para 2x MERIT/MIND rewards (30 días)
├── Burn para dispute insurance
└── NO hay otros burns (mantener escasez)
```

### 📊 Proyección de Supply

```python
# Simulación 10 años

Year 0:
MERIT: 500M  | MIND: 300M   | TRUST: 0
Total Value: $10M

Year 1:
MERIT: 530M  | MIND: 350M   | TRUST: 5M
Burned: 20M MERIT, 150M MIND
Net Supply: ↑6% MERIT, ↑17% MIND, NEW TRUST

Year 5:
MERIT: 650M  | MIND: 600M   | TRUST: 40M
Burned: 150M MERIT, 800M MIND
Net Supply: ↑30% MERIT, ↑100% MIND, NEW TRUST
Emission slowing down...

Year 10:
MERIT: 800M  | MIND: 900M   | TRUST: 80M
Burned: 400M MERIT, 2B MIND
Net Supply: ↑60% MERIT, ↑200% MIND, ↑80% TRUST
Near equilibrium (burn ≈ emission)

Year 20:
MERIT: ~1B (MAX) | MIND: ~1.2B | TRUST: ~100M (MAX)
Fully deflationary (burn > emission)
```

### 💰 Proyección de Valor

```
Assumptions:
- 10,000 active users by Year 1
- 100,000 active users by Year 5
- $100M total value locked by Year 5

Price per token (estimated):

Year 1:
MERIT: $0.015 (530M supply, $8M TVL)
MIND:  $0.020 (350M supply, $7M TVL)
TRUST: $100   (5M supply, escaso, $500M potential)

Year 5:
MERIT: $0.10  (650M supply, $65M TVL)
MIND:  $0.08  (600M supply, $48M TVL)
TRUST: $1,000 (40M supply, muy escaso, $40B potential)

Year 10:
MERIT: $0.50  (deflation + adoption)
MIND:  $0.30  (más uso = más burn = más escasez)
TRUST: $5,000 (extremadamente valioso, reputación = oro)

Note: TRUST puede ser el más valioso a largo plazo
porque no se puede comprar, solo ganar.
```

---

## 6. Comparación con Otros Proyectos

### 🔍 Aurora vs Traditional Crypto

| Feature | Bitcoin | Ethereum | Filecoin | **Aurora** |
|---------|---------|----------|----------|-----------|
| **Tokens** | 1 (BTC) | 1 (ETH) | 1 (FIL) | **3 (MERIT, MIND, TRUST)** |
| **Purpose** | Store of value | Smart contracts | Storage | **AI + P2P + Social** |
| **Supply** | Fixed (21M) | Unlimited | Variable | **3 políticas diferentes** |
| **Burn** | No | Yes (EIP-1559) | Yes | **Yes (todos)** |
| **Soulbound** | No | No | No | **Yes (TRUST)** |
| **Governance** | None | Token weighted | Token weighted | **Multi-token weighted** |
| **Social Layer** | No | No | No | **Yes (TRUST)** |

### 💡 Innovaciones de Aurora

1. **Tri-Token System** (único en la industria)
   - Cada token tiene función específica
   - No compiten entre sí
   - Se complementan para valor holístico

2. **TRUST Soulbound** (pionero)
   - No se puede comprar
   - No especulativo
   - Verdadera reputación on-chain

3. **Burn Multi-Fuente**
   - MERIT: fees + slashing
   - MIND: payments + failures
   - TRUST: voluntary (boost)

4. **Governance Ponderada**
   - Propuestas técnicas → MERIT vota más
   - Propuestas económicas → MIND vota más
   - Propuestas sociales → TRUST vota más
   - Evita plutocracy (rule by wealthy)

---

## 7. Roadmap de Implementación

### 📅 Fase 1: Genesis (Mes 1-2)

```solidity
// Deploy orden:
1. Deploy MeritToken
   - Genesis mint: 500M
   - Distribute to founders
   
2. Deploy MindToken
   - Genesis mint: 300M
   - Distribute to developers
   
3. Deploy TrustToken
   - Genesis mint: 0
   - Setup oracle

4. Deploy AuroraEcosystem (master contract)
   - Connect three tokens
   - Setup governance
```

### 📅 Fase 2: Liquidity (Mes 2-3)

```typescript
// Setup DEX pools:
await uniswap.createPool(MERIT, USDC, {
  initialLiquidity: {
    MERIT: 150_000_000,
    USDC: 2_000_000
  }
});

await uniswap.createPool(MIND, USDC, {
  initialLiquidity: {
    MIND: 90_000_000,
    USDC: 1_500_000
  }
});

// Note: TRUST no tiene pool (no vendible)
```

### 📅 Fase 3: Incentivos (Mes 3-6)

```javascript
// Lanzar programas de incentivos:
const incentivePrograms = [
  {
    name: "Early Validator Program",
    token: MERIT,
    duration: "6 months",
    multiplier: 3,
    slots: 100
  },
  {
    name: "Model Developer Grants",
    token: MIND,
    duration: "12 months",
    reward: 500_000,
    slots: 50
  },
  {
    name: "Community Builder Airdrops",
    token: TRUST,
    duration: "ongoing",
    reward: 50,
    slots: 1000
  }
];
```

### 📅 Fase 4: Madurez (Mes 6+)

```
- Supply alcanzando equilibrio
- Burn mechanisms activos
- Governance operativa
- Ecosystem auto-sostenible
```

---

## 🎓 Conclusión

### ¿Por qué este diseño es superior?

1. **Separación de Preocupaciones**
   - MERIT = infraestructura
   - MIND = economía
   - TRUST = social
   - Cada uno optimizado para su propósito

2. **Anti-Especulación**
   - TRUST no vendible
   - Burn mechanisms
   - Value ligado a uso real

3. **Incentivos Alineados**
   - Providers ganan con calidad
   - Users ganan con participación
   - Community gana con colaboración

4. **Sostenibilidad Long-Term**
   - No depende de hype
   - Value intrínseco (AI compute)
   - Deflación natural

5. **Innovación Social**
   - Primera plataforma con "reputation token"
   - Cooperativas nativas
   - Economia del bien común

---

## 📚 Recursos Adicionales

- **Whitepaper completo**: [próximamente]
- **Smart contract audits**: [CertiK, OpenZeppelin]
- **Tokenomics simulator**: https://aurora-sim.app
- **Community Discord**: https://discord.gg/aurora
- **DAO Forum**: https://forum.aurora.program

---

**Aurora: Donde la Infraestructura, la Inteligencia y la Confianza convergen.** 🌅
