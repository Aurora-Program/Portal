"""
Test para Aurora Recursive Deduction Network

Demuestra cómo la red resuelve NULLs iterativamente mediante
propagación bidireccional entre niveles fractales.
"""

from core import (
    FractalTensor,
    FractalKnowledgeBase,
    Extender,
    RecursiveDeductionNetwork,
    RecursiveNetworkConfig
)


def test_simple_null_deduction():
    """
    Test 1: Deducción simple de un NULL usando arquetipo.
    """
    print("\n" + "="*60)
    print("TEST 1: Deducción Simple de NULL")
    print("="*60)
    
    # Crear KB con arquetipo conocido
    kb = FractalKnowledgeBase()
    
    # Arquetipo: patrón [1, 0, 1]
    archetype = FractalTensor(nivel_3=[[1, 0, 1]])
    archetype.Ms = [1, 0, 1]
    archetype.MetaM = [0, 1, 0]
    kb.add_archetype('test_space', 'pattern_101', archetype, [1, 0, 1])
    
    print("\n📚 KB: Arquetipo 'pattern_101' = [1, 0, 1]")
    
    # Input incompleto: [1, NULL, NULL]
    incomplete = FractalTensor(nivel_3=[[1, None, None]])
    print(f"❓ Input incompleto: {incomplete.nivel_3[0]}")
    
    # Crear red recursiva
    network = RecursiveDeductionNetwork(kb)
    
    # Resolver
    result = network.recursive_solve(incomplete, 'test_space')
    
    print(f"\n✅ Resuelto: {result['resolved_tensor'].nivel_3[0]}")
    print(f"📊 Iteraciones: {result['iterations']}")
    print(f"🎯 Coherencia: {result['final_coherence']:.2%}")
    print(f"✓ Convergió: {result['converged']}")
    
    print("\n📜 Trace:")
    for line in result['trace']:
        print(f"  {line}")
    
    assert result['converged'], "Debería converger"
    assert result['resolved_tensor'].nivel_3[0] == [1, 0, 1], "Debería deducir [1,0,1]"
    
    print("\n✅ Test 1 PASSED")


def test_multiple_nulls():
    """
    Test 2: Multiple NULLs requieren varias iteraciones.
    """
    print("\n" + "="*60)
    print("TEST 2: Múltiples NULLs")
    print("="*60)
    
    kb = FractalKnowledgeBase()
    
    # Varios arquetipos para diferentes patrones
    for pattern, name in [
        ([1, 1, 0], 'pattern_110'),
        ([0, 1, 1], 'pattern_011'),
        ([1, 0, 0], 'pattern_100'),
    ]:
        arch = FractalTensor(nivel_3=[pattern])
        arch.Ms = pattern
        arch.MetaM = [0, 0, 0]
        kb.add_archetype('test_space', name, arch, pattern)
    
    print("\n📚 KB: 3 arquetipos registrados")
    
    # Input con 2 NULLs
    incomplete = FractalTensor(nivel_3=[[1, None, None]])
    print(f"❓ Input: {incomplete.nivel_3[0]} (2 NULLs)")
    
    network = RecursiveDeductionNetwork(kb)
    result = network.recursive_solve(incomplete, 'test_space')
    
    print(f"\n✅ Resuelto: {result['resolved_tensor'].nivel_3[0]}")
    print(f"📊 Iteraciones: {result['iterations']}")
    print(f"🎯 Coherencia: {result['final_coherence']:.2%}")
    
    # Debería haber seleccionado uno de los arquetipos que empiezan con 1
    resolved = result['resolved_tensor'].nivel_3[0]
    assert resolved[0] == 1, "Primer bit debería ser 1 (dado)"
    assert None not in resolved, "No deberían quedar NULLs"
    
    print("\n✅ Test 2 PASSED")


def test_extender_auto_detection():
    """
    Test 3: Extender detecta NULLs automáticamente.
    """
    print("\n" + "="*60)
    print("TEST 3: Auto-detección de NULLs en Extender")
    print("="*60)
    
    kb = FractalKnowledgeBase()
    
    # Arquetipo
    arch = FractalTensor(nivel_3=[[0, 1, 0]])
    arch.Ms = [0, 1, 0]
    arch.MetaM = [1, 0, 1]
    kb.add_archetype('auto_space', 'pattern_010', arch, [0, 1, 0])
    
    # Extender
    extender = Extender(kb)
    
    # Input con NULL
    input_with_null = [0, None, 0]
    print(f"❓ Input: {input_with_null}")
    
    # extend_fractal detecta NULLs automáticamente
    result = extender.extend_fractal(
        input_with_null,
        {'space_id': 'auto_space'}
    )
    
    print(f"\n✅ Método usado: {result['reconstruction_method']}")
    print(f"📊 Coherencia: {result.get('coherence', 'N/A')}")
    print(f"🎯 Resultado: {result['reconstructed_tensor'].nivel_3[0]}")
    
    assert 'recursive_deduction' in result['reconstruction_method']
    assert None not in result['reconstructed_tensor'].nivel_3[0]
    
    print("\n✅ Test 3 PASSED")


