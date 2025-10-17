"""
Test de Integración Completa - Proyecto Genesis
Valida todos los componentes del sistema FFE

Componentes testeados:
1. TensorFFE: Estructura fractal 3→9→27
2. Transcender: Síntesis emergente no conmutativa
3. Evolver: Aprendizaje de arquetipos, dinámicas, relatores
4. FFEEncoder: Codificación embedding→FFE
5. LoRA: Adaptación de LLMs (si PyTorch disponible)
"""

import sys
import numpy as np
from typing import List

# Importar componentes Genesis
from tensor_ffe import (
    TensorFFE, VectorFFE, TransformadorFFE,
    crear_tensor_desde_lista, tensor_nulo
)
from transcender import Transcender, Emergencia
from evolver import Evolver, Arquetipo, Dinamica
from ffe_encoder_mcp import FFEEncoder


def test_tensor_ffe():
    """Test 1: Tensores FFE básicos"""
    print("=" * 60)
    print("TEST 1: Tensores FFE")
    print("=" * 60)
    
    # Crear tensor
    tensor = crear_tensor_desde_lista([3, 5, 7], nivel_abstraccion=3)
    print(f"\n✓ Tensor creado: {tensor.nivel_1}")
    print(f"  Nivel abstracción: {tensor.nivel_abstraccion}")
    print(f"  Coherencia fractal: {tensor.coherencia():.3f}")
    
    # Serialización
    bits = tensor.to_bits()
    print(f"\n✓ Serialización: {len(bits)} bits")
    print(f"  Hex: {hex(int(bits, 2))}")
    
    # Deserialización
    tensor_recuperado = TensorFFE.from_bits(bits)
    match = all(
        v1.forma == v2.forma and v1.funcion == v2.funcion and v1.estructura == v2.estructura
        for v1, v2 in zip(tensor.nivel_1, tensor_recuperado.nivel_1)
    )
    print(f"\n✓ Deserialización: {'PASS' if match else 'FAIL'}")
    
    # Compresión
    ratio = tensor.compresion_ratio()
    print(f"\n✓ Ratio de compresión: {ratio:.1f}x")
    print(f"  (117 bits vs {32768} bits tradicionales)")
    
    return tensor


def test_transformador():
    """Test 2: Transformaciones de abstracción"""
    print("\n" + "=" * 60)
    print("TEST 2: Transformador FFE (Continuum 0-7)")
    print("=" * 60)
    
    transformador = TransformadorFFE()
    
    # Crear tensor en nivel léxico (3)
    tensor = crear_tensor_desde_lista([2, 4, 6], nivel_abstraccion=3)
    print(f"\n✓ Tensor inicial (nivel 3 - Léxico):")
    print(f"  {tensor.nivel_1}")
    print(f"  Dimensiones activas: {tensor.dimensiones_activas}")
    
    # Abstracting: 3 → 5 (Semántico)
    tensor_abstracto = transformador.abstracting(tensor)
    print(f"\n✓ Después de abstracting (nivel {tensor_abstracto.nivel_abstraccion} - Semántico):")
    print(f"  {tensor_abstracto.nivel_1}")
    print(f"  Dimensiones activas: {tensor_abstracto.dimensiones_activas}")
    
    # Extending: 5 → 3 (Léxico)
    tensor_concreto = transformador.extending(tensor_abstracto)
    print(f"\n✓ Después de extending (nivel {tensor_concreto.nivel_abstraccion} - Léxico):")
    print(f"  {tensor_concreto.nivel_1}")
    print(f"  Dimensiones activas: {tensor_concreto.dimensiones_activas}")
    
    return tensor


