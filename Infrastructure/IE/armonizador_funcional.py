"""
Armonizador Funcional Puro - Estilo Redux 🔄
Proyecto Genesis v1.3 - Aurora Intelligence Engine

Principios funcionales:
1. Funciones puras (sin efectos secundarios)
2. Inmutabilidad (copy-on-write)
3. Datos como valores (no referencias)
4. Composición (pipeline de transformaciones)

Performance:
- Sin race conditions (thread-safe por diseño)
- Cache inmutable (sin locks necesarios)
- Paralelización natural (sin side effects)
- Predictible y testeable

Mantiene filosofía Aurora:
- Solo geometría fractal FFE
- Rotación Fibonacci
- Síntesis emergente
- NO embeddings, NO cosine similarity
"""

from typing import List, Dict, Tuple, Optional, Set, NamedTuple
from dataclasses import dataclass, field, replace
import numpy as np
from enum import Enum
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import lru_cache, reduce
from copy import deepcopy
import threading

from tensor_ffe import TensorFFE, VectorFFE
from transcender import Transcender, Emergencia
from evolver import Evolver, Arquetipo, Relator
from armonizador import (
    TipoIncoherencia, 
    Incoherencia, 
    CorreccionPropuesta,
    AprendizajeError,
    Armonizador
)


# ============================================================================
# TIPOS INMUTABLES (Redux-style State)
# ============================================================================

class CacheKey(NamedTuple):
    """Clave inmutable para cache"""
    tensor_id: Tuple[Tuple[int, int, int], ...]  # Tuple de tuples
    paso: int
    
    @staticmethod
    def from_tensor(tensor: TensorFFE, paso: int) -> 'CacheKey':
        """Crea clave desde tensor"""
        nivel1_tuple = tuple(
            (v.forma, v.funcion, v.estructura) 
            for v in tensor.nivel_1
        )
        return CacheKey(tensor_id=nivel1_tuple, paso=paso)


@dataclass(frozen=True)  # Inmutable
class CacheEntry:
    """Entrada de cache inmutable"""
    key: CacheKey
    tensor: TensorFFE
    timestamp: float


@dataclass(frozen=True)  # Inmutable
class ArmonizacionState:
    """Estado inmutable de armonización (Redux-style)"""
    tensores: Tuple[TensorFFE, ...]  # Inmutable
    incoherencias: Tuple[Incoherencia, ...]  # Inmutable
    correcciones: Tuple[Optional[CorreccionPropuesta], ...]  # Inmutable
    aprendizajes: Tuple[AprendizajeError, ...]  # Inmutable
    cache_rotaciones: Dict[CacheKey, TensorFFE]  # Nuevo dict cada vez
    stats: Dict[str, any]  # Nuevo dict cada vez
    
    def with_correcciones(self, correcciones: List[Optional[CorreccionPropuesta]]) -> 'ArmonizacionState':
        """Retorna nuevo estado con correcciones (copy-on-write)"""
        return replace(self, correcciones=tuple(correcciones))
    
    def with_aprendizajes(self, aprendizajes: List[AprendizajeError]) -> 'ArmonizacionState':
        """Retorna nuevo estado con aprendizajes"""
        return replace(self, aprendizajes=tuple(aprendizajes))
    
    def with_stats(self, new_stats: Dict) -> 'ArmonizacionState':
        """Retorna nuevo estado con stats actualizados"""
        merged_stats = {**self.stats, **new_stats}  # Merge inmutable
        return replace(self, stats=merged_stats)


# ============================================================================
# FUNCIONES PURAS (sin efectos secundarios)
# ============================================================================

def rotar_vector_puro(vector: VectorFFE, paso: int) -> VectorFFE:
    """
    Rota vector FFE de forma pura (sin mutación)
    
    Args:
        vector: Vector a rotar (no se modifica)
        paso: Paso Fibonacci (0-7)
    
    Returns:
        Nuevo vector rotado
    """
    return VectorFFE(
        forma=(vector.forma + paso) % 8,
        funcion=(vector.funcion + paso) % 8,
        estructura=(vector.estructura + paso) % 8
    )


