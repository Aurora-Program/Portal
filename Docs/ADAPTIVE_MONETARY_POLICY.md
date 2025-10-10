# Sistema de Política Monetaria Adaptativa con IA

## 🧠 Visión: Economía Auto-Regulada

**Aurora no es solo una blockchain con tokens fijos. Es un sistema VIVO que se adapta a las condiciones del ecosistema usando inteligencia artificial para optimizar tres objetivos:**

```
┌─────────────────────────────────────────┐
│         SISTEMA NERVIOSO DE AURORA      │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │   AI Policy Controller (Core)     │ │
│  └──────────┬────────────────────────┘ │
│             │                           │
│    ┌────────┴────────┐                 │
│    │                 │                 │
│    ▼                 ▼                 │
│ ┌──────┐         ┌──────┐             │
│ │Sense │         │Adapt │             │
│ └──┬───┘         └───┬──┘             │
│    │                 │                 │
│    │    ┌────────┐   │                │
│    └───►│Analyze │◄──┘                │
│         └────┬───┘                     │
│              │                         │
│              ▼                         │
│      ┌───────────────┐                │
│      │   3 Objetivos │                │
│      │               │                │
│      │ △ Confiabilidad                │
│      │ ○ Sostenibilidad               │
│      │ U Crecimiento Comunitario      │
│      └───────────────┘                │
└─────────────────────────────────────────┘
```

---

## 1. Los Tres Pilares del Sistema

### 🎯 Objetivo 1: Confiabilidad (△ MERIT)

**Definición:** La red debe ser estable, disponible y confiable 24/7

**Métricas Clave:**
```javascript
const reliability = {
  networkUptime: 99.9,        // % del tiempo la red está operativa
  avgNodeUptime: 99.5,        // % promedio uptime de nodos
  latency: 50,                // ms, tiempo de respuesta promedio
  peersConnected: 1000,       // número de peers activos
  relayNodesActive: 50,       // nodos relay disponibles
  validatorsOnline: 100,      // validators activos
};

// Score de confiabilidad (0-100)
function calculateReliabilityScore(metrics) {
  return (
    metrics.networkUptime * 0.3 +
    metrics.avgNodeUptime * 0.3 +
    (100 - metrics.latency / 10) * 0.2 +
    Math.min(metrics.peersConnected / 10, 100) * 0.1 +
    Math.min(metrics.relayNodesActive, 100) * 0.1
  );
}
```

**¿Qué necesita para mejorar?**
- Más validators (requiere MERIT staking)
- Mejores nodos relay (requiere incentivos)
- Infraestructura robusta (requiere inversión)

### 🌱 Objetivo 2: Sostenibilidad (○ MIND)

**Definición:** Los nodos y providers deben obtener recursos suficientes para subsistir y crecer

**Métricas Clave:**
```javascript
const sustainability = {
  avgNodeRevenue: 500,        // MIND/mes por nodo promedio
  avgNodeCosts: 300,          // USD/mes costos operativos
  providerProfitability: 1.67, // ratio revenue/costs
  churnRate: 0.05,            // % nodos que abandonan/mes
  newProviders: 10,           // nuevos providers/mes
  activeInferences: 10000,    // inferencias/día
};

// Score de sostenibilidad (0-100)
function calculateSustainabilityScore(metrics) {
  const profitMargin = Math.min((metrics.providerProfitability - 1) * 100, 100);
  const retention = (1 - metrics.churnRate) * 100;
  const growth = Math.min(metrics.newProviders * 10, 100);
  const utilization = Math.min(metrics.activeInferences / 100, 100);
  
  return (
    profitMargin * 0.4 +
    retention * 0.3 +
    growth * 0.2 +
    utilization * 0.1
  );
}
```

**¿Qué necesita para mejorar?**
- Más demanda (más users pagando MIND)
- Mejores rewards (emisión de MIND)
- Reducir costos operativos (eficiencia)

### 🤝 Objetivo 3: Crecimiento Comunitario (U TRUST)

**Definición:** La comunidad debe crecer, colaborar y auto-organizarse

**Métricas Clave:**
```javascript
const community = {
  activeUsers: 5000,          // usuarios activos/mes
  newUsers: 500,              // nuevos usuarios/mes
  mentorships: 50,            // mentorías activas
  collaborations: 100,        // proyectos colaborativos
  avgTrustPerUser: 75,        // TRUST promedio por usuario
  daoParticipation: 0.35,     // % usuarios que votan
  communityProjects: 20,      // proyectos comunitarios activos
};

// Score de comunidad (0-100)
function calculateCommunityScore(metrics) {
  const userGrowth = Math.min(metrics.newUsers / 10, 100);
  const engagement = Math.min(metrics.mentorships + metrics.collaborations, 100);
  const maturity = Math.min(metrics.avgTrustPerUser, 100);
  const governance = metrics.daoParticipation * 100;
  
  return (
    userGrowth * 0.3 +
    engagement * 0.3 +
    maturity * 0.2 +
    governance * 0.2
  );
}
```

