# 🐹 Aurora Reputation System - Design Document

## Filosofía

> *"Los patrones revelan la verdad, no los eventos aislados."*  
> *"Toda criatura merece una segunda oportunidad."*  
> *"La exclusión es el último recurso, no el primero."*  
> — Pepino, el guía ético

## Problema a Resolver

En redes P2P descentralizadas, **nodos tóxicos** pueden:
- Enviar datos corruptos
- Consumir recursos sin contribuir
- Atacar con spam o DoS
- Comportarse de forma egoísta (no cooperar)

### Solución Tradicional (Problemática)
- **Ban inmediato** después de X errores
- **Lista negra centralizada**
- **Sin oportunidad de redención**
- **Sin transparencia** en decisiones

### Nuestra Solución (Ética + ML)
- **Detección de patrones** (no eventos aislados)
- **Reputación distribuida** (consenso comunitario)
- **Segunda oportunidad** (redemption paths)
- **Transparencia total** (explica sus decisiones)

## Arquitectura

```
┌────────────────────────────────────────────────────────────┐
│              Reputation System (Client-Side)               │
└────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ Interaction  │    │   Pattern    │    │  Community   │
│   Tracking   │    │   Detection  │    │   Reports    │
│              │    │     (ML)     │    │              │
└──────────────┘    └──────────────┘    └──────────────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            │
                            ▼
                    ┌──────────────┐
                    │ Reputation   │
                    │    Score     │
                    │  (0.0-1.0)   │
                    └──────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ Should       │    │ Redemption   │    │ Explanation  │
│ Connect?     │    │    Path      │    │  (Human)     │
└──────────────┘    └──────────────┘    └──────────────┘
```

## Componentes

### 1. Interaction Tracking
Registra todas las interacciones con otros peers:
- **Tipo**: tensor_exchange, message, contract, etc.
- **Resultado**: success/failure
- **Timestamp**: cuándo ocurrió
- **Metadata**: contexto adicional

**Ventana deslizante:** Últimas 20 interacciones (configurable)

### 2. Pattern Detection (ML)
Detecta patrones de comportamiento usando técnicas simples de ML:

#### Patrones Detectados:

**a) Fallos Consecutivos**
```python
# Ejemplo: 5+ fallos seguidos = patrón sospechoso
if max_consecutive_failures >= 5:
    patterns['alert_consecutive_failures'] = True
```

**b) Comportamiento Bot-like**
```python
# Intervalos muy regulares = posible bot malicioso
if coefficient_of_variation < 0.1:
    patterns['alert_bot_like_behavior'] = True
```

**c) Tendencias Temporales**
```python
# ¿Está mejorando o empeorando?
trend = second_half_success - first_half_success
if trend > 0.2:
    patterns['improving'] = True  # ¡Dale segunda oportunidad!
```

**d) Reportes Múltiples**
```python
# 3+ peers diferentes reportan = serio
if unique_reporters >= 3:
    patterns['alert_multiple_reporters'] = True
```

### 3. Score Calculation

**Fórmula:**
```python
final_score = base_score * ml_adjustment * community_factor
```

**Base Score:**
- Simple ratio: éxitos / total interacciones

**ML Adjustment:**
- Penalizaciones por patrones tóxicos
- Bonificaciones por mejora
- Factor 0.7-1.2x

**Community Factor:**
- Basado en reportes de otros peers
- Más peso si son múltiples reporteros
- Factor 0.3-1.0x

**Resultado:** Score entre 0.0 (tóxico) y 1.0 (excelente)

### 4. Confidence Level

```python
confidence = min(1.0, interaction_count / MIN_INTERACTIONS)
```

- **Baja confianza** (< 10 interacciones): Dar benefit of doubt
- **Alta confianza** (> 10 interacciones): Score más confiable

### 5. Decision Making

```python
if score >= 0.8:
    return "Conectar - Peer confiable"
elif score >= 0.5:
    return "Conectar con precaución"
elif peer_in_redemption:
    return "Conectar - En proceso de mejora"
elif score < 0.3 and confidence > 0.7:
    return "NO conectar - Patrón tóxico confirmado"
else:
    return "Dar oportunidad - Poca información"
```

### 6. Redemption Path

Cuando un peer tiene score bajo, **NO lo baneamos**. Le damos un path de redención:

```python
redemption_path = {
    'goals': [
        {
            'type': 'reduce_failures',
            'target': 'Achieve 80% success rate in next 20 interactions',
            'metric': 'success_rate',
            'threshold': 0.8
        }
    ],
    'expires_at': now + 7_days,
    'explanation': "🐹 Pepino dice: 'Completa estos objetivos...'"
}
```