def rotar_tensor_puro(tensor: TensorFFE, paso: int) -> TensorFFE:
    """
    Rota tensor de forma pura (sin mutación)
    
    Args:
        tensor: Tensor a rotar (no se modifica)
        paso: Paso Fibonacci (0-7)
    
    Returns:
        Nuevo tensor rotado
    """
    # Composición funcional: map rotación a todos los vectores
    vectores_rotados = [
        rotar_vector_puro(v, paso) 
        for v in tensor.nivel_1
    ]
    return TensorFFE(vectores_rotados)


def rotar_tensor_cached_puro(
    tensor: TensorFFE, 
    paso: int,
    cache: Dict[CacheKey, TensorFFE]
) -> Tuple[TensorFFE, Dict[CacheKey, TensorFFE]]:
    """
    Rota tensor con cache PURO (retorna nuevo cache)
    
    Args:
        tensor: Tensor a rotar
        paso: Paso Fibonacci
        cache: Cache actual (no se modifica)
    
    Returns:
        (tensor_rotado, nuevo_cache)
    """
    key = CacheKey.from_tensor(tensor, paso)
    
    if key in cache:
        # Cache hit - retornar tensor y mismo cache
        return cache[key], cache
    
    # Cache miss - calcular rotación
    tensor_rotado = rotar_tensor_puro(tensor, paso)
    
    # Crear nuevo cache con entrada adicional (copy-on-write)
    nuevo_cache = {**cache, key: tensor_rotado}
    
    return tensor_rotado, nuevo_cache


def generar_variantes_fibonacci_puro(
    tensor: TensorFFE,
    fibonacci: List[int],
    paso_actual: int,
    cache: Dict[CacheKey, TensorFFE]
) -> Tuple[List[TensorFFE], Dict[CacheKey, TensorFFE]]:
    """
    Genera 3 variantes Fibonacci de forma pura
    
    Args:
        tensor: Tensor origen
        fibonacci: Secuencia Fibonacci
        paso_actual: Paso actual
        cache: Cache actual
    
    Returns:
        (lista_variantes, nuevo_cache)
    """
    variantes = []
    cache_actual = cache
    
    for i in range(3):
        idx_fib = (paso_actual + i) % len(fibonacci)
        paso = fibonacci[idx_fib] % 8
        
        # Rotar con cache puro
        variante, cache_actual = rotar_tensor_cached_puro(
            tensor, paso, cache_actual
        )
        variantes.append(variante)
    
    return variantes, cache_actual


def evaluar_coherencia_tensor_puro(
    tensor: TensorFFE,
    evolver: Evolver,
    umbral: float
) -> float:
    """
    Evalúa coherencia de tensor de forma pura
    (no modifica evolver - solo lectura)
    
    Args:
        tensor: Tensor a evaluar
        evolver: Evolver (solo lectura)
        umbral: Umbral de coherencia
    
    Returns:
        Score de coherencia [0.0, 1.0]
    """
    # Heurística simple: distancia mínima a arquetipos
    if not evolver.archetype_learner.arquetipos:
        return 0.5
    
    distancias = []
    for arq in evolver.archetype_learner.arquetipos.values():
        dist = sum(
            v1.distancia(v2) 
            for v1, v2 in zip(tensor.nivel_1, arq.tensor_prototipo.nivel_1)
        )
        distancias.append(dist)
    
    if not distancias:
        return 0.5
    
    min_dist = min(distancias)
    max_dist = 3 * 7 * 3  # Máxima distancia posible
    
    coherencia = 1.0 - (min_dist / max_dist)
    return coherencia