**¿Qué necesita para mejorar?**
- Más incentivos para colaboración (TRUST rewards)
- Mejor onboarding (recursos educativos)
- Programas de mentorship (matching)

---

## 2. El Motor de IA: Adaptive Policy Controller

### 🤖 Arquitectura del Controlador

```rust
// Core AI controller
pub struct AdaptivePolicyController {
    // State
    current_metrics: SystemMetrics,
    historical_data: Vec<HistoricalSnapshot>,
    policy_parameters: PolicyParameters,
    
    // AI Models
    predictor: TimeSeriesPredictor,
    optimizer: PolicyOptimizer,
    anomaly_detector: AnomalyDetector,
    
    // Governance
    governance_contract: Address,
    emergency_pause: bool,
}

pub struct SystemMetrics {
    reliability: ReliabilityMetrics,
    sustainability: SustainabilityMetrics,
    community: CommunityMetrics,
    timestamp: u64,
}

pub struct PolicyParameters {
    // MERIT parameters
    merit_emission_rate: u64,
    merit_burn_rate: f64,
    merit_staking_requirement: u64,
    
    // MIND parameters
    mind_emission_multiplier: f64,
    mind_burn_rate: f64,
    mind_base_price: u64,
    
    // TRUST parameters
    trust_interaction_rewards: HashMap<InteractionType, u64>,
    trust_transfer_limit: f64,
    
    // Global
    last_update: u64,
    update_frequency: u64, // cada cuántos bloques actualizar
}
```

### 🔄 Ciclo de Adaptación (Cada 24 Horas)

```rust
impl AdaptivePolicyController {
    pub async fn run_adaptation_cycle(&mut self) -> Result<PolicyAdjustments> {
        // 1. SENSE: Recopilar métricas actuales
        let current = self.collect_current_metrics().await?;
        
        // 2. ANALYZE: Calcular scores y detectar problemas
        let scores = self.analyze_system_health(&current);
        let anomalies = self.detect_anomalies(&current);
        
        // 3. PREDICT: Proyectar próximos 7 días
        let forecast = self.predict_future_state(&current, 7).await?;
        
        // 4. OPTIMIZE: Calcular ajustes óptimos
        let adjustments = self.optimize_policy(&scores, &forecast).await?;
        
        // 5. VALIDATE: Simular impacto de cambios
        let simulation = self.simulate_adjustments(&adjustments).await?;
        
        // 6. DECIDE: Aplicar si mejora score total
        if simulation.total_score > scores.total_score {
            self.apply_adjustments(&adjustments).await?;
            Ok(adjustments)
        } else {
            Ok(PolicyAdjustments::no_change())
        }
    }
    
    fn analyze_system_health(&self, metrics: &SystemMetrics) -> HealthScores {
        let reliability = calculateReliabilityScore(&metrics.reliability);
        let sustainability = calculateSustainabilityScore(&metrics.sustainability);
        let community = calculateCommunityScore(&metrics.community);
        
        // Score ponderado total (0-100)
        let total = (reliability * 0.4 + sustainability * 0.35 + community * 0.25);
        
        HealthScores {
            reliability,
            sustainability,
            community,
            total,
            timestamp: metrics.timestamp,
        }
    }
}
```

---

## 3. Estrategias de Adaptación por Escenario

### 📊 Escenario 1: Confiabilidad Baja (Score < 70)

**Problema:** Pocos validators, red inestable, latencia alta

**Diagnóstico IA:**
```python
# Análisis
reliability_score = 65  # ⚠️ Bajo
sustainability_score = 80
community_score = 75

# Root cause analysis
root_causes = [
    "Solo 30 validators activos (necesita 100+)",
    "Uptime promedio: 97% (target: 99%)",
    "10 relay nodes (necesita 50+)"
]

# ¿Por qué tan pocos validators?
- MERIT rewards no son suficientes
- Staking requirement muy alto (10k MERIT)
- Competencia con otras chains
```

**Acción IA: Aumentar Incentivos MERIT**

```rust
fn adapt_for_low_reliability(&mut self) -> PolicyAdjustments {
    PolicyAdjustments {
        // Aumentar emission de MERIT 20%
        merit_emission_rate: self.policy.merit_emission_rate * 1.2,
        
        // Reducir staking requirement 30%
        merit_staking_requirement: self.policy.merit_staking_requirement * 0.7,
        
        // Aumentar fees distribuidos a validators (80% vs 60%)
        merit_validator_fee_share: 0.8,
        
        // Reducir burn temporalmente (15% vs 20%)
        merit_burn_rate: 0.15,
        
        // Justificación
        reason: "Incentivando nuevos validators para mejorar confiabilidad",
        expected_impact: ExpectedImpact {
            reliability: +15,  // espera mejorar 15 puntos
            sustainability: -5, // pequeño trade-off (más inflación)
            community: 0,
        },
        duration_blocks: 100_000, // ~2 semanas, luego re-evaluar
    }
}
```

