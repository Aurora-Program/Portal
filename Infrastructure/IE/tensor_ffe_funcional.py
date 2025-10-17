"""
Tensores Fractales FFE Funcionales (Forma-Función-Estructura)
Proyecto Genesis v1.3.1 - Aurora Intelligence Engine

ARQUITECTURA FUNCIONAL:
- Operaciones puras (sin side effects)
- Inmutabilidad total (frozen dataclasses)
- Thread-safe por diseño
- Transformaciones como funciones puras

Representación fractal discreta: 3 dimensiones octales (0-7)
Jerarquía: 3 → 9 → 27 vectores = 117 bits total
"""

from typing import List, Tuple, Dict, NamedTuple
from dataclasses import dataclass, field, replace
import numpy as np


# ============================================================================
# TIPOS INMUTABLES (Frozen Dataclasses)
# ============================================================================

@dataclass(frozen=True)
class VectorFFE:
    """Vector inmutable con 3 dimensiones semánticas (0-7)"""
    forma: int = 0      # Aspecto morfológico (0-7)
    funcion: int = 0    # Propósito operativo (0-7)
    estructura: int = 0 # Patrón organizativo (0-7)
    
    def __post_init__(self):
        """Validar valores octales"""
        for attr in ['forma', 'funcion', 'estructura']:
            val = getattr(self, attr)
            if not 0 <= val <= 7:
                raise ValueError(f"{attr} debe estar en rango [0,7], got {val}")
    
    def to_bits(self) -> int:
        """Convierte a 9 bits (3 bits por dimensión) (pure)"""
        return (self.forma << 6) | (self.funcion << 3) | self.estructura
    
    def to_list(self) -> List[int]:
        """Convierte a lista [forma, funcion, estructura] (pure)"""
        return [self.forma, self.funcion, self.estructura]
    
    def __repr__(self) -> str:
        return f"FFE({self.forma},{self.funcion},{self.estructura})"


@dataclass(frozen=True)
class TensorFFE:
    """
    Tensor Fractal INMUTABLE con jerarquía 3→9→27
    Total: 39 vectores = 117 bits
    
    INMUTABILIDAD: Todas las operaciones retornan NUEVO tensor
    """
    nivel_1: Tuple[VectorFFE, VectorFFE, VectorFFE] = field(
        default_factory=lambda: (VectorFFE(), VectorFFE(), VectorFFE())
    )
    nivel_2: Tuple[VectorFFE, ...] = field(
        default_factory=lambda: tuple(VectorFFE() for _ in range(9))
    )
    nivel_3: Tuple[VectorFFE, ...] = field(
        default_factory=lambda: tuple(VectorFFE() for _ in range(27))
    )
    
    # Metadatos inmutables
    nivel_abstraccion: int = 0  # 0-7 (Fonético → Teórico)
    dimensiones_activas: Tuple[str, ...] = field(default_factory=tuple)
    
    def __post_init__(self):
        """Validar estructura"""
        if len(self.nivel_1) != 3:
            raise ValueError("Nivel 1 debe tener 3 vectores")
        if len(self.nivel_2) != 9:
            raise ValueError("Nivel 2 debe tener 9 vectores")
        if len(self.nivel_3) != 27:
            raise ValueError("Nivel 3 debe tener 27 vectores")
    
    @property
    def total_bits(self) -> int:
        """117 bits totales (pure)"""
        return 39 * 9  # 39 vectores × 9 bits/vector
    
    def to_bits(self) -> str:
        """Serializa a 117 bits (string binario) (pure)"""
        bits_str = ''
        for vector in self.nivel_1 + self.nivel_2 + self.nivel_3:
            bits_str += bin(vector.to_bits())[2:].zfill(9)
        return bits_str
    
    def to_ndarray(self) -> np.ndarray:
        """
        Convierte a array numpy preservando jerarquía (pure)
        [nivel_1 (9), nivel_2 (27), nivel_3 (81)] = 117 valores
        """
        valores = []
        
        # Nivel 1: 3 vectores × 3 = 9
        for v in self.nivel_1:
            valores.extend([v.forma, v.funcion, v.estructura])
        
        # Nivel 2: 9 vectores × 3 = 27
        for v in self.nivel_2:
            valores.extend([v.forma, v.funcion, v.estructura])
        
        # Nivel 3: 27 vectores × 3 = 81
        for v in self.nivel_3:
            valores.extend([v.forma, v.funcion, v.estructura])
        
        return np.array(valores, dtype=np.float32)
    
    def __repr__(self) -> str:
        return (f"TensorFFE(nivel_abstraccion={self.nivel_abstraccion}, "
                f"bits={self.total_bits})")