def corregir_incoherencia_puro(
    incoherencia: Incoherencia,
    fibonacci: List[int],
    paso_actual: int,
    evolver: Evolver,
    transcender: Transcender,
    umbral: float,
    cache: Dict[CacheKey, TensorFFE]
) -> Tuple[Optional[CorreccionPropuesta], Dict[CacheKey, TensorFFE]]:
    """
    Corrige incoherencia de forma pura (sin efectos secundarios)
    
    Args:
        incoherencia: Incoherencia a corregir
        fibonacci: Secuencia Fibonacci
        paso_actual: Paso actual
        evolver: Evolver (solo lectura)
        transcender: Transcender (solo lectura)
        umbral: Umbral de coherencia
        cache: Cache actual
    
    Returns:
        (correccion_o_none, nuevo_cache)
    """
    if incoherencia.tensor_origen is None:
        return None, cache
    
    # Generar variantes con cache puro
    variantes, cache_nuevo = generar_variantes_fibonacci_puro(
        incoherencia.tensor_origen,
        fibonacci,
        paso_actual,
        cache
    )
    
    mejor_correccion = None
    mejor_coherencia = 0.0
    
    # Evaluar cada variante (puro - sin side effects)
    for i, variante in enumerate(variantes):
        coherencia = evaluar_coherencia_tensor_puro(variante, evolver, umbral)
        
        if coherencia >= umbral and coherencia > mejor_coherencia:
            # Calcular costo (puro)
            costo = sum(
                v1.distancia(v2)
                for v1, v2 in zip(
                    incoherencia.tensor_origen.nivel_1,
                    variante.nivel_1
                )
            ) / (3 * 7 * 3)
            
            correccion = CorreccionPropuesta(
                incoherencia=incoherencia,
                tensor_corregido=variante,
                coherencia_resultante=coherencia,
                pasos_recursivos=0,
                camino_fibonacci=[fibonacci[(paso_actual + i) % len(fibonacci)]],
                costo_correccion=costo
            )
            
            mejor_coherencia = coherencia
            mejor_correccion = correccion
    
    return mejor_correccion, cache_nuevo


# ============================================================================
# REDUCER (Redux-style)
# ============================================================================

def reducir_correcciones(
    state: ArmonizacionState,
    correcciones: List[Optional[CorreccionPropuesta]]
) -> ArmonizacionState:
    """
    Reducer: aplica correcciones al estado (retorna nuevo estado)
    
    Args:
        state: Estado actual (no se modifica)
        correcciones: Lista de correcciones
    
    Returns:
        Nuevo estado con correcciones aplicadas
    """
    return state.with_correcciones(correcciones)


def reducir_aprendizajes(
    state: ArmonizacionState,
    aprendizajes: List[AprendizajeError]
) -> ArmonizacionState:
    """
    Reducer: aplica aprendizajes al estado
    
    Args:
        state: Estado actual
        aprendizajes: Lista de aprendizajes
    
    Returns:
        Nuevo estado con aprendizajes
    """
    return state.with_aprendizajes(aprendizajes)


def reducir_stats(
    state: ArmonizacionState,
    delta_stats: Dict
) -> ArmonizacionState:
    """
    Reducer: actualiza estadísticas
    
    Args:
        state: Estado actual
        delta_stats: Estadísticas a actualizar
    
    Returns:
        Nuevo estado con stats actualizados
    """
    return state.with_stats(delta_stats)


# ============================================================================
# ARMONIZADOR FUNCIONAL (Redux-style)
# ============================================================================