**Resultado Esperado (7 días después):**
```
Antes:
- Validators: 30
- Uptime: 97%
- Reliability Score: 65

Después:
- Validators: 55 (+83% 🎉)
- Uptime: 98.5% (+1.5%)
- Reliability Score: 82 (+17)

Side effects:
- MERIT supply: +2% inflación adicional (temporal)
- Sustainability score: -3 puntos (acceptable trade-off)
```

---

### 📊 Escenario 2: Sostenibilidad Baja (Score < 60)

**Problema:** Providers no ganan suficiente, churn rate alto

**Diagnóstico IA:**
```python
# Análisis
reliability_score = 85
sustainability_score = 55  # ⚠️ Crítico
community_score = 70

# Root cause analysis
root_causes = [
    "Avg provider revenue: 200 MIND/mes",
    "Avg provider costs: 300 USD/mes",
    "Profitability: 0.67 (perdiendo dinero!)",
    "Churn rate: 15%/mes (muy alto)",
    "Solo 3 nuevos providers/mes"
]

# ¿Por qué tan pocos ingresos?
- Poca demanda (solo 2000 inferences/día)
- Precio muy bajo (5 MIND por inference)
- Muchos providers compitiendo (race to bottom)
```

**Acción IA: Aumentar Rewards y Demanda**

```rust
fn adapt_for_low_sustainability(&mut self) -> PolicyAdjustments {
    PolicyAdjustments {
        // Aumentar emission multiplier de MIND (5x → 8x)
        mind_emission_multiplier: 8.0,
        
        // Aumentar precio base sugerido
        mind_base_price: 10, // 5 → 10 MIND
        
        // Reducir burn temporalmente (20% vs 30%)
        mind_burn_rate: 0.2,
        
        // Bonus para providers con alto TRUST
        trust_provider_bonus: 0.3, // +30% si TRUST > 100
        
        // Subsidio del treasury para providers críticos
        treasury_subsidy_pool: 50_000, // MIND/mes
        
        reason: "Subsidiar providers para prevenir colapso de red",
        expected_impact: ExpectedImpact {
            reliability: -5, // puede bajar un poco (menos providers)
            sustainability: +25, // gran mejora
            community: +5, // providers más felices
        },
        duration_blocks: 200_000, // ~1 mes
    }
}
```

**Resultado Esperado (30 días después):**
```
Antes:
- Avg revenue: 200 MIND/mes
- Profitability: 0.67 (pérdida)
- Churn: 15%/mes
- Sustainability Score: 55

Después:
- Avg revenue: 450 MIND/mes (+125% 🎉)
- Profitability: 1.5 (ganando)
- Churn: 5%/mes (-67%)
- New providers: 15/mes (+400%)
- Sustainability Score: 80 (+25)

Side effects:
- MIND supply: +8% inflación temporal
- Treasury: -50k MIND/mes (sostenible 20 meses)
```

---

### 📊 Escenario 3: Comunidad Estancada (Score < 65)

**Problema:** Poco crecimiento, baja participación, falta colaboración

**Diagnóstico IA:**
```python
# Análisis
reliability_score = 88
sustainability_score = 82
community_score = 60  # ⚠️ Bajo

# Root cause analysis
root_causes = [
    "Solo 100 nuevos usuarios/mes (need 500+)",
    "5 mentorships activas (very low)",
    "DAO participation: 15% (muy bajo)",
    "Avg TRUST per user: 20 (indica poca colaboración)",
    "0 proyectos comunitarios nuevos este mes"
]

# ¿Por qué tan poco engagement?
- Difícil ganar TRUST (solo 5 mentorships)
- No hay incentivos claros para colaborar
- Onboarding complicado
- Falta de visibilidad de oportunidades
```

**Acción IA: Programas de Crecimiento Comunitario**

```rust
fn adapt_for_low_community(&mut self) -> PolicyAdjustments {
    PolicyAdjustments {
        // Aumentar rewards de TRUST significativamente
        trust_mentorship_reward: 20, // 10 → 20 TRUST
        trust_collaboration_reward: 10, // 5 → 10 TRUST
        
        // Airdrop para nuevos usuarios
        trust_welcome_airdrop: 10, // 10 TRUST al registrarse
        
        // Bonus por participación en governance
        trust_voting_reward: 1, // 1 TRUST por voto
        
        // Matching fund para proyectos comunitarios
        community_project_matching: 2.0, // 2x matching de contribuciones
        
        // Usar treasury MIND para financiar mentorships
        mentorship_subsidy: 50, // 50 MIND/mes al mentor
        
        reason: "Impulsar crecimiento y engagement comunitario",
        expected_impact: ExpectedImpact {
            reliability: 0,
            sustainability: -3, // pequeño costo (treasury)
            community: +20, // gran mejora esperada
        },
        duration_blocks: 150_000, // ~3 semanas
    }
}
```

