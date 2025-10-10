# Comparación de Políticas Monetarias: MERIT vs MIND vs TRUST

## 🎯 Overview Conceptual

```
MERIT (△)     MIND (○)      TRUST (U)
──────────    ──────────    ──────────
Escasez       Abundancia    Extrema
MODERADA      RELATIVA      ESCASEZ
    ↓             ↓            ↓
Bitcoin-      Ethereum-    Soulbound
 like          like          único
    ↓             ↓            ↓
Store of      Medium of    Proof of
  Value       Exchange      Reputation
```

---

## 1. △ MERIT - Modelo Bitcoin Híbrido

### 📊 Características Fundamentales

```solidity
contract MeritToken {
    // Supply Policy
    uint256 constant GENESIS_SUPPLY = 500_000_000 * 10**18;
    uint256 constant MAX_SUPPLY = 1_000_000_000 * 10**18;
    uint256 constant INITIAL_REWARD = 10 * 10**18;
    uint256 constant HALVING_INTERVAL = 5_256_000; // ~2 años
    
    // Similar a Bitcoin pero:
    // 1. Genesis supply (50% vs 0% de Bitcoin)
    // 2. Más rápido (2 años vs 4 años halving)
    // 3. Burn mechanism (no existe en Bitcoin)
}
```

### 🔄 Curva de Emisión

```python
# Proyección de supply MERIT

Year 0:  500,000,000 (genesis)
Year 1:  500M + (10 * 5.256M blocks) = 552,560,000
Year 2:  552.56M + (10 * 5.256M) = 605,120,000

# Primera halving (año 2)
Year 3:  605.12M + (5 * 5.256M) = 631,400,000
Year 4:  631.4M + (5 * 5.256M) = 657,680,000

# Segunda halving (año 4)
Year 5:  657.68M + (2.5 * 5.256M) = 670,820,000
Year 6:  670.82M + (2.5 * 5.256M) = 683,960,000

# Tercera halving (año 6)
Year 7:  683.96M + (1.25 * 5.256M) = 690,530,000
Year 8:  690.53M + (1.25 * 5.256M) = 697,100,000

# Asintóticamente hacia 1B
Year 10: ~703M
Year 15: ~725M
Year 20: ~750M
Year 50: ~900M
Year 100: ~990M
```

### 📉 Burn Mechanism

```solidity
function processFee(uint256 feeAmount) internal {
    uint256 burnAmount = feeAmount * 20 / 100; // 20%
    uint256 validatorReward = feeAmount * 60 / 100; // 60%
    uint256 treasuryAmount = feeAmount * 20 / 100; // 20%
    
    _burn(address(this), burnAmount);
    _transfer(address(this), validator, validatorReward);
    _transfer(address(this), treasury, treasuryAmount);
}

// Ejemplo real:
// Fee de 100 MERIT:
// - 20 MERIT quemados (deflación)
// - 60 MERIT a validator
// - 20 MERIT a treasury
```

### 📈 Punto de Equilibrio

```python
# ¿Cuándo burn = emission?

Assumptions:
- 10,000 active users
- 100 transactions/day per user
- Fee promedio: 0.1 MERIT/tx
- 20% burn rate

Daily burn = 10,000 users * 100 tx * 0.1 MERIT * 0.2
          = 20,000 MERIT/day

Daily emission (Year 1) = 10 MERIT/block * ~14,400 blocks/day
                        = 144,000 MERIT/day

Equilibrio cuando:
emission = burn
144,000 = daily_burn
daily_burn = users * 100 * 0.1 * 0.2
users = 144,000 / 2 = 72,000 users

Conclusion: Con 72k+ users, MERIT se vuelve deflacionario
```

### 🎯 Decisión de Diseño: ¿Por qué híbrido?

**Bitcoin puro (no genesis):**
```
Pros:
✅ Máxima descentralización inicial
✅ Narrativa de "fair launch"

Cons:
❌ Difícil bootstrap network
❌ No hay fondos para desarrollo
❌ Slow adoption inicial
```

