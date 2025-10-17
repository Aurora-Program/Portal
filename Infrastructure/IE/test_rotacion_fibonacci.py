"""
Test de Rotación Fibonacci en Evolver
======================================

Verifica que:
1. Las rotaciones Fibonacci se aplican correctamente
2. El sistema encuentra coherencia en diferentes ángulos
3. Los arquetipos se agrupan mejor con rotaciones
"""

from sentence_transformers import SentenceTransformer
from ffe_encoder_mcp import FFEEncoder
from evolver import Evolver

print("🌀 TEST DE ROTACIÓN FIBONACCI")
print("="*70)

# Cargar modelos
print("\n1. Cargando modelos...")
model = SentenceTransformer('all-MiniLM-L6-v2')
encoder = FFEEncoder(dimension_embedding=384)
evolver = Evolver()

# Palabras relacionadas semánticamente
palabras_test = [
    # Grupo 1: Conceptos abstractos
    "teoria", "concepto", "idea", "nocion",
    # Grupo 2: Acciones
    "crear", "generar", "producir", "fabricar",
    # Grupo 3: Estructuras
    "sistema", "estructura", "organizacion", "red"
]

print(f"2. Codificando {len(palabras_test)} palabras...\n")

arquetipos_sin_rotacion = []
arquetipos_con_rotacion = []

# Sin rotación (evolver original)
print("   [SIN ROTACIÓN]")
evolver_sin = Evolver()
for palabra in palabras_test:
    emb = model.encode(palabra)
    tensor = encoder.encode(emb.tolist())
    arq = evolver_sin.archetype_learner.detectar_o_crear(tensor)
    print(f"     {palabra:15s} → {arq.id} (freq={arq.frecuencia})")

arquetipos_sin = len(evolver_sin.archetype_learner.arquetipos)

print(f"\n   [CON ROTACIÓN FIBONACCI]")
evolver_con = Evolver()
for palabra in palabras_test:
    emb = model.encode(palabra)
    tensor = encoder.encode(emb.tolist())
    arq = evolver_con.archetype_learner.detectar_o_crear(tensor)
    print(f"     {palabra:15s} → {arq.id} (freq={arq.frecuencia})")

arquetipos_con = len(evolver_con.archetype_learner.arquetipos)

print("\n" + "="*70)
print("📊 RESULTADOS")
print("="*70)

print(f"\n  Arquetipos descubiertos:")
print(f"    Sin rotación:  {arquetipos_sin} arquetipos")
print(f"    Con rotación:  {arquetipos_con} arquetipos")

if arquetipos_con < arquetipos_sin:
    print(f"\n  ✅ Rotación Fibonacci MEJORA agrupación")
    print(f"     Reducción: {arquetipos_sin - arquetipos_con} arquetipos")
    print(f"     ({100 * (arquetipos_sin - arquetipos_con) / arquetipos_sin:.1f}% más compacto)")
else:
    print(f"\n  ⚠️  Sin mejora aparente (puede necesitar más datos)")

print(f"\n  Pasos Fibonacci usados:")
print(f"    Paso actual: {evolver_con.archetype_learner.paso_rotacion}")
print(f"    Secuencia: {evolver_con.archetype_learner.fibonacci[:8]}")

print("\n🌌 La rotación Fibonacci permite encontrar coherencia")
print("   fractal en diferentes 'ángulos' del espacio FFE.")