**Resultado Esperado (21 días después):**
```
Antes:
- New users: 100/mes
- Mentorships: 5
- DAO participation: 15%
- Avg TRUST: 20
- Community Score: 60

Después:
- New users: 450/mes (+350% 🎉)
- Mentorships: 35 (+600%)
- DAO participation: 35% (+133%)
- Avg TRUST: 45 (+125%)
- Community projects: 8 nuevos
- Community Score: 80 (+20)

Side effects:
- TRUST supply: +15% (saludable, más gente involucrada)
- Treasury MIND: -20k (investment en comunidad)
```

---

## 4. Equilibrio Dinámico: The Balancing Act

### ⚖️ Sistema de Trade-offs

**El sistema NUNCA optimiza solo un pilar. Siempre busca equilibrio:**

```rust
fn calculate_total_value(scores: &HealthScores, weights: &Weights) -> f64 {
    // Función objetivo que la IA maximiza
    let base_score = 
        scores.reliability * weights.reliability +
        scores.sustainability * weights.sustainability +
        scores.community * weights.community;
    
    // Penalización por desequilibrio extremo
    let balance_penalty = calculate_imbalance_penalty(scores);
    
    // Bonus por sinergia (todos altos)
    let synergy_bonus = if scores.all_above(75) { 10.0 } else { 0.0 };
    
    base_score - balance_penalty + synergy_bonus
}

fn calculate_imbalance_penalty(scores: &HealthScores) -> f64 {
    // Si un pilar es muy bajo comparado con otros, penalizar
    let min_score = scores.min();
    let max_score = scores.max();
    let gap = max_score - min_score;
    
    if gap > 30.0 {
        // Penalización cuadrática por desequilibrio
        (gap - 30.0).powf(2.0) / 10.0
    } else {
        0.0
    }
}
```

**Ejemplo de Penalización:**

```
Scenario A: Desequilibrado
- Reliability: 95
- Sustainability: 85
- Community: 45 ⚠️
- Raw score: 95*0.4 + 85*0.35 + 45*0.25 = 79.5
- Imbalance penalty: (95-45-30)² / 10 = 40
- Total: 79.5 - 40 = 39.5 ❌

Scenario B: Equilibrado
- Reliability: 80
- Sustainability: 75
- Community: 70
- Raw score: 80*0.4 + 75*0.35 + 70*0.25 = 75.75
- Imbalance penalty: 0 (gap = 10 < 30)
- Synergy bonus: 0 (no todos > 75)
- Total: 75.75 ✅

¡El sistema prefiere Scenario B aunque scores individuales sean menores!
```

---

## 5. Machine Learning: Predicción y Optimización

### 🧮 Modelos de IA Implementados

#### **A. Time Series Predictor**

```python
# Modelo LSTM para predecir métricas futuras
class TimeSeriesPredictor:
    def __init__(self):
        self.model = LSTM(
            input_size=15,  # 15 métricas
            hidden_size=128,
            num_layers=3,
            output_size=15,
            dropout=0.2
        )
        self.scaler = StandardScaler()
        
    def predict_next_week(self, historical_data, policy_params):
        """
        Predice métricas de próximos 7 días dado:
        - Datos históricos (últimos 30 días)
        - Parámetros de política actual
        
        Returns: predicted_metrics[7] (array de 7 días)
        """
        # Preprocesar
        X = self.prepare_features(historical_data, policy_params)
        X_scaled = self.scaler.transform(X)
        
        # Predecir
        with torch.no_grad():
            predictions = self.model(X_scaled)
        
        # Postprocesar
        return self.scaler.inverse_transform(predictions)
    
    def train_on_historical_data(self, data):
        """
        Entrena modelo con datos históricos reales
        Se re-entrena cada mes con nuevos datos
        """
        X_train, y_train = self.create_sequences(data, seq_length=30)
        
        optimizer = Adam(self.model.parameters(), lr=0.001)
        criterion = MSELoss()
        
        for epoch in range(100):
            optimizer.zero_grad()
            output = self.model(X_train)
            loss = criterion(output, y_train)
            loss.backward()
            optimizer.step()
```

#### **B. Policy Optimizer**