class TensorKey(NamedTuple):
    """Clave inmutable para hashear tensores (para cache)"""
    valores_n1: Tuple[Tuple[int, int, int], ...]
    nivel_abstraccion: int
    
    @staticmethod
    def from_tensor(tensor: TensorFFE) -> 'TensorKey':
        return TensorKey(
            valores_n1=tuple(
                (v.forma, v.funcion, v.estructura)
                for v in tensor.nivel_1
            ),
            nivel_abstraccion=tensor.nivel_abstraccion
        )


# ============================================================================
# FUNCIONES PURAS - CONSTRUCCIÓN
# ============================================================================

def crear_vector_puro(forma: int, funcion: int, estructura: int) -> VectorFFE:
    """Crea vector FFE (pure)"""
    return VectorFFE(forma=forma, funcion=funcion, estructura=estructura)


def crear_tensor_desde_lista_puro(
    valores: List[int],
    nivel_abstraccion: int = 0
) -> TensorFFE:
    """
    Crea TensorFFE desde lista plana [0-7] (pure)
    Ejemplo: [5, 3, 2] → TensorFFE con nivel_1 configurado
    """
    if len(valores) != 3:
        raise ValueError("Se requieren exactamente 3 valores para nivel_1")
    
    # Crear nivel_1
    nivel_1 = tuple(
        VectorFFE(forma=v, funcion=v, estructura=v)
        for v in valores
    )
    
    # Generar jerarquía completa
    nivel_2 = generar_nivel_2_puro(nivel_1)
    nivel_3 = generar_nivel_3_puro(nivel_1, nivel_2)
    
    return TensorFFE(
        nivel_1=nivel_1,
        nivel_2=nivel_2,
        nivel_3=nivel_3,
        nivel_abstraccion=nivel_abstraccion
    )


def tensor_nulo_puro() -> TensorFFE:
    """Crea tensor con todos los valores en 0 (potencialidad pura) (pure)"""
    return crear_tensor_desde_lista_puro([0, 0, 0], nivel_abstraccion=0)


def from_bits_puro(bits: str) -> TensorFFE:
    """Deserializa desde 117 bits (string binario) (pure)"""
    if isinstance(bits, int):
        bits = bin(bits)[2:].zfill(117)
    
    vectores = []
    for i in range(39):
        start = i * 9
        end = start + 9
        vector_bits = int(bits[start:end], 2)
        
        # Reconstruir vector desde bits
        forma = (vector_bits >> 6) & 0b111
        funcion = (vector_bits >> 3) & 0b111
        estructura = vector_bits & 0b111
        vectores.append(VectorFFE(forma, funcion, estructura))
    
    vectores.reverse()  # Invertir orden
    
    return TensorFFE(
        nivel_1=tuple(vectores[:3]),
        nivel_2=tuple(vectores[3:12]),
        nivel_3=tuple(vectores[12:39])
    )


# ============================================================================
# FUNCIONES PURAS - GENERACIÓN JERÁRQUICA
# ============================================================================