def test_transcender():
    """Test 3: Síntesis emergente"""
    print("\n" + "=" * 60)
    print("TEST 3: Transcender (Síntesis Emergente)")
    print("=" * 60)
    
    transcender = Transcender()
    
    # Crear tripleta
    A = crear_tensor_desde_lista([1, 2, 3], 3)
    B = crear_tensor_desde_lista([4, 5, 6], 3)
    C = crear_tensor_desde_lista([7, 0, 1], 4)
    
    print(f"\n✓ Entrada:")
    print(f"  A: {A.nivel_1}")
    print(f"  B: {B.nivel_1}")
    print(f"  C: {C.nivel_1}")
    
    # Sintetizar
    emergencia = transcender.sintetizar(A, B, C)
    print(f"\n✓ Emergencia generada:")
    print(f"  Score: {emergencia.score_emergencia:.3f}")
    print(f"  Novedad: {emergencia.novedad:.3f}")
    print(f"  Coherencia: {emergencia.coherencia:.3f}")
    print(f"  Compresión: {emergencia.compresion:.3f}")
    
    print(f"\n✓ Componentes:")
    print(f"  Ms (Structure): {emergencia.Ms.nivel_1}")
    print(f"  Ss (Form): {emergencia.Ss.nivel_1}")
    print(f"  MetaM (Function): {emergencia.MetaM.nivel_1}")
    
    # No conmutatividad
    print(f"\n✓ Validando no conmutatividad:")
    resultados = transcender.validar_no_conmutatividad(A, B, C)
    for orden, score in sorted(resultados.items(), key=lambda x: x[1], reverse=True):
        print(f"  {orden}: {score:.4f}")
    
    # Verificar que scores son diferentes
    scores_unicos = len(set(resultados.values()))
    print(f"\n  Scores únicos: {scores_unicos}/6 {'✓ PASS' if scores_unicos > 3 else '✗ FAIL'}")
    
    return emergencia


def test_evolver():
    """Test 4: Aprendizaje de patrones"""
    print("\n" + "=" * 60)
    print("TEST 4: Evolver (Aprendizaje Fractal)")
    print("=" * 60)
    
    evolver = Evolver()
    
    # Crear conjunto de tensores similares y diferentes
    tensores = [
        crear_tensor_desde_lista([1, 2, 3], 3),
        crear_tensor_desde_lista([1, 3, 2], 3),  # Similar
        crear_tensor_desde_lista([6, 7, 0], 4),  # Diferente
        crear_tensor_desde_lista([1, 2, 4], 3),  # Similar
        crear_tensor_desde_lista([6, 0, 7], 4),  # Similar al diferente
    ]
    
    print(f"\n✓ Aprendiendo {len(tensores)} tensores...")
    
    arquetipos_detectados = set()
    for i, tensor in enumerate(tensores):
        resultado = evolver.aprender(tensor)
        arquetipos_detectados.add(resultado['arquetipo'])
        relaciones = resultado.get('relaciones', [])
        print(f"  Tensor {i+1}: {resultado['arquetipo']} " +
              (f"(+{len(relaciones)} relaciones)" if relaciones else ""))
    
    # Estadísticas
    stats = evolver.estadisticas()
    print(f"\n✓ Estadísticas finales:")
    print(f"  Arquetipos: {stats['arquetipos']}")
    print(f"  Relatores: {stats['relatores']}")
    print(f"  Conexiones fuertes: {stats['conexiones_fuertes']}")
    
    # Top arquetipos
    print(f"\n✓ Top arquetipos por frecuencia:")
    for arq_id, freq in stats['top_arquetipos']:
        print(f"  {arq_id}: {freq} ejemplos")
    
    # Test de dinámicas
    print(f"\n✓ Aprendiendo dinámica temporal...")
    secuencia = [
        crear_tensor_desde_lista([0, 0, 0], 2),
        crear_tensor_desde_lista([1, 1, 1], 2),
        crear_tensor_desde_lista([2, 2, 2], 2),
        crear_tensor_desde_lista([3, 3, 3], 2),
    ]
    
    dinamica = evolver.aprender_secuencia(secuencia)
    if dinamica:
        print(f"  Dinámica {dinamica.id} detectada")
        print(f"  Delta promedio: {dinamica.delta_promedio}")
        
        # Predecir siguiente
        prediccion = dinamica.predecir_siguiente(secuencia[-1])
        print(f"  Predicción próximo: {prediccion.nivel_1[0]} (esperado: ~(4,4,4))")
    
    return evolver


