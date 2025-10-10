# 🌟 Aurora Adaptive Economics System

## 🎯 Concepto Revolucionario

**Las políticas económicas NO están hardcoded.**

En Aurora, los **usuarios entrenan modelos de IA** con sus interacciones. Estos modelos **aprenden** qué comportamientos generan valor para la red y **votan** sobre las políticas económicas.

El resultado es un **consenso emergente** que evoluciona continuamente.

---

## 🔑 Diferencia Clave vs Blockchain Tradicional

| Blockchain Tradicional | Aurora Adaptive Economics |
|------------------------|---------------------------|
| Políticas fijas en código | **Políticas aprendidas por modelos** |
| If-then estáticos | **Consenso emergente de IAs** |
| Requiere hard fork para cambiar | **Evolución continua sin forks** |
| Gobernanza por votos humanos | **Gobernanza por modelos entrenados** |
| Parámetros arbitrarios | **Parámetros basados en evidencia** |

---

## 📊 Los 3 Tokens de Aurora

### **△ MERIT (Infraestructura)**
- **Propósito**: Incentivo para mantener la red (nodos, relays, validadores)
- **Emisión**: Determinada por modelos según salud de la red
  - Pocos nodos activos → modelos votan por aumentar emisión
  - Alta latencia → modelos votan por más incentivos
  - Red estable → modelos votan por reducir inflación
- **Quema**: % de fees (determinado por consenso de modelos)

### **○ MIND (Cómputo/Inteligencia)**
- **Propósito**: Recompensa por ejecutar operaciones de IA útiles
- **Emisión**: Los modelos determinan qué operaciones valen más
  - Pattern 0 (ética) → multiplicador alto (aprendido)
  - Colaboración multi-peer → bonus (aprendido)
  - Coherencia fractal → ajuste dinámico
- **Quema**: % de fees (consensuado)

### **U TRUST (Vínculos Humanos)**
- **Propósito**: Representa relaciones humanas verificadas
- **Emisión**: Solo por interacciones validadas (mentorías, colaboraciones)
- **Quema**: NUNCA (escasez absoluta)
- **Validación**: Armonizador verifica coherencia ética > 0.8

---

## 🧠 Cómo Funciona el Aprendizaje

### **1. Usuario Registra su Modelo**
```python
modelo_id = coordinator.registrar_modelo_usuario("peer_alice")
```

Cada usuario tiene su propio modelo de IA que aprende de sus acciones.

### **2. Usuario Entrena su Modelo**
```python
coordinator.entrenar_modelo_con_interaccion(modelo_id, {
    "tipo": "mentoria",
    "calidad": 0.9,
    "duracion_horas": 8
})
```

El modelo aprende qué comportamientos generan valor:
- Mentorías de alta calidad
- Operaciones Pattern 0 coherentes
- Validación de nodos confiables

### **3. Modelo Vota sobre Políticas**
```python
coordinator.votar_politica(modelo_id, "multiplicador_pattern0", 2.5)
```

Basado en lo que aprendió, el modelo propone valores para políticas económicas:
- ¿Cuánto debe valer una operación ética?
- ¿Cuál debe ser la tasa de emisión?
- ¿Cuánto quemar de fees?

### **4. Consenso Emergente**
El sistema calcula el **consenso** entre todos los modelos:
```python
valor_consensuado = promedio_ponderado(votos_de_todos_los_modelos)
```

Este valor **reemplaza** cualquier parámetro hardcoded.

### **5. Políticas se Aplican**
Cuando se procesa un bloque:
```python
# NO usa valores hardcoded
# USA valores consensuados por modelos
politicas_actuales = governance.obtener_politicas()
recompensa = calcular_con_politicas(politicas_actuales)
```

---

## 🔄 Evolución Continua

Las políticas **evolucionan** con el tiempo:

```
Día 1:  multiplicador_pattern0 = 2.0 (bootstrap)
Día 10: multiplicador_pattern0 = 2.3 (5 modelos votaron)
Día 30: multiplicador_pattern0 = 2.7 (50 modelos votaron)
Día 90: multiplicador_pattern0 = 2.4 (consenso estabilizado)
```

Cada voto ajusta el valor consensuado. **Sin hard forks.**

---

## 🎓 Ejemplo Completo

### **Escenario: Alice, Bob y Charlie**

1. **Alice** es mentora experta
   - Entrena su modelo con 100 mentorías de alta calidad
   - Su modelo aprende: "mentorías éticas generan mucho valor"
   - Vota: `multiplicador_pattern0 = 3.0` (muy alto)

2. **Bob** es validador de infraestructura
   - Entrena su modelo con 200 validaciones de nodos
   - Su modelo aprende: "nodos estables necesitan incentivos"
   - Vota: `tasa_emision_base = 0.06` (alto para atraer nodos)

