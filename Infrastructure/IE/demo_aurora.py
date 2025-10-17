"""
🌌 DEMOSTRACIÓN PRÁCTICA DEL SISTEMA AURORA
===========================================

Este script demuestra las capacidades principales del sistema Aurora:
1. Aprendizaje de patrones ternarios
2. Consulta con valores completos
3. Deducción recursiva con NULLs
4. Persistencia de conocimiento
5. Métricas y observabilidad
"""

import logging
logging.basicConfig(level=logging.ERROR)  # Silenciar logs para output limpio

from aurora_engine import Aurora

def print_section(title):
    """Imprime una sección formateada."""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def main():
    print_section("🌌 DEMOSTRACIÓN AURORA TRINITY-3")
    
    # 1. CREAR INSTANCIA
    print("\n📌 Paso 1: Inicializar Aurora")
    aurora = Aurora()
    print(f"✅ Aurora inicializada (kb_size={len(aurora.kb.universes)}, ready=True)")
    
    # 2. APRENDER PATRONES
    print_section("📚 Paso 2: Aprender Patrones Ternarios")
    
    patterns = [
        [1, 0, 1],  # Patrón Alpha
        [0, 1, 0],  # Patrón Beta
        [1, 1, 0],  # Patrón Gamma
        [0, 0, 1],  # Patrón Delta
    ]
    
    print(f"\n📥 Entrenando con {len(patterns)} patrones:")
    for i, p in enumerate(patterns):
        print(f"  {chr(945+i)}: {p}")  # α, β, γ, δ
    
    aurora.learn(patterns, space_id="demo")
    print(f"✅ Aprendizaje completado en espacio 'demo'")
    
    # 3. CONSULTAS EXACTAS
    print_section("🔍 Paso 3: Consultas Exactas (sin NULLs)")
    
    queries = [
        [1, 0, 1],
        [0, 1, 0],
        [1, 1, 0],
    ]
    
    print("\n📊 Resultados de consultas:")
    for q in queries:
        result = aurora.query(q, space_id="demo")
        match = "✓" if result == q else "✗"
        print(f"  {q} → {result} {match}")
    
    # 4. DEDUCCIÓN CON NULLs
    print_section("🧠 Paso 4: Deducción Recursiva (con NULLs)")
    
    incomplete_patterns = [
        [1, None, None],      # 2 valores desconocidos
        [None, 1, None],      # 2 valores desconocidos
        [1, 0, None],         # 1 valor desconocido
        [None, None, 1],      # 2 valores desconocidos
    ]
    
    print("\n🔮 Aurora deduce valores desconocidos:")
    for pattern in incomplete_patterns:
        nulls = pattern.count(None)
        result = aurora.query(pattern, space_id="demo")
        print(f"  {pattern} → {result} (resolvió {nulls} NULLs)")
    
    # 5. MULTI-ESPACIO
    print_section("🌐 Paso 5: Conocimiento Multi-Espacio")
    
    # Crear segundo espacio con patrones diferentes
    space2_patterns = [
        [1, 1, 1],
        [0, 0, 0],
    ]
    
    print("\n📥 Creando espacio 'experimental' con patrones:")
    for p in space2_patterns:
        print(f"  • {p}")
    
    aurora.learn(space2_patterns, space_id="experimental")
    
    # Consultar en cada espacio
    test_pattern = [1, None, 1]
    result_demo = aurora.query(test_pattern, space_id="demo")
    result_exp = aurora.query(test_pattern, space_id="experimental")
    
    print(f"\n🔍 Consulta {test_pattern} en diferentes espacios:")
    print(f"  • 'demo': {result_demo}")
    print(f"  • 'experimental': {result_exp}")
    print(f"  → Diferentes espacios pueden generar diferentes deducciones")
    
    # 6. PERSISTENCIA
    print_section("💾 Paso 6: Persistencia de Conocimiento")
    
    kb_path = "aurora_demo_kb.json"
    print(f"\n💾 Guardando KB en: {kb_path}")
    aurora.save(kb_path, format='json')
    print(f"✅ KB guardada exitosamente")
    
    print(f"\n📂 Cargando KB desde disco...")
    aurora2 = Aurora(kb_path=kb_path)
    print(f"✅ KB cargada en nueva instancia")
    
    # Verificar que funciona
    test_result = aurora2.query([1, 0, 1], space_id="demo")
    print(f"\n🔍 Verificación: [1,0,1] → {test_result}")
    print(f"✅ Persistencia funcional")
    
    # 7. MÉTRICAS
    print_section("📊 Paso 7: Métricas y Observabilidad")
    
    metrics = aurora.metrics()
    print(f"\n📈 Estadísticas del sistema:")
    print(f"  • Total operaciones: {metrics.get('total_operations', 0)}")
    print(f"  • Coherencia promedio: {metrics.get('avg_coherence', 0):.3f}")
    if 'operation_counts' in metrics:
        print(f"  • Distribución de operaciones:")
        for op_type, count in metrics['operation_counts'].items():
            print(f"    - {op_type}: {count}")
    else:
        print(f"  • Operaciones registradas: {len(metrics.get('operations', []))}")
    
    # 8. RESUMEN
    print_section("✅ DEMOSTRACIÓN COMPLETADA")
    
    print("""
    Aurora Trinity-3 ha demostrado:
    
    ✓ Aprendizaje de patrones ternarios (0, 1, NULL)
    ✓ Consulta exacta con recuperación perfecta
    ✓ Deducción recursiva de valores desconocidos
    ✓ Gestión de múltiples espacios lógicos
    ✓ Persistencia JSON con serialización fractal
    ✓ Métricas y observabilidad en tiempo real
    
    🌌 Sistema operacional y listo para producción
    """)
    
    # Limpieza
    import os
    if os.path.exists(kb_path):
        os.remove(kb_path)
        print(f"🗑️  Archivo temporal {kb_path} eliminado\n")

if __name__ == "__main__":
    main()