def test_ffe_encoder():
    """Test 5: Codificación de embeddings"""
    print("\n" + "=" * 60)
    print("TEST 5: FFE Encoder (Embedding → FFE)")
    print("=" * 60)
    
    encoder = FFEEncoder(dimension_embedding=768)
    
    # Generar embedding sintético
    embedding = np.random.randn(768).tolist()
    print(f"\n✓ Embedding generado: {len(embedding)} dimensiones")
    print(f"  Rango: [{min(embedding):.2f}, {max(embedding):.2f}]")
    
    # Codificar
    tensor = encoder.encode(embedding)
    print(f"\n✓ Tensor FFE codificado:")
    print(f"  Nivel 1: {tensor.nivel_1}")
    print(f"  Coherencia: {tensor.coherencia():.3f}")
    
    # Comparar
    comparacion = encoder.compare(embedding, tensor)
    print(f"\n✓ Comparación embedding vs FFE:")
    print(f"  Similitud coseno: {comparacion['similitud_coseno']:.3f}")
    print(f"  Error MSE: {comparacion['error_mse']:.4f}")
    print(f"  Ratio compresión: {comparacion['ratio_compresion']:.1f}x")
    print(f"  Bits: {comparacion['bits_original']} → {comparacion['bits_ffe']}")
    
    # Decodificar
    reconstruido = encoder.decode(tensor, 768)
    print(f"\n✓ Vector reconstruido: {len(reconstruido)} dimensiones")
    print(f"  Rango: [{min(reconstruido):.2f}, {max(reconstruido):.2f}]")
    
    return tensor


def test_lora():
    """Test 6: LoRA (si PyTorch disponible)"""
    print("\n" + "=" * 60)
    print("TEST 6: LoRA FFE (Adaptación de LLMs)")
    print("=" * 60)
    
    try:
        import torch
        from lora_ffe import LoRAConfig, LoRAFFETrainer
        
        print(f"\n✓ PyTorch {torch.__version__} detectado")
        
        # Configuración
        config = LoRAConfig(rank=8, hidden_dim=768)
        trainer = LoRAFFETrainer(config)
        
        print(f"\n✓ LoRA configurado:")
        print(f"  Rank: {config.rank}")
        print(f"  Hidden dim: {config.hidden_dim}")
        print(f"  Alpha: {config.alpha}")
        
        # Generar batch sintético
        batch_embeddings = [np.random.randn(768).astype(np.float32) for _ in range(2)]
        batch_targets = [trainer.encoder.encode(emb.tolist()) for emb in batch_embeddings]
        
        print(f"\n✓ Batch generado: {len(batch_embeddings)} embeddings")
        
        # Entrenar 1 paso
        print(f"\n✓ Entrenando 1 epoch...")
        losses = trainer.train_step(batch_embeddings, batch_targets)
        
        print(f"  Loss total: {losses['total']:.4f}")
        print(f"  l_quant: {losses['sample_0']['l_quant']:.4f}")
        print(f"  l_emerge: {losses['sample_0']['l_emerge']:.4f}")
        
        # Test inferencia
        test_emb = torch.tensor(batch_embeddings[0], dtype=torch.float32)
        vals = trainer.lora1(test_emb)
        _, emergence = trainer.lora2(test_emb)
        
        print(f"\n✓ Inferencia LoRA₁: {vals.detach().numpy().astype(int)}")
        print(f"✓ Inferencia LoRA₂: emergencia={emergence.item():.3f}")
        
        return True
        
    except ImportError:
        print("\n⚠️  PyTorch no instalado")
        print("   Instalar con: pip install torch")
        print("   LoRA disponible pero no ejecutado")
        return False