def test_no_convergence():
    """
    Test 4: Sistema maneja casos sin convergencia gracefully.
    """
    print("\n" + "="*60)
    print("TEST 4: Caso Sin Convergencia")
    print("="*60)
    
    kb = FractalKnowledgeBase()  # KB vacía
    
    # Input difícil: todos NULLs
    impossible = FractalTensor(nivel_3=[[None, None, None]])
    print(f"❓ Input imposible: {impossible.nivel_3[0]} (todos NULLs, KB vacía)")
    
    # Configuración estricta
    config = RecursiveNetworkConfig()
    config.MAX_ITERATIONS = 3
    config.COHERENCE_THRESHOLD = 1.0  # Exigir 100%
    
    network = RecursiveDeductionNetwork(kb, config)
    result = network.recursive_solve(impossible, 'empty_space')
    
    print(f"\n⚠️ Convergió: {result['converged']}")
    print(f"📊 Iteraciones: {result['iterations']}")
    print(f"🎯 Coherencia final: {result['final_coherence']:.2%}")
    print(f"✓ Mejor aproximación: {result['resolved_tensor'].nivel_3[0]}")
    
    # No debería converger, pero tampoco crashear
    assert not result['converged'], "No debería converger con KB vacía"
    assert result['resolved_tensor'] is not None, "Debe devolver mejor aproximación"
    
    print("\n✅ Test 4 PASSED (manejó caso imposible gracefully)")


def test_coherence_validation():
    """
    Test 5: Validación de coherencia multi-nivel.
    """
    print("\n" + "="*60)
    print("TEST 5: Validación de Coherencia Multi-Nivel")
    print("="*60)
    
    kb = FractalKnowledgeBase()
    network = RecursiveDeductionNetwork(kb)
    
    # Tensor coherente
    coherent = FractalTensor(nivel_3=[[1, 0, 1]])
    coherent._generate_hierarchy()
    score1 = network._coherence_score(coherent)
    
    print(f"✅ Tensor coherente: {coherent.nivel_3[0]}")
    print(f"   Coherencia: {score1:.2%}")
    
    # Tensor con NULLs
    incomplete = FractalTensor(nivel_3=[[1, None, None]])
    incomplete._generate_hierarchy()
    score2 = network._coherence_score(incomplete)
    
    print(f"\n⚠️ Tensor incompleto: {incomplete.nivel_3[0]}")
    print(f"   Coherencia: {score2:.2%}")
    
    assert score1 > score2, "Tensor coherente debe tener mayor score"
    assert score1 == 1.0, "Tensor sin NULLs debe tener score perfecto"
    
    print("\n✅ Test 5 PASSED")


def test_bidirectional_flow():
    """
    Test 6: Flujo bidireccional (forward + backward).
    """
    print("\n" + "="*60)
    print("TEST 6: Flujo Bidireccional")
    print("="*60)
    
    kb = FractalKnowledgeBase()
    
    # Arquetipo con estructura completa
    arch = FractalTensor(nivel_3=[[1, 1, 1]])
    arch.Ms = [1, 1, 1]
    arch.MetaM = [0, 0, 0]
    arch._generate_hierarchy()
    kb.add_archetype('flow_space', 'pattern_111', arch, [1, 1, 1])
    
    network = RecursiveDeductionNetwork(kb)
    
    # Input parcial
    partial = FractalTensor(nivel_3=[[1, 1, None]])
    print(f"❓ Input: {partial.nivel_3[0]}")
    
    # Forward pass
    print("\n→ Forward Pass (propagación hacia arriba)")
    after_forward = network.forward_propagate(partial)
    print(f"   Nivel 3: {after_forward.nivel_3[0]}")
    print(f"   Nivel 1: {after_forward.nivel_1}")
    
    # Backward pass
    print("\n← Backward Pass (deducción desde arriba)")
    after_backward = network.backward_deduce(after_forward, 'flow_space')
    print(f"   Nivel 3: {after_backward.nivel_3[0]}")
    
    assert None not in after_backward.nivel_3[0], "Backward debe resolver NULLs"
    
    print("\n✅ Test 6 PASSED")


if __name__ == '__main__':
    print("\n" + "🕸️"*30)
    print("AURORA RECURSIVE DEDUCTION NETWORK - TEST SUITE")
    print("🕸️"*30)
    
    try:
        test_simple_null_deduction()
        test_multiple_nulls()
        test_extender_auto_detection()
        test_no_convergence()
        test_coherence_validation()
        test_bidirectional_flow()
        
        print("\n" + "="*60)
        print("🎉 TODOS LOS TESTS PASSED")
        print("="*60)
        print("\nLa red recursiva funciona correctamente:")
        print("  ✅ Deduce NULLs desde arquetipos")
        print("  ✅ Converge iterativamente")
        print("  ✅ Valida coherencia multi-nivel")
        print("  ✅ Maneja casos sin convergencia")
        print("  ✅ Flujo bidireccional funcional")
        print("\n🕸️ Aurora Recursive Network: OPERATIONAL")
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        raise
    except Exception as e:
        print(f"\n💥 ERROR: {e}")
        raise