**Genesis + Halving (Aurora MERIT):**
```
Pros:
✅ Bootstrap rápido (500M disponibles)
✅ Fondos para desarrollo (100M team allocation)
✅ Liquidez inicial (150M para pools)
✅ Still has scarcity narrative (50% emitido, 50% por ganar)

Cons:
❌ Menos "pure" que Bitcoin
❌ Risk de dump inicial (mitigado por vesting)
```

---

## 2. ○ MIND - Modelo Ethereum Dinámico

### 📊 Características Fundamentales

```solidity
contract MindToken {
    // Supply Policy
    uint256 constant GENESIS_SUPPLY = 300_000_000 * 10**18;
    uint256 constant MAX_SUPPLY = 2_000_000_000 * 10**18;
    // NO HAY HALVING - emisión dinámica
    
    // Similar a Ethereum post-Merge:
    // 1. Emisión basada en actividad
    // 2. Burn based on usage
    // 3. Puede ser inflacionario o deflacionario según demanda
}
```

### 🔄 Emisión Dinámica

```javascript
// MIND se emite por actividad real

function rewardInference(
    address provider,
    uint256 computeCost,
    uint8 qualityRating
) external {
    // Base reward proporcional al trabajo
    uint256 baseReward = computeCost * 10;
    
    // Quality multiplier (1x - 1.5x)
    uint256 qualityMultiplier = 100 + (qualityRating - 3) * 25;
    
    // Total reward
    uint256 reward = baseReward * qualityMultiplier / 100;
    
    _mint(provider, reward);
}

// Ejemplo:
// Inference que cuesta 10 MIND de compute
// Quality rating: 5/5
// Reward: 10 * 10 * (100 + 50) / 100 = 150 MIND
//
// Esto significa que provider GANA más de lo que user pagó
// ¿Inflacionario? Sí, pero...
```

### 📉 Burn Agresivo

```solidity
function payForInference(
    address provider,
    uint256 amount
) external {
    // User paga 100 MIND
    uint256 providerAmount = amount * 70 / 100; // 70 MIND
    uint256 burnAmount = amount * 30 / 100;     // 30 MIND
    
    _transfer(msg.sender, provider, providerAmount);
    _burn(msg.sender, burnAmount);
    
    // Luego provider recibe reward adicional (emisión)
    // Net effect depende de ratio burn/emission
}
```

### 📊 Ecuación de Equilibrio

```python
# Supply de MIND es dinámico

Variables:
- daily_inferences: número de inferencias/día
- avg_cost: costo promedio por inferencia
- burn_rate: 30%
- emission_multiplier: 10x (provider gana 10 MIND por 1 MIND de compute)

Daily burn = daily_inferences * avg_cost * 0.3
Daily emission = daily_inferences * avg_cost * emission_multiplier

Net supply change = emission - burn

Example (low usage):
- 1,000 inferences/day
- avg_cost: 10 MIND
- burn: 1,000 * 10 * 0.3 = 3,000 MIND
- emission: 1,000 * 10 * 10 = 100,000 MIND
- net: +97,000 MIND/day (inflacionario)

Example (high usage):
- 100,000 inferences/day
- avg_cost: 10 MIND
- burn: 100,000 * 10 * 0.3 = 300,000 MIND
- emission: 100,000 * 10 * 10 = 10,000,000 MIND (wait...)
- net: +9,700,000 MIND/day (MUY inflacionario)

Problem: Emission too high!

Solution: Emission multiplier debe DISMINUIR con adoption
```

### 🔧 Ajuste Dinámico