```python
# Usa reinforcement learning para encontrar mejores políticas
class PolicyOptimizer:
    def __init__(self):
        self.actor = PolicyNetwork(state_dim=45, action_dim=12)
        self.critic = ValueNetwork(state_dim=45)
        
    def optimize_policy(self, current_state, predictor):
        """
        Encuentra ajustes óptimos de policy parameters usando PPO
        
        State: [reliability_metrics, sustainability_metrics, community_metrics]
        Action: [merit_emission_delta, mind_emission_delta, ..., trust_rewards_delta]
        Reward: improvement in total_score
        """
        # Current state embedding
        state_vector = self.embed_state(current_state)
        
        # Sample multiple policy adjustments
        candidate_policies = []
        for _ in range(100):
            # Actor propone ajustes
            action = self.actor.sample(state_vector)
            policy_delta = self.action_to_policy_delta(action)
            
            # Predecir impacto con predictor
            future_state = predictor.predict_with_policy(
                current_state, 
                policy_delta,
                days=7
            )
            
            # Calcular reward
            current_score = calculate_total_value(current_state)
            future_score = calculate_total_value(future_state)
            reward = future_score - current_score
            
            candidate_policies.append((policy_delta, reward))
        
        # Retornar mejor política
        best_policy, best_reward = max(candidate_policies, key=lambda x: x[1])
        return best_policy, best_reward
    
    def train_from_experience(self, experiences):
        """
        Aprende de ajustes previos (buenos y malos)
        Experiences: [(state, action, reward, next_state)]
        """
        # PPO training loop
        for state, action, reward, next_state in experiences:
            # Calcular advantage
            value = self.critic(state)
            next_value = self.critic(next_state)
            advantage = reward + 0.99 * next_value - value
            
            # Update actor (policy)
            actor_loss = -self.actor.log_prob(action) * advantage
            actor_loss.backward()
            
            # Update critic (value function)
            critic_loss = (reward + 0.99 * next_value - value).pow(2)
            critic_loss.backward()
```

#### **C. Anomaly Detector**

```python
# Detecta comportamientos anómalos que requieren intervención
class AnomalyDetector:
    def __init__(self):
        self.autoencoder = Autoencoder(input_dim=15, latent_dim=5)
        self.threshold = 0.1  # reconstruction error threshold
        
    def detect_anomalies(self, current_metrics):
        """
        Detecta si métricas actuales son anómalas
        """
        X = self.preprocess(current_metrics)
        reconstruction = self.autoencoder(X)
        error = F.mse_loss(X, reconstruction)
        
        if error > self.threshold:
            # Analizar qué métrica es más anómala
            anomalies = self.identify_anomalous_features(X, reconstruction)
            return True, anomalies
        return False, []
    
    def identify_anomalous_features(self, original, reconstructed):
        """
        Identifica cuáles métricas específicas son anómalas
        """
        errors = (original - reconstructed).pow(2)
        anomalous_indices = torch.where(errors > self.threshold)[0]
        
        metric_names = [
            'network_uptime', 'avg_node_uptime', 'latency',
            'peers_connected', 'validators_online',
            'avg_node_revenue', 'provider_profitability', 'churn_rate',
            'active_users', 'new_users', 'mentorships',
            'dao_participation', 'avg_trust'
        ]
        
        return [metric_names[i] for i in anomalous_indices]
```

---

## 6. Implementación: Smart Contract + Off-Chain IA

### 🔗 Arquitectura Híbrida

```
┌─────────────────────────────────────────────────┐
│                 OFF-CHAIN (IA)                  │
│                                                 │
│  ┌──────────────────────────────────────────┐  │
│  │  Python AI Engine (Cloud)                │  │
│  │  - Time series prediction                │  │
│  │  - Policy optimization                   │  │
│  │  - Anomaly detection                     │  │
│  └──────────────┬───────────────────────────┘  │
│                 │                               │
│                 │ Propone ajustes               │
│                 ▼                               │
│  ┌──────────────────────────────────────────┐  │
│  │  Oracle Node (Rust)                      │  │
│  │  - Valida propuestas                     │  │
│  │  - Firma transacciones                   │  │
│  └──────────────┬───────────────────────────┘  │
└─────────────────┼───────────────────────────────┘
                  │
                  │ Envia tx
                  ▼
┌─────────────────────────────────────────────────┐
│              ON-CHAIN (Blockchain)              │
│                                                 │
│  ┌──────────────────────────────────────────┐  │
│  │  AdaptivePolicyContract (Solidity)       │  │
│  │  - Recibe propuestas del oracle          │  │
│  │  - Valida límites de cambio              │  │
│  │  - Aplica ajustes si aprobados           │  │
│  │  - Emite eventos                         │  │
│  └──────────────┬───────────────────────────┘  │
│                 │                               │
│                 │ Actualiza parámetros          │
│                 ▼                               │
│  ┌──────────────────────────────────────────┐  │
│  │  MeritToken / MindToken / TrustToken     │  │
│  │  - Ajustan emission rates                │  │
│  │  - Ajustan burn rates                    │  │
│  │  - Ajustan rewards                       │  │
│  └──────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
```

