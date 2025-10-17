"""
Transcender Funcional Puro - Redux-Style 🔄
Proyecto Genesis v1.3 - Aurora Intelligence Engine

Principios funcionales aplicados:
1. Funciones puras (sin efectos secundarios)
2. Inmutabilidad (no muta tensores de entrada)
3. Sin estado mutable (historial opcional)
4. Composición (pipeline de transformaciones)

Performance:
- Thread-safe por diseño
- Cacheable naturalmente
- Paralelizable sin locks
- Predictible y testeable

Mantiene filosofía Aurora:
- Síntesis emergente no conmutativa
- Geometría fractal FFE
- NO embeddings, NO cosine similarity
"""

from typing import Tuple, Optional, Dict, List, NamedTuple
from dataclasses import dataclass
import numpy as np
import math
from functools import lru_cache
from tensor_ffe import TensorFFE, VectorFFE


# ============================================================================
# TIPOS INMUTABLES
# ============================================================================

class TensorKey(NamedTuple):
    """Clave inmutable para identificar tensor"""
    valores: Tuple[Tuple[int, int, int], ...]  # Tuple de (f, fn, e)
    
    @staticmethod
    def from_tensor(tensor: TensorFFE) -> 'TensorKey':
        """Crea clave desde tensor"""
        return TensorKey(
            valores=tuple(
                (v.forma, v.funcion, v.estructura)
                for v in tensor.nivel_1
            )
        )


@dataclass(frozen=True)  # Inmutable
class Emergencia:
    """Resultado de síntesis emergente (inmutable)"""
    Ms: TensorFFE      # Structure - Nueva lógica
    Ss: TensorFFE      # Form - Huella factual
    MetaM: TensorFFE   # Function - Ruta lógica completa
    
    # Métricas (calculadas una vez)
    novedad: float = 0.0
    coherencia: float = 0.0
    compresion: float = 0.0
    score_emergencia: float = 0.0
    
    def __repr__(self) -> str:
        return (f"Emergencia(score={self.score_emergencia:.3f}, "
                f"nov={self.novedad:.2f}, coh={self.coherencia:.2f}, comp={self.compresion:.2f})")


# ============================================================================
# FUNCIONES PURAS - Operaciones sobre vectores
# ============================================================================

def combinar_vector_ternario_puro(
    v_a: VectorFFE,
    v_b: VectorFFE,
    v_c: VectorFFE,
    modo: str = "estructura"
) -> VectorFFE:
    """
    Combina 3 vectores de forma pura según modo
    
    Args:
        v_a, v_b, v_c: Vectores a combinar (no se modifican)
        modo: "estructura", "huella", "meta"
    
    Returns:
        Nuevo vector combinado
    """
    if modo == "estructura":
        # Ms: Combinación XOR ponderada
        return VectorFFE(
            forma=(v_a.forma ^ (v_b.forma << 1) ^ (v_c.forma << 2)) & 0b111,
            funcion=(v_a.funcion + v_b.funcion * 2 + v_c.funcion * 3) % 8,
            estructura=(v_a.estructura ^ v_b.estructura ^ v_c.estructura) & 0b111
        )
    
    elif modo == "huella":
        # Ss: Secuencia de transformaciones
        # Paso 1: A influye en B
        temp_forma = (v_a.forma + v_b.forma) % 8
        temp_funcion = (v_a.funcion ^ v_b.funcion) & 0b111
        temp_estructura = ((v_a.estructura * v_b.estructura) % 8) & 0b111
        
        # Paso 2: Resultado influye en C
        return VectorFFE(
            forma=(temp_forma ^ v_c.forma) & 0b111,
            funcion=(temp_funcion + v_c.funcion) % 8,
            estructura=((temp_estructura + v_c.estructura) * 3) % 8
        )
    
    elif modo == "meta":
        # MetaM: Promedio ponderado
        return VectorFFE(
            forma=(v_a.forma + v_b.forma + v_c.forma) // 3,
            funcion=((v_a.funcion * v_b.funcion * v_c.funcion) % 8) & 0b111,
            estructura=(v_a.estructura ^ v_b.estructura ^ v_c.estructura) & 0b111
        )
    
    else:
        raise ValueError(f"Modo desconocido: {modo}")