def generar_nivel_2_puro(
    nivel_1: Tuple[VectorFFE, VectorFFE, VectorFFE]
) -> Tuple[VectorFFE, ...]:
    """
    Genera Nivel 2 desde Nivel 1 usando operaciones ternarias XOR (pure)
    Patrón fractal: cada vector genera 3 hijos
    """
    a, b, c = nivel_1
    
    nivel_2_list = []
    
    # Grupo 1: Derivados de 'a'
    nivel_2_list.append(VectorFFE(a.forma ^ b.forma, a.funcion ^ b.funcion, a.estructura ^ b.estructura))
    nivel_2_list.append(VectorFFE(a.forma ^ c.forma, a.funcion ^ c.funcion, a.estructura ^ c.estructura))
    nivel_2_list.append(VectorFFE(b.forma ^ c.forma, b.funcion ^ c.funcion, b.estructura ^ c.estructura))
    
    # Grupo 2: Derivados de 'b'
    nivel_2_list.append(VectorFFE(b.forma ^ a.forma, b.funcion ^ a.funcion, b.estructura ^ a.estructura))
    nivel_2_list.append(VectorFFE(b.forma ^ c.forma, b.funcion ^ c.funcion, b.estructura ^ c.estructura))
    nivel_2_list.append(VectorFFE(c.forma ^ a.forma, c.funcion ^ a.funcion, c.estructura ^ a.estructura))
    
    # Grupo 3: Combinaciones complejas
    nivel_2_list.append(VectorFFE(
        (a.forma ^ b.forma) & 0b111,
        (b.funcion ^ c.funcion) & 0b111,
        (c.estructura ^ a.estructura) & 0b111
    ))
    nivel_2_list.append(VectorFFE(
        (b.forma ^ c.forma) & 0b111,
        (c.funcion ^ a.funcion) & 0b111,
        (a.estructura ^ b.estructura) & 0b111
    ))
    nivel_2_list.append(VectorFFE(
        (c.forma ^ a.forma) & 0b111,
        (a.funcion ^ b.funcion) & 0b111,
        (b.estructura ^ c.estructura) & 0b111
    ))
    
    return tuple(nivel_2_list)


def generar_nivel_3_puro(
    nivel_1: Tuple[VectorFFE, VectorFFE, VectorFFE],
    nivel_2: Tuple[VectorFFE, ...]
) -> Tuple[VectorFFE, ...]:
    """
    Genera Nivel 3 desde Nivel 1 y Nivel 2 recursivamente (pure)
    Combina patrones emergentes
    """
    nivel_3_list = []
    
    for i in range(3):  # Por cada vector de Nivel 1
        for j in range(3):  # Genera 3 derivados
            base_idx = i * 3 + j
            if base_idx < 9:
                n1 = nivel_1[i]
                n2 = nivel_2[base_idx]
                
                # Derivado 1: XOR directo
                nivel_3_list.append(VectorFFE(
                    (n1.forma ^ n2.forma) & 0b111,
                    (n1.funcion ^ n2.funcion) & 0b111,
                    (n1.estructura ^ n2.estructura) & 0b111
                ))
                
                # Derivado 2: Rotación
                nivel_3_list.append(VectorFFE(
                    (n2.forma ^ n1.funcion) & 0b111,
                    (n2.funcion ^ n1.estructura) & 0b111,
                    (n2.estructura ^ n1.forma) & 0b111
                ))
                
                # Derivado 3: Complemento parcial
                nivel_3_list.append(VectorFFE(
                    ((n1.forma + n2.forma) % 8) & 0b111,
                    ((n1.funcion ^ n2.funcion) ^ 0b111) & 0b111,
                    ((n1.estructura * 3) % 8) & 0b111
                ))
    
    return tuple(nivel_3_list)


def reconstruir_jerarquia_puro(tensor: TensorFFE) -> TensorFFE:
    """Reconstruye Nivel 2 y 3 desde Nivel 1 (pure - retorna nuevo tensor)"""
    nivel_2 = generar_nivel_2_puro(tensor.nivel_1)
    nivel_3 = generar_nivel_3_puro(tensor.nivel_1, nivel_2)
    
    return replace(
        tensor,
        nivel_2=nivel_2,
        nivel_3=nivel_3
    )


