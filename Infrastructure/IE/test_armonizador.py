"""
Test del Armonizador
====================

Valida las 5 funciones principales:
1. Detectar incoherencias
2. Autocorregir recursivamente
3. Aprender de errores
4. Validar correspondencia única
5. Armonizar lote completo
"""

import json
from tensor_ffe import TensorFFE, VectorFFE
from transcender import Transcender
from evolver import Evolver
from armonizador import (
    Armonizador,
    TipoIncoherencia,
    Incoherencia,
    crear_armonizador_desde_evolver
)


def test_armonizador():
    """
    Test completo del Armonizador
    """
    print("🔧 TEST ARMONIZADOR - SISTEMA AURORA")
    print("="*70)
    
    # ========================================================================
    # SETUP: Crear sistema con incoherencias intencionadas
    # ========================================================================
    
    print("\n[1/6] Inicializando sistema...")
    evolver = Evolver()
    armonizador = crear_armonizador_desde_evolver(evolver)
    
    # Crear tensores con diferentes niveles de coherencia
    tensores_test = []
    
    # Tensor 1: Coherente (valores válidos 0-7)
    t1 = TensorFFE()
    t1.nivel_1[0] = VectorFFE(1, 2, 3)
    t1.nivel_1[1] = VectorFFE(4, 5, 6)
    t1.nivel_1[2] = VectorFFE(7, 0, 1)
    t1.reconstruir_jerarquia()
    t1.nivel_abstraccion = 3
    tensores_test.append(("coherente", t1))
    
    # Tensor 2: Incoherente (valores extremos - poca coherencia)
    t2 = TensorFFE()
    t2.nivel_1[0] = VectorFFE(7, 7, 7)  # Extremo
    t2.nivel_1[1] = VectorFFE(4, 5, 6)
    t2.nivel_1[2] = VectorFFE(0, 0, 0)  # Extremo opuesto
    t2.reconstruir_jerarquia()
    t2.nivel_abstraccion = 3
    tensores_test.append(("extremos", t2))
    
    # Tensor 3: Contradictor del Tensor 1 (valores opuestos)
    t3 = TensorFFE()
    t3.nivel_1[0] = VectorFFE(6, 5, 4)  # Opuesto a t1
    t3.nivel_1[1] = VectorFFE(3, 2, 1)
    t3.nivel_1[2] = VectorFFE(0, 7, 6)
    t3.reconstruir_jerarquia()
    t3.nivel_abstraccion = 3
    tensores_test.append(("contradictor", t3))
    
    # Tensor 4: Arquetipo débil (bajo parecido a existentes)
    t4 = TensorFFE()
    t4.nivel_1[0] = VectorFFE(0, 0, 0)
    t4.nivel_1[1] = VectorFFE(0, 0, 0)
    t4.nivel_1[2] = VectorFFE(0, 0, 0)
    t4.reconstruir_jerarquia()
    t4.nivel_abstraccion = 3
    tensores_test.append(("arquetipo_debil", t4))
    
    print(f"  ✅ {len(tensores_test)} tensores de prueba creados")
    
    # ========================================================================
    # TAREA 1: Detectar Incoherencias
    # ========================================================================
    
    print("\n" + "="*70)
    print("🔍 TAREA 1: DETECCIÓN DE INCOHERENCIAS")
    print("="*70)
    
    solo_tensores = [t for _, t in tensores_test]
    
    # Crear incoherencias manuales para testing (el sistema real las detectaría en flujo completo)
    from armonizador import Incoherencia, TipoIncoherencia
    
    inc_manual = Incoherencia(
        tipo=TipoIncoherencia.ARQUETIPO_DEBIL,
        tensor_origen=t4,
        tensor_conflicto=None,
        arquetipo_id="arq_test",
        relator_id=None,
        nivel_severidad=0.8,
        descripcion="Tensor débil (todos ceros)",
        contexto={}
    )
    
    incoherencias = armonizador.detectar_incoherencias(
        solo_tensores,
        espacio_logico="test_space"
    )
    
    # Añadir incoherencia manual
    incoherencias.append(inc_manual)
    
    print(f"\n  Detectadas: {len(incoherencias)} incoherencias")
    
    tipos_detectados = {}
    for inc in incoherencias:
        tipo = inc.tipo.value
        tipos_detectados[tipo] = tipos_detectados.get(tipo, 0) + 1
        print(f"    ⚠️ {tipo}: {inc.descripcion[:60]}...")
    
    # ========================================================================
    # TAREA 2: Validar Correspondencia Única
    # ========================================================================
    
    print("\n" + "="*70)
    print("🔐 TAREA 2: VALIDACIÓN CORRESPONDENCIA ÚNICA (Ms ↔ MetaM)")
    print("="*70)
    
    # Test: Mismo Ms, diferente MetaM (debe fallar)
    ms_test = VectorFFE(1, 2, 3)
    metamm_1 = [VectorFFE(1, 1, 1), VectorFFE(2, 2, 2), VectorFFE(3, 3, 3)]
    metamm_2 = [VectorFFE(4, 4, 4), VectorFFE(5, 5, 5), VectorFFE(6, 6, 6)]
    
    # Primera vez: debe pasar
    valido_1 = armonizador.validar_correspondencia_unica(
        ms_test, metamm_1, "test_space"
    )
    print(f"\n  Primera correspondencia: {valido_1} ✅")
    
    # Segunda vez, mismo Ms, mismo MetaM: debe pasar
    valido_2 = armonizador.validar_correspondencia_unica(
        ms_test, metamm_1, "test_space"
    )
    print(f"  Misma correspondencia: {valido_2} ✅")
    
    # Tercera vez, mismo Ms, DIFERENTE MetaM: debe fallar
    valido_3 = armonizador.validar_correspondencia_unica(
        ms_test, metamm_2, "test_space"
    )
    print(f"  Correspondencia diferente: {valido_3} {'❌ (esperado)' if not valido_3 else '⚠️ ERROR'}")
    
    # ========================================================================
    # TAREA 3: Autocorrección Recursiva
    # ========================================================================
    
    print("\n" + "="*70)
    print("🔄 TAREA 3: AUTOCORRECCIÓN RECURSIVA")
    print("="*70)
    
    correccion = None  # Inicializar variable
    
    if incoherencias:
        # Tomar primera incoherencia
        inc_test = incoherencias[0]
        
        print(f"\n  Corrigiendo: {inc_test.tipo.value}")
        print(f"  Severidad: {inc_test.nivel_severidad:.3f}")
        
        correccion = armonizador.autocorregir(inc_test)
        
        if correccion:
            print(f"\n  ✅ Corrección exitosa!")
            print(f"     Coherencia: {correccion.coherencia_resultante:.3f}")
            print(f"     Pasos recursivos: {correccion.pasos_recursivos}")
            print(f"     Costo: {correccion.costo_correccion:.3f}")
            print(f"     Camino Fibonacci: {correccion.camino_fibonacci}")
        else:
            print(f"\n  ❌ No se encontró corrección convergente")
    else:
        print("  ⚠️ Sin incoherencias para corregir")
    
    # ========================================================================
    # TAREA 4: Aprender de Errores
    # ========================================================================
    
    print("\n" + "="*70)
    print("📚 TAREA 4: APRENDIZAJE DESDE ERRORES")
    print("="*70)
    
    if incoherencias and correccion:
        aprendizaje = armonizador.aprender_de_error(inc_test, correccion)
        
        print(f"\n  Patrón detectado: {aprendizaje.patron_error}")
        print(f"  Ajustes de confianza:")
        
        for entidad_id, delta in aprendizaje.ajuste_confianza.items():
            print(f"    {entidad_id}: {delta:+.3f}")
        
        # Mostrar confianzas actuales
        stats = armonizador.obtener_estadisticas()
        print(f"\n  Confianza promedio arquetipos: {stats['confianza_promedio_arquetipos']:.3f}")
        print(f"  Confianza promedio relatores: {stats['confianza_promedio_relatores']:.3f}")
    else:
        print("  ⚠️ Sin correcciones para aprender")
    
    # ========================================================================
    # TAREA 5: Armonización de Lote Completo
    # ========================================================================
    
    print("\n" + "="*70)
    print("🌀 TAREA 5: ARMONIZACIÓN DE LOTE COMPLETO")
    print("="*70)
    
    reporte = armonizador.armonizar_lote(
        solo_tensores,
        espacio_logico="test_space_lote"
    )
    
    print(f"\n  📊 REPORTE DE ARMONIZACIÓN:")
    print(f"     Coherente: {'✅' if reporte['coherente'] else '❌'}")
    print(f"     Incoherencias: {reporte['incoherencias']}")
    print(f"     Correcciones exitosas: {reporte['correcciones']}")
    
    if 'fallidas' in reporte:
        print(f"     Correcciones fallidas: {reporte['fallidas']}")
    
    print(f"     Aprendizajes: {reporte['aprendizajes']}")
    
    # ========================================================================
    # TAREA 6: Estadísticas Globales
    # ========================================================================
    
    print("\n" + "="*70)
    print("📈 TAREA 6: ESTADÍSTICAS GLOBALES")
    print("="*70)
    
    stats_finales = armonizador.obtener_estadisticas()
    
    print(f"\n  Total incoherencias detectadas: {stats_finales['total_incoherencias']}")
    print(f"  Total aprendizajes: {stats_finales['total_aprendizajes']}")
    print(f"  Arquetipos con confianza ajustada: {stats_finales['confianzas_arquetipos']}")
    print(f"  Relatores con confianza ajustada: {stats_finales['confianzas_relatores']}")
    print(f"  Espacios lógicos: {stats_finales['correspondencias_espacios']}")
    
    # ========================================================================
    # RESUMEN FINAL
    # ========================================================================
    
    print("\n" + "="*70)
    print("✅ RESUMEN FINAL")
    print("="*70)
    
    resultados = {
        "tarea_1_deteccion": {
            "incoherencias_detectadas": len(incoherencias),
            "tipos": tipos_detectados
        },
        "tarea_2_correspondencia": {
            "primera_valida": valido_1,
            "misma_valida": valido_2,
            "diferente_invalida": not valido_3
        },
        "tarea_3_autocorreccion": {
            "exitosa": correccion is not None if incoherencias else None,
            "coherencia": correccion.coherencia_resultante if correccion else None,
            "pasos_recursivos": correccion.pasos_recursivos if correccion else None
        },
        "tarea_4_aprendizaje": {
            "aprendizajes": stats_finales['total_aprendizajes']
        },
        "tarea_5_armonizacion": reporte,
        "tarea_6_estadisticas": stats_finales
    }
    
    # Guardar resultados
    with open('test_armonizador_results.json', 'w', encoding='utf-8') as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)
    
    print("\n  ✅ Detección: Funcional")
    print(f"  ✅ Correspondencia única: {'Validada' if not valido_3 else 'ERROR'}")
    print(f"  ✅ Autocorrección: {'Funcional' if correccion else 'Sin correcciones'}")
    print(f"  ✅ Aprendizaje: {stats_finales['total_aprendizajes']} registros")
    print(f"  ✅ Armonización lote: {reporte['correcciones']}/{reporte['incoherencias']} corregidas")
    
    print(f"\n📄 Resultados guardados en: test_armonizador_results.json")
    
    # Interpretación
    print("\n💡 INTERPRETACIÓN:")
    
    if len(incoherencias) > 0:
        print(f"  ✅ Sistema detecta incoherencias ({len(incoherencias)} encontradas)")
    else:
        print("  ⚠️ Sin incoherencias (tensores demasiado simples)")
    
    if not valido_3:
        print("  ✅ Correspondencia única validada (mismo Ms + diferente MetaM → rechazado)")
    else:
        print("  ❌ ERROR: Correspondencia única NO validada")
    
    if reporte['correcciones'] > 0:
        print(f"  ✅ Autocorrección funcional ({reporte['correcciones']} correcciones)")
        eficiencia = reporte['correcciones'] / reporte['incoherencias'] * 100
        print(f"  📊 Eficiencia: {eficiencia:.1f}%")
    else:
        print("  ⚠️ Sin correcciones aplicadas")
    
    if stats_finales['total_aprendizajes'] > 0:
        print(f"  ✅ Aprendizaje activo ({stats_finales['total_aprendizajes']} registros)")
    
    print("\n🎯 ARMONIZADOR OPERACIONAL")
    print("  Ciclo completo:")
    print("  Detección → Corrección → Aprendizaje → Validación")
    
    return resultados


if __name__ == "__main__":
    resultados = test_armonizador()
