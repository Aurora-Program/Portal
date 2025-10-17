"""
Ejemplo Completo - Proyecto Genesis
Demostración del flujo completo desde embeddings hasta emergencias

Escenario: Análisis semántico de tres conceptos relacionados
- "inteligencia artificial"
- "redes neuronales"
- "aprendizaje profundo"
"""

import numpy as np
from typing import List

# Importar componentes Genesis
from tensor_ffe import crear_tensor_desde_lista, TransformadorFFE
from transcender import Transcender
from evolver import Evolver
from ffe_encoder_mcp import FFEEncoder


def generar_embedding_simulado(concepto: str, seed: int) -> List[float]:
    """
    Simula un embedding de LLM para un concepto
    En producción: usar modelo real (OpenAI, Mistral, etc.)
    """
    np.random.seed(seed)
    base = np.random.randn(768)
    
    # Añadir "firma" del concepto
    if "inteligencia" in concepto:
        base[0:100] += 2.0  # Dimensiones abstractas
    if "redes" in concepto or "neuronal" in concepto:
        base[100:200] += 1.5  # Dimensiones estructurales
    if "aprendizaje" in concepto or "profundo" in concepto:
        base[200:300] += 1.8  # Dimensiones funcionales
    
    return base.tolist()


def ejemplo_basico():
    """Ejemplo 1: Crear y manipular un tensor FFE básico"""
    print("=" * 70)
    print("EJEMPLO 1: Tensor FFE Básico")
    print("=" * 70)
    
    # Crear tensor desde valores simples
    print("\n1.1 Creación de tensor")
    print("-" * 50)
    tensor = crear_tensor_desde_lista([3, 5, 7], nivel_abstraccion=3)
    
    print(f"✓ Tensor creado en nivel 3 (Léxico):")
    print(f"  Nivel 1 (3 vectores): {tensor.nivel_1}")
    print(f"  Nivel 2 (9 vectores): {tensor.nivel_2[:3]}... (truncado)")
    print(f"  Nivel 3 (27 vectores): {tensor.nivel_3[:3]}... (truncado)")
    print(f"  Coherencia fractal: {tensor.coherencia():.3f}")
    
    # Serialización
    print("\n1.2 Serialización a 117 bits")
    print("-" * 50)
    bits = tensor.to_bits()
    print(f"✓ Binario (117 bits): {bits[:30]}...{bits[-10:]}")
    print(f"✓ Hexadecimal: {hex(int(bits, 2))}")
    print(f"✓ Bytes necesarios: {len(bits) // 8 + 1}")
    
    # Compresión
    print("\n1.3 Ratio de compresión")
    print("-" * 50)
    bits_tradicional = 32768  # Embedding típico
    ratio = tensor.compresion_ratio(bits_tradicional)
    print(f"✓ Embedding tradicional: {bits_tradicional} bits")
    print(f"✓ Tensor FFE: 117 bits")
    print(f"✓ Compresión: {ratio:.1f}x más eficiente")


def ejemplo_continuum():
    """Ejemplo 2: Navegar el continuum de abstracción"""
    print("\n" + "=" * 70)
    print("EJEMPLO 2: Continuum de Abstracción 0-7")
    print("=" * 70)
    
    transformador = TransformadorFFE()
    
    # Crear tensor concreto (nivel 2 - Morfémico)
    print("\n2.1 Tensor inicial (concreto)")
    print("-" * 50)
    tensor = crear_tensor_desde_lista([2, 4, 6], nivel_abstraccion=2)
    print(f"✓ Nivel 2 (Morfémico): {tensor.nivel_1}")
    print(f"  Dimensiones activas: {len(tensor.dimensiones_activas)}")
    print(f"  Ejemplo dims: {list(tensor.dimensiones_activas)[:3] if tensor.dimensiones_activas else 'ninguna'}")
    
    # Abstracting: subir 3 niveles
    print("\n2.2 Abstracting (subir abstracción)")
    print("-" * 50)
    for i in range(3):
        tensor = transformador.abstracting(tensor)
        nivel_nombre = transformador.NIVELES[tensor.nivel_abstraccion]
        print(f"  Paso {i+1}: Nivel {tensor.nivel_abstraccion} ({nivel_nombre})")
        print(f"    Dims activas: {len(tensor.dimensiones_activas)}")
    
    # Extending: bajar 2 niveles
    print("\n2.3 Extending (bajar a concreto)")
    print("-" * 50)
    for i in range(2):
        tensor = transformador.extending(tensor)
        nivel_nombre = transformador.NIVELES[tensor.nivel_abstraccion]
        print(f"  Paso {i+1}: Nivel {tensor.nivel_abstraccion} ({nivel_nombre})")
        print(f"    Dims activas: {len(tensor.dimensiones_activas)}")
    
    print(f"\n✓ Tensor final en nivel {tensor.nivel_abstraccion}: {tensor.nivel_1}")