**Período:** 7 días para demostrar mejora  
**Tracking:** Sistema monitorea progreso  
**Resultado:** Score puede recuperarse

## Integración con Discovery Server

### API Enhancement

**Request:**
```bash
GET /discover?archetype=pepino&reputation=true
```

**Response:**
```json
{
  "peers": [
    {
      "peer_id": "peer-123",
      "address": "192.168.1.100",
      "port": 9000,
      "archetypes": ["pepino"],
      "reputation_hint": {
        "score": 0.85,
        "is_new": false,
        "age_hours": 48.5,
        "note": "Simple hint - full reputation calculated client-side"
      }
    }
  ]
}
```

**Nota:** El Discovery Server solo da un **hint simple**. La reputación completa con ML se calcula **client-side** para descentralización.

## Flujo de Uso

### Caso 1: Nuevo Peer (Sin Historial)

```python
# Primer encuentro con peer-new
reputation = system.calculate_reputation("peer-new")

# Output:
# score: 0.7 (neutral-positive)
# confidence: 0.1 (baja)
# decision: "Conectar - Dar oportunidad"
```

**Filosofía:** "Todo nuevo ser merece benefit of the doubt"

### Caso 2: Peer con Buen Historial

```python
# 50 interacciones, 90% éxito
reputation = system.calculate_reputation("peer-good")

# Output:
# score: 0.92
# confidence: 1.0
# decision: "Conectar - Peer altamente confiable"
```

### Caso 3: Peer con Fallos (Primera Vez)

```python
# 15 interacciones, 40% éxito (pero solo 15!)
reputation = system.calculate_reputation("peer-shaky")

# Output:
# score: 0.45
# confidence: 0.5 (media)
# decision: "Conectar con precaución - Monitorear"
```

**No baneamos:** Poca data todavía

### Caso 4: Peer Tóxico Confirmado

```python
# 30 interacciones, 20% éxito, 5+ reportes
reputation = system.calculate_reputation("peer-toxic")

# Output:
# score: 0.25
# confidence: 0.95
# patterns: ['alert_consecutive_failures', 'alert_multiple_reporters']
# decision: "NO conectar - Patrón tóxico confirmado"
# redemption_path: {...}  # Pero le damos un path!
```

### Caso 5: Peer en Redención

```python
# Peer-toxic después de 5 días mejorando
# Nuevas 20 interacciones, 85% éxito

reputation = system.calculate_reputation("peer-toxic")

# Output:
# score: 0.65 (subió de 0.25!)
# patterns: ['improving']
# redemption_progress: 75%
# decision: "Conectar - En proceso de mejora exitosa"
```

**¡Segunda oportunidad funcionó!** 🎉

## Implementación

### Python (Server-side / Testing)

```python
from reputation_system import ReputationSystem

# Crear sistema
system = ReputationSystem(peer_id="my-peer")

# Registrar interacciones
system.record_interaction("peer-bob", "tensor_exchange", success=True)

# Calcular reputación
reputation = system.calculate_reputation("peer-bob")

# Decidir si conectar
should_connect, reason = system.should_connect_to_peer("peer-bob")
```

### Rust (WASM Client)

```rust
// TODO: Port to Rust for WASM
use aurora_wasm::reputation::ReputationSystem;

let mut system = ReputationSystem::new("my-peer-id");

// Record interaction
system.record_interaction(
    "peer-bob",
    InteractionType::TensorExchange,
    true, // success
    None  // metadata
);

// Calculate reputation
let reputation = system.calculate_reputation("peer-bob");

// Decide
if system.should_connect("peer-bob") {
    // Connect...
}
```

### JavaScript (Browser)

```javascript
import { ReputationSystem } from './reputation.js';

const system = new ReputationSystem('my-peer-id');

// Record interaction
system.recordInteraction('peer-bob', 'tensor_exchange', true);

// Calculate
const reputation = system.calculateReputation('peer-bob');
console.log(`Score: ${reputation.score}`);

// Decide
const [shouldConnect, reason] = system.shouldConnectToPeer('peer-bob');
```

## Métricas y Thresholds

| Métrica | Valor | Significado |
|---------|-------|-------------|
| `EXCELLENT_THRESHOLD` | 0.8 | Score para peers confiables |
| `WARNING_THRESHOLD` | 0.5 | Score que genera precaución |
| `TOXIC_THRESHOLD` | 0.3 | Score para peers problemáticos |
| `MIN_INTERACTIONS` | 10 | Mínimo para score confiable |
| `PATTERN_WINDOW` | 20 | Ventana de interacciones |
| `REDEMPTION_PERIOD` | 7 días | Tiempo para mejorar |

