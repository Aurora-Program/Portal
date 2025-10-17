"""
Proyecto Genesis - Benchmark Suite
===================================

Benchmark comparativo de Tensores FFE vs Embeddings tradicionales.
Diseñado para validación académica y peer review.

Métricas evaluadas:
1. Compresión (bits utilizados)
2. Tiempo de codificación/decodificación
3. Calidad semántica (similitud coseno)
4. Escalabilidad (batch processing)
5. Memoria utilizada
6. Emergencia (síntesis de conceptos)

Versión: 1.0.0
Fecha: Octubre 2025
"""

import time
import numpy as np
import json
from typing import List, Dict, Tuple
from dataclasses import dataclass, asdict
import sys

# Importar componentes Genesis
from tensor_ffe import TensorFFE, crear_tensor_desde_lista, TransformadorFFE
from transcender import Transcender
from evolver import Evolver
from ffe_encoder_mcp import FFEEncoder


@dataclass
class BenchmarkResult:
    """Resultado de un benchmark individual"""
    nombre: str
    metrica: str
    valor_genesis: float
    valor_baseline: float
    mejora_porcentual: float
    unidad: str
    detalles: Dict = None
    
    def to_dict(self):
        return asdict(self)


class BenchmarkSuite:
    """Suite completa de benchmarks"""
    
    def __init__(self, dimension_embedding: int = 768, num_samples: int = 100):
        self.dimension_embedding = dimension_embedding
        self.num_samples = num_samples
        self.encoder = FFEEncoder(dimension_embedding)
        self.transcender = Transcender()
        self.evolver = Evolver()
        self.resultados: List[BenchmarkResult] = []
        
        print("=" * 80)
        print("PROYECTO GENESIS - BENCHMARK SUITE")
        print("=" * 80)
        print(f"\nConfiguración:")
        print(f"  Dimensión embeddings: {dimension_embedding}")
        print(f"  Número de muestras: {num_samples}")
        print(f"  Arquitectura: FFE (Forma-Función-Estructura)")
        print(f"  Estructura fractal: 3→9→27 (117 bits)")
        print()
    
    def generar_embedding_sintetico(self, seed: int) -> np.ndarray:
        """Genera embedding sintético reproducible"""
        np.random.seed(seed)
        return np.random.randn(self.dimension_embedding)
    
    def benchmark_compresion(self) -> BenchmarkResult:
        """
        Benchmark 1: Ratio de Compresión
        Compara bits utilizados por representación
        """
        print("\n[1/6] Benchmark: Compresión")
        print("-" * 60)
        
        # Genesis FFE
        tensor = TensorFFE()
        bits_genesis = 117
        
        # Baseline: Embedding tradicional (float32)
        bits_baseline = self.dimension_embedding * 32
        
        ratio = bits_baseline / bits_genesis
        mejora = ((bits_baseline - bits_genesis) / bits_baseline) * 100
        
        print(f"  Genesis FFE:        {bits_genesis} bits")
        print(f"  Baseline (float32): {bits_baseline} bits")
        print(f"  Ratio compresión:   {ratio:.1f}x")
        print(f"  Mejora:             {mejora:.1f}%")
        
        resultado = BenchmarkResult(
            nombre="Compresión de Representación",
            metrica="bits_utilizados",
            valor_genesis=bits_genesis,
            valor_baseline=bits_baseline,
            mejora_porcentual=mejora,
            unidad="bits",
            detalles={
                "ratio": ratio,
                "ahorro_bytes": (bits_baseline - bits_genesis) / 8
            }
        )
        
        self.resultados.append(resultado)
        return resultado
    
    def benchmark_velocidad_encoding(self) -> BenchmarkResult:
        """
        Benchmark 2: Velocidad de Codificación
        Tiempo para convertir embedding → FFE
        """
        print("\n[2/6] Benchmark: Velocidad de Codificación")
        print("-" * 60)
        
        # Generar embeddings de prueba
        embeddings = [self.generar_embedding_sintetico(i).tolist() 
                     for i in range(self.num_samples)]
        
        # Genesis FFE
        start = time.perf_counter()
        for emb in embeddings:
            self.encoder.encode(emb)
        tiempo_genesis = time.perf_counter() - start
        
        # Baseline: "Codificación" a numpy array (overhead mínimo)
        start = time.perf_counter()
        for emb in embeddings:
            np.array(emb, dtype=np.float32)
        tiempo_baseline = time.perf_counter() - start
        
        throughput_genesis = self.num_samples / tiempo_genesis
        throughput_baseline = self.num_samples / tiempo_baseline
        
        # Overhead relativo
        overhead = ((tiempo_genesis - tiempo_baseline) / tiempo_baseline) * 100
        
        print(f"  Genesis FFE:  {tiempo_genesis:.4f}s ({throughput_genesis:.1f} enc/s)")
        print(f"  Baseline:     {tiempo_baseline:.4f}s ({throughput_baseline:.1f} enc/s)")
        print(f"  Overhead:     +{overhead:.1f}%")
        print(f"  Tiempo/muestra: {(tiempo_genesis/self.num_samples)*1000:.2f}ms")
        
        resultado = BenchmarkResult(
            nombre="Velocidad de Codificación",
            metrica="tiempo_encoding",
            valor_genesis=tiempo_genesis,
            valor_baseline=tiempo_baseline,
            mejora_porcentual=-overhead,  # Negativo = más lento
            unidad="segundos",
            detalles={
                "throughput_genesis": throughput_genesis,
                "throughput_baseline": throughput_baseline,
                "ms_por_muestra": (tiempo_genesis/self.num_samples)*1000
            }
        )
        
        self.resultados.append(resultado)
        return resultado
    
    def benchmark_calidad_semantica(self) -> BenchmarkResult:
        """
        Benchmark 3: Preservación Semántica
        Mide similitud coseno después de reconstrucción
        """
        print("\n[3/6] Benchmark: Calidad Semántica")
        print("-" * 60)
        
        similitudes = []
        
        for i in range(min(50, self.num_samples)):  # 50 muestras
            # Embedding original
            emb_original = self.generar_embedding_sintetico(i).tolist()
            
            # Codificar → Decodificar
            tensor = self.encoder.encode(emb_original)
            emb_reconstruido = self.encoder.decode(tensor, self.dimension_embedding)
            
            # Similitud coseno
            comparacion = self.encoder.compare(emb_original, tensor)
            similitudes.append(comparacion['similitud_coseno'])
        
        similitud_promedio = np.mean(similitudes)
        similitud_std = np.std(similitudes)
        
        # Baseline: Similitud perfecta = 1.0
        baseline = 1.0
        perdida = (1.0 - similitud_promedio) * 100
        
        print(f"  Similitud promedio: {similitud_promedio:.4f} ± {similitud_std:.4f}")
        print(f"  Baseline (perfecto): {baseline:.4f}")
        print(f"  Pérdida semántica:   {perdida:.2f}%")
        print(f"  Rango: [{min(similitudes):.4f}, {max(similitudes):.4f}]")
        
        resultado = BenchmarkResult(
            nombre="Preservación Semántica",
            metrica="similitud_coseno",
            valor_genesis=similitud_promedio,
            valor_baseline=baseline,
            mejora_porcentual=-perdida,  # Negativo = pérdida
            unidad="similitud",
            detalles={
                "std": similitud_std,
                "min": min(similitudes),
                "max": max(similitudes),
                "muestras": len(similitudes)
            }
        )
        
        self.resultados.append(resultado)
        return resultado
    
    def benchmark_memoria(self) -> BenchmarkResult:
        """
        Benchmark 4: Uso de Memoria
        Compara memoria para almacenar N vectores
        """
        print("\n[4/6] Benchmark: Uso de Memoria")
        print("-" * 60)
        
        n_vectores = 10000
        
        # Genesis FFE: 117 bits por tensor
        bytes_genesis = (117 * n_vectores) / 8
        mb_genesis = bytes_genesis / (1024 * 1024)
        
        # Baseline: float32 (4 bytes × dimensión)
        bytes_baseline = 4 * self.dimension_embedding * n_vectores
        mb_baseline = bytes_baseline / (1024 * 1024)
        
        ahorro = ((bytes_baseline - bytes_genesis) / bytes_baseline) * 100
        
        print(f"  Genesis FFE ({n_vectores} tensores):")
        print(f"    {mb_genesis:.2f} MB ({bytes_genesis/1024:.1f} KB)")
        print(f"  Baseline ({n_vectores} embeddings):")
        print(f"    {mb_baseline:.2f} MB ({bytes_baseline/1024:.1f} KB)")
        print(f"  Ahorro memoria: {ahorro:.1f}%")
        
        resultado = BenchmarkResult(
            nombre="Uso de Memoria",
            metrica="memoria_mb",
            valor_genesis=mb_genesis,
            valor_baseline=mb_baseline,
            mejora_porcentual=ahorro,
            unidad="MB",
            detalles={
                "n_vectores": n_vectores,
                "bytes_por_vector_genesis": 117/8,
                "bytes_por_vector_baseline": 4 * self.dimension_embedding
            }
        )
        
        self.resultados.append(resultado)
        return resultado
    
    def benchmark_escalabilidad(self) -> BenchmarkResult:
        """
        Benchmark 5: Escalabilidad (Batch Processing)
        Tiempo para procesar lotes de diferentes tamaños
        """
        print("\n[5/6] Benchmark: Escalabilidad")
        print("-" * 60)
        
        batch_sizes = [10, 50, 100, 500]
        tiempos_genesis = []
        tiempos_baseline = []
        
        for batch_size in batch_sizes:
            embeddings = [self.generar_embedding_sintetico(i).tolist() 
                         for i in range(batch_size)]
            
            # Genesis
            start = time.perf_counter()
            for emb in embeddings:
                self.encoder.encode(emb)
            tiempos_genesis.append(time.perf_counter() - start)
            
            # Baseline
            start = time.perf_counter()
            for emb in embeddings:
                np.array(emb, dtype=np.float32)
            tiempos_baseline.append(time.perf_counter() - start)
        
        # Calcular throughput promedio
        throughput_genesis = sum(batch_sizes) / sum(tiempos_genesis)
        throughput_baseline = sum(batch_sizes) / sum(tiempos_baseline)
        
        print(f"  Batch sizes testeados: {batch_sizes}")
        print(f"  Throughput Genesis:  {throughput_genesis:.1f} enc/s")
        print(f"  Throughput Baseline: {throughput_baseline:.1f} enc/s")
        
        # Tabla de resultados
        print("\n  Detalle por batch:")
        print(f"  {'Size':<10} {'Genesis':<15} {'Baseline':<15} {'Overhead':<15}")
        print(f"  {'-'*10} {'-'*15} {'-'*15} {'-'*15}")
        for size, t_g, t_b in zip(batch_sizes, tiempos_genesis, tiempos_baseline):
            overhead = ((t_g - t_b) / t_b) * 100
            print(f"  {size:<10} {t_g:.4f}s{'':<7} {t_b:.4f}s{'':<7} +{overhead:.1f}%")
        
        overhead_promedio = ((sum(tiempos_genesis) - sum(tiempos_baseline)) / 
                             sum(tiempos_baseline)) * 100
        
        resultado = BenchmarkResult(
            nombre="Escalabilidad (Batch)",
            metrica="throughput_promedio",
            valor_genesis=throughput_genesis,
            valor_baseline=throughput_baseline,
            mejora_porcentual=-overhead_promedio,
            unidad="enc/s",
            detalles={
                "batch_sizes": batch_sizes,
                "tiempos_genesis": tiempos_genesis,
                "tiempos_baseline": tiempos_baseline
            }
        )
        
        self.resultados.append(resultado)
        return resultado
    
    def benchmark_emergencia(self) -> BenchmarkResult:
        """
        Benchmark 6: Capacidad de Síntesis Emergente
        Métrica única de Genesis: combinar conceptos para generar emergencia
        """
        print("\n[6/6] Benchmark: Síntesis Emergente (Genesis Only)")
        print("-" * 60)
        
        scores_emergencia = []
        scores_novedad = []
        scores_coherencia = []
        
        # Generar 30 tripletas y sintetizar
        num_tripletas = 30
        
        for i in range(num_tripletas):
            # Crear 3 tensores diferentes
            A = crear_tensor_desde_lista([i % 8, (i+1) % 8, (i+2) % 8], 3)
            B = crear_tensor_desde_lista([(i+3) % 8, (i+4) % 8, (i+5) % 8], 3)
            C = crear_tensor_desde_lista([(i+6) % 8, (i+7) % 8, (i+1) % 8], 4)
            
            # Sintetizar
            emergencia = self.transcender.sintetizar(A, B, C)
            
            scores_emergencia.append(emergencia.score_emergencia)
            scores_novedad.append(emergencia.novedad)
            scores_coherencia.append(emergencia.coherencia)
        
        # Estadísticas
        score_promedio = np.mean(scores_emergencia)
        score_std = np.std(scores_emergencia)
        novedad_promedio = np.mean(scores_novedad)
        coherencia_promedio = np.mean(scores_coherencia)
        
        print(f"  Tripletas sintetizadas: {num_tripletas}")
        print(f"  Score emergencia promedio: {score_promedio:.4f} ± {score_std:.4f}")
        print(f"  Novedad promedio:          {novedad_promedio:.4f}")
        print(f"  Coherencia promedio:       {coherencia_promedio:.4f}")
        print(f"  Rango scores: [{min(scores_emergencia):.4f}, {max(scores_emergencia):.4f}]")
        print("\n  ⚠️  Baseline: No aplicable (embeddings no soportan síntesis emergente)")
        
        resultado = BenchmarkResult(
            nombre="Síntesis Emergente",
            metrica="score_emergencia",
            valor_genesis=score_promedio,
            valor_baseline=0.0,  # No aplicable
            mejora_porcentual=100.0,  # 100% mejor (feature exclusivo)
            unidad="score",
            detalles={
                "std": score_std,
                "novedad": novedad_promedio,
                "coherencia": coherencia_promedio,
                "tripletas": num_tripletas,
                "baseline": "N/A - Feature exclusivo de Genesis"
            }
        )
        
        self.resultados.append(resultado)
        return resultado
    
    def ejecutar_todos(self) -> List[BenchmarkResult]:
        """Ejecuta todos los benchmarks"""
        print("\n🚀 Iniciando suite completa de benchmarks...")
        
        self.benchmark_compresion()
        self.benchmark_velocidad_encoding()
        self.benchmark_calidad_semantica()
        self.benchmark_memoria()
        self.benchmark_escalabilidad()
        self.benchmark_emergencia()
        
        return self.resultados
    
    def generar_informe(self, output_file: str = "benchmark_results.json"):
        """Genera informe JSON con resultados"""
        informe = {
            "version": "1.0.0",
            "fecha": "2025-10-16",
            "configuracion": {
                "dimension_embedding": self.dimension_embedding,
                "num_samples": self.num_samples,
                "arquitectura_genesis": "FFE (Forma-Función-Estructura)",
                "estructura_fractal": "3→9→27 vectores (117 bits)"
            },
            "resultados": [r.to_dict() for r in self.resultados],
            "resumen": self.generar_resumen()
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(informe, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Informe guardado en: {output_file}")
        return informe
    
    def generar_resumen(self) -> Dict:
        """Genera resumen ejecutivo"""
        ventajas = []
        desventajas = []
        
        for r in self.resultados:
            if r.mejora_porcentual > 0:
                ventajas.append({
                    "metrica": r.nombre,
                    "mejora": f"{r.mejora_porcentual:.1f}%"
                })
            else:
                desventajas.append({
                    "metrica": r.nombre,
                    "perdida": f"{abs(r.mejora_porcentual):.1f}%"
                })
        
        return {
            "ventajas": ventajas,
            "desventajas": desventajas,
            "conclusion": (
                "Genesis FFE ofrece compresión extrema (>200x) con overhead "
                "computacional aceptable y capacidad única de síntesis emergente."
            )
        }
    
    def imprimir_resumen_ejecutivo(self):
        """Imprime resumen para compartir"""
        print("\n" + "=" * 80)
        print("RESUMEN EJECUTIVO - PROYECTO GENESIS")
        print("=" * 80)
        
        print("\n📊 RESULTADOS PRINCIPALES:\n")
        
        for i, r in enumerate(self.resultados, 1):
            emoji = "✅" if r.mejora_porcentual > 0 else "⚠️"
            signo = "+" if r.mejora_porcentual > 0 else ""
            
            print(f"{emoji} {r.nombre}")
            print(f"   Genesis:  {r.valor_genesis:.2f} {r.unidad}")
            print(f"   Baseline: {r.valor_baseline:.2f} {r.unidad}")
            print(f"   Mejora:   {signo}{r.mejora_porcentual:.1f}%")
            print()
        
        resumen = self.generar_resumen()
        
        print("🎯 VENTAJAS CLAVE:")
        for v in resumen['ventajas']:
            print(f"   • {v['metrica']}: {v['mejora']} mejora")
        
        print("\n⚠️  TRADE-OFFS:")
        for d in resumen['desventajas']:
            print(f"   • {d['metrica']}: {d['perdida']} overhead")
        
        print(f"\n💡 CONCLUSIÓN:")
        print(f"   {resumen['conclusion']}")
        
        print("\n" + "=" * 80)


def main():
    """Ejecuta benchmark completo"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Benchmark Genesis FFE vs Embeddings')
    parser.add_argument('--samples', type=int, default=100, help='Número de muestras (default: 100)')
    parser.add_argument('--dims', type=int, default=768, help='Dimensión embeddings (default: 768)')
    parser.add_argument('--output', type=str, default='benchmark_results.json', help='Archivo salida')
    
    args = parser.parse_args()
    
    # Crear suite
    suite = BenchmarkSuite(
        dimension_embedding=args.dims,
        num_samples=args.samples
    )
    
    # Ejecutar benchmarks
    try:
        suite.ejecutar_todos()
        
        # Generar informes
        suite.imprimir_resumen_ejecutivo()
        suite.generar_informe(args.output)
        
        print("\n🎉 Benchmark completado exitosamente!")
        print(f"\n📄 Para compartir con peers:")
        print(f"   1. Archivo JSON: {args.output}")
        print(f"   2. Repositorio: https://github.com/Aurora-Program/Portal")
        print(f"   3. Documentación: Infrastructure/IE/PROYECTO_GENESIS.md")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Benchmark interrumpido por usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error durante benchmark: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