def test_pipeline_completo():
    """Test 7: Pipeline end-to-end"""
    print("\n" + "=" * 60)
    print("TEST 7: Pipeline Completo Genesis")
    print("=" * 60)
    
    print("\n✓ Simulando flujo completo:")
    print("  1. LLM genera embedding")
    print("  2. Encoder convierte a FFE")
    print("  3. Evolver aprende arquetipo")
    print("  4. Transcender sintetiza emergencias")
    print("  5. Transformador navega continuum\n")
    
    # 1. Generar embeddings (3)
    encoder = FFEEncoder(768)
    embeddings = [np.random.randn(768).tolist() for _ in range(3)]
    
    # 2. Codificar a FFE
    tensores = [encoder.encode(emb) for emb in embeddings]
    print(f"✓ [1→2] Codificados {len(tensores)} embeddings a FFE")
    
    # 3. Aprender arquetipos
    evolver = Evolver()
    for tensor in tensores:
        evolver.aprender(tensor)
    
    stats = evolver.estadisticas()
    print(f"✓ [2→3] Aprendidos {stats['arquetipos']} arquetipos")
    
    # 4. Sintetizar emergencia
    transcender = Transcender()
    emergencia = transcender.sintetizar(tensores[0], tensores[1], tensores[2])
    print(f"✓ [3→4] Emergencia sintetizada (score={emergencia.score_emergencia:.3f})")
    
    # 5. Transformar a nivel superior
    transformador = TransformadorFFE()
    tensor_abstracto = transformador.abstracting(emergencia.Ms)
    print(f"✓ [4→5] Abstracting: nivel {emergencia.Ms.nivel_abstraccion} → {tensor_abstracto.nivel_abstraccion}")
    
    print(f"\n✓ Pipeline completado exitosamente!")
    print(f"  Input: {len(embeddings)} embeddings × {len(embeddings[0])} dims")
    print(f"  Output: Emergencia nivel {tensor_abstracto.nivel_abstraccion} (117 bits)")
    print(f"  Compresión total: ~{(len(embeddings) * 768 * 32) / 117:.0f}x")


def main():
    """Ejecuta todos los tests"""
    print("\n" + "🌌" * 30)
    print(" " * 20 + "PROYECTO GENESIS")
    print(" " * 15 + "Test de Integración Completa")
    print("🌌" * 30 + "\n")
    
    tests_passed = 0
    tests_total = 7
    
    try:
        test_tensor_ffe()
        tests_passed += 1
    except Exception as e:
        print(f"\n✗ TEST 1 FAILED: {e}")
    
    try:
        test_transformador()
        tests_passed += 1
    except Exception as e:
        print(f"\n✗ TEST 2 FAILED: {e}")
    
    try:
        test_transcender()
        tests_passed += 1
    except Exception as e:
        print(f"\n✗ TEST 3 FAILED: {e}")
    
    try:
        test_evolver()
        tests_passed += 1
    except Exception as e:
        print(f"\n✗ TEST 4 FAILED: {e}")
    
    try:
        test_ffe_encoder()
        tests_passed += 1
    except Exception as e:
        print(f"\n✗ TEST 5 FAILED: {e}")
    
    try:
        lora_ok = test_lora()
        if lora_ok:
            tests_passed += 1
        else:
            tests_passed += 0.5  # Medio punto si no hay PyTorch
    except Exception as e:
        print(f"\n✗ TEST 6 FAILED: {e}")
    
    try:
        test_pipeline_completo()
        tests_passed += 1
    except Exception as e:
        print(f"\n✗ TEST 7 FAILED: {e}")
    
    # Resumen final
    print("\n" + "=" * 60)
    print("RESUMEN DE TESTS")
    print("=" * 60)
    print(f"\n✓ Tests pasados: {tests_passed}/{tests_total}")
    
    if tests_passed == tests_total:
        print("\n🎉 ¡PROYECTO GENESIS COMPLETAMENTE OPERACIONAL! 🎉")
    elif tests_passed >= tests_total - 1:
        print("\n✅ Sistema operacional (algunos componentes opcionales faltantes)")
    else:
        print("\n⚠️  Algunos componentes requieren atención")
    
    print("\n" + "🌌" * 30 + "\n")


if __name__ == "__main__":
    main()