### 📜 Smart Contract Principal

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract AdaptivePolicyContract {
    // Oracle autorizado (IA engine)
    address public oracle;
    
    // Parámetros actuales
    PolicyParameters public params;
    
    // Historial de ajustes
    PolicyAdjustment[] public adjustments;
    
    // Governance
    address public governance;
    uint256 public constant MIN_DELAY = 1 days;
    uint256 public constant MAX_CHANGE_PERCENT = 30; // max 30% change per adjustment
    
    struct PolicyParameters {
        // MERIT
        uint256 meritEmissionRate;
        uint256 meritBurnRate;      // basis points (10000 = 100%)
        uint256 meritStakingReq;
        
        // MIND
        uint256 mindEmissionMultiplier; // scaled by 100
        uint256 mindBurnRate;
        uint256 mindBasePrice;
        
        // TRUST
        uint256 trustMentorshipReward;
        uint256 trustCollabReward;
        uint256 trustWelcomeAirdrop;
        
        // Metadata
        uint256 lastUpdate;
        string reason;
    }
    
    struct PolicyAdjustment {
        PolicyParameters proposed;
        uint256 proposedAt;
        uint256 executedAt;
        HealthScores scoresBefore;
        HealthScores scoresAfter;
        bool executed;
    }
    
    struct HealthScores {
        uint256 reliability;      // 0-100
        uint256 sustainability;   // 0-100
        uint256 community;        // 0-100
        uint256 total;           // weighted average
    }
    
    event PolicyProposed(uint256 indexed adjustmentId, string reason);
    event PolicyExecuted(uint256 indexed adjustmentId);
    event PolicyRejected(uint256 indexed adjustmentId, string reason);
    event AnomalyDetected(string[] anomalousMetrics);
    
    modifier onlyOracle() {
        require(msg.sender == oracle, "Only oracle");
        _;
    }
    
    modifier onlyGovernance() {
        require(msg.sender == governance, "Only governance");
        _;
    }
    
    constructor(address _oracle, address _governance) {
        oracle = _oracle;
        governance = _governance;
        
        // Initial parameters
        params = PolicyParameters({
            meritEmissionRate: 10 * 10**18,
            meritBurnRate: 2000, // 20%
            meritStakingReq: 10_000 * 10**18,
            
            mindEmissionMultiplier: 1000, // 10x
            mindBurnRate: 3000, // 30%
            mindBasePrice: 10 * 10**18,
            
            trustMentorshipReward: 10 * 10**18,
            trustCollabReward: 5 * 10**18,
            trustWelcomeAirdrop: 5 * 10**18,
            
            lastUpdate: block.timestamp,
            reason: "Genesis parameters"
        });
    }
    
    function proposeAdjustment(
        PolicyParameters calldata proposed,
        HealthScores calldata currentScores,
        string calldata reason
    ) external onlyOracle returns (uint256) {
        // Validar cambios no son demasiado drásticos
        require(validateAdjustment(proposed), "Changes too large");
        
        // Crear propuesta
        PolicyAdjustment memory adjustment = PolicyAdjustment({
            proposed: proposed,
            proposedAt: block.timestamp,
            executedAt: 0,
            scoresBefore: currentScores,
            scoresAfter: HealthScores(0, 0, 0, 0), // TBD
            executed: false
        });
        
        adjustments.push(adjustment);
        uint256 adjustmentId = adjustments.length - 1;
        
        emit PolicyProposed(adjustmentId, reason);
        return adjustmentId;
    }
    
    function executeAdjustment(
        uint256 adjustmentId,
        HealthScores calldata scoresAfter
    ) external onlyOracle {
        PolicyAdjustment storage adjustment = adjustments[adjustmentId];
        
        require(!adjustment.executed, "Already executed");
        require(
            block.timestamp >= adjustment.proposedAt + MIN_DELAY,
            "Delay not met"
        );
        
        // Verificar que scores mejoraron (o no empeoraron mucho)
        require(
            scoresAfter.total >= adjustment.scoresBefore.total - 5,
            "Scores would decrease too much"
        );
        
        // Aplicar cambios
        params = adjustment.proposed;
        params.lastUpdate = block.timestamp;
        
        adjustment.executed = true;
        adjustment.executedAt = block.timestamp;
        adjustment.scoresAfter = scoresAfter;
        
        // Notificar a token contracts
        notifyTokenContracts();
        
        emit PolicyExecuted(adjustmentId);
    }
    
    function validateAdjustment(
        PolicyParameters calldata proposed
    ) internal view returns (bool) {
        // Validar que cambios no excedan MAX_CHANGE_PERCENT
        
        // MERIT checks
        if (!withinBounds(proposed.meritEmissionRate, params.meritEmissionRate)) return false;
        if (!withinBounds(proposed.meritBurnRate, params.meritBurnRate)) return false;
        if (!withinBounds(proposed.meritStakingReq, params.meritStakingReq)) return false;
        
        // MIND checks
        if (!withinBounds(proposed.mindEmissionMultiplier, params.mindEmissionMultiplier)) return false;
        if (!withinBounds(proposed.mindBurnRate, params.mindBurnRate)) return false;
        
        // TRUST checks
        if (!withinBounds(proposed.trustMentorshipReward, params.trustMentorshipReward)) return false;
        
        return true;
    }
    
    function withinBounds(uint256 proposed, uint256 current) internal pure returns (bool) {
        if (current == 0) return proposed < 1000 * 10**18; // arbitrary max for new params
        
        uint256 change = proposed > current 
            ? (proposed - current) * 100 / current
            : (current - proposed) * 100 / current;
            
        return change <= MAX_CHANGE_PERCENT;
    }
    
    function notifyTokenContracts() internal {
        // Llamar a MeritToken.updateParameters()
        // Llamar a MindToken.updateParameters()
        // Llamar a TrustToken.updateParameters()
        // (omitido por brevedad)
    }
    
    function reportAnomaly(string[] calldata anomalousMetrics) external onlyOracle {
        emit AnomalyDetected(anomalousMetrics);
        // Podría trigger emergency pause si crítico
    }
    
    // Governance puede override en emergencias
    function emergencyOverride(PolicyParameters calldata override_params) external onlyGovernance {
        params = override_params;
        params.lastUpdate = block.timestamp;
    }
}
```

---

## 7. Simulación: Primer Año de Operación

### 📈 Timeline con Adaptaciones

```
MES 0 (GENESIS):
├── Reliability: 70 (pocos validators)
├── Sustainability: 50 (providers perdiendo dinero)
├── Community: 40 (casi nadie)
└── Total: 55 ⚠️ CRÍTICO