## Ventajas vs. Sistemas Tradicionales

| Característica | Sistema Tradicional | Aurora Reputation System |
|----------------|---------------------|--------------------------|
| **Detección** | Ban después de X errores | Detecta patrones ML |
| **Oportunidad** | Ban permanente | Path de redención |
| **Transparencia** | Opaco | Explica decisiones |
| **Descentralización** | Lista negra centralizada | Cálculo client-side |
| **Aprendizaje** | Reglas fijas | Aprende de comunidad |
| **Filosofía** | Castigo | Rehabilitación |

## Casos de Uso Reales

### 1. Spam Bot

**Detección:**
- Intervalos muy regulares (bot-like)
- 100% fallos en tensor exchange
- Múltiples reportes de spam

**Acción:**
- Score: 0.15
- NO conectar
- Redemption path: "Variar comportamiento, conseguir 30 interacciones exitosas"

### 2. Peer Sobrecargado

**Detección:**
- 60% de fallos recientes
- Pero historial bueno anterior
- Patrón: degrading (empeorando)

**Acción:**
- Score: 0.55
- Conectar con precaución
- Warning: "Peer puede estar sobrecargado"
- NO ban (problema temporal posible)

### 3. Peer Nuevo Legítimo

**Detección:**
- Solo 3 interacciones
- 100% éxito
- Sin reportes

**Acción:**
- Score: 0.7
- Conectar
- Nota: "Dar oportunidad, monitorear"

### 4. Peer Mejorando

**Detección:**
- Historial malo (score 0.3)
- Últimas 10 interacciones: 90% éxito
- Patrón: improving

**Acción:**
- Score: 0.6 (subiendo)
- Conectar
- Mensaje: "Peer en mejora, apoyar recuperación"

## Roadmap

### Phase 1: Python Implementation ✅
- [x] Core reputation system
- [x] Pattern detection
- [x] Redemption paths
- [x] Unit tests

### Phase 2: Integration (📋 Current)
- [ ] Port to Rust for WASM
- [ ] Integrate with Discovery Client
- [ ] Add to Aurora Agent
- [ ] Browser demo

### Phase 3: Advanced ML (🔮 Future)
- [ ] TensorFlow.js integration
- [ ] Collaborative filtering
- [ ] Anomaly detection
- [ ] Federated learning

### Phase 4: Governance (🔮 Future)
- [ ] Community voting on bans
- [ ] Appeal mechanism
- [ ] Reputation staking
- [ ] DAO integration

## Testing

```bash
# Run Python tests
cd Infrastructure/P2P
python reputation_system.py

# Expected output:
# ✅ Score calculation
# ✅ Pattern detection
# ✅ Redemption paths
# ✅ Decision making
```

## Security Considerations

1. **Sybil Attacks:** Múltiples identidades falsas
   - **Mitigation:** Require stake/proof-of-work para peer_id
   
2. **Reputation Washing:** Crear nuevo peer_id
   - **Mitigation:** New peers start at 0.7 (not 1.0)
   
3. **Collusion:** Peers que se votan positivo mutuamente
   - **Mitigation:** ML detecta patrones anormales
   
4. **False Reports:** Reportes maliciosos
   - **Mitigation:** Verificar reportero tiene buena reputación

## Pepino's Principles in Code

```python
# Principle 1: Benefit of the doubt
if interactions < 3:
    return ReputationScore(score=0.7, ...)  # Start positive

# Principle 2: Patterns over events
if consecutive_failures >= 5:  # Not just 1 failure
    patterns['alert'] = True

# Principle 3: Second chance
if score < WARNING_THRESHOLD:
    reputation.redemption_path = generate_path(...)

# Principle 4: Transparency
def get_reputation_explanation(peer_id):
    return f"Score: {score}\nPatterns: {patterns}\nReason: {reason}"
```

## Conclusion

El **Aurora Reputation System** no es solo un filtro de nodos malos. Es un **sistema ético** que:

✅ Detecta comportamientos tóxicos **inteligentemente**  
✅ Da **segundas oportunidades** a quien mejora  
✅ Es **transparente** en sus decisiones  
✅ **Aprende** de la comunidad  
✅ Refleja los valores de **Pepino** y Aurora

> *"La tecnología debe conectar, no dividir. Un sistema de reputación debe buscar redención, no solo castigo."*  
> — Aurora Alliance

---

**Next Steps:**
1. Port to Rust/WASM
2. Integrate with Discovery Client
3. Add to Aurora Agent
4. Deploy and test in production

**Status:** 🟢 Python implementation complete, ready for Rust port