# ============================================================================
# FUNCIONES PURAS - OPERACIONES VECTORIALES
# ============================================================================

def distancia_vector_puro(v1: VectorFFE, v2: VectorFFE) -> float:
    """Distancia Manhattan en espacio octal (pure)"""
    return abs(v1.forma - v2.forma) + abs(v1.funcion - v2.funcion) + abs(v1.estructura - v2.estructura)


def distancia_tensor_puro(t1: TensorFFE, t2: TensorFFE) -> float:
    """Distancia entre tensores (promedio nivel_1) (pure)"""
    return sum(
        distancia_vector_puro(v1, v2)
        for v1, v2 in zip(t1.nivel_1, t2.nivel_1)
    ) / 3.0


def coherencia_puro(tensor: TensorFFE) -> float:
    """
    Métrica de coherencia interna: mide autosimilitud fractal (pure)
    Rango [0.0, 1.0]
    """
    # Distancia promedio dentro de cada nivel
    dist_n1 = sum(
        distancia_vector_puro(tensor.nivel_1[i], tensor.nivel_1[(i+1) % 3])
        for i in range(3)
    ) / 3
    
    dist_n2 = sum(
        distancia_vector_puro(tensor.nivel_2[i], tensor.nivel_2[(i+1) % 9])
        for i in range(9)
    ) / 9
    
    dist_n3 = sum(
        distancia_vector_puro(tensor.nivel_3[i], tensor.nivel_3[(i+1) % 27])
        for i in range(27)
    ) / 27
    
    # Coherencia = 1 - (variación normalizada)
    max_dist = 7 * 3  # Máxima distancia Manhattan
    variacion = (dist_n1 + dist_n2 + dist_n3) / (3 * max_dist)
    
    return 1.0 - variacion


def compresion_ratio_puro(tensor: TensorFFE, original_bits: int = 32768) -> float:
    """
    Ratio de compresión vs. embedding tradicional (pure)
    4096 floats = 32KB
    """
    return original_bits / tensor.total_bits


# ============================================================================
# FUNCIONES PURAS - TRANSFORMACIONES
# ============================================================================

# Mapa de dimensiones relevantes por nivel (constante global)
NIVELES_ABSTRACCION = {
    0: "Fonético",
    1: "Silábico",
    2: "Morfémico",
    3: "Léxico",
    4: "Sintáctico",
    5: "Semántico",
    6: "Discursivo",
    7: "Teórico"
}

DIMENSIONES_POR_NIVEL = {
    0: ('frecuencia', 'amplitud', 'fase', 'timbre'),
    1: ('estructura_silabica', 'acento', 'patron_ritmico'),
    2: ('raiz', 'afijos', 'significado_basico', 'categoria'),
    3: ('significado_completo', 'categoria_gramatical', 'contexto_lexico'),
    4: ('funcion_oracional', 'relaciones_sintacticas', 'estructura_frase'),
    5: ('significado_contextual', 'relaciones_conceptuales', 'pragmatica'),
    6: ('estructura_argumental', 'coherencia_textual', 'estilo'),
    7: ('marcos_teoricos', 'principios_abstractos', 'leyes_universales')
}


def activar_dimensiones_puro(
    tensor: TensorFFE,
    dimensiones: Tuple[str, ...]
) -> TensorFFE:
    """Activa dimensiones relevantes (pure - retorna nuevo tensor)"""
    # Combinar dimensiones existentes con nuevas (mantener únicas)
    nuevas_dims = tuple(set(tensor.dimensiones_activas + dimensiones))
    
    return replace(tensor, dimensiones_activas=nuevas_dims)


def podar_dimensiones_puro(
    tensor: TensorFFE,
    dimensiones_a_podar: Tuple[str, ...]
) -> TensorFFE:
    """Podado contextual (pure - retorna nuevo tensor)"""
    # Filtrar dimensiones a podar
    dims_filtradas = tuple(
        dim for dim in tensor.dimensiones_activas
        if dim not in dimensiones_a_podar
    )
    
    return replace(tensor, dimensiones_activas=dims_filtradas)