AI Action: Emergency bootstrap mode
- Aumentar MERIT emission 50%
- Subsidios MIND del treasury
- Airdrops masivos de TRUST
```

```
MES 1:
├── Reliability: 75 (+5, más validators)
├── Sustainability: 65 (+15, subsidios working)
├── Community: 55 (+15, airdrops atraen gente)
└── Total: 66 ⚠️ Mejorando pero aún bajo

AI Action: Continue bootstrap
- Mantener incentivos altos
- Focus en onboarding
```

```
MES 3:
├── Reliability: 82 (+7, red estabilizándose)
├── Sustainability: 72 (+7, demanda aumentando)
├── Community: 68 (+13, early adopters engaged)
└── Total: 75 ✅ Saludable

AI Action: Empezar a normalizar
- Reducir emission MERIT 10%
- Mantener MIND incentives
- Bonus TRUST para mentors
```

```
MES 6:
├── Reliability: 88 (+6, 100+ validators)
├── Sustainability: 80 (+8, providers profitable)
├── Community: 75 (+7, comunidad activa)
└── Total: 82 ✅ Muy saludable

AI Action: Optimizar eficiencia
- Reducir emission MERIT a normal
- Aumentar burn rates (deflación)
- Focus en quality (TRUST)
```

```
MES 9:
├── Reliability: 85 (-3, algunos validators salen)
├── Sustainability: 88 (+8, demanda explota)
├── Community: 78 (+3, crecimiento estable)
└── Total: 84 ✅ Excelente

AI Action: Balance
- Pequeño aumento MERIT incentives (prevent más salidas)
- Reducir MIND emission (supply control)
- Maintain TRUST programs
```

```
MES 12 (AÑO 1):
├── Reliability: 87 (+2, red madura)
├── Sustainability: 85 (-3, normalizado)
├── Community: 82 (+4, cultura establecida)
└── Total: 85 ✅ EQUILIBRIO ALCANZADO

