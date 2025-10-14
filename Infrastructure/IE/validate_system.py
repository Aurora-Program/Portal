"""
Validación Rápida del Sistema Aurora
=====================================

Script de validación que verifica que todos los componentes
estén funcionando correctamente.

Uso:
    python validate_system.py
"""

import sys
from pathlib import Path

def validate_imports():
    """Validar que todos los módulos se importen correctamente."""
    print("✅ PASO 1: Validando imports...")
    
    try:
        from core import (
            FractalTensor, Trigate, FractalKnowledgeBase,
            Transcender, Evolver, Extender, Armonizador
        )
        print("  ✓ core.py importado")
    except Exception as e:
        print(f"  ✗ Error en core.py: {e}")
        return False
    
    try:
        from aurora_engine import (
            Aurora, AuroraCognitiveCycle,
            MetricsCollector, KnowledgeBasePersistence
        )
        print("  ✓ aurora_engine.py importado")
    except Exception as e:
        print(f"  ✗ Error en aurora_engine.py: {e}")
        return False
    
    return True

def validate_trigate():
    """Validar operaciones básicas de Trigate."""
    print("\n✅ PASO 2: Validando Trigate (LUTs)...")
    
    from core import Trigate
    
    tg = Trigate()
    
    # Test inference
    result = tg.infer([1, 0, 1], [0, 1, 0], [1, 1, 1])
    if result is None or len(result) != 3:
        print("  ✗ Trigate.infer falló")
        return False
    print(f"  ✓ Trigate.infer: {result}")
    
    # Test learning
    m_learned = tg.learn([1, 0, 1], [0, 1, 0], [1, 1, 1])
    if m_learned is None or len(m_learned) != 3:
        print("  ✗ Trigate.learn falló")
        return False
    print(f"  ✓ Trigate.learn: {m_learned}")
    
    return True

def validate_fractal_tensor():
    """Validar FractalTensor."""
    print("\n✅ PASO 3: Validando FractalTensor...")
    
    from core import FractalTensor
    
    # Crear tensor
    tensor = FractalTensor(nivel_3=[[1, 0, 1]])
    
    # Validar estructura
    if not hasattr(tensor, 'nivel_1') or not hasattr(tensor, 'nivel_3'):
        print("  ✗ FractalTensor no tiene estructura correcta")
        return False
    
    print(f"  ✓ Tensor creado: {tensor}")
    print(f"    - nivel_1: {tensor.nivel_1}")
    print(f"    - nivel_3: {tensor.nivel_3[:2]}")
    
    return True

def validate_knowledge_base():
    """Validar Knowledge Base."""
    print("\n✅ PASO 4: Validando Knowledge Base...")
    
    from core import FractalKnowledgeBase, FractalTensor
    
    kb = FractalKnowledgeBase()
    
    # Agregar arquetipo
    tensor = FractalTensor(nivel_3=[[1, 0, 1]])
    tensor.Ms = [1, 0, 1]
    tensor.MetaM = [0, 1, 0]
    
    try:
        kb.add_archetype("test_space", "test_archetype", tensor, [1, 0, 1])
        print("  ✓ Arquetipo agregado")
    except Exception as e:
        print(f"  ✗ Error al agregar arquetipo: {e}")
        return False
    
    # Recuperar arquetipo
    retrieved = kb.get_archetype("test_space", "test_archetype")
    if retrieved is None:
        print("  ✗ No se pudo recuperar arquetipo")
        return False
    
    print(f"  ✓ Arquetipo recuperado: {retrieved.Ms}")
    
    return True

def validate_cognitive_cycle():
    """Validar ciclo cognitivo completo."""
    print("\n✅ PASO 5: Validando Ciclo Cognitivo...")
    
    from aurora_engine import Aurora
    
    # Crear Aurora
    aurora = Aurora()
    
    # Learn
    try:
        aurora.learn([[1, 0, 1], [0, 1, 0]], space_id="validation")
        print("  ✓ Learn ejecutado")
    except Exception as e:
        print(f"  ✗ Error en learn: {e}")
        return False
    
    # Query
    try:
        result = aurora.query([1, None, None], space_id="validation")
        print(f"  ✓ Query ejecutado: {result.nivel_3[0]}")
    except Exception as e:
        print(f"  ✗ Error en query: {e}")
        return False
    
    return True

def validate_persistence():
    """Validar persistencia."""
    print("\n✅ PASO 6: Validando Persistencia...")
    
    from aurora_engine import Aurora
    
    test_path = "test_validation_kb.json"
    
    # Guardar
    try:
        aurora = Aurora()
        aurora.learn([[1, 0, 1]], space_id="persist_test")
        aurora.save(test_path)
        print(f"  ✓ KB guardada en {test_path}")
    except Exception as e:
        print(f"  ✗ Error al guardar: {e}")
        return False
    
    # Cargar
    try:
        aurora2 = Aurora(kb_path=test_path)
        result = aurora2.query([1, None, None], space_id="persist_test")
        print(f"  ✓ KB cargada y consultada: {result.nivel_3[0]}")
    except Exception as e:
        print(f"  ✗ Error al cargar: {e}")
        return False
    finally:
        # Cleanup
        Path(test_path).unlink(missing_ok=True)
    
    return True

def validate_metrics():
    """Validar sistema de métricas."""
    print("\n✅ PASO 7: Validando Métricas...")
    
    from aurora_engine import Aurora
    
    aurora = Aurora()
    
    # Generar actividad
    aurora.learn([[1, 0, 1]], space_id="metrics_test")
    aurora.query([1, None, None], space_id="metrics_test")
    
    # Obtener métricas
    metrics = aurora.metrics()
    
    if not metrics or 'total_operations' not in metrics:
        print("  ✗ Métricas no generadas correctamente")
        return False
    
    print(f"  ✓ Métricas generadas:")
    print(f"    - Total operaciones: {metrics.get('total_operations', 0)}")
    print(f"    - Coherencia promedio: {metrics.get('avg_coherence', 0):.3f}")
    
    return True

def main():
    """Ejecutar todas las validaciones."""
    print("="*70)
    print("  🌌 VALIDACIÓN DEL SISTEMA AURORA")
    print("="*70)
    
    validators = [
        ("Imports", validate_imports),
        ("Trigate", validate_trigate),
        ("FractalTensor", validate_fractal_tensor),
        ("Knowledge Base", validate_knowledge_base),
        ("Ciclo Cognitivo", validate_cognitive_cycle),
        ("Persistencia", validate_persistence),
        ("Métricas", validate_metrics),
    ]
    
    results = []
    for name, validator in validators:
        try:
            success = validator()
            results.append((name, success))
        except Exception as e:
            print(f"\n  ✗ Error inesperado en {name}: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))
    
    # Resumen
    print("\n" + "="*70)
    print("  📊 RESUMEN DE VALIDACIÓN")
    print("="*70)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  {status} - {name}")
    
    print("\n" + "="*70)
    print(f"  Resultados: {passed}/{total} pruebas pasadas")
    
    if passed == total:
        print("  🎉 ¡SISTEMA COMPLETAMENTE FUNCIONAL!")
    else:
        print("  ⚠️  Algunos componentes necesitan atención")
    
    print("="*70 + "\n")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
