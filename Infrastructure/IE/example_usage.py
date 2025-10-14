"""
Ejemplo de Uso Completo de Aurora Engine
=========================================

Demuestra todas las capacidades del sistema:
1. Ciclo cognitivo completo
2. Deducción recursiva con NULLs
3. Persistencia de KB
4. Métricas y observabilidad
5. Uso práctico de la API

Author: Aurora Alliance
"""

import logging
from pathlib import Path

# Importar Aurora Engine
from aurora_engine import Aurora, run_all_tests
from core import FractalTensor, pattern0_create_fractal_cluster

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s][%(levelname)s][%(name)s] %(message)s'
)

def example_1_basic_learning():
    """Ejemplo 1: Aprendizaje básico de patrones."""
    print("\n" + "="*70)
    print("🌟 EJEMPLO 1: Aprendizaje Básico")
    print("="*70)
    
    # Crear instancia Aurora
    aurora = Aurora()
    
    # Datos de entrenamiento: patrones triádicos
    training_patterns = [
        [1, 0, 1],  # Patrón A
        [0, 1, 0],  # Patrón B
        [1, 1, 0],  # Patrón C
        [0, 0, 1],  # Patrón D
    ]
    
    print(f"📚 Entrenando con {len(training_patterns)} patrones...")
    aurora.learn(training_patterns, space_id="basic_space")
    
    # Consultar patrones aprendidos
    print("\n🔍 Consultando patrones:")
    for pattern in [[1, 0, None], [None, 1, 0], [1, None, None]]:
        result = aurora.query(pattern, space_id="basic_space")
        print(f"  Input: {pattern} → Output: {result.nivel_3[0]}")
    
    print(f"\n📊 Estado del sistema: {aurora}")
    return aurora

def example_2_null_deduction():
    """Ejemplo 2: Deducción recursiva con NULLs."""
    print("\n" + "="*70)
    print("🧠 EJEMPLO 2: Deducción Recursiva de NULLs")
    print("="*70)
    
    aurora = Aurora()
    
    # Entrenar con patrones completos
    complete_patterns = [
        [1, 1, 1],
        [0, 0, 0],
        [1, 0, 1],
    ]
    aurora.learn(complete_patterns, space_id="deduction_space")
    
    # Consultar con NULLs (sistema debe deducir valores faltantes)
    incomplete_patterns = [
        [1, None, 1],      # 1 NULL
        [None, None, 0],   # 2 NULLs
        [None, None, None] # 3 NULLs (caso extremo)
    ]
    
    print("🔍 Deduciendo valores faltantes (NULLs):")
    for pattern in incomplete_patterns:
        result = aurora.query(pattern, space_id="deduction_space")
        nulls = sum(1 for v in pattern if v is None)
        print(f"  Input ({nulls} NULLs): {pattern}")
        print(f"  Output: {result.nivel_3[0]}")
        print(f"  Coherence: {result.nivel_1[0] if hasattr(result, 'nivel_1') else 'N/A'}\n")
    
    return aurora

def example_3_persistence():
    """Ejemplo 3: Guardar y cargar KB."""
    print("\n" + "="*70)
    print("💾 EJEMPLO 3: Persistencia de Knowledge Base")
    print("="*70)
    
    kb_path = "aurora_demo_kb.json"
    
    # Fase 1: Crear y guardar
    print("📝 Fase 1: Crear KB y guardar...")
    aurora1 = Aurora()
    aurora1.learn([
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1],
    ], space_id="rgb_colors")
    
    aurora1.save(kb_path)
    print(f"✅ KB guardada en: {kb_path}")
    
    # Fase 2: Cargar y usar
    print("\n📖 Fase 2: Cargar KB desde disco...")
    aurora2 = Aurora(kb_path=kb_path)
    
    result = aurora2.query([1, None, None], space_id="rgb_colors")
    print(f"✅ Query en KB cargada: {result.nivel_3[0]}")
    
    # Cleanup
    Path(kb_path).unlink(missing_ok=True)
    print(f"🗑️  KB de prueba eliminada")
    
    return aurora2