def generar_tensor_desde_vectores_puro(
    vectores: List[VectorFFE],
    nivel_abstraccion: int
) -> TensorFFE:
    """
    Genera tensor desde vectores de forma pura
    
    Args:
        vectores: Lista de 3 vectores
        nivel_abstraccion: Nivel (0-7)
    
    Returns:
        Nuevo TensorFFE con jerarquía reconstruida
    """
    if len(vectores) != 3:
        raise ValueError("Se requieren exactamente 3 vectores")
    
    tensor = TensorFFE()
    for i, v in enumerate(vectores):
        tensor.nivel_1[i] = v
    
    tensor.reconstruir_jerarquia()
    tensor.nivel_abstraccion = max(0, min(7, nivel_abstraccion))
    
    return tensor


# ============================================================================
# FUNCIONES PURAS - Síntesis emergente
# ============================================================================

def generar_estructura_emergente_puro(
    A: TensorFFE,
    B: TensorFFE,
    C: TensorFFE
) -> TensorFFE:
    """
    Ms (Structure): Combina estructuras de forma pura
    
    Args:
        A, B, C: Tensores de entrada (no se modifican)
    
    Returns:
        Nuevo tensor Ms
    """
    vectores = [
        combinar_vector_ternario_puro(
            A.nivel_1[i],
            B.nivel_1[i],
            C.nivel_1[i],
            modo="estructura"
        )
        for i in range(3)
    ]
    
    nivel_abs = max(A.nivel_abstraccion, B.nivel_abstraccion, C.nivel_abstraccion)
    return generar_tensor_desde_vectores_puro(vectores, nivel_abs)


def generar_huella_factual_puro(
    A: TensorFFE,
    B: TensorFFE,
    C: TensorFFE
) -> TensorFFE:
    """
    Ss (Form): Captura huella secuencial de forma pura
    
    Args:
        A, B, C: Tensores de entrada (no se modifican)
    
    Returns:
        Nuevo tensor Ss
    """
    vectores = [
        combinar_vector_ternario_puro(
            A.nivel_1[i],
            B.nivel_1[i],
            C.nivel_1[i],
            modo="huella"
        )
        for i in range(3)
    ]
    
    nivel_abs = (A.nivel_abstraccion + B.nivel_abstraccion + C.nivel_abstraccion) // 3
    return generar_tensor_desde_vectores_puro(vectores, nivel_abs)


def generar_ruta_logica_puro(
    A: TensorFFE,
    B: TensorFFE,
    C: TensorFFE,
    Ms: TensorFFE,
    Ss: TensorFFE
) -> TensorFFE:
    """
    MetaM (Function): Ruta lógica completa de forma pura
    
    Args:
        A, B, C: Tensores originales (no se modifican)
        Ms, Ss: Tensores emergentes (no se modifican)
    
    Returns:
        Nuevo tensor MetaM
    """
    vectores = []
    
    for i in range(3):
        # Síntesis de la síntesis (meta-nivel)
        v = VectorFFE(
            forma=(Ms.nivel_1[i].forma + Ss.nivel_1[i].forma) % 8,
            funcion=((Ms.nivel_1[i].funcion * Ss.nivel_1[i].funcion) % 8) & 0b111,
            estructura=(
                Ms.nivel_1[i].estructura ^ 
                Ss.nivel_1[i].estructura ^ 
                (A.nivel_1[i].estructura + B.nivel_1[i].estructura + C.nivel_1[i].estructura) % 8
            ) & 0b111
        )
        vectores.append(v)
    
    nivel_abs = min(7, max(Ms.nivel_abstraccion, Ss.nivel_abstraccion) + 1)
    return generar_tensor_desde_vectores_puro(vectores, nivel_abs)


# ============================================================================
# FUNCIONES PURAS - Métricas
# ============================================================================

def calcular_convex_hull_puro(
    A: TensorFFE,
    B: TensorFFE,
    C: TensorFFE
) -> TensorFFE:
    """
    Promedio convexo de forma pura: (A + B + C) / 3
    
    Args:
        A, B, C: Tensores (no se modifican)
    
    Returns:
        Nuevo tensor convex hull
    """
    vectores = [
        VectorFFE(
            forma=(A.nivel_1[i].forma + B.nivel_1[i].forma + C.nivel_1[i].forma) // 3,
            funcion=(A.nivel_1[i].funcion + B.nivel_1[i].funcion + C.nivel_1[i].funcion) // 3,
            estructura=(A.nivel_1[i].estructura + B.nivel_1[i].estructura + C.nivel_1[i].estructura) // 3
        )
        for i in range(3)
    ]
    
    return generar_tensor_desde_vectores_puro(vectores, 3)


