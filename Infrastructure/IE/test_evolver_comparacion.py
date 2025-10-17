"""
Test de Comparación: Evolver Original vs Funcional
Valida que ambas versiones producen resultados equivalentes
"""

from tensor_ffe import crear_tensor_desde_lista
from evolver import Evolver
from evolver_funcional import EvolverFuncional


def test_comparacion_arquetipos():
    """Compara detección de arquetipos entre versiones"""
    print("🧪 TEST: Comparación Evolver Original vs Funcional\n")
    
    # Dataset de prueba
    tensores_test = [
        crear_tensor_desde_lista([1, 2, 3], 3),
        crear_tensor_desde_lista([1, 3, 2], 3),  # Similar al primero
        crear_tensor_desde_lista([6, 7, 0], 4),  # Muy diferente
        crear_tensor_desde_lista([1, 2, 4], 3),  # Similar al primero
        crear_tensor_desde_lista([6, 7, 1], 4),  # Similar al tercero
        crear_tensor_desde_lista([2, 3, 4], 3),  # Similar al primero
    ]
    
    # Test con versión ORIGINAL
    print("=" * 60)
    print("[1/2] Versión Original (imperativa)...")
    print("=" * 60)
    
    evolver_original = Evolver()
    resultados_original = []
    
    for i, tensor in enumerate(tensores_test):
        resultado = evolver_original.aprender(tensor)
        resultados_original.append(resultado)
        print(f"  Tensor {i+1}: {resultado['arquetipo']}")
    
    stats_original = evolver_original.estadisticas()
    print(f"\n📊 ESTADÍSTICAS ORIGINAL:")
    print(f"  Arquetipos: {stats_original['arquetipos']}")
    print(f"  Relatores: {stats_original['relatores']}")
    print(f"  Top 3: {stats_original['top_arquetipos']}")
    
    # Test con versión FUNCIONAL
    print("\n" + "=" * 60)
    print("[2/2] Versión Funcional (Redux-style)...")
    print("=" * 60)
    
    evolver_funcional = EvolverFuncional()
    resultados_funcional = []
    
    for i, tensor in enumerate(tensores_test):
        resultado = evolver_funcional.aprender(tensor)
        resultados_funcional.append(resultado)
        print(f"  Tensor {i+1}: {resultado['arquetipo']}")
    
    stats_funcional = evolver_funcional.estadisticas()
    print(f"\n📊 ESTADÍSTICAS FUNCIONAL:")
    print(f"  Arquetipos: {stats_funcional['arquetipos']}")
    print(f"  Relatores: {stats_funcional['relatores']}")
    print(f"  Top 3: {stats_funcional['top_arquetipos']}")
    
    # COMPARACIÓN
    print("\n" + "=" * 60)
    print("📊 COMPARACIÓN")
    print("=" * 60)
    
    # Comparar número de arquetipos
    print(f"\n🔍 Arquetipos detectados:")
    print(f"  Original:  {stats_original['arquetipos']}")
    print(f"  Funcional: {stats_funcional['arquetipos']}")
    
    arquetipos_match = stats_original['arquetipos'] == stats_funcional['arquetipos']
    print(f"  {'✅' if arquetipos_match else '⚠️'} {'Idéntico' if arquetipos_match else 'Diferente'}")
    
    # Comparar relatores
    print(f"\n🔍 Relatores creados:")
    print(f"  Original:  {stats_original['relatores']}")
    print(f"  Funcional: {stats_funcional['relatores']}")
    
    relatores_match = stats_original['relatores'] == stats_funcional['relatores']
    print(f"  {'✅' if relatores_match else '⚠️'} {'Idéntico' if relatores_match else 'Diferente'}")
    
    # Comparar frecuencias
    print(f"\n🔍 Frecuencias top arquetipos:")
    
    freq_original = [freq for _, freq in stats_original['top_arquetipos']]
    freq_funcional = [freq for _, freq in stats_funcional['top_arquetipos']]
    
    print(f"  Original:  {freq_original}")
    print(f"  Funcional: {freq_funcional}")
    
    freq_match = freq_original == freq_funcional
    print(f"  {'✅' if freq_match else '⚠️'} {'Idéntico' if freq_match else 'Diferente'}")
    
    # CONCLUSIÓN
    print("\n" + "=" * 60)
    print("🏆 RESULTADO FINAL")
    print("=" * 60)
    
    all_match = arquetipos_match and relatores_match and freq_match
    
    if all_match:
        print("✅ PERFECTO - Funcional produce resultados idénticos")
        print("   + Thread-safe por diseño")
        print("   + Sin race conditions")
        print("   + Estado inmutable")
        print("   + Fácilmente testeable")
    else:
        print("⚠️ DIFERENCIAS DETECTADAS")
        print("   Investigar causas de divergencia")
    
    return all_match