```solidity
function calculateEmissionMultiplier() internal view returns (uint256) {
    uint256 supplyPercentage = totalSupply() * 100 / MAX_SUPPLY;
    
    if (supplyPercentage < 20) return 1000; // 10x early stage
    if (supplyPercentage < 40) return 700;  // 7x
    if (supplyPercentage < 60) return 500;  // 5x
    if (supplyPercentage < 80) return 300;  // 3x
    return 200; // 2x late stage
    
    // Esto asegura que emission se reduce conforme crece supply
}

function rewardInference(...) external {
    uint256 multiplier = calculateEmissionMultiplier();
    uint256 reward = computeCost * multiplier / 100;
    _mint(provider, reward);
}
```

### 📈 Proyección de Supply

```python
# Con emission dinámica

Year 0: 300M (genesis)

Year 1 (early, 10x multiplier):
- 10k inferences/day * 365 days = 3.65M inferences
- avg_cost: 10 MIND
- emission: 3.65M * 10 * 10 = 365M
- burn: 3.65M * 10 * 0.3 = 10.95M
- net: +354M
- total: 654M

Year 2 (growing, 7x multiplier):
- 50k inferences/day
- emission: 18.25M * 10 * 7 = 1,277M
- burn: 18.25M * 10 * 0.3 = 54.75M
- net: +1,222M
- total: 1,876M (near max!)

Year 3 (mature, 3x multiplier):
- 100k inferences/day
- emission: 36.5M * 10 * 3 = 1,095M
- burn: 36.5M * 10 * 0.3 = 109.5M
- net: +985M
- total: 2,000M (MAX reached!)

From Year 3+: Only burn, no more emission
- Supply starts decreasing
- Deflationary phase begins
```

### 🎯 Decisión de Diseño: ¿Por qué dinámico?

**Fixed emission (Bitcoin-style):**
```
Pros:
✅ Predecible
✅ Simple de entender

Cons:
❌ No refleja demanda real
❌ Puede sobre/sub-incentivar
```

**Dynamic emission (Aurora MIND):**
```
Pros:
✅ Rewards proporcionales al trabajo
✅ Self-adjusting supply
✅ Incentiva early adoption (10x) pero se modera

Cons:
❌ Más complejo
❌ Requiere governance para ajustar parámetros
```

---

## 3. U TRUST - Modelo Soulbound Único

### 📊 Características Fundamentales

```solidity
contract TrustToken {
    // Supply Policy
    uint256 constant GENESIS_SUPPLY = 0; // ¡CERO!
    uint256 constant MAX_SUPPLY = 100_000_000 * 10**18;
    
    // NO emission automática
    // Solo creación por interacciones humanas verificadas
    
    // Similar a:
    // - Proof of Humanity (PoH)
    // - Soulbound Tokens (SBT)
    // - Reputation systems (Gitcoin Passport)
    
    // Pero único en que:
    // 1. Es transferible (limitadamente)
    // 2. Se puede quemar voluntariamente
    // 3. Tiene valor económico (indirecto)
}
```

### 🔄 Creación de TRUST

```solidity
function mintFromInteraction(
    bytes32 interactionId,
    InteractionType iType,
    address[] participants,
    uint8[] ratings
) external onlyOracle {
    require(ratings.length == participants.length);
    
    uint256 baseReward = getBaseReward(iType);
    
    for (uint i = 0; i < participants.length; i++) {
        require(ratings[i] >= 4, "Rating too low");
        
        // Duration bonus
        uint256 durationBonus = getDuration(interactionId) / 30 days;
        
        // Rating bonus
        uint256 ratingBonus = (ratings[i] - 3) * baseReward / 10;
        
        uint256 totalReward = baseReward + durationBonus + ratingBonus;
        
        _mint(participants[i], totalReward);
    }
}

// Ejemplo:
// Mentorship de 3 meses, rating 5/5
// baseReward: 10 TRUST
// durationBonus: 3 TRUST
// ratingBonus: 2 TRUST
// total: 15 TRUST (para ambos mentor y mentee)
```

### 🚫 Transferibilidad Limitada