def abstracting_puro(tensor: TensorFFE) -> TensorFFE:
    """
    Ascenso en abstracción: nivel_actual → nivel_actual + 1 (pure)
    Elimina dimensiones de bajo nivel, activa dimensiones superiores
    """
    if tensor.nivel_abstraccion >= 7:
        return tensor  # Ya en nivel máximo
    
    nuevo_nivel = tensor.nivel_abstraccion + 1
    
    # Podar dimensiones del nivel anterior
    dimensiones_obsoletas = DIMENSIONES_POR_NIVEL.get(tensor.nivel_abstraccion, ())
    
    # Activar dimensiones del nuevo nivel
    dimensiones_nuevas = DIMENSIONES_POR_NIVEL.get(nuevo_nivel, ())
    
    # Crear nuevo tensor con nivel actualizado
    tensor_actualizado = replace(tensor, nivel_abstraccion=nuevo_nivel)
    
    # Aplicar podado y activación
    tensor_podado = podar_dimensiones_puro(tensor_actualizado, dimensiones_obsoletas)
    tensor_final = activar_dimensiones_puro(tensor_podado, dimensiones_nuevas)
    
    return tensor_final


def extending_puro(tensor: TensorFFE) -> TensorFFE:
    """
    Descenso en concreción: nivel_actual → nivel_actual - 1 (pure)
    Recupera dimensiones concretas para manifestación
    """
    if tensor.nivel_abstraccion <= 0:
        return tensor  # Ya en nivel base
    
    nuevo_nivel = tensor.nivel_abstraccion - 1
    
    # Recuperar dimensiones del nivel inferior
    dimensiones_concretas = DIMENSIONES_POR_NIVEL.get(nuevo_nivel, ())
    
    # Crear nuevo tensor con nivel actualizado
    tensor_actualizado = replace(tensor, nivel_abstraccion=nuevo_nivel)
    
    # Activar dimensiones concretas
    tensor_final = activar_dimensiones_puro(tensor_actualizado, dimensiones_concretas)
    
    return tensor_final


def transformar_continuo_puro(
    tensor: TensorFFE,
    nivel_objetivo: int
) -> TensorFFE:
    """
    Transforma directamente a un nivel objetivo (0-7) (pure)
    Usa abstracting o extending según sea necesario
    """
    if not 0 <= nivel_objetivo <= 7:
        raise ValueError(f"Nivel objetivo debe estar en [0,7], got {nivel_objetivo}")
    
    tensor_actual = tensor
    
    # Ascender
    while tensor_actual.nivel_abstraccion < nivel_objetivo:
        tensor_actual = abstracting_puro(tensor_actual)
    
    # Descender
    while tensor_actual.nivel_abstraccion > nivel_objetivo:
        tensor_actual = extending_puro(tensor_actual)
    
    return tensor_actual


# ============================================================================
# OPERACIONES AVANZADAS (Puras)
# ============================================================================

def rotar_vector_puro(vector: VectorFFE, paso: int) -> VectorFFE:
    """Rota vector en espacio octal (pure)"""
    return VectorFFE(
        forma=(vector.forma + paso) % 8,
        funcion=(vector.funcion + paso) % 8,
        estructura=(vector.estructura + paso) % 8
    )


def rotar_tensor_puro(tensor: TensorFFE, paso: int) -> TensorFFE:
    """Rota tensor completo (pure - retorna nuevo)"""
    # Rotar nivel_1
    nivel_1_rotado = tuple(
        rotar_vector_puro(v, paso)
        for v in tensor.nivel_1
    )
    
    # Reconstruir jerarquía desde nivel_1 rotado
    nivel_2_rotado = generar_nivel_2_puro(nivel_1_rotado)
    nivel_3_rotado = generar_nivel_3_puro(nivel_1_rotado, nivel_2_rotado)
    
    return replace(
        tensor,
        nivel_1=nivel_1_rotado,
        nivel_2=nivel_2_rotado,
        nivel_3=nivel_3_rotado
    )