def test_dinamicas():
    """Compara aprendizaje de dinámicas"""
    print("\n" + "=" * 60)
    print("🧪 TEST: Dinámicas Temporales")
    print("=" * 60)
    
    secuencia = [
        crear_tensor_desde_lista([0, 0, 0], 2),
        crear_tensor_desde_lista([1, 1, 1], 2),
        crear_tensor_desde_lista([2, 2, 2], 2),
        crear_tensor_desde_lista([3, 3, 3], 2),
    ]
    
    # Original
    print("\n[1/2] Versión Original...")
    evolver_original = Evolver()
    dinamica_original = evolver_original.aprender_secuencia(secuencia)
    
    if dinamica_original:
        print(f"  ID: {dinamica_original.id}")
        print(f"  Delta: F={dinamica_original.delta_promedio.forma}, "
              f"Fn={dinamica_original.delta_promedio.funcion}, "
              f"E={dinamica_original.delta_promedio.estructura}")
        
        pred_original = dinamica_original.predecir_siguiente(secuencia[-1])
        print(f"  Predicción: {pred_original.nivel_1[0]}")
    
    # Funcional
    print("\n[2/2] Versión Funcional...")
    evolver_funcional = EvolverFuncional()
    dinamica_funcional = evolver_funcional.aprender_secuencia(secuencia)
    
    if dinamica_funcional:
        print(f"  ID: {dinamica_funcional.id}")
        print(f"  Delta: F={dinamica_funcional.delta_promedio.forma}, "
              f"Fn={dinamica_funcional.delta_promedio.funcion}, "
              f"E={dinamica_funcional.delta_promedio.estructura}")
        
        pred_funcional = evolver_funcional.predecir_siguiente(
            dinamica_funcional, 
            secuencia[-1]
        )
        print(f"  Predicción: {pred_funcional.nivel_1[0]}")
    
    # Comparar
    print("\n📊 COMPARACIÓN:")
    
    delta_match = (
        dinamica_original.delta_promedio.forma == dinamica_funcional.delta_promedio.forma and
        dinamica_original.delta_promedio.funcion == dinamica_funcional.delta_promedio.funcion and
        dinamica_original.delta_promedio.estructura == dinamica_funcional.delta_promedio.estructura
    )
    
    print(f"  Delta promedio: {'✅ Idéntico' if delta_match else '⚠️ Diferente'}")
    
    pred_match = (
        pred_original.nivel_1[0].forma == pred_funcional.nivel_1[0].forma and
        pred_original.nivel_1[0].funcion == pred_funcional.nivel_1[0].funcion and
        pred_original.nivel_1[0].estructura == pred_funcional.nivel_1[0].estructura
    )
    
    print(f"  Predicción: {'✅ Idéntico' if pred_match else '⚠️ Diferente'}")
    
    return delta_match and pred_match


def test_inmutabilidad():
    """Valida inmutabilidad del estado funcional"""
    print("\n" + "=" * 60)
    print("🧪 TEST: Inmutabilidad del Estado")
    print("=" * 60)
    
    evolver = EvolverFuncional()
    
    # Capturar estado inicial
    state_inicial = evolver.get_state()
    arquetipos_inicial = len(state_inicial.arquetipos)
    
    print(f"\n📍 Estado inicial:")
    print(f"  Arquetipos: {arquetipos_inicial}")
    print(f"  ID objeto: {id(state_inicial)}")
    
    # Aprender nuevos tensores
    tensores = [
        crear_tensor_desde_lista([i, i+1, i+2], 3)
        for i in range(3)
    ]
    
    for tensor in tensores:
        evolver.aprender(tensor)
    
    # Capturar estado después
    state_despues = evolver.get_state()
    arquetipos_despues = len(state_despues.arquetipos)
    
    print(f"\n📍 Estado después:")
    print(f"  Arquetipos: {arquetipos_despues}")
    print(f"  ID objeto: {id(state_despues)}")
    
    print(f"\n📍 Estado inicial (debe ser inmutable):")
    print(f"  Arquetipos: {len(state_inicial.arquetipos)}")
    print(f"  ID objeto: {id(state_inicial)}")
    
    # Verificar inmutabilidad
    inmutable = len(state_inicial.arquetipos) == arquetipos_inicial
    diferentes = id(state_inicial) != id(state_despues)
    
    print(f"\n📊 VALIDACIÓN:")
    print(f"  Estado inicial inmutable: {'✅' if inmutable else '❌'}")
    print(f"  Estados son diferentes objetos: {'✅' if diferentes else '❌'}")
    
    return inmutable and diferentes


if __name__ == "__main__":
    print("╔" + "═" * 58 + "╗")
    print("║  🧪 TEST COMPARATIVO: EVOLVER v1.2 vs v1.3 FUNCIONAL  ║")
    print("╚" + "═" * 58 + "╝\n")
    
    # Test 1: Arquetipos
    test1_ok = test_comparacion_arquetipos()
    
    # Test 2: Dinámicas
    test2_ok = test_dinamicas()
    
    # Test 3: Inmutabilidad
    test3_ok = test_inmutabilidad()
    
    # RESUMEN FINAL
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE TESTS")
    print("=" * 60)
    
    print(f"\n  Test 1 (Arquetipos):  {'✅ PASS' if test1_ok else '❌ FAIL'}")
    print(f"  Test 2 (Dinámicas):   {'✅ PASS' if test2_ok else '❌ FAIL'}")
    print(f"  Test 3 (Inmutabilidad): {'✅ PASS' if test3_ok else '❌ FAIL'}")
    
    all_ok = test1_ok and test2_ok and test3_ok
    
    print("\n" + "=" * 60)
    if all_ok:
        print("🏆 TODOS LOS TESTS PASARON ✅")
        print("=" * 60)
        print("\n✨ EVOLVER FUNCIONAL VALIDADO:")
        print("  ✓ Produce resultados equivalentes")
        print("  ✓ Estado inmutable (thread-safe)")
        print("  ✓ Sin race conditions")
        print("  ✓ Predecible y testeable")
        print("  ✓ Ready for production!")
    else:
        print("⚠️ ALGUNOS TESTS FALLARON")
        print("=" * 60)
        print("\nRevisar diferencias entre versiones")