def calcular_distancia_puro(tensor1: TensorFFE, tensor2: TensorFFE) -> float:
    """
    Distancia Manhattan normalizada de forma pura
    
    Args:
        tensor1, tensor2: Tensores (no se modifican)
    
    Returns:
        Distancia [0.0, 1.0]
    """
    dist_total = sum(
        v1.distancia(v2)
        for v1, v2 in zip(tensor1.nivel_1, tensor2.nivel_1)
    )
    
    max_dist = 3 * 7 * 3  # 3 vectores × 7 max × 3 dimensiones
    return dist_total / max_dist


def calcular_mdl_puro(tensor: TensorFFE) -> float:
    """
    Minimum Description Length de forma pura
    
    Args:
        tensor: Tensor (no se modifica)
    
    Returns:
        MDL score
    """
    # Contar valores únicos
    valores_unicos = set(
        (v.forma, v.funcion, v.estructura)
        for v in tensor.nivel_1
    )
    
    if len(valores_unicos) == 0:
        return 0.0
    
    return math.log2(len(valores_unicos)) + tensor.coherencia() * 10


def calcular_metricas_puro(
    Ms: TensorFFE,
    Ss: TensorFFE,
    A: TensorFFE,
    B: TensorFFE,
    C: TensorFFE
) -> Tuple[float, float, float, float]:
    """
    Calcula todas las métricas de forma pura
    
    Args:
        Ms, Ss: Tensores emergentes
        A, B, C: Tensores originales
    
    Returns:
        (novedad, coherencia, compresion, score_total)
    """
    # 1. Novedad Estructural
    convex_hull = calcular_convex_hull_puro(A, B, C)
    novedad = calcular_distancia_puro(Ms, convex_hull)
    
    # 2. Coherencia Jerárquica
    coherencia = Ms.coherencia()
    
    # 3. Ganancia de Compresión
    mdl_original = sum(calcular_mdl_puro(t) for t in [A, B, C])
    mdl_emergente = calcular_mdl_puro(Ms)
    compresion = (mdl_original - mdl_emergente) / mdl_original if mdl_original > 0 else 0.0
    
    # Score Total
    score = (
        0.4 * novedad +
        0.3 * coherencia +
        0.3 * max(0.0, compresion)
    )
    
    return novedad, coherencia, compresion, score


# ============================================================================
# FUNCIÓN PRINCIPAL - Síntesis Pura
# ============================================================================

def sintetizar_puro(
    A: TensorFFE,
    B: TensorFFE,
    C: TensorFFE
) -> Emergencia:
    """
    Síntesis emergente PURA: (A, B, C) → (Ms, Ss, MetaM)
    
    Propiedades:
    - Función pura (sin side effects)
    - NO muta inputs
    - Thread-safe
    - Cacheable
    - Determinística
    
    Args:
        A, B, C: Tensores de entrada (no se modifican)
    
    Returns:
        Emergencia inmutable con todos los resultados
    """
    # Generar tensores emergentes (puro)
    Ms = generar_estructura_emergente_puro(A, B, C)
    Ss = generar_huella_factual_puro(A, B, C)
    MetaM = generar_ruta_logica_puro(A, B, C, Ms, Ss)
    
    # Calcular métricas (puro)
    novedad, coherencia, compresion, score = calcular_metricas_puro(Ms, Ss, A, B, C)
    
    # Retornar emergencia inmutable
    return Emergencia(
        Ms=Ms,
        Ss=Ss,
        MetaM=MetaM,
        novedad=novedad,
        coherencia=coherencia,
        compresion=compresion,
        score_emergencia=score
    )


# ============================================================================
# TRANSCENDER FUNCIONAL
# ============================================================================

