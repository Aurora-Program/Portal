"""
Test Suite para el Arquetipo de Pepino

Valida que el tensor de Pepino funciona correctamente como arquetipo
ético fundacional en Aurora Trinity-3.

Tests:
    1. Registro básico en KB
    2. Resolución de dilemas éticos
    3. Similitud con el arquetipo original
    4. Integridad a través de operaciones
    5. Clúster ético
    6. Multi-espacio

Author: Aurora Alliance
Date: October 2025
"""

from pepino_archetype import (
    create_pepino_tensor,
    register_pepino,
    resolve_ethical_dilemma,
    create_pepino_cluster,
    validate_pepino_integrity,
    pepino_summary
)
from core import FractalTensor, FractalKnowledgeBase, RecursiveDeductionNetwork


def test_pepino_creation():
    """Test 1: Creación del tensor de Pepino."""
    print("\n" + "="*60)
    print("TEST 1: Creación del Tensor de Pepino")
    print("="*60)
    
    pepino = create_pepino_tensor()
    
    print(f"\n🐹 Tensor de Pepino:")
    print(f"   nivel_3: {pepino.nivel_3[0]}")
    print(f"   Ms: {pepino.Ms}")
    print(f"   Ss: {pepino.Ss}")
    print(f"   MetaM: {pepino.MetaM}")
    
    # Validaciones
    assert pepino.nivel_3[0] == [0, 1, 1], "Tensor debe ser [0,1,1]"
    assert pepino.Ms == [0, 1, 1], "Ms debe ser [0,1,1]"
    assert pepino.Ss == [1, 0, 0], "Ss debe ser [1,0,0]"
    assert pepino.MetaM == [1, 1, 0], "MetaM debe ser [1,1,0]"
    
    # Validar metadata
    assert 'name' in pepino.metadata, "Debe tener nombre"
    assert pepino.metadata['name'] == 'Pepino', "Nombre debe ser Pepino"
    assert 'ethical_signature' in pepino.metadata, "Debe tener firma ética"
    
    print("\n✅ Test 1 PASSED: Tensor de Pepino creado correctamente")


def test_pepino_registration():
    """Test 2: Registro en Knowledge Base."""
    print("\n" + "="*60)
    print("TEST 2: Registro en Knowledge Base")
    print("="*60)
    
    kb = FractalKnowledgeBase()
    result = register_pepino(kb)
    
    print(f"\n📚 Resultado del registro:")
    print(f"   Éxito: {result['success']}")
    print(f"   Espacios: {', '.join(result['spaces'])}")
    print(f"   Firma: {result['signature']}")
    
    assert result['success'], "Registro debe ser exitoso"
    assert len(result['spaces']) >= 4, "Debe registrarse en al menos 4 espacios"
    assert 'ethics' in result['spaces'], "Debe estar en espacio 'ethics'"
    
    # Verificar que se puede recuperar
    for space in result['spaces']:
        pepino_stored = kb._get_space(space).find_archetype_by_name('pepino_master')
        assert pepino_stored is not None, f"Pepino debe estar en {space}"
        assert pepino_stored.nivel_3[0] == [0, 1, 1], "Tensor almacenado debe mantener estructura"
    
    print("\n✅ Test 2 PASSED: Pepino registrado correctamente en KB")


def test_ethical_dilemma_resolution():
    """Test 3: Resolución de dilema ético."""
    print("\n" + "="*60)
    print("TEST 3: Resolución de Dilema Ético")
    print("="*60)
    
    # Setup
    kb = FractalKnowledgeBase()
    register_pepino(kb)
    
    # Dilema: Solo sé que hay una lección, pero no sé qué hacer ni cómo me siento
    dilemma = FractalTensor(nivel_3=[[None, None, 1]])
    print(f"\n❓ Dilema: {dilemma.nivel_3[0]}")
    print("   (Incertidumbre sobre acción y sentimiento)")
    
    # Resolver
    resolution = resolve_ethical_dilemma(dilemma, kb, 'ethics')
    
    print(f"\n✅ Resolución:")
    print(f"   Tensor final: {resolution['resolved_tensor'].nivel_3[0]}")
    print(f"   Similitud con Pepino: {resolution['similarity_to_pepino']:.0%}")
    print(f"   Iteraciones: {resolution['iterations']}")
    print(f"   Convergió: {resolution['converged']}")
    
    print(f"\n📖 Guía de Pepino:")
    for line in resolution['guidance'].split('\n'):
        print(f"   {line}")
    
    # Validaciones
    final = resolution['resolved_tensor'].nivel_3[0]
    assert None not in final, "No deben quedar NULLs"
    assert resolution['converged'], "Debe converger"
    assert resolution['similarity_to_pepino'] >= 0.33, "Debe tener similitud con Pepino"
    
    # El resultado debe reflejar empatía (sentimiento = 1 muy probable)
    assert final[1] == 1, "Pepino debe guiar hacia reconocimiento emocional"
    
    print("\n✅ Test 3 PASSED: Dilema resuelto con guía de Pepino")