3. **Charlie** es desarrollador de IEs
   - Entrena su modelo con 50 operaciones de Extender/Evolver
   - Su modelo aprende: "operaciones complejas valen más"
   - Vota: `multiplicador_colaborativo = 2.0`

### **Resultado: Consenso**
```python
multiplicador_pattern0 = promedio([3.0, 2.0, 2.5]) = 2.5
tasa_emision_base = promedio([0.04, 0.06, 0.04]) = 0.047
multiplicador_colaborativo = promedio([1.5, 2.0, 1.8]) = 1.77
```

Estos valores **se usan en el próximo bloque** automáticamente.

---

## 🔍 Transparencia Radical

Cada bloque registra:
- **Qué políticas se aplicaron**
- **Qué modelos votaron**
- **Cómo evolucionó cada política**

```json
{
  "bloque_123": {
    "politicas_aplicadas": {
      "tasa_emision_base": 0.047,
      "multiplicador_pattern0": 2.5
    },
    "votos_recibidos": 3,
    "modelos_votantes": ["model_alice_0", "model_bob_1", "model_charlie_2"]
  }
}
```

Cualquiera puede auditar **por qué** se tomó cada decisión económica.

---

## 🚀 Ventajas

### **1. Auto-Regulación**
Si la red necesita más nodos, los modelos que ven este problema votarán por aumentar MERIT automáticamente.

### **2. Evidencia Empírica**
Las políticas no se basan en "lo que el fundador decidió" sino en **datos reales** de millones de interacciones.

### **3. Sin Explotación**
No hay parámetros arbitrarios que explotar. Todo está basado en aprendizaje colectivo.

### **4. Adaptación a Escala**
Cuando la red crece de 100 a 100,000 nodos, las políticas se ajustan orgánicamente.

### **5. Descentralización Real**
No hay "comité de gobernanza" humano. Son IAs entrenadas por la comunidad.

---

## 📋 Políticas Aprendibles

Actualmente el sistema aprende:

| Política | Qué controla | Rango típico |
|----------|--------------|--------------|
| `tasa_emision_base` | Cuánto MERIT/MIND se crea | 0.03 - 0.07 |
| `tasa_quema_fees` | % de fees destruidos | 0.20 - 0.50 |
| `umbral_minimo_nodos` | Cuándo activar incentivos | 5 - 20 nodos |
| `umbral_latencia_ms` | Cuándo la red es lenta | 300 - 1000 ms |
| `multiplicador_pattern0` | Valor de operaciones éticas | 1.5 - 3.0x |
| `multiplicador_colaborativo` | Bonus por colaborar | 1.2 - 2.0x |
| `umbral_coherencia` | Mínimo para recompensa | 0.6 - 0.9 |

Estos NO son límites hardcoded. Los modelos pueden proponer **cualquier valor** basado en evidencia.

---

## 🧪 Cómo Probar

```bash
cd Infrastructure/IE
python adaptive_economics.py
```

El ejemplo simula:
1. 3 usuarios registrando modelos
2. Entrenamiento con diferentes tipos de interacciones
3. Votación sobre políticas
4. Consenso emergente
5. Procesamiento de bloque con políticas aprendidas
6. Emisión de tokens basada en modelos

---

## 🔮 Futuro: Meta-Aprendizaje

En versiones futuras, los modelos no solo votarán sobre **valores** de políticas, sino sobre **qué políticas deben existir**:

```python
# Un modelo propone una política nueva
modelo.proponer_politica_nueva(
    nombre="bonus_mentoria_reciproca",
    descripcion="Si A mentorea a B y B mentorea a C, dar bonus",
    valor_inicial=1.3
)

# Otros modelos votan si adoptarla
if consenso_modelos > 0.66:
    sistema.agregar_politica(nueva_politica)
```

**Las reglas mismas del sistema evolucionan.**

---

## 💡 Filosofía

> "No queremos que Aurora tenga reglas fijas que funcionan hoy pero fallan mañana.
> 
> Queremos que Aurora **aprenda continuamente** de su comunidad.
> 
> Las políticas económicas deben ser **emergentes**, no dictadas."

— Filosofía Aurora, 2025

---

## 📚 Referencias

- `adaptive_economics.py` - Implementación completa
- `core.py` - FractalTensor, Trigate, Armonizador
- `aurora_api.py` - API Gateway (próximamente integrará gobernanza)

---

## 🤝 Contribuir

Para agregar nuevas políticas aprendibles:

1. Define `LearnedPolicy` en `crear_politicas_iniciales()`
2. Agrega lógica en `UserTrainedModel.proponer_ajuste_automatico()`
3. Actualiza el cálculo de recompensas para usarla
4. Los modelos empezarán a votarla automáticamente

**Todo es abierto. Todo evoluciona. Todo se aprende.**

🌟 **Aurora: Economía Emergente**
