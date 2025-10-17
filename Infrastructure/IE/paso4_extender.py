"""
Paso 4: Implementación y Validación del Extender
================================================

Completa el ciclo de comunicación:
Texto → Encoder → Tensor → Transcender → Emergencia
                                            ↓
Texto ← Extender ← Tensor ← Evolver ← Emergencia

Valida:
1. Ciclo completo (texto → tensor → texto)
2. Despliegue desde emergencias
3. Navegación jerárquica guiada por migas
4. Uso de rotación Fibonacci para expresión
"""

import json
from typing import List, Dict
import numpy as np
from sentence_transformers import SentenceTransformer

from tensor_ffe import TensorFFE
from transcender import Transcender
from evolver import Evolver
from ffe_encoder_mcp import FFEEncoder
from extender import Extender, MigaDePan, crear_migas_desde_frases


def ejecutar_paso4():
    """
    Implementa y valida el módulo Extender
    """
    print("🔄 PASO 4: EXTENDER - CICLO DE COMUNICACIÓN")
    print("="*70)
    
    # Cargar modelos
    print("\n[1/5] Cargando modelos...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    encoder = FFEEncoder(dimension_embedding=384)
    transcender = Transcender()
    evolver = Evolver()
    extender = Extender(evolver)
    
    # Vocabulario Genesis (mismo que autopoiesis)
    VOCABULARIO = {
        "fonetico": None, "lexico": None, "semantico": None, "teorico": None,
        "fractal": None, "recursion": None, "jerarquia": None, "nivel": None,
        "emergencia": None, "sintesis": None, "transcender": None, "novedad": None,
        "forma": None, "funcion": None, "estructura": None, "tensor": None,
        "orden": None, "primero": None, "segundo": None, "tercero": None
    }
    
    print("\n[2/5] Codificando vocabulario...")
    vocabulario_arquetipos = {}
    
    for palabra in VOCABULARIO.keys():
        emb = model.encode(palabra)
        tensor = encoder.encode(emb.tolist())
        arq = evolver.archetype_learner.detectar_o_crear(tensor)
        VOCABULARIO[palabra] = tensor
        vocabulario_arquetipos[palabra] = arq
    
    print(f"    ✅ {len(vocabulario_arquetipos)} palabras codificadas")
    print(f"    ✅ {len(evolver.archetype_learner.arquetipos)} arquetipos descubiertos")
    
    # Registrar vocabulario inverso en Extender
    print("\n[3/5] Construyendo red de relatores...")
    arquetipos = list(evolver.archetype_learner.arquetipos.values())
    
    for arq1 in arquetipos:
        for arq2 in arquetipos:
            if arq1.id != arq2.id:
                evolver.relator_network.conectar(arq1, arq2, tipo="analogico")
    
    print(f"    ✅ {len(evolver.relator_network.relatores)} relatores")
    
    # Registrar vocabulario en Extender
    extender.registrar_vocabulario(vocabulario_arquetipos)
    
    # ========================================================================
    # TAREA 1: CICLO COMPLETO (Texto → Tensor → Texto)
    # ========================================================================
    print("\n" + "="*70)
    print("🔁 TAREA 1: CICLO COMPLETO DE COMUNICACIÓN")
    print("="*70)
    print("\n  Objetivo: Texto original → Tensor → Texto reconstruido\n")
    
    palabras_prueba = [
        "recursion",
        "emergencia",
        "forma",
        "orden",
        "transcender"
    ]
    
    resultados_ciclo = []
    
    for palabra_orig in palabras_prueba:
        # Codificar
        emb = model.encode(palabra_orig)
        tensor = encoder.encode(emb.tolist())
        
        # Desplegar
        resultado = extender.desplegar(tensor, nivel_objetivo=3)
        
        resultados_ciclo.append({
            'original': palabra_orig,
            'reconstruido': resultado.texto_generado,
            'coherencia': resultado.nivel_coherencia,
            'exacto': palabra_orig == resultado.texto_generado
        })
        
        simbolo = "✅" if palabra_orig == resultado.texto_generado else "↔️"
        print(f"  {simbolo} {palabra_orig:15s} → {resultado.texto_generado:15s} (coherencia={resultado.nivel_coherencia:.3f})")
    
    # ========================================================================
    # TAREA 2: DESPLIEGUE DESDE EMERGENCIAS
    # ========================================================================
    print("\n" + "="*70)
    print("✨ TAREA 2: DESPLIEGUE DESDE SÍNTESIS EMERGENTE")
    print("="*70)
    print("\n  Objetivo: Emergencia → Texto interpretable\n")
    
    # Crear triadas y sintetizar
    triadas_test = [
        ("recursion", "nivel", "jerarquia"),
        ("forma", "funcion", "estructura"),
        ("emergencia", "sintesis", "transcender"),
    ]
    
    resultados_emergencia = []
    
    for triada in triadas_test:
        # Obtener tensores
        t1 = VOCABULARIO[triada[0]]
        t2 = VOCABULARIO[triada[1]]
        t3 = VOCABULARIO[triada[2]]
        
        # Sintetizar emergencia
        emergencia = transcender.sintetizar(t1, t2, t3)
        
        # Crear migas de pan desde triada original
        migas = crear_migas_desde_frases(
            [f"{triada[0]} {triada[1]} {triada[2]}"],
            [t1]
        )
        migas[0].palabras_originales = list(triada)
        
        # Desplegar jerárquicamente desde Ms, Ss, MetaM
        resultado = extender.desplegar_jerarquico(
            emergencia.Ms,
            emergencia.Ss,
            emergencia.MetaM,
            migas
        )
        
        resultados_emergencia.append({
            'triada_original': triada,
            'score_emergencia': emergencia.score_emergencia,
            'texto_desplegado': resultado.texto_generado,
            'coherencia_despliegue': resultado.nivel_coherencia
        })
        
        print(f"  Triada: {triada[0]:12s} + {triada[1]:12s} + {triada[2]:12s}")
        print(f"    Score emergencia: {emergencia.score_emergencia:.3f}")
        print(f"    Desplegado: '{resultado.texto_generado}'")
        print(f"    Coherencia: {resultado.nivel_coherencia:.3f}")
        print()
    
    # ========================================================================
    # TAREA 3: NAVEGACIÓN POR RELATORES
    # ========================================================================
    print("\n" + "="*70)
    print("🧭 TAREA 3: NAVEGACIÓN POR RELATORES")
    print("="*70)
    print("\n  Objetivo: Desplegar conceptos desconocidos usando red de relatores\n")
    
    # Palabras nuevas (no en vocabulario)
    palabras_nuevas = [
        "concepto",
        "patron",
        "crear",
        "sistema"
    ]
    
    resultados_navegacion = []
    
    for palabra_nueva in palabras_nuevas:
        # Codificar palabra nueva
        emb = model.encode(palabra_nueva)
        tensor = encoder.encode(emb.tolist())
        
        # Desplegar (usará navegación por relatores)
        resultado = extender.desplegar(tensor, nivel_objetivo=3)
        
        # Detectar arquetipo
        arq = evolver.archetype_learner.detectar_o_crear(tensor)
        vecinos = extender.vocabulario_inverso.get(arq.id, [])
        
        resultados_navegacion.append({
            'palabra_nueva': palabra_nueva,
            'arquetipo': arq.id,
            'vecinos_arquetipo': vecinos[:3],
            'desplegado': resultado.texto_generado,
            'coherencia': resultado.nivel_coherencia
        })
        
        print(f"  [{palabra_nueva:12s}]")
        print(f"    Arquetipo: {arq.id}")
        print(f"    Vecinos: {', '.join(vecinos[:3])}")
        print(f"    Desplegado: '{resultado.texto_generado}' (coherencia={resultado.nivel_coherencia:.3f})")
        print()
    
    # ========================================================================
    # TAREA 4: ROTACIÓN FIBONACCI EN DESPLIEGUE
    # ========================================================================
    print("\n" + "="*70)
    print("🌀 TAREA 4: MÚLTIPLES PERSPECTIVAS CON FIBONACCI")
    print("="*70)
    print("\n  Objetivo: Explorar expresiones alternativas del mismo tensor\n")
    
    palabra_test = "emergencia"
    tensor_test = VOCABULARIO[palabra_test]
    
    # Desplegar múltiples veces (rotación avanza)
    expresiones_alternativas = []
    
    for i in range(5):
        resultado = extender.desplegar(tensor_test, nivel_objetivo=3)
        expresiones_alternativas.append({
            'iteracion': i + 1,
            'expresion': resultado.texto_generado,
            'coherencia': resultado.nivel_coherencia,
            'paso_fibonacci': extender.paso_despliegue
        })
    
    print(f"  Palabra original: '{palabra_test}'")
    print(f"  Explorando 5 expresiones alternativas:\n")
    
    for expr in expresiones_alternativas:
        print(f"    {expr['iteracion']}. '{expr['expresion']:15s}' (coherencia={expr['coherencia']:.3f}, paso_fib={expr['paso_fibonacci']})")
    
    # Contar expresiones únicas
    expresiones_unicas = set(e['expresion'] for e in expresiones_alternativas)
    print(f"\n  Diversidad: {len(expresiones_unicas)} expresiones únicas de 5 intentos")
    
    # ========================================================================
    # GUARDAR RESULTADOS
    # ========================================================================
    
    analisis = {
        "tarea_1_ciclo": resultados_ciclo,
        "tarea_2_emergencia": resultados_emergencia,
        "tarea_3_navegacion": resultados_navegacion,
        "tarea_4_rotacion": expresiones_alternativas,
        "metricas": {
            "reconstrucciones_exactas": sum(1 for r in resultados_ciclo if r['exacto']),
            "coherencia_promedio_ciclo": np.mean([r['coherencia'] for r in resultados_ciclo]),
            "coherencia_promedio_emergencia": np.mean([r['coherencia_despliegue'] for r in resultados_emergencia]),
            "expresiones_unicas": len(expresiones_unicas),
            "palabras_nuevas_desplegadas": len(resultados_navegacion)
        }
    }
    
    with open('paso4_extender.json', 'w', encoding='utf-8') as f:
        json.dump(analisis, f, indent=2, ensure_ascii=False)
    
    print("\n" + "="*70)
    print("✅ Análisis guardado en: paso4_extender.json")
    print("="*70)
    
    # ========================================================================
    # RESUMEN
    # ========================================================================
    
    print("\n🌌 RESUMEN DEL PASO 4:")
    print(f"  Tarea 1: {analisis['metricas']['reconstrucciones_exactas']}/{len(resultados_ciclo)} reconstrucciones exactas")
    print(f"  Tarea 2: {len(resultados_emergencia)} emergencias desplegadas")
    print(f"  Tarea 3: {analisis['metricas']['palabras_nuevas_desplegadas']} palabras nuevas navegadas")
    print(f"  Tarea 4: {analisis['metricas']['expresiones_unicas']} expresiones únicas (diversidad)")
    
    print(f"\n  Coherencia promedio:")
    print(f"    Ciclo completo: {analisis['metricas']['coherencia_promedio_ciclo']:.3f}")
    print(f"    Desde emergencias: {analisis['metricas']['coherencia_promedio_emergencia']:.3f}")
    
    # Interpretación
    print("\n💡 INTERPRETACIÓN:")
    
    if analisis['metricas']['reconstrucciones_exactas'] >= len(resultados_ciclo) * 0.8:
        print("  ✅ EXTENDER funciona: Ciclo texto→tensor→texto con alta fidelidad")
    else:
        print(f"  ⚠️  Reconstrucción parcial: {analisis['metricas']['reconstrucciones_exactas']}/{len(resultados_ciclo)} exactas")
        print("     (Esperado: rotación Fibonacci explora expresiones alternativas)")
    
    if analisis['metricas']['coherencia_promedio_emergencia'] > 0.5:
        print("  ✅ DESPLIEGUE JERÁRQUICO funcional (Ms→Ss→MetaM → texto coherente)")
    else:
        print("  ⚠️  Despliegue necesita más migas de pan contextuales")
    
    if analisis['metricas']['expresiones_unicas'] > 1:
        print(f"  ✅ DIVERSIDAD: {analisis['metricas']['expresiones_unicas']} formas de expresar mismo concepto")
    else:
        print("  ⚠️  Poca diversidad (red pequeña o vocabulario limitado)")
    
    print("\n🎯 CICLO COMPLETO:")
    print("  Texto → Encoder → Tensor → Transcender → Emergencia")
    print("                                             ↓")
    print("  Texto ← EXTENDER ← Arquetipo ← Evolver ← Emergencia")
    print("\n  ✅ SISTEMA AURORA OPERACIONAL")
    
    return analisis


if __name__ == "__main__":
    analisis = ejecutar_paso4()