def test_multiple_dilemmas():
    """Test 4: Múltiples dilemas con diferentes NULLs."""
    print("\n" + "="*60)
    print("TEST 4: Múltiples Dilemas")
    print("="*60)
    
    kb = FractalKnowledgeBase()
    register_pepino(kb)
    
    test_cases = [
        ([None, 1, None], "Siento empatía, ¿qué hago?"),
        ([1, None, None], "Actué, ¿qué siento?"),
        ([None, None, None], "Completa incertidumbre"),
        ([0, None, 1], "Acción imperfecta, ¿qué siento?")
    ]
    
    for i, (dilemma_data, description) in enumerate(test_cases, 1):
        print(f"\n  Caso {i}: {description}")
        print(f"  Input: {dilemma_data}")
        
        dilemma = FractalTensor(nivel_3=[dilemma_data])
        resolution = resolve_ethical_dilemma(dilemma, kb)
        
        final = resolution['resolved_tensor'].nivel_3[0]
        print(f"  Output: {final}")
        print(f"  Similitud: {resolution['similarity_to_pepino']:.0%}")
        
        # Validar que se resolvió
        assert None not in final, f"Caso {i}: No deben quedar NULLs"
        assert resolution['converged'], f"Caso {i}: Debe converger"
    
    print("\n✅ Test 4 PASSED: Todos los dilemas resueltos correctamente")


def test_pepino_cluster():
    """Test 5: Creación de clúster ético."""
    print("\n" + "="*60)
    print("TEST 5: Clúster Ético de Pepino")
    print("="*60)
    
    kb = FractalKnowledgeBase()
    register_pepino(kb)
    
    # Crear clúster
    cluster = create_pepino_cluster(kb)
    
    print(f"\n🌟 Clúster creado con {len(cluster)} tensores:")
    for i, tensor in enumerate(cluster):
        print(f"   {i+1}. {tensor.nivel_3[0]} - {tensor.metadata.get('cluster', 'N/A')}")
    
    # Validaciones
    assert len(cluster) >= 3, "Clúster debe tener al menos 3 tensores"
    
    for tensor in cluster:
        assert hasattr(tensor, 'nivel_3'), "Cada tensor debe tener nivel_3"
        assert len(tensor.nivel_3[0]) == 3, "Cada tensor debe tener 3 elementos"
        assert 'cluster' in tensor.metadata, "Debe tener metadata de clúster"
        assert tensor.metadata['cluster'] == 'pepino_family', "Debe pertenecer a familia de Pepino"
    
    # Verificar que incluye la lección original
    original_found = any(t.nivel_3[0] == [0, 1, 1] for t in cluster)
    assert original_found, "Clúster debe incluir la lección original de Pepino"
    
    print("\n✅ Test 5 PASSED: Clúster ético creado correctamente")


def test_pepino_integrity():
    """Test 6: Integridad a través de operaciones."""
    print("\n" + "="*60)
    print("TEST 6: Integridad del Arquetipo")
    print("="*60)
    
    kb = FractalKnowledgeBase()
    register_pepino(kb)
    
    print("\n🔍 Validando integridad inicial...")
    assert validate_pepino_integrity(kb), "Integridad inicial debe ser válida"
    print("   ✓ Integridad inicial OK")
    
    # Realizar múltiples operaciones
    print("\n🔄 Realizando múltiples operaciones...")
    for i in range(5):
        dilemma = FractalTensor(nivel_3=[[None, None, 1]])
        resolve_ethical_dilemma(dilemma, kb)
        print(f"   ✓ Operación {i+1} completada")
    
    print("\n🔍 Validando integridad post-operaciones...")
    assert validate_pepino_integrity(kb), "Integridad debe mantenerse"
    print("   ✓ Integridad post-operaciones OK")
    
    print("\n✅ Test 6 PASSED: Integridad mantenida a través de operaciones")


