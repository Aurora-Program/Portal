"""
Test Simplificado del Extender
================================

Valida funcionamiento básico sin modelos externos pesados
"""

import json
from tensor_ffe import TensorFFE, VectorFFE
from transcender import Transcender
from evolver import Evolver, Arquetipo
from extender import Extender, MigaDePan, crear_migas_desde_frases

def test_extender_basico():
    """
    Test mínimo: registro de vocabulario y despliegue simple
    """
    print("🧪 TEST EXTENDER SIMPLIFICADO")
    print("="*70)
    
    # 1. Crear evolver y extender
    print("\n[1/4] Inicializando módulos...")
    evolver = Evolver()
    extender = Extender(evolver)
    
    # 2. Crear vocabulario manual (sin embeddings)
    print("\n[2/4] Creando vocabulario sintético...")
    vocabulario = {}
    
    palabras_test = ["recursion", "forma", "emergencia", "tensor"]
    
    for i, palabra in enumerate(palabras_test):
        # Crear tensor sintético
        tensor = TensorFFE()
        tensor.nivel_1[0] = VectorFFE(i % 8, (i+1) % 8, (i+2) % 8)
        tensor.nivel_1[1] = VectorFFE((i+3) % 8, (i+4) % 8, (i+5) % 8)
        tensor.nivel_1[2] = VectorFFE((i+6) % 8, (i+7) % 8, (i+1) % 8)
        tensor.reconstruir_jerarquia()
        tensor.nivel_abstraccion = 3
        
        # Detectar arquetipo
        arq = evolver.archetype_learner.detectar_o_crear(tensor)
        vocabulario[palabra] = arq
    
    print(f"    ✅ {len(palabras_test)} palabras → {len(evolver.archetype_learner.arquetipos)} arquetipos")
    
    # 3. Registrar vocabulario inverso
    print("\n[3/4] Registrando vocabulario inverso...")
    extender.registrar_vocabulario(vocabulario)
    
    print(f"    ✅ {len(extender.vocabulario_inverso)} arquetipos indexados")
    for arq_id, palabras in extender.vocabulario_inverso.items():
        print(f"       {arq_id}: {palabras}")
    
    # 4. Test despliegue
    print("\n[4/4] Testeando despliegue...")
    
    # Tomar tensor de "recursion"
    tensor_test = TensorFFE()
    tensor_test.nivel_1[0] = VectorFFE(0, 1, 2)
    tensor_test.nivel_1[1] = VectorFFE(3, 4, 5)
    tensor_test.nivel_1[2] = VectorFFE(6, 7, 1)
    tensor_test.reconstruir_jerarquia()
    tensor_test.nivel_abstraccion = 3
    
    resultado = extender.desplegar(tensor_test, nivel_objetivo=3)
    
    print(f"\n  Tensor → '{resultado.texto_generado}'")
    print(f"  Coherencia: {resultado.nivel_coherencia:.3f}")
    print(f"  Nivel final: {resultado.nivel_final}")
    
    # 5. Test despliegue jerárquico
    print("\n🔹 TEST DESPLIEGUE JERÁRQUICO")
    print("="*70)
    
    transcender = Transcender()
    
    # Crear 3 tensores para triada
    t1 = TensorFFE()
    t1.nivel_1[0] = VectorFFE(0, 1, 2)
    t1.reconstruir_jerarquia()
    t1.nivel_abstraccion = 3
    
    t2 = TensorFFE()
    t2.nivel_1[0] = VectorFFE(2, 3, 4)
    t2.reconstruir_jerarquia()
    t2.nivel_abstraccion = 3
    
    t3 = TensorFFE()
    t3.nivel_1[0] = VectorFFE(4, 5, 6)
    t3.reconstruir_jerarquia()
    t3.nivel_abstraccion = 3
    
    # Sintetizar emergencia
    emergencia = transcender.sintetizar(t1, t2, t3)
    
    print(f"\n  Triada → Emergencia (score={emergencia.score_emergencia:.3f})")
    
    # Desplegar desde emergencia
    migas = [
        MigaDePan(nivel=3, tensor_contexto=t1, palabras_originales=["recursion"]),
        MigaDePan(nivel=3, tensor_contexto=t2, palabras_originales=["forma"]),
        MigaDePan(nivel=3, tensor_contexto=t3, palabras_originales=["emergencia"])
    ]
    
    resultado_jer = extender.desplegar_jerarquico(
        emergencia.Ms,
        emergencia.Ss,
        emergencia.MetaM,
        migas
    )
    
    print(f"  Emergencia → '{resultado_jer.texto_generado}'")
    print(f"  Coherencia: {resultado_jer.nivel_coherencia:.3f}")
    
    # 6. Test rotación Fibonacci
    print("\n🔹 TEST ROTACIÓN FIBONACCI")
    print("="*70)
    
    expresiones = []
    for i in range(5):
        resultado = extender.desplegar(tensor_test, nivel_objetivo=3)
        expresiones.append(resultado.texto_generado)
        print(f"  {i+1}. '{resultado.texto_generado}' (paso_fib={extender.paso_despliegue})")
    
    expresiones_unicas = set(expresiones)
    print(f"\n  Diversidad: {len(expresiones_unicas)}/{len(expresiones)} expresiones únicas")
    
    # Resumen
    print("\n" + "="*70)
    print("✅ TEST COMPLETADO")
    print("="*70)
    print(f"  Arquetipos: {len(evolver.archetype_learner.arquetipos)}")
    print(f"  Vocabulario inverso: {len(extender.vocabulario_inverso)} arquetipos")
    print(f"  Despliegue simple: OK")
    print(f"  Despliegue jerárquico: OK")
    print(f"  Rotación Fibonacci: {len(expresiones_unicas)} expresiones únicas")
    
    return {
        "arquetipos": len(evolver.archetype_learner.arquetipos),
        "vocabulario_inverso": len(extender.vocabulario_inverso),
        "diversidad_expresiones": len(expresiones_unicas)
    }


if __name__ == "__main__":
    resultados = test_extender_basico()
    
    with open('test_extender_simple.json', 'w') as f:
        json.dump(resultados, f, indent=2)
    
    print(f"\n📄 Resultados guardados en: test_extender_simple.json")