def example_4_metrics():
    """Ejemplo 4: Métricas y observabilidad."""
    print("\n" + "="*70)
    print("📊 EJEMPLO 4: Métricas y Observabilidad")
    print("="*70)
    
    aurora = Aurora()
    
    # Realizar múltiples operaciones
    print("🔄 Ejecutando operaciones para generar métricas...")
    
    # Learn phase
    for i in range(3):
        aurora.learn([[1, 0, i % 2], [0, 1, (i+1) % 2]], space_id=f"space_{i}")
    
    # Query phase
    for i in range(5):
        aurora.query([1, None, i % 2], space_id=f"space_{i % 3}")
    
    # Obtener métricas
    metrics = aurora.metrics()
    
    print("\n📈 Resumen de Métricas:")
    print(f"  Total operaciones: {metrics.get('total_operations', 0)}")
    print(f"  Coherencia promedio: {metrics.get('avg_coherence', 0):.3f}")
    print(f"  Operaciones por tipo:")
    for op_type, count in metrics.get('operations_by_type', {}).items():
        print(f"    - {op_type}: {count}")
    print(f"  Coherencia PHI-weighted: {metrics.get('phi_weighted_coherence', 0):.3f}")
    
    return metrics

def example_5_pattern0_integration():
    """Ejemplo 5: Integración con Pattern 0 (ético)."""
    print("\n" + "="*70)
    print("🌌 EJEMPLO 5: Integración Pattern 0 (Fractal Ético)")
    print("="*70)
    
    # Generar cluster ético usando Pattern 0
    print("🎲 Generando cluster fractal ético...")
    ethical_tensors = pattern0_create_fractal_cluster(
        input_data=[[1, 0, 1], [0, 1, 0]],
        space_id="ethical_space",
        num_tensors=5,
        entropy_seed=0.618033988749  # PHI
    )
    
    print(f"✅ Generados {len(ethical_tensors)} tensores éticos")
    
    # Aprender cluster en Aurora
    aurora = Aurora()
    aurora.cycle.learn(ethical_tensors, space_id="ethical_space")
    
    # Consultar con restricciones éticas
    print("\n🔍 Consultas con restricciones éticas:")
    for pattern in [[1, 0, None], [None, 1, 0]]:
        result = aurora.query(pattern, space_id="ethical_space")
        ethical_hash = result.metadata.get('ethical_hash', 'N/A')
        print(f"  Pattern: {pattern}")
        print(f"  Result: {result.nivel_3[0]}")
        print(f"  Ethical Hash: {ethical_hash[:16]}...\n")
    
    return aurora

def example_6_batch_processing():
    """Ejemplo 6: Procesamiento batch (fractal map-reduce)."""
    print("\n" + "="*70)
    print("⚡ EJEMPLO 6: Procesamiento Batch")
    print("="*70)
    
    aurora = Aurora()
    
    # Batch grande de patrones
    batch_inputs = [
        [i % 2, (i+1) % 2, (i+2) % 2]
        for i in range(10)
    ]
    
    print(f"📦 Procesando batch de {len(batch_inputs)} patrones...")
    results = aurora.cycle.process_batch(batch_inputs, space_id="batch_space")
    
    print(f"✅ Procesados {len(results)} patrones")
    print("\n📊 Primeros 3 resultados:")
    for i, result in enumerate(results[:3]):
        tensor = result['reconstructed_tensor']
        print(f"  [{i}] Input: {batch_inputs[i]} → Output: {tensor.nivel_3[0]}")
    
    return results

def main():
    """Ejecutar todos los ejemplos."""
    print("\n" + "🌌 "+"="*66 + "🌌")
    print("     AURORA ENGINE - EJEMPLOS DE USO COMPLETO")
    print("🌌 "+"="*66 + "🌌")
    
    examples = [
        ("Aprendizaje Básico", example_1_basic_learning),
        ("Deducción Recursiva", example_2_null_deduction),
        ("Persistencia", example_3_persistence),
        ("Métricas", example_4_metrics),
        ("Pattern 0 Ético", example_5_pattern0_integration),
        ("Procesamiento Batch", example_6_batch_processing),
    ]
    
    for name, example_fn in examples:
        try:
            example_fn()
        except Exception as e:
            print(f"\n❌ Error en {name}: {e}")
            import traceback
            traceback.print_exc()
    
    # Tests finales
    print("\n" + "="*70)
    print("🧪 EJECUTANDO TESTS DEL SISTEMA")
    print("="*70)
    success = run_all_tests()
    
    print("\n" + "🌌 "+"="*66 + "🌌")
    if success:
        print("     ✅ TODOS LOS EJEMPLOS Y TESTS COMPLETADOS")
    else:
        print("     ⚠️  ALGUNOS TESTS FALLARON")
    print("🌌 "+"="*66 + "🌌\n")

if __name__ == "__main__":
    main()