def ejemplo_sintesis_emergente():
    """Ejemplo 3: Síntesis emergente de tres conceptos"""
    print("\n" + "=" * 70)
    print("EJEMPLO 3: Síntesis Emergente (Transcender)")
    print("=" * 70)
    
    # Crear tres tensores representando conceptos
    print("\n3.1 Conceptos de entrada")
    print("-" * 50)
    
    A = crear_tensor_desde_lista([1, 3, 5], nivel_abstraccion=4)  # "Redes"
    B = crear_tensor_desde_lista([2, 4, 6], nivel_abstraccion=4)  # "Aprendizaje"
    C = crear_tensor_desde_lista([3, 5, 7], nivel_abstraccion=5)  # "Inteligencia"
    
    print(f"A (Redes):        {A.nivel_1}")
    print(f"B (Aprendizaje):  {B.nivel_1}")
    print(f"C (Inteligencia): {C.nivel_1}")
    
    # Sintetizar
    print("\n3.2 Síntesis emergente")
    print("-" * 50)
    transcender = Transcender()
    emergencia = transcender.sintetizar(A, B, C)
    
    print(f"✓ Emergencia generada:")
    print(f"  Score total: {emergencia.score_emergencia:.3f}")
    print(f"  └─ Novedad:    {emergencia.novedad:.3f} (40% peso)")
    print(f"  └─ Coherencia: {emergencia.coherencia:.3f} (30% peso)")
    print(f"  └─ Compresión: {emergencia.compresion:.3f} (30% peso)")
    
    print(f"\n✓ Componentes emergentes:")
    print(f"  Ms (Structure):  {emergencia.Ms.nivel_1}")
    print(f"  Ss (Form):       {emergencia.Ss.nivel_1}")
    print(f"  MetaM (Function): {emergencia.MetaM.nivel_1}")
    
    # Demostrar no conmutatividad
    print("\n3.3 No conmutatividad (orden importa)")
    print("-" * 50)
    
    emergencia_BAC = transcender.sintetizar(B, A, C)
    emergencia_CBA = transcender.sintetizar(C, B, A)
    
    print(f"  ABC: score={emergencia.score_emergencia:.4f}")
    print(f"  BAC: score={emergencia_BAC.score_emergencia:.4f}")
    print(f"  CBA: score={emergencia_CBA.score_emergencia:.4f}")
    print(f"  ✓ Diferentes órdenes → Diferentes emergencias")


def ejemplo_aprendizaje():
    """Ejemplo 4: Aprendizaje de arquetipos y patrones"""
    print("\n" + "=" * 70)
    print("EJEMPLO 4: Aprendizaje de Arquetipos (Evolver)")
    print("=" * 70)
    
    evolver = Evolver()
    
    # Dataset: conceptos de IA
    print("\n4.1 Dataset de conceptos")
    print("-" * 50)
    
    conceptos = [
        ("Deep Learning", [5, 6, 7]),
        ("Neural Networks", [5, 6, 6]),
        ("Machine Learning", [4, 5, 6]),
        ("AI Safety", [7, 2, 3]),
        ("Ethics AI", [7, 2, 4]),
        ("Transformers", [5, 7, 6]),
    ]
    
    print(f"✓ {len(conceptos)} conceptos a analizar:")
    for nombre, _ in conceptos:
        print(f"  - {nombre}")
    
    # Aprender arquetipos
    print("\n4.2 Detección de arquetipos")
    print("-" * 50)
    
    arquetipos_por_concepto = {}
    for nombre, valores in conceptos:
        tensor = crear_tensor_desde_lista(valores, nivel_abstraccion=4)
        resultado = evolver.aprender(tensor)
        arquetipos_por_concepto[nombre] = resultado['arquetipo']
        
        relaciones = len(resultado.get('relaciones', []))
        print(f"  {nombre:20} → {resultado['arquetipo']} " + 
              (f"(+{relaciones} relaciones)" if relaciones > 0 else ""))
    
    # Estadísticas
    print("\n4.3 Estadísticas de aprendizaje")
    print("-" * 50)
    
    stats = evolver.estadisticas()
    print(f"✓ Arquetipos detectados: {stats['arquetipos']}")
    print(f"✓ Relatores creados: {stats['relatores']}")
    print(f"✓ Conexiones fuertes (>0.7): {stats['conexiones_fuertes']}")
    
    print(f"\n✓ Top arquetipos por frecuencia:")
    for arq_id, freq in stats['top_arquetipos']:
        # Encontrar conceptos con este arquetipo
        ejemplos = [nombre for nombre, aid in arquetipos_por_concepto.items() if aid == arq_id]
        print(f"  {arq_id}: {freq} ejemplos - {', '.join(ejemplos[:2])}")


