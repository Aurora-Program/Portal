"""
Benchmark Test: Armonizador v1.2 vs v1.3 Optimizado
Proyecto Genesis - Performance Comparison

Compara:
- v1.2: Secuencial (armonizador.py)
- v1.3: Paralelo + Cache (armonizador_optimizado.py)

Esperado:
- v1.3 es 5x más rápido
- Cache hit rate > 60%
- Misma coherencia (algoritmo idéntico)
"""

import sys
import time
import numpy as np
from typing import List

from tensor_ffe import TensorFFE, VectorFFE
from transcender import Transcender
from evolver import Evolver
from armonizador import Armonizador
from armonizador_optimizado import ArmonizadorOptimizado
from armonizador_funcional import ArmonizadorFuncional


def crear_tensores_prueba(n: int = 100) -> List[TensorFFE]:
    """Crea n tensores de prueba sintéticos"""
    transcender = Transcender()
    
    print(f"[1/3] Creando {n} tensores de prueba...")
    
    tensores = []
    
    # Crear tensores base sintéticos (variedad aleatoria)
    for i in range(n // 3):
        # Generar 3 vectores aleatorios (valores 0-7)
        vectores = [
            VectorFFE(
                forma=np.random.randint(0, 8),
                funcion=np.random.randint(0, 8),
                estructura=np.random.randint(0, 8)
            )
            for _ in range(3)
        ]
        tensor = TensorFFE(vectores)
        tensores.append(tensor)
    
    # Crear tensores síntesis (frases)
    for i in range(n // 3):
        idx1 = i % len(tensores)
        idx2 = (i + 1) % len(tensores)
        
        if idx1 < len(tensores) and idx2 < len(tensores):
            emergencia = transcender.sintetizar(
                tensores[idx1],
                tensores[idx2],
                tensores[0]  # dummy
            )
            tensores.append(emergencia.Ms)
    
    # Crear tensores emergencias (triadas)
    for i in range(n - len(tensores)):
        idx1 = i % len(tensores)
        idx2 = (i + 1) % len(tensores)
        idx3 = (i + 2) % len(tensores)
        
        if idx1 < len(tensores) and idx2 < len(tensores) and idx3 < len(tensores):
            emergencia = transcender.sintetizar(
                tensores[idx1],
                tensores[idx2],
                tensores[idx3]
            )
            tensores.append(emergencia.Ms)
    
    print(f"  ✅ {len(tensores)} tensores creados")
    return tensores[:n]


def benchmark_v1_2(tensores: List[TensorFFE], evolver: Evolver, transcender: Transcender) -> dict:
    """Benchmark Armonizador v1.2 (secuencial)"""
    print("\n" + "="*60)
    print("🐢 BENCHMARK v1.2 - SECUENCIAL")
    print("="*60)
    
    armonizador = Armonizador(
        evolver=evolver,
        transcender=transcender,
        umbral_coherencia=0.7,
        max_recursion=10
    )
    
    inicio = time.time()
    reporte = armonizador.armonizar_lote(tensores)
    tiempo_total = time.time() - inicio
    
    return {
        'version': 'v1.2',
        'tiempo': tiempo_total,
        'correcciones': reporte.get('correcciones_exitosas', 0),
        'coherencia_promedio': reporte.get('coherencia_promedio', 0.0),
        'reporte': reporte
    }


def benchmark_v1_3_funcional(tensores: List[TensorFFE], evolver: Evolver, transcender: Transcender) -> dict:
    """Benchmark Armonizador v1.3 Funcional (Redux-style)"""
    print("\n" + "="*60)
    print("� BENCHMARK v1.3 - FUNCIONAL PURO")
    print("="*60)
    
    armonizador = ArmonizadorFuncional(
        evolver=evolver,
        transcender=transcender,
        umbral_coherencia=0.7,
        max_recursion=10,
        num_workers=4,  # Usar 4 workers
        batch_size=25   # Batches de 25
    )
    
    inicio = time.time()
    reporte = armonizador.armonizar_lote_funcional(tensores)
    tiempo_total = time.time() - inicio
    
    return {
        'version': 'v1.3-funcional',
        'tiempo': tiempo_total,
        'correcciones': reporte.get('correcciones_exitosas', 0),
        'coherencia_promedio': reporte.get('coherencia_promedio', 0.0),
        'cache_hit_rate': f"{reporte.get('cache_hit_rate', 0):.1f}%",
        'velocidad': reporte.get('velocidad', 0),
        'reporte': reporte
    }


def comparar_resultados(resultado_v12: dict, resultado_v13: dict):
    """Compara resultados de ambas versiones"""
    print("\n" + "="*60)
    print("📊 COMPARACIÓN v1.2 vs v1.3")
    print("="*60)
    
    tiempo_v12 = resultado_v12['tiempo']
    tiempo_v13 = resultado_v13['tiempo']
    speedup = tiempo_v12 / tiempo_v13 if tiempo_v13 > 0 else 0
    
    print(f"\n⏱️ TIEMPO:")
    print(f"  v1.2 (secuencial): {tiempo_v12:.2f}s")
    print(f"  v1.3 (paralelo):   {tiempo_v13:.2f}s")
    print(f"  Speedup:           {speedup:.2f}x {'✅' if speedup >= 3 else '⚠️'}")
    
    print(f"\n🎯 CORRECCIONES:")
    print(f"  v1.2: {resultado_v12['correcciones']}")
    print(f"  v1.3: {resultado_v13['correcciones']}")
    
    coh_v12 = resultado_v12['coherencia_promedio']
    coh_v13 = resultado_v13['coherencia_promedio']
    print(f"\n📈 COHERENCIA PROMEDIO:")
    print(f"  v1.2: {coh_v12:.3f}")
    print(f"  v1.3: {coh_v13:.3f}")
    print(f"  Delta: {abs(coh_v12 - coh_v13):.3f} {'✅' if abs(coh_v12 - coh_v13) < 0.01 else '⚠️'}")
    
    print(f"\n💾 CACHE (v1.3):")
    print(f"  Hit rate: {resultado_v13.get('cache_hit_rate', 'N/A')}")
    
    print("\n" + "="*60)
    print("🏆 RESULTADO:")
    
    if speedup >= 3 and abs(coh_v12 - coh_v13) < 0.01:
        print("  ✅ OPTIMIZACIÓN EXITOSA")
        print(f"  🚀 v1.3 es {speedup:.1f}x más rápido")
        print("  🎯 Coherencia idéntica (algoritmo preservado)")
    elif speedup >= 2:
        print("  ⚠️ MEJORA MODERADA")
        print(f"  v1.3 es {speedup:.1f}x más rápido (esperado 3x+)")
    else:
        print("  ❌ OPTIMIZACIÓN INSUFICIENTE")
        print(f"  v1.3 solo {speedup:.1f}x más rápido")
    
    print("="*60)


def main():
    """Ejecuta benchmark completo"""
    print("\n" + "="*60)
    print("🧪 BENCHMARK: ARMONIZADOR v1.2 vs v1.3")
    print("="*60)
    
    # Crear componentes
    print("\n[1/4] Inicializando componentes...")
    evolver = Evolver()
    transcender = evolver.transcender
    
    # Crear tensores de prueba
    print("\n[2/4] Generando dataset de prueba...")
    tensores = crear_tensores_prueba(n=100)
    
    # Construir red de relatores (para generar incoherencias)
    print("\n[3/4] Construyendo red de relatores...")
    for tensor in tensores:
        evolver.aprender(tensor)  # Método correcto
    
    # Conectar arquetipos adicionales
    arquetipos = list(evolver.archetype_learner.arquetipos.values())
    print(f"  Arquetipos descubiertos: {len(arquetipos)}")
    
    # Crear más conexiones para más incoherencias
    for i, arq1 in enumerate(arquetipos[:min(10, len(arquetipos))]):
        for j, arq2 in enumerate(arquetipos[i+1:min(15, len(arquetipos))]):
            evolver.relator_network.conectar(arq1, arq2)
    
    print(f"  Relatores creados: {len(evolver.relator_network.relatores)}")
    
    # Ejecutar benchmarks
    print("\n[4/4] Ejecutando benchmarks...")
    
    # v1.2 Secuencial
    resultado_v12 = benchmark_v1_2(tensores, evolver, transcender)
    
    # v1.3 Funcional Puro
    resultado_v13 = benchmark_v1_3_funcional(tensores, evolver, transcender)
    
    # Comparar
    comparar_resultados(resultado_v12, resultado_v13)
    
    print("\n✅ BENCHMARK COMPLETADO\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️ Benchmark interrumpido por usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error en benchmark: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