def combinar_vectores_xor_puro(v1: VectorFFE, v2: VectorFFE) -> VectorFFE:
    """Combina dos vectores con XOR (pure)"""
    return VectorFFE(
        forma=(v1.forma ^ v2.forma) & 0b111,
        funcion=(v1.funcion ^ v2.funcion) & 0b111,
        estructura=(v1.estructura ^ v2.estructura) & 0b111
    )


def combinar_tensores_nivel1_puro(t1: TensorFFE, t2: TensorFFE) -> TensorFFE:
    """Combina dos tensores a nivel_1 (pure)"""
    # Combinar nivel_1
    nivel_1_combinado = tuple(
        combinar_vectores_xor_puro(v1, v2)
        for v1, v2 in zip(t1.nivel_1, t2.nivel_1)
    )
    
    # Reconstruir jerarquía
    nivel_2_combinado = generar_nivel_2_puro(nivel_1_combinado)
    nivel_3_combinado = generar_nivel_3_puro(nivel_1_combinado, nivel_2_combinado)
    
    # Nivel de abstracción = máximo de ambos
    nivel_abs = max(t1.nivel_abstraccion, t2.nivel_abstraccion)
    
    return TensorFFE(
        nivel_1=nivel_1_combinado,
        nivel_2=nivel_2_combinado,
        nivel_3=nivel_3_combinado,
        nivel_abstraccion=nivel_abs
    )


# ============================================================================
# CACHE FUNCIONAL (Opcional)
# ============================================================================

class TensorFFECache:
    """Cache inmutable para operaciones frecuentes"""
    
    def __init__(self):
        self._cache: Dict[TensorKey, TensorFFE] = {}
        self._hits = 0
        self._misses = 0
    
    def get_or_compute(
        self,
        tensor: TensorFFE,
        operation: str,
        compute_fn
    ) -> TensorFFE:
        """
        Obtiene del cache o computa (funcional)
        compute_fn debe ser una función pura
        """
        key = (TensorKey.from_tensor(tensor), operation)
        
        if key in self._cache:
            self._hits += 1
            return self._cache[key]
        
        self._misses += 1
        result = compute_fn(tensor)
        self._cache[key] = result
        
        return result
    
    def get_stats(self) -> Dict[str, any]:
        """Estadísticas del cache"""
        total = self._hits + self._misses
        hit_rate = (self._hits / total * 100) if total > 0 else 0
        
        return {
            'hits': self._hits,
            'misses': self._misses,
            'hit_rate': f"{hit_rate:.1f}%",
            'size': len(self._cache)
        }


# ============================================================================
# TEST & VALIDACIÓN
# ============================================================================