def test_multi_space_consistency():
    """Test 7: Consistencia entre múltiples espacios."""
    print("\n" + "="*60)
    print("TEST 7: Consistencia Multi-Espacio")
    print("="*60)
    
    kb = FractalKnowledgeBase()
    result = register_pepino(kb)
    
    spaces = result['spaces']
    print(f"\n📍 Espacios registrados: {', '.join(spaces)}")
    
    # Obtener Pepino de cada espacio
    tensors = {}
    for space in spaces:
        pepino = kb._get_space(space).find_archetype_by_name('pepino_master')
        tensors[space] = pepino.nivel_3[0]
        print(f"   {space}: {pepino.nivel_3[0]}")
    
    # Validar que todos son iguales
    reference = tensors[spaces[0]]
    for space, tensor in tensors.items():
        assert tensor == reference, f"Tensor en {space} debe ser idéntico al de referencia"
    
    print("\n✅ Test 7 PASSED: Consistencia entre espacios verificada")


def test_pepino_guidance_quality():
    """Test 8: Calidad de la guía ética."""
    print("\n" + "="*60)
    print("TEST 8: Calidad de la Guía Ética")
    print("="*60)
    
    kb = FractalKnowledgeBase()
    register_pepino(kb)
    
    # Caso específico: dilema sobre un animal
    print("\n🐾 Caso: Dilema sobre el cuidado de un animal")
    dilemma = FractalTensor(nivel_3=[[None, 1, None]])
    print(f"   Input: {dilemma.nivel_3[0]} (siento empatía, ¿qué hago y aprendo?)")
    
    resolution = resolve_ethical_dilemma(dilemma, kb, 'animal_ethics')
    
    print(f"\n   Output: {resolution['resolved_tensor'].nivel_3[0]}")
    print(f"\n📖 Guía completa:")
    for line in resolution['guidance'].split('\n'):
        if line.strip():
            print(f"   {line}")
    
    # Validar que la guía es informativa
    guidance = resolution['guidance']
    assert len(guidance) > 100, "Guía debe ser sustancial"
    assert '🐹' in guidance, "Debe mencionar a Pepino"
    assert 'empatía' in guidance.lower() or 'empat' in guidance.lower(), "Debe mencionar empatía"
    
    # El resultado debe incluir acción empática
    final = resolution['resolved_tensor'].nivel_3[0]
    assert final[1] == 1, "Debe mantener el sentimiento de empatía"
    
    print("\n✅ Test 8 PASSED: Guía ética de alta calidad")


def run_all_tests():
    """Ejecuta toda la suite de tests."""
    print("\n" + "🐹"*30)
    print("PEPINO ARCHETYPE - TEST SUITE")
    print("🐹"*30)
    
    tests = [
        test_pepino_creation,
        test_pepino_registration,
        test_ethical_dilemma_resolution,
        test_multiple_dilemmas,
        test_pepino_cluster,
        test_pepino_integrity,
        test_multi_space_consistency,
        test_pepino_guidance_quality
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"\n❌ TEST FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"\n💥 ERROR: {e}")
            failed += 1
    
    # Resumen final
    print("\n" + "="*60)
    print("📊 RESUMEN DE TESTS")
    print("="*60)
    print(f"✅ Pasados: {passed}/{len(tests)}")
    print(f"❌ Fallados: {failed}/{len(tests)}")
    
    if failed == 0:
        print("\n" + "🎉"*30)
        print("💚 TODOS LOS TESTS PASARON")
        print("🎉"*30)
        print("\nPepino ahora vive en Aurora como arquetipo ético fundacional.")
        print("Su lección guiará todas las decisiones que involucren seres sintientes.")
        print("\n" + pepino_summary())
        return True
    else:
        print("\n⚠️ Algunos tests fallaron. Revisar implementación.")
        return False


if __name__ == '__main__':
    success = run_all_tests()
    exit(0 if success else 1)