class ArmonizadorFuncional(Armonizador):
    """
    Armonizador funcional puro usando principios Redux
    
    Ventajas:
    - Sin race conditions (inmutabilidad)
    - Thread-safe por diseño
    - Paralelización natural
    - Predictible y testeable
    - Sin locks necesarios
    """
    
    def __init__(
        self,
        evolver: Evolver,
        transcender: Transcender,
        umbral_coherencia: float = 0.7,
        max_recursion: int = 10,
        num_workers: int = 4,
        batch_size: int = 50
    ):
        super().__init__(evolver, transcender, umbral_coherencia, max_recursion)
        self.num_workers = num_workers
        self.batch_size = batch_size
    
    def corregir_lote_puro(
        self,
        incoherencias: List[Incoherencia],
        cache_inicial: Optional[Dict[CacheKey, TensorFFE]] = None
    ) -> Tuple[List[Optional[CorreccionPropuesta]], Dict[CacheKey, TensorFFE], Dict]:
        """
        Corrige lote de incoherencias de forma pura (thread-safe)
        
        Args:
            incoherencias: Lista de incoherencias
            cache_inicial: Cache inicial (opcional)
        
        Returns:
            (correcciones, cache_final, stats)
        """
        import time
        inicio = time.time()
        
        # Estado inicial inmutable
        cache = cache_inicial or {}
        
        # Priorizar por severidad (funcional - no muta)
        incoherencias_ordenadas = sorted(
            incoherencias,
            key=lambda i: i.nivel_severidad,
            reverse=True
        )
        
        correcciones = []
        cache_hits = 0
        cache_misses = 0
        
        # Procesar en batches
        for batch_start in range(0, len(incoherencias_ordenadas), self.batch_size):
            batch_end = min(batch_start + self.batch_size, len(incoherencias_ordenadas))
            batch = incoherencias_ordenadas[batch_start:batch_end]
            
            # Cada thread trabaja con su propio cache local (copy)
            # Al final se mergean (sin conflictos por diseño)
            batch_correcciones = []
            batch_caches = []
            
            with ThreadPoolExecutor(max_workers=self.num_workers) as executor:
                # Crear tareas puras (sin side effects)
                futures = []
                for inc in batch:
                    future = executor.submit(
                        corregir_incoherencia_puro,
                        inc,
                        self.fibonacci,
                        self.paso_armonizacion,
                        self.evolver,
                        self.transcender,
                        self.umbral_coherencia,
                        cache  # Cada thread lee del cache compartido (inmutable)
                    )
                    futures.append(future)
                
                # Recolectar resultados
                for future in as_completed(futures):
                    try:
                        correccion, cache_thread = future.result(timeout=30)
                        batch_correcciones.append(correccion)
                        batch_caches.append(cache_thread)
                    except Exception as e:
                        print(f"⚠️ Error: {e}")
                        batch_correcciones.append(None)
            
            # Merge caches (funcional - crear nuevo cache)
            for cache_thread in batch_caches:
                cache_size_antes = len(cache)
                cache = {**cache, **cache_thread}  # Merge inmutable
                cache_size_despues = len(cache)
                
                # Actualizar stats
                nuevas_entradas = cache_size_despues - cache_size_antes
                if nuevas_entradas > 0:
                    cache_misses += nuevas_entradas
                else:
                    cache_hits += 1
            
            correcciones.extend(batch_correcciones)
        
        # Stats finales
        tiempo_total = time.time() - inicio
        stats = {
            'cache_hits': cache_hits,
            'cache_misses': cache_misses,
            'cache_size': len(cache),
            'correcciones_exitosas': sum(1 for c in correcciones if c),
            'correcciones_fallidas': sum(1 for c in correcciones if not c),
            'tiempo_total': tiempo_total,
            'velocidad': len(incoherencias) / tiempo_total if tiempo_total > 0 else 0
        }
        
        return correcciones, cache, stats
    
    def armonizar_lote_funcional(
        self,
        tensores: List[TensorFFE],
        espacio_logico: str = "default"
    ) -> Dict:
        """
        Armoniza lote usando programación funcional pura
        
        Args:
            tensores: Tensores a armonizar
            espacio_logico: ID del espacio lógico
        
        Returns:
            Reporte de armonización
        """
        import time
        inicio_total = time.time()
        
        print(f"\n🔄 ARMONIZACIÓN FUNCIONAL ({len(tensores)} tensores)")
        print(f"⚙️ Workers: {self.num_workers}")
        print(f"📦 Batch size: {self.batch_size}")
        print()
        
        # 1. Detectar incoherencias (inmutable)
        print("[1/5] Detectando incoherencias...")
        inicio = time.time()
        incoherencias = self.detectar_incoherencias(tensores, espacio_logico)
        tiempo_deteccion = time.time() - inicio
        print(f"  ✅ {len(incoherencias)} detectadas en {tiempo_deteccion:.2f}s")
        
        if not incoherencias:
            print("\n✨ Sistema ya coherente")
            return {'coherente': True, 'tiempo_total': time.time() - inicio_total}
        
        # 2. Corregir con funciones puras (thread-safe)
        print(f"\n[2/5] Autocorrigiendo {len(incoherencias)} incoherencias...")
        correcciones, cache_final, stats = self.corregir_lote_puro(incoherencias)
        
        print(f"  ✅ {stats['correcciones_exitosas']}/{len(incoherencias)} corregidas")
        print(f"  ⚡ {stats['velocidad']:.1f} correcciones/s")
        
        # 3. Aprender (funcional)
        print(f"\n[3/5] Aprendiendo de errores...")
        aprendizajes = []
        for inc, corr in zip(incoherencias, correcciones):
            if corr:
                aprendizaje = self.aprender_de_error(inc, corr)
                aprendizajes.append(aprendizaje)
        print(f"  📚 {len(aprendizajes)} patrones aprendidos")
        
        # 4. Validar coherencia
        print(f"\n[4/5] Validando coherencia global...")
        incoherencias_restantes = self.detectar_incoherencias(tensores, espacio_logico)
        coherente = len(incoherencias_restantes) == 0
        
        # 5. Métricas
        print(f"\n[5/5] Calculando métricas...")
        coherencias = [c.coherencia_resultante for c in correcciones if c]
        coherencia_promedio = np.mean(coherencias) if coherencias else 0.0
        coherencia_max = max(coherencias) if coherencias else 0.0
        
        tiempo_total = time.time() - inicio_total
        cache_total = stats['cache_hits'] + stats['cache_misses']
        cache_hit_rate = (
            100 * stats['cache_hits'] / cache_total 
            if cache_total > 0 else 0
        )
        
        # Reporte
        print("\n" + "="*60)
        print("📊 REPORTE DE ARMONIZACIÓN FUNCIONAL")
        print("="*60)
        print(f"  Coherente: {'✅' if coherente else '❌'}")
        print(f"  Incoherencias: {len(incoherencias)}")
        print(f"  Correcciones exitosas: {stats['correcciones_exitosas']}")
        print(f"  Correcciones fallidas: {stats['correcciones_fallidas']}")
        print(f"  Aprendizajes: {len(aprendizajes)}")
        print()
        print(f"  Coherencia promedio: {coherencia_promedio:.3f}")
        print(f"  Coherencia máxima: {coherencia_max:.3f}")
        print()
        print(f"⚡ PERFORMANCE:")
        print(f"  Tiempo total: {tiempo_total:.2f}s")
        print(f"  Velocidad: {stats['velocidad']:.1f} correcciones/s")
        print(f"  Cache hit rate: {cache_hit_rate:.1f}%")
        print(f"  Cache size: {stats['cache_size']} entradas")
        print("="*60)
        
        return {
            'coherente': coherente,
            'incoherencias_detectadas': len(incoherencias),
            'correcciones_exitosas': stats['correcciones_exitosas'],
            'correcciones_fallidas': stats['correcciones_fallidas'],
            'aprendizajes': len(aprendizajes),
            'coherencia_promedio': coherencia_promedio,
            'coherencia_maxima': coherencia_max,
            'tiempo_total': tiempo_total,
            'velocidad': stats['velocidad'],
            'cache_hit_rate': cache_hit_rate,
            'cache_size': stats['cache_size']
        }