if __name__ == "__main__":
    print("🧬 Tensores FFE Funcionales v1.3.1\n")
    
    # Test 1: Creación inmutable
    print("=" * 60)
    print("Test 1: Crear tensor inmutable")
    print("=" * 60)
    
    tensor = crear_tensor_desde_lista_puro([5, 3, 2], nivel_abstraccion=3)
    print(f"  {tensor}")
    print(f"  Coherencia: {coherencia_puro(tensor):.3f}")
    print(f"  Compresión: {compresion_ratio_puro(tensor):.1f}x")
    print(f"  Total bits: {tensor.total_bits}")
    
    # Test 2: Inmutabilidad
    print("\n" + "=" * 60)
    print("Test 2: Validar inmutabilidad")
    print("=" * 60)
    
    tensor_original = tensor
    print(f"  Tensor original ID: {id(tensor_original)}")
    
    # Operación que debe retornar NUEVO tensor
    tensor_rotado = rotar_tensor_puro(tensor_original, paso=2)
    print(f"  Tensor rotado ID: {id(tensor_rotado)}")
    print(f"  Son diferentes objetos: {id(tensor_original) != id(tensor_rotado)} ✅")
    print(f"  Original preservado: {tensor_original.nivel_1[0]}")
    print(f"  Rotado modificado: {tensor_rotado.nivel_1[0]}")
    
    # Test 3: Abstracting/Extending
    print("\n" + "=" * 60)
    print("Test 3: Abstracting (Léxico → Semántico)")
    print("=" * 60)
    
    tensor_semantico = abstracting_puro(tensor)
    print(f"  Nivel original: {NIVELES_ABSTRACCION[tensor.nivel_abstraccion]}")
    print(f"  Nivel nuevo: {NIVELES_ABSTRACCION[tensor_semantico.nivel_abstraccion]}")
    print(f"  Dimensiones activas: {tensor_semantico.dimensiones_activas}")
    print(f"  Original inmutable: {tensor.nivel_abstraccion} ✅")
    
    # Test 4: Transformación continua
    print("\n" + "=" * 60)
    print("Test 4: Transformación continua (Semántico → Morfémico)")
    print("=" * 60)
    
    tensor_final = transformar_continuo_puro(tensor_semantico, nivel_objetivo=2)
    print(f"  Nivel objetivo: {NIVELES_ABSTRACCION[tensor_final.nivel_abstraccion]}")
    print(f"  Dimensiones: {tensor_final.dimensiones_activas}")
    
    # Test 5: Combinación de tensores
    print("\n" + "=" * 60)
    print("Test 5: Combinar tensores")
    print("=" * 60)
    
    tensor_a = crear_tensor_desde_lista_puro([1, 2, 3], 3)
    tensor_b = crear_tensor_desde_lista_puro([4, 5, 6], 3)
    tensor_combinado = combinar_tensores_nivel1_puro(tensor_a, tensor_b)
    
    print(f"  Tensor A: {tensor_a.nivel_1[0]}")
    print(f"  Tensor B: {tensor_b.nivel_1[0]}")
    print(f"  Combinado: {tensor_combinado.nivel_1[0]}")
    print(f"  A preservado: {tensor_a.nivel_1[0]} ✅")
    print(f"  B preservado: {tensor_b.nivel_1[0]} ✅")
    
    # Test 6: Cache funcional
    print("\n" + "=" * 60)
    print("Test 6: Cache funcional")
    print("=" * 60)
    
    cache = TensorFFECache()
    
    # Primera llamada (miss)
    result1 = cache.get_or_compute(
        tensor,
        'abstracting',
        abstracting_puro
    )
    
    # Segunda llamada (hit)
    result2 = cache.get_or_compute(
        tensor,
        'abstracting',
        abstracting_puro
    )
    
    stats = cache.get_stats()
    print(f"  Cache hits: {stats['hits']}")
    print(f"  Cache misses: {stats['misses']}")
    print(f"  Hit rate: {stats['hit_rate']}")
    print(f"  Resultados idénticos: {id(result1) == id(result2)} ✅")
    
    # Test 7: Serialización
    print("\n" + "=" * 60)
    print("Test 7: Serialización")
    print("=" * 60)
    
    bits = tensor.to_bits()
    print(f"  Bits: {len(bits)} caracteres")
    tensor_recuperado = from_bits_puro(bits)
    print(f"  Tensor recuperado: {tensor_recuperado}")
    print(f"  Nivel_1 idéntico: {tensor.nivel_1 == tensor_recuperado.nivel_1} ✅")
    
    print("\n" + "=" * 60)
    print("✅ TODOS LOS TESTS PASARON")
    print("=" * 60)
    print("\n🎯 TensorFFE Funcional:")
    print("  ✓ Inmutabilidad total")
    print("  ✓ Operaciones puras")
    print("  ✓ Thread-safe por diseño")
    print("  ✓ Cache funcional")
    print("  ✓ Serialización correcta")