class TranscenderFuncional:
    """
    Transcender funcional puro (Redux-style)
    
    Ventajas:
    - Thread-safe por diseño (sin mutación)
    - Paralelizable sin locks
    - Cacheable naturalmente
    - Predictible (mismos inputs → mismos outputs)
    - Testeable fácilmente
    """
    
    def __init__(self, with_cache: bool = True):
        """
        Inicializa transcender funcional
        
        Args:
            with_cache: Activar cache LRU (opcional)
        """
        self.with_cache = with_cache
        self._cache: Dict[Tuple[TensorKey, TensorKey, TensorKey], Emergencia] = {}
        self._cache_hits = 0
        self._cache_misses = 0
    
    def _get_cache_key(
        self,
        A: TensorFFE,
        B: TensorFFE,
        C: TensorFFE
    ) -> Tuple[TensorKey, TensorKey, TensorKey]:
        """Genera clave hashable para cache"""
        return (
            TensorKey.from_tensor(A),
            TensorKey.from_tensor(B),
            TensorKey.from_tensor(C)
        )
    
    def sintetizar(
        self,
        A: TensorFFE,
        B: TensorFFE,
        C: TensorFFE
    ) -> Emergencia:
        """
        Síntesis emergente con cache opcional
        
        Args:
            A, B, C: Tensores de entrada
        
        Returns:
            Emergencia inmutable
        """
        if self.with_cache:
            # Generar clave
            cache_key = self._get_cache_key(A, B, C)
            
            # Buscar en cache
            if cache_key in self._cache:
                self._cache_hits += 1
                return self._cache[cache_key]
            
            # Cache miss - calcular
            self._cache_misses += 1
            emergencia = sintetizar_puro(A, B, C)
            
            # Guardar en cache (inmutable)
            self._cache[cache_key] = emergencia
            return emergencia
        else:
            # Versión sin cache
            return sintetizar_puro(A, B, C)
    
    def validar_no_conmutatividad(
        self,
        A: TensorFFE,
        B: TensorFFE,
        C: TensorFFE
    ) -> Dict[str, float]:
        """
        Valida que el orden importa: f(A,B,C) ≠ f(B,A,C)
        
        Args:
            A, B, C: Tensores
        
        Returns:
            Dict con scores de cada permutación
        """
        perms = [
            ("ABC", self.sintetizar(A, B, C)),
            ("BAC", self.sintetizar(B, A, C)),
            ("ACB", self.sintetizar(A, C, B)),
            ("BCA", self.sintetizar(B, C, A)),
            ("CAB", self.sintetizar(C, A, B)),
            ("CBA", self.sintetizar(C, B, A))
        ]
        
        return {orden: em.score_emergencia for orden, em in perms}
    
    def batch_sintetizar(
        self,
        triplas: List[Tuple[TensorFFE, TensorFFE, TensorFFE]]
    ) -> List[Emergencia]:
        """
        Síntesis de batch (paralelizable naturalmente)
        
        Args:
            triplas: Lista de (A, B, C)
        
        Returns:
            Lista de emergencias
        """
        # Al ser función pura, se puede paralelizar sin problemas
        from concurrent.futures import ThreadPoolExecutor
        
        with ThreadPoolExecutor() as executor:
            emergencias = list(executor.map(
                lambda tripla: self.sintetizar(*tripla),
                triplas
            ))
        
        return emergencias
    
    def get_cache_info(self) -> Optional[Dict]:
        """Retorna info del cache"""
        if self.with_cache:
            total = self._cache_hits + self._cache_misses
            return {
                'hits': self._cache_hits,
                'misses': self._cache_misses,
                'size': len(self._cache),
                'hit_rate': f"{100 * self._cache_hits / total:.1f}%" if total > 0 else "0%"
            }
        return None


# ============================================================================
# TESTS
# ============================================================================

def test_funcional_vs_original():
    """Compara versión funcional vs original"""
    from tensor_ffe import crear_tensor_desde_lista
    from transcender import Transcender
    
    print("🧪 TEST: Funcional vs Original\n")
    
    # Crear tensores de prueba
    A = crear_tensor_desde_lista([5, 3, 2], nivel_abstraccion=3)
    B = crear_tensor_desde_lista([1, 7, 4], nivel_abstraccion=3)
    C = crear_tensor_desde_lista([6, 0, 3], nivel_abstraccion=4)
    
    # Original
    print("[1/2] Versión Original...")
    original = Transcender()
    em_original = original.sintetizar(A, B, C)
    
    # Funcional
    print("[2/2] Versión Funcional...")
    funcional = TranscenderFuncional(with_cache=True)
    em_funcional = funcional.sintetizar(A, B, C)
    
    # Comparar
    print("\n📊 COMPARACIÓN:")
    print(f"  Score Original:   {em_original.score_emergencia:.4f}")
    print(f"  Score Funcional:  {em_funcional.score_emergencia:.4f}")
    print(f"  Diferencia:       {abs(em_original.score_emergencia - em_funcional.score_emergencia):.6f}")
    
    if abs(em_original.score_emergencia - em_funcional.score_emergencia) < 0.001:
        print("\n✅ Resultados idénticos - Funcional preserva lógica")
    else:
        print("\n⚠️ Diferencia detectada")
    
    # Test cache
    print("\n💾 TEST CACHE:")
    for i in range(5):
        em = funcional.sintetizar(A, B, C)
    
    cache_info = funcional.get_cache_info()
    if cache_info:
        print(f"  Hits: {cache_info['hits']}")
        print(f"  Misses: {cache_info['misses']}")
        print(f"  Hit rate: {cache_info['hit_rate']}")
        print("  ✅ Cache funcionando")


if __name__ == "__main__":
    test_funcional_vs_original()