def ejemplo_dinamicas():
    """Ejemplo 5: Aprendizaje de dinámicas temporales"""
    print("\n" + "=" * 70)
    print("EJEMPLO 5: Dinámicas Temporales")
    print("=" * 70)
    
    evolver = Evolver()
    
    # Secuencia: evolución de un concepto en el tiempo
    print("\n5.1 Secuencia temporal")
    print("-" * 50)
    
    print("✓ Evolución de 'Capacidad de IA' (tiempo t=0 a t=4):")
    
    secuencia = []
    for t in range(5):
        # Simular crecimiento: capacidad aumenta con el tiempo
        valores = [t, t+1, t+2]
        tensor = crear_tensor_desde_lista(valores, nivel_abstraccion=3)
        secuencia.append(tensor)
        print(f"  t={t}: {tensor.nivel_1[0]}")
    
    # Aprender dinámica
    print("\n5.2 Detección de patrón")
    print("-" * 50)
    
    dinamica = evolver.aprender_secuencia(secuencia)
    
    if dinamica:
        print(f"✓ Dinámica {dinamica.id} detectada")
        print(f"  Delta promedio: {dinamica.delta_promedio}")
        print(f"  Periodicidad: {dinamica.periodicidad if dinamica.periodicidad else 'No periódica'}")
        
        # Predicción
        print("\n5.3 Predicción del futuro")
        print("-" * 50)
        
        ultimo = secuencia[-1]
        prediccion = dinamica.predecir_siguiente(ultimo)
        
        print(f"  Último tensor (t=4): {ultimo.nivel_1[0]}")
        print(f"  Predicción (t=5):    {prediccion.nivel_1[0]}")
        print(f"  Esperado:            FFE(5,6,7)")


def ejemplo_embeddings():
    """Ejemplo 6: Codificación de embeddings reales"""
    print("\n" + "=" * 70)
    print("EJEMPLO 6: Embeddings → Tensores FFE")
    print("=" * 70)
    
    encoder = FFEEncoder(dimension_embedding=768)
    
    # Generar embeddings simulados
    print("\n6.1 Generación de embeddings")
    print("-" * 50)
    
    conceptos = {
        "inteligencia artificial": generar_embedding_simulado("inteligencia artificial", 42),
        "redes neuronales": generar_embedding_simulado("redes neuronales", 123),
        "aprendizaje profundo": generar_embedding_simulado("aprendizaje profundo", 456)
    }
    
    for nombre, emb in conceptos.items():
        print(f"✓ '{nombre}':")
        print(f"    {len(emb)} dimensiones, rango [{min(emb):.2f}, {max(emb):.2f}]")
    
    # Codificar
    print("\n6.2 Codificación a FFE")
    print("-" * 50)
    
    tensores = {}
    for nombre, embedding in conceptos.items():
        tensor = encoder.encode(embedding)
        tensores[nombre] = tensor
        
        print(f"✓ '{nombre}':")
        print(f"    Tensor: {tensor.nivel_1}")
        print(f"    Coherencia: {tensor.coherencia():.3f}")
        print(f"    Compresión: {tensor.compresion_ratio():.1f}x")
    
    # Comparación
    print("\n6.3 Calidad de reconstrucción")
    print("-" * 50)
    
    for nombre in list(conceptos.keys())[:2]:  # Primeros 2
        embedding = conceptos[nombre]
        tensor = tensores[nombre]
        
        comparacion = encoder.compare(embedding, tensor)
        
        print(f"✓ '{nombre}':")
        print(f"    Similitud coseno: {comparacion['similitud_coseno']:.3f}")
        print(f"    Error MSE: {comparacion['error_mse']:.4f}")
        print(f"    {comparacion['bits_original']} bits → {comparacion['bits_ffe']} bits")


