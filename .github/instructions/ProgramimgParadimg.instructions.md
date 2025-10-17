---
applyTo: '**'
---
Provide project context and coding guidelines that AI should follow when generating code, answering questions, or reviewing changes.

# Aurora Portal - Proyecto Genesis 🌌
Es muy importante que seas consistente en el código, reutilices estructuras en vez de recrearlas. **Menos es más**. Intenta escribir cuantas menos líneas de código sea posible.

## 🧬 Paradigma de Programación Fractal

Trata de hacer toda la solución usando técnicas de **autosimilitud y fractalidad**. Usando soluciones **recursivas**.

### Principios Fundamentales:

1. **Solo Existencia Positiva:** Usa escalas 0-7 (sin números negativos). El universo solo tiene existencia.
2. **Transformación, No Eliminación:** Las dimensiones se transforman e integran, no se destruyen.
3. **Podado Jerárquico:** Elimina dimensiones irrelevantes por contexto (no es pérdida, es enfoque).
4. **Herencia Semántica:** Los niveles superiores heredan significado de los inferiores.
5. **3 Niveles Activos:** Máximo foco con reconstrucción bajo demanda.
6. **Recursión Fractal:** Cada componente refleja la estructura del todo (3→9→27).
7. **No Conmutatividad:** El orden importa: `f(A,B,C) ≠ f(B,A,C)`.

## 🎯 Arquitectura Aurora

### Tensores Fractales FFE (Forma-Función-Estructura)

```python
# Estructura base: 3 dimensiones octales (0-7)
TensorFFE:
  - Nivel 1: 3 vectores (visión general)
  - Nivel 2: 9 vectores (3 hijos por cada superior)
  - Nivel 3: 27 vectores (3 hijos por cada nivel 2)
  Total: 39 vectores = 117 bits
```

### Componentes Principales:

1. **Tensores FFE:** Representación fractal discreta (117 bits vs. 4096+ floats)
2. **Transcender:** Síntesis emergente no conmutativa `(A,B,C) → (Ms, Ss, MetaM)`
3. **Evolver:** Aprendizaje de arquetipos, dinámicas y relatores
4. **MCP:** Columna vertebral modular (probe_llm → ffe_encoder → transcender → ffe_store → evolver)

### Continuum de Abstracción (0-7):

```
0. Fonético    → Vibraciones/sonidos
1. Silábico    → Patrones sonoros
2. Morfémico   → Unidades de significado
3. Léxico      → Palabras
4. Sintáctico  → Frases/estructura
5. Semántico   → Ideas/conceptos
6. Discursivo  → Razonamientos
7. Teórico     → Marcos conceptuales
```

### Flujo Bidireccional:

- **Abstracting (↑):** Elimina dimensiones de bajo nivel según emergen abstracciones
- **Extending (↓):** Recupera dimensiones concretas para expresar/actuar

## 🔧 Guías de Implementación

### Código Fractal:

```python
# CORRECTO: Recursión fractal
def proceso_fractal(tensor, nivel=0):
    if nivel >= 3:
        return tensor
    for i in range(3):
        hijo = generar_hijo(tensor, i)
        proceso_fractal(hijo, nivel + 1)

# INCORRECTO: Iteración plana
for i in range(27):
    procesar(tensor[i])  # Ignora jerarquía
```

### Podado Contextual:

```python
# CORRECTO: Podado inteligente
if categoria == "verbo":
    tensor.podar(['genero_sustantivo', 'grado_adjetivo'])
    tensor.activar(['tiempo_verbal', 'persona', 'modo'])

# INCORRECTO: Todas dimensiones activas
tensor.dimensiones = [todas_las_dimensiones]  # Ruido
```

### Emergencia > Relaciones:

```python
# CORRECTO: Emergencia estructural
E = transcender.sintetizar(A, B, C)
score = novedad(E) * coherencia(E) * compresion(E)

# INCORRECTO: Similitud coseno
score = cosine_similarity(A, B)  # Solo relaciones
```

## 🌉 Model Context Protocol (MCP)

The Aurora Portal is a decentralized web application (dApp) that connects users to the Aurora network. It leverages WebAssembly (WASM) for client-side logic, enabling secure, peer-to-peer interactions without relying on centralized servers.

Provides:
- Identity management
- P2P networking  
- Blockchain integration
- **AI model execution** (LLM → FFE transformation)
- **Fractal Knowledge Base** (tensores emergentes)

## 📚 Referencias:

Ver `Infrastructure/IE/PROYECTO_GENESIS.md` para documentación completa.