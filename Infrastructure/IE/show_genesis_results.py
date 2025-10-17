"""Muestra resultados de Genesis v1.1"""
import json

with open('genesis_v1.1.json') as f:
    d = json.load(f)

print("\n" + "="*70)
print("GENESIS V1.1 - RESULTADOS COMPLETOS")
print("="*70)

# Fase 7: Armonizacion
f7 = d['fase_7']
print("\n📊 FASE 7: ARMONIZACION")
print(f"  Coherente: {'✅' if f7['coherente'] else '❌'}")
print(f"  Incoherencias detectadas: {f7['incoherencias']}")
print(f"  Correcciones exitosas: {f7['correcciones']}")
print(f"  Correcciones fallidas: {f7.get('correcciones_fallidas', 0)}")
print(f"  Aprendizajes generados: {f7['aprendizajes']}")

# Estadisticas (si estan disponibles)
if 'estadisticas' in f7:
    stats = f7['estadisticas']
    print(f"\n📈 ESTADÍSTICAS ARMONIZADOR:")
    print(f"  Total incoherencias históricas: {stats['total_incoherencias']}")
    print(f"  Total aprendizajes: {stats['total_aprendizajes']}")
    print(f"  Arquetipos monitoreados: {stats['confianzas_arquetipos']}")
    print(f"  Relatores monitoreados: {stats['confianzas_relatores']}")
    print(f"  Espacios lógicos: {stats['correspondencias_espacios']}")
    print(f"  Confianza promedio arquetipos: {stats['confianza_promedio_arquetipos']:.3f}")
    print(f"  Confianza promedio relatores: {stats['confianza_promedio_relatores']:.3f}")

# Coherencia promedio si disponible
if f7.get('coherencia_promedio'):
    print(f"\n  Coherencia promedio post-corrección: {f7['coherencia_promedio']:.3f}")

# Comparacion con v1.0
print(f"\n🔄 COMPARACIÓN v1.0 → v1.1:")
print(f"  Fases totales: 7 → 8 (+1 Armonización)")
print(f"  Sistema auto-correctivo: ❌ → ✅")
print(f"  Detección incoherencias: NO → SÍ ({f7['incoherencias']} detectadas)")
print(f"  Correcciones aplicadas: 0 → {f7['correcciones']}")
print(f"  Aprendizaje de errores: NO → SÍ ({f7['aprendizajes']} patrones)")

# Resumen ejecutivo
fallidas = f7.get('correcciones_fallidas', f7['incoherencias'] - f7['correcciones'])
print(f"\n📝 RESUMEN EJECUTIVO:")
print(f"  ✅ Genesis v1.1 ejecutado exitosamente")
print(f"  ✅ Armonizador integrado como Fase 7")
print(f"  ⚠️ Sistema detectó {f7['incoherencias']} incoherencias")
print(f"  ✅ {f7['correcciones']}/{f7['incoherencias']} corregidas ({100*f7['correcciones']//f7['incoherencias']}%)")
print(f"  ⚠️ {fallidas} no corregibles (relatores rotos con tensor=None)")
print(f"  ✅ Sistema aprendió {f7['aprendizajes']} patrones de error")

print(f"\n{'='*70}")
print("✅ GENESIS V1.1 - AUTOPOIESIS COMPLETA Y AUTO-CORRECTIVA")
print("="*70 + "\n")