Sistema auto-regulándose!
- Policy changes ahora son pequeños tweaks (<10%)
- AI ha aprendido patrones
- Ecosistema sostenible
```

---

## 8. Governance: Humanos + IA

### 🤝 Hybrid Decision Making

```solidity
contract HybridGovernance {
    // AI puede proponer, pero DAO puede vetar
    
    enum ProposalStatus {
        Proposed,      // AI propuso
        UnderReview,   // DAO revisando
        Approved,      // DAO aprobó
        Rejected,      // DAO rechazó
        Executed       // Ejecutado
    }
    
    struct Proposal {
        uint256 id;
        PolicyParameters params;
        string aiReasoning;
        HealthScores predictedImpact;
        
        ProposalStatus status;
        uint256 votesFor;
        uint256 votesAgainst;
        uint256 quorum;
        
        uint256 proposedAt;
        uint256 votingEndsAt;
    }
    
    function proposeByAI(
        PolicyParameters calldata params,
        string calldata reasoning,
        HealthScores calldata predicted
    ) external onlyOracle returns (uint256) {
        // AI propone
        Proposal memory prop = Proposal({
            id: proposals.length,
            params: params,
            aiReasoning: reasoning,
            predictedImpact: predicted,
            status: ProposalStatus.Proposed,
            votesFor: 0,
            votesAgainst: 0,
            quorum: calculateQuorum(params),
            proposedAt: block.timestamp,
            votingEndsAt: block.timestamp + 3 days
        });
        
        proposals.push(prop);
        
        emit AIProposal(prop.id, reasoning);
        return prop.id;
    }
    
    function calculateQuorum(PolicyParameters calldata params) internal pure returns (uint256) {
        // Cambios grandes requieren más quorum
        // Cambios pequeños pueden auto-ejecutarse
        
        // ... lógica para determinar si necesita voto DAO
        // Si cambio < 10%: quorum = 0 (auto-execute)
        // Si cambio 10-20%: quorum = 10% token holders
        // Si cambio > 20%: quorum = 30% token holders
    }
    
    function vote(uint256 proposalId, bool support) external {
        // Voting power basado en tres tokens
        uint256 power = calculateVotingPower(msg.sender);
        
        Proposal storage prop = proposals[proposalId];
        
        if (support) {
            prop.votesFor += power;
        } else {
            prop.votesAgainst += power;
        }
        
        // Si alcanza quorum, cambiar status
        if (prop.votesFor + prop.votesAgainst >= prop.quorum) {
            if (prop.votesFor > prop.votesAgainst) {
                prop.status = ProposalStatus.Approved;
            } else {
                prop.status = ProposalStatus.Rejected;
            }
        }
    }
}
```

### 🚨 Emergency Override

```solidity
// En caso de mal funcionamiento de AI
function emergencyPause() external {
    require(
        msg.sender == governance || 
        msg.sender == emergencyMultisig,
        "Not authorized"
    );
    
    aiEnabled = false;
    
    emit EmergencyPause(msg.sender, block.timestamp);
}

// Ejemplos de cuando pausar AI:
// 1. AI propone cambios irracionales
// 2. Oracle está comprometido
// 3. Bugs detectados en prediction model
// 4. Comunidad vota para pausar
```

---

## 9. Métricas de Éxito del Sistema Adaptativo

### ✅ KPIs del Sistema de IA

```javascript
const aiSystemMetrics = {
  // Accuracy
  predictionAccuracy: 0.85,        // 85% accurate forecasts
  policyImprovementRate: 0.78,     // 78% de ajustes mejoran scores
  
  // Efficiency
  avgCycleTime: 24,                // horas entre ciclos
  computeCost: 50,                 // USD/día para run AI
  
  // Impact
  scoreImprovement: +30,           // total score mejoró 30 puntos en año 1
  stabilityIndex: 0.9,             // 90% del tiempo scores > 75
  
  // Governance
  daoOverrideRate: 0.05,           // Solo 5% de propuestas rechazadas
  emergencyPauses: 0,              // Nunca tuvo que pausarse
  
  // Learning
  modelRetrainingFrequency: 30,    // días entre re-training
  experienceBufferSize: 365,       // 1 año de histórico
};
```

### 🎯 Objetivos a Largo Plazo

```
AÑO 1: Bootstrap y estabilización
- Objetivo: Total score > 80
- Estado: ✅ LOGRADO (85)

AÑO 2: Optimización y eficiencia
- Objetivo: Reducir policy changes a <5/mes
- Estado: 🔄 EN PROGRESO

AÑO 3: Auto-sostenibilidad
- Objetivo: Sistema funciona sin intervención humana
- Estado: 🎯 META FUTURA

AÑO 5: Ecosystem maduro
- Objetivo: AI ha evolucionado con comunidad
- Estado: 🌟 VISIÓN
```

---

## 10. Conclusión: Un Sistema Vivo

### 🌱 La Diferencia Clave

**Blockchains tradicionales:**
```
Parámetros fijos → Community sufre → Hard fork required
                 → Lento, contencioso, puede split chain
```

**Aurora con AI adaptativa:**
```
Métricas en tiempo real → AI detecta problemas → Propone solución
                        → DAO valida → Ajuste automático
                        → Sistema mejora continuamente
```

### 💎 Tres Principios Fundamentales

1. **Resiliencia**: Sistema se adapta a crisis
2. **Sostenibilidad**: Nodos siempre rentables
3. **Crecimiento**: Comunidad floreciente

### 🚀 Visión Final

```
Aurora es más que una blockchain.
Es un ecosistema VIVO que:

- SIENTE (métricas en tiempo real)
- PIENSA (AI analiza y optimiza)
- ACTÚA (ajusta políticas)
- APRENDE (mejora con el tiempo)
- EQUILIBRA (nunca sacrifica un pilar)

Todo orquestado para que:
△ Nodos sean confiables
○ Providers subsistan
U Comunidad crezca

Juntos, sostenibles, para siempre.
```

---

**Aurora: El primer blockchain con sistema nervioso. 🧠🌅**