```solidity
function transfer(address to, uint256 amount) public override returns (bool) {
    // Rule 1: Max 10% del balance
    uint256 maxTransfer = balanceOf(msg.sender) / 10;
    require(amount <= maxTransfer, "Exceeds 10% limit");
    
    // Rule 2: Recipient debe estar whitelisted
    require(isValidRecipient(to), "Recipient not validated");
    
    // Rule 3: Cooldown de 30 días entre transfers
    require(block.timestamp > lastTransfer[msg.sender] + 30 days, "Cooldown");
    
    // Rule 4: No se puede transferir a exchanges
    require(!isExchange(to), "Cannot sell TRUST");
    
    lastTransfer[msg.sender] = block.timestamp;
    return super.transfer(to, amount);
}

// Esto hace que TRUST sea:
// - Mayormente soulbound (tied to identity)
// - Pero con escape valve (10% para colaboraciones)
```

### 📈 Proyección de Supply

```python
# TRUST supply crece ORGÁNICAMENTE

Year 0: 0 (no genesis!)

Year 1 (early community):
- 1,000 early adopters
- Promedio: 50 TRUST cada uno (airdrops + earning)
- Total: 50,000 TRUST (0.05% of max supply)

Year 2 (growing):
- 10,000 active community members
- New members: ~20 TRUST average
- Old members: +30 TRUST
- Total: 10k * 20 + 1k * 30 = 230,000 TRUST

Year 5 (established):
- 100,000 community members
- Distribution:
  * 1,000 power users: 1,000 TRUST each = 1M
  * 9,000 active: 200 TRUST each = 1.8M
  * 90,000 casual: 20 TRUST each = 1.8M
- Total: ~4.6M TRUST (4.6% of max)

Year 10 (mature):
- 1M community members
- Distribution follows power law:
  * Top 0.1% (1,000): avg 10,000 TRUST = 10M
  * Top 1% (10,000): avg 2,000 TRUST = 20M
  * Top 10% (100,000): avg 500 TRUST = 50M
  * Rest (890,000): avg 20 TRUST = 17.8M
- Total: ~97.8M TRUST (97.8% of max)

Year 20+: Asymptotic to 100M max supply
```

### 💎 Curva de Valor (Price Discovery)

```python
# ¿Cuánto vale TRUST?

Método 1: Comparison con MERIT/MIND
- MERIT: 1B supply, $10M TVL → $0.01/token
- MIND: 2B supply, $15M TVL → $0.0075/token
- TRUST: 5M supply (year 1), ???

Si TRUST captura 10% del valor total:
- Total value: $25M
- TRUST value: $2.5M
- Price: $2.5M / 50k = $50 per TRUST

Year 5: $100M TVL, 4.6M TRUST
- TRUST value (20%): $20M
- Price: $20M / 4.6M = $4.35 per TRUST

Year 10: $500M TVL, 97M TRUST
- TRUST value (30%): $150M
- Price: $150M / 97M = $1.55 per TRUST

Paradox: TRUST price CAE conforme supply aumenta
Pero: Holders tempranos tienen MÁS TRUST
```

### 🔥 Burn for Boost

```solidity
function burnForBoost(uint256 amount) external {
    require(amount >= 10 * 10**18, "Min 10 TRUST");
    require(amount <= balanceOf(msg.sender), "Insufficient balance");
    
    _burn(msg.sender, amount);
    
    // Otorgar boost en MERIT/MIND rewards
    uint256 boostDuration = (amount / 10**18) * 7 days; // 7 días por TRUST
    uint256 boostMultiplier = 200; // 2x
    
    boosts[msg.sender] = Boost({
        multiplier: boostMultiplier,
        expiresAt: block.timestamp + boostDuration
    });
    
    emit BoostActivated(msg.sender, amount, boostDuration);
}

// Ejemplo:
// Alice tiene 100 TRUST
// Quema 50 TRUST
// Recibe: 2x rewards en MERIT/MIND por 350 días
//
// ¿Vale la pena?
// Si Alice gana 1000 MIND/mes normalmente
// Con boost: 2000 MIND/mes
// Extra: 1000 MIND/mes * 11.5 meses = 11,500 MIND
// 
// Si 1 TRUST = 10 MIND (ratio de mercado)
// Alice "invirtió" 50 TRUST = 500 MIND
// Alice "ganó" 11,500 MIND
// ROI: 2200%!
//
// Esto incentiva burn → deflation → más escasez → más valor
```