def ejemplo_pipeline_completo():
    """Ejemplo 7: Pipeline end-to-end completo"""
    print("\n" + "=" * 70)
    print("EJEMPLO 7: Pipeline Completo Genesis")
    print("=" * 70)
    
    print("\n✓ Flujo completo:")
    print("  LLM → Embedding → FFE → Arquetipos → Emergencia → Continuum")
    
    # Paso 1: Embeddings
    print("\n[1/5] Generación de embeddings")
    print("-" * 50)
    
    conceptos = ["IA", "Redes", "Aprendizaje"]
    embeddings = [generar_embedding_simulado(c, i*100) for i, c in enumerate(conceptos)]
    print(f"✓ {len(embeddings)} embeddings generados (768 dims c/u)")
    
    # Paso 2: Codificación FFE
    print("\n[2/5] Codificación a tensores FFE")
    print("-" * 50)
    
    encoder = FFEEncoder(768)
    tensores = [encoder.encode(emb) for emb in embeddings]
    print(f"✓ {len(tensores)} tensores FFE (117 bits c/u)")
    print(f"  Compresión promedio: {encoder.ratio_compresion_promedio:.1f}x")
    
    # Paso 3: Aprendizaje
    print("\n[3/5] Aprendizaje de arquetipos")
    print("-" * 50)
    
    evolver = Evolver()
    for i, tensor in enumerate(tensores):
        resultado = evolver.aprender(tensor)
        print(f"  Concepto {i+1} → {resultado['arquetipo']}")
    
    stats = evolver.estadisticas()
    print(f"✓ {stats['arquetipos']} arquetipos, {stats['relatores']} relatores")
    
    # Paso 4: Síntesis emergente
    print("\n[4/5] Síntesis emergente")
    print("-" * 50)
    
    transcender = Transcender()
    emergencia = transcender.sintetizar(tensores[0], tensores[1], tensores[2])
    
    print(f"✓ Emergencia sintetizada:")
    print(f"  Score: {emergencia.score_emergencia:.3f}")
    print(f"  Ms: {emergencia.Ms.nivel_1}")
    
    # Paso 5: Navegación continuum
    print("\n[5/5] Abstracting al máximo nivel")
    print("-" * 50)
    
    transformador = TransformadorFFE()
    tensor_max = emergencia.Ms
    
    while tensor_max.nivel_abstraccion < 7:
        tensor_max = transformador.abstracting(tensor_max)
    
    nivel_nombre = transformador.NIVELES[tensor_max.nivel_abstraccion]
    print(f"✓ Nivel máximo alcanzado: {tensor_max.nivel_abstraccion} ({nivel_nombre})")
    print(f"  Tensor abstracto: {tensor_max.nivel_1}")
    
    # Resumen
    print("\n" + "=" * 70)
    print("RESUMEN DEL PIPELINE")
    print("=" * 70)
    
    print(f"\n✓ Input:  3 embeddings × 768 dims × 32 bits = {3*768*32} bits")
    print(f"✓ Output: 1 tensor FFE × 117 bits = 117 bits")
    print(f"✓ Compresión total: {(3*768*32)/117:.1f}x")
    print(f"✓ Nivel final: {tensor_max.nivel_abstraccion} (Teórico)")
    print(f"✓ Arquetipos aprendidos: {stats['arquetipos']}")
    print(f"✓ Emergencia score: {emergencia.score_emergencia:.3f}")


def main():
    """Ejecuta todos los ejemplos"""
    import sys
    auto_mode = '--auto' in sys.argv
    
    print("\n" + "🌌" * 35)
    print(" " * 25 + "PROYECTO GENESIS")
    print(" " * 20 + "Ejemplos Completos de Uso")
    print("🌌" * 35 + "\n")
    
    try:
        ejemplo_basico()
        if not auto_mode:
            input("\nPresiona Enter para continuar al siguiente ejemplo...")
        
        ejemplo_continuum()
        if not auto_mode:
            input("\nPresiona Enter para continuar al siguiente ejemplo...")
        
        ejemplo_sintesis_emergente()
        if not auto_mode:
            input("\nPresiona Enter para continuar al siguiente ejemplo...")
        
        ejemplo_aprendizaje()
        if not auto_mode:
            input("\nPresiona Enter para continuar al siguiente ejemplo...")
        
        ejemplo_dinamicas()
        if not auto_mode:
            input("\nPresiona Enter para continuar al siguiente ejemplo...")
        
        ejemplo_embeddings()
        if not auto_mode:
            input("\nPresiona Enter para continuar al ejemplo final...")
        
        ejemplo_pipeline_completo()
        
        print("\n" + "🌌" * 35)
        print("\n✅ ¡Todos los ejemplos completados!")
        print("\n🎉 Proyecto Genesis operacional - ¡Listo para producción!")
        print("\n" + "🌌" * 35 + "\n")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Ejemplos interrumpidos por el usuario")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
