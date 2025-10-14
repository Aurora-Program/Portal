"""
Test Interactivo Simple de Aurora
==================================

Prueba rápida y visual del sistema Aurora.
"""

from aurora_engine import Aurora
import logging

# Silenciar warnings de logging
logging.getLogger('aurora.armonizador').setLevel(logging.ERROR)
logging.getLogger('aurora.trinity').setLevel(logging.ERROR)

print("="*70)
print("  🌌 PRUEBA SIMPLE DE AURORA ENGINE")
print("="*70)

# 1. Crear Aurora
print("\n📌 Paso 1: Crear instancia Aurora")
aurora = Aurora()
print(f"✅ {aurora}")

# 2. Aprender patrones
print("\n📌 Paso 2: Aprender patrones")
training_data = [
    [1, 0, 1],  # Patrón A
    [0, 1, 0],  # Patrón B  
    [1, 1, 0],  # Patrón C
]
print(f"Datos de entrenamiento:")
for i, pattern in enumerate(training_data):
    print(f"  Patrón {chr(65+i)}: {pattern}")

aurora.learn(training_data, space_id="demo")
print("✅ Aprendizaje completado")

# 3. Consultar con valores completos
print("\n📌 Paso 3: Consultas con valores completos")
queries_complete = [[1, 0, 1], [0, 1, 0]]
for query in queries_complete:
    result = aurora.query(query, space_id="demo")
    print(f"  Query: {query} → Result: {result.nivel_3[0]}")

# 4. Consultar con NULLs (deducción)
print("\n📌 Paso 4: Deducción con NULLs")
queries_incomplete = [
    [1, None, None],      # 2 NULLs
    [None, 1, None],      # 2 NULLs
    [1, 0, None],         # 1 NULL
]
for query in queries_incomplete:
    result = aurora.query(query, space_id="demo")
    nulls = sum(1 for v in query if v is None)
    print(f"  Query ({nulls} NULLs): {query} → Deducido: {result.nivel_3[0]}")

# 5. Guardar KB
print("\n📌 Paso 5: Persistencia")
kb_path = "aurora_test.json"
aurora.save(kb_path)
print(f"✅ KB guardada en: {kb_path}")

# 6. Cargar KB
aurora2 = Aurora(kb_path=kb_path)
test_query = [None, None, 0]
result = aurora2.query(test_query, space_id="demo")
print(f"✅ KB cargada y consultada: {test_query} → {result.nivel_3[0]}")

# 7. Métricas
print("\n📌 Paso 6: Métricas del sistema")
metrics = aurora.metrics()
print(f"  Total operaciones: {metrics.get('total_operations', 0)}")
print(f"  Coherencia promedio: {metrics.get('avg_coherence', 0):.3f}")
print(f"  Operaciones: {metrics.get('operations_by_type', {})}")

print("\n" + "="*70)
print("  ✅ PRUEBA COMPLETADA CON ÉXITO")
print("="*70)

# Cleanup
import os
try:
    os.remove(kb_path)
    print(f"\n🗑️  Archivo temporal {kb_path} eliminado")
except:
    pass