### 🎯 Decisión de Diseño: ¿Por qué Soulbound?

**Fully tradeable (ERC-20 normal):**
```
Pros:
✅ Liquidez
✅ Price discovery fácil

Cons:
❌ Especulación
❌ Pump & dump
❌ No refleja reputación real (se puede comprar)
❌ Rich pueden manipular
```

**Fully soulbound (no transferible):**
```
Pros:
✅ Verdadera reputación (no se puede comprar)
✅ Anti-especulación

Cons:
❌ Sin valor económico
❌ No se puede compensar contributors
❌ Difícil bootstrap (no airdrops posibles)
```

**Partially soulbound (Aurora TRUST):**
```
Pros:
✅ Mayormente tied to identity (90% non-transferible)
✅ Escape valve (10% para colaboraciones legítimas)
✅ Burn mechanism (value sink)
✅ Económicamente valioso pero no especulativo

Cons:
❌ Más complejo que los otros dos
❌ Requiere whitelisting infrastructure
```

---

## 4. Comparative Analysis

### 📊 Tabla Comparativa Completa

| Propiedad | △ MERIT | ○ MIND | U TRUST |
|-----------|---------|--------|---------|
| **Max Supply** | 1B | 2B | 100M |
| **Genesis %** | 50% | 15% | 0% |
| **Scarcity** | Media | Baja | Extrema |
| **Emission** | Fixed + Halving | Dynamic | Interaction-based |
| **Burn Rate** | 20% fees | 30% payments | Voluntary |
| **Velocity** | Baja (staking) | Alta (payments) | Muy baja (soulbound) |
| **Transferable** | 100% | 100% | 10% |
| **Price Discovery** | Fácil (DEX) | Fácil (DEX) | Difícil (no liquid) |
| **Speculation** | Media | Alta | Muy baja |
| **Utility** | Staking, governance | Payments | Reputation |
| **Store of Value** | Alta | Media | N/A |
| **Medium of Exchange** | Baja | Alta | N/A |
| **Unit of Account** | Posible | Principal | No |
| **Inflation (Y1)** | +6% | +100% | N/A |
| **Long-term** | Deflacionario | Deflacionario | Asintótico |

### 💡 Synergies Between Tokens

```javascript
// Los tres tokens se complementan

Scenario 1: Nuevo provider
- Compra 10k MERIT → Stakea → Validator
- Gana MIND por inferencias
- Gana TRUST por mentoring otros
- TRUST boost aumenta MERIT/MIND rewards
- Ciclo virtuoso!

Scenario 2: Usuario de comunidad
- No tiene capital inicial
- Gana TRUST por colaboraciones
- Usa TRUST para acceder a features premium
- Gana un poco de MIND/MERIT
- Eventualmente puede comprar más tokens
- Bootstrapping sin capital!

Scenario 3: Especulador
- Compra MERIT/MIND en DEX
- No puede comprar TRUST (no vendible)
- Para maximizar gains necesita:
  * Participar en red (ganar TRUST)
  * Esto lo convierte en usuario real
- Especulación → Participation → Value creation
```

### 📈 Value Capture por Token

```python
# ¿Dónde está el valor?

MERIT captures:
- Infrastructure value
- Network security
- Governance rights
- Predictable scarcity (Bitcoin narrative)
- Target: Conservative investors, validators

MIND captures:
- Transaction volume
- AI compute market
- Developer ecosystem
- High velocity (money-like)
- Target: Active users, traders

TRUST captures:
- Social capital
- Reputation premium
- Community value
- Ultra-scarce (only earneable)
- Target: Long-term contributors, arbiters

Total value = MERIT + MIND + TRUST + synergies
```

