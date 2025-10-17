"""
Test Rápido: Armonizador en Genesis
====================================
Prueba simple de integración sin ejecutar Genesis completo.
"""

import sys
sys.path.append('.')

from tensor_ffe import TensorFFE, VectorFFE
from transcender import Transcender
from evolver import Evolver
from armonizador import Armonizador

def test_integracion_rapida():
    """Test mínimo de integración"""
    
    print("\n🔧 TEST INTEGRACIÓN ARMONIZADOR ← → GENESIS")
    print("="*60)
    
    # 1. Crear componentes
    print("\n[1/4] Creando componentes...")
    evolver = Evolver()
    transcender = Transcender()
    armonizador = Armonizador(
        evolver=evolver,
        transcender=transcender,
        umbral_coherencia=0.7
    )
    print("  ✅ Evolver, Transcender, Armonizador creados")
    
    # 2. Crear tensores de prueba
    print("\n[2/4] Creando tensores de prueba...")
    tensores = []
    for i in range(5):
        t = TensorFFE()
        t.nivel_1[0] = VectorFFE(i % 8, (i+1) % 8, (i+2) % 8)
        t.nivel_1[1] = VectorFFE((i+3) % 8, (i+4) % 8, (i+5) % 8)
        t.nivel_1[2] = VectorFFE((i+6) % 8, i % 8, (i+1) % 8)
        t.reconstruir_jerarquia()
        tensores.append(t)
    print(f"  ✅ {len(tensores)} tensores creados")
    
    # 3. Armonizar
    print("\n[3/4] Armonizando tensores...")
    reporte = armonizador.armonizar_lote(tensores, "test_integracion")
    
    print(f"\n  📊 REPORTE:")
    print(f"     Coherente: {'✅' if reporte['coherente'] else '❌'}")
    print(f"     Incoherencias: {reporte['incoherencias']}")
    print(f"     Correcciones: {reporte.get('correcciones', 0)}")
    print(f"     Aprendizajes: {reporte.get('aprendizajes', 0)}")
    
    if 'coherencia_promedio' in reporte and reporte['coherencia_promedio']:
        print(f"     Coherencia: {reporte['coherencia_promedio']:.3f}")
    
    # 4. Estadísticas
    print("\n[4/4] Estadísticas globales...")
    stats = armonizador.obtener_estadisticas()
    print(f"  Total incoherencias históricas: {stats.get('total_incoherencias', 0)}")
    print(f"  Total aprendizajes: {stats.get('total_aprendizajes', 0)}")
    if 'espacios_logicos' in stats:
        print(f"  Espacios lógicos: {len(stats['espacios_logicos'])}")
    
    # Veredicto
    print("\n" + "="*60)
    if reporte['coherente'] or reporte.get('correcciones', 0) > 0:
        print("✅ INTEGRACIÓN EXITOSA")
        print("   Armonizador funciona correctamente con Evolver + Transcender")
    else:
        print("⚠️ INTEGRACIÓN PARCIAL")
        print("   Funcionó pero no detectó incoherencias (puede ser normal)")
    
    return reporte

if __name__ == "__main__":
    try:
        reporte = test_integracion_rapida()
        print(f"\n💾 Reporte: {reporte}")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