---

## 5. Riesgos y Mitigaciones

### ⚠️ MERIT Risks

**Risk 1: Over-emission en early stage**
```
Si muy pocos users pero mucha emission:
→ Inflación alta
→ Price dump

Mitigation:
- Genesis supply grande (500M) diluye impact
- Halving agresivo (2 años vs 4 de Bitcoin)
- Burn mechanism activo desde día 1
```

**Risk 2: Validator centralization**
```
Si solo pocos validators con mucho stake:
→ Centralización
→ No es P2P real

Mitigation:
- Staking requirement moderado (10k MERIT, ~$100)
- Slashing penalty para mal comportamiento
- Reputation (TRUST) también cuenta
```

### ⚠️ MIND Risks

**Risk 1: Hyper-inflation en growth phase**
```
Si adoption explota:
→ Millones de inferences/día
→ Trillones de MIND emitidos
→ Value destruction

Mitigation:
- Dynamic emission multiplier (10x → 2x)
- Max supply hard cap (2B)
- Aggressive burn (30%)
- Puede pausar emission si es necesario (governance)
```

**Risk 2: Death spiral**
```
Si nadie usa platform:
→ No hay burn
→ Pero sigue emission
→ Inflación sin control

Mitigation:
- Genesis supply bajo (15%) vs MERIT (50%)
- Emission solo cuando hay actividad real
- Treasury puede buy-and-burn si es necesario
```

### ⚠️ TRUST Risks

**Risk 1: Sybil attacks**
```
Crear múltiples identities falsas:
→ Self-mentorships
→ Fake collaborations
→ Farm TRUST

Mitigation:
- Oracle valida interacciones (no automático)
- Requiere ratings mutuales
- Long duration requirements
- Web of trust (new users need referral)
```

**Risk 2: No price discovery**
```
Si no es tradeable:
→ No hay mercado
→ Difícil valuación
→ No clear incentive económico

Mitigation:
- 10% transferibility permite cierto trading
- Burn-for-boost da value sink
- Indirect value (access, priority, governance)
- OTC markets pueden emerger
```

**Risk 3: Too slow growth**
```
Si muy difícil ganar TRUST:
→ Solo elites lo tienen
→ No democratizado
→ Va contra valores Aurora

Mitigation:
- Multiple ways to earn (mentorship, collaboration, code review)
- Airdrops para early adopters (bootstrap)
- Pequeñas cantidades son suficientes para benefits
- Programas de onboarding con TRUST rewards
```

---

## 6. Conclusión: ¿Por qué tres políticas?

### 🎯 Filosofía de Diseño

```
Sistema Tradicional (1 token):
└── Un token debe ser:
    ├── Store of value
    ├── Medium of exchange
    ├── Unit of account
    └── Governance
    
Problema: No optimization possible
- Si escaso → mal para payments
- Si abundante → mal para store of value
- Compromises everywhere

Sistema Aurora (3 tokens):
├── MERIT → Optimizado para store of value + governance
├── MIND → Optimizado para medium of exchange
└── TRUST → Optimizado para reputation
    
Resultado: Best of all worlds
- No compromises
- Cada token hace su trabajo
- Synergies entre ellos
```

### 💎 Resultado Final

```
Year 10 projection:

△ MERIT (Infrastructure):
- Supply: 703M / 1B (70%)
- Tendencia: Deflacionaria (burn > emission)
- Rol: "Bitcoin de Aurora"

○ MIND (Economy):
- Supply: 1.8B / 2B (90%)
- Tendencia: Near-equilibrium
- Rol: "Ether de Aurora"

U TRUST (Social):
- Supply: 97M / 100M (97%)
- Tendencia: Asintótica
- Rol: "Único en la industria"

Together:
- Ecosystem maduro
- Auto-regulado
- Sostenible indefinidamente
- Valores alineados con Aurora philosophy
```

---

**Los tres tokens no compiten, colaboran.** 🌅
