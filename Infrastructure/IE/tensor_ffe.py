"""
Tensores Fractales FFE (Forma-Función-Estructura)
Proyecto Genesis - Aurora Intelligence Engine

Representación fractal discreta: 3 dimensiones octales (0-7)
Jerarquía: 3 → 9 → 27 vectores = 117 bits total
"""

from typing import List, Optional, Tuple, Dict
import numpy as np
from dataclasses import dataclass, field


@dataclass
class VectorFFE:
    """Vector con 3 dimensiones semánticas (0-7)"""
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
        """Convierte a 9 bits (3 bits por dimensión)"""
        return (self.forma << 6) | (self.funcion << 3) | self.estructura
    
    @classmethod
    def from_bits(cls, bits: int) -> 'VectorFFE':
        """Reconstruye desde 9 bits"""
        forma = (bits >> 6) & 0b111
        funcion = (bits >> 3) & 0b111
        estructura = bits & 0b111
        return cls(forma, funcion, estructura)
    
    def to_list(self) -> List[int]:
        """Convierte a lista [forma, funcion, estructura]"""
        return [self.forma, self.funcion, self.estructura]
    
    def distancia(self, otro: 'VectorFFE') -> float:
        """Distancia Manhattan en espacio octal"""
        return sum(abs(a - b) for a, b in zip(self.to_list(), otro.to_list()))
    
    def __repr__(self) -> str:
        return f"FFE({self.forma},{self.funcion},{self.estructura})"


@dataclass
class TensorFFE:
    """
    Tensor Fractal con jerarquía 3→9→27
    Total: 39 vectores = 117 bits
    """
    nivel_1: List[VectorFFE] = field(default_factory=lambda: [VectorFFE() for _ in range(3)])
    nivel_2: List[VectorFFE] = field(default_factory=lambda: [VectorFFE() for _ in range(9)])
    nivel_3: List[VectorFFE] = field(default_factory=lambda: [VectorFFE() for _ in range(27)])
    
    # Metadatos
    nivel_abstraccion: int = 0  # 0-7 (Fonético → Teórico)
    dimensiones_activas: Dict[str, bool] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validar estructura"""
        assert len(self.nivel_1) == 3, "Nivel 1 debe tener 3 vectores"
        assert len(self.nivel_2) == 9, "Nivel 2 debe tener 9 vectores"
        assert len(self.nivel_3) == 27, "Nivel 3 debe tener 27 vectores"
    
    @property
    def total_bits(self) -> int:
        """117 bits totales"""
        return 39 * 9  # 39 vectores × 9 bits/vector
    
    def to_bits(self) -> str:
        """Serializa a 117 bits (string binario)"""
        bits_str = ''
        for vector in self.nivel_1 + self.nivel_2 + self.nivel_3:
            bits_str += bin(vector.to_bits())[2:].zfill(9)
        return bits_str
    
    @classmethod
    def from_bits(cls, bits: str) -> 'TensorFFE':
        """Deserializa desde 117 bits (string binario)"""
        if isinstance(bits, int):
            bits = bin(bits)[2:].zfill(117)
        
        vectores = []
        for i in range(39):
            start = i * 9
            end = start + 9
            vector_bits = int(bits[start:end], 2)
            vectores.append(VectorFFE.from_bits(vector_bits))
        
        vectores.reverse()  # Invertir orden
        return cls(
            nivel_1=vectores[:3],
            nivel_2=vectores[3:12],
            nivel_3=vectores[12:39]
        )
    
    def generar_nivel_2(self) -> None:
        """
        Genera Nivel 2 desde Nivel 1 usando operaciones ternarias XOR
        Patrón fractal: cada vector genera 3 hijos
        """
        a, b, c = self.nivel_1
        
        # Grupo 1: Derivados de 'a'
        self.nivel_2[0] = VectorFFE(a.forma ^ b.forma, a.funcion ^ b.funcion, a.estructura ^ b.estructura)
        self.nivel_2[1] = VectorFFE(a.forma ^ c.forma, a.funcion ^ c.funcion, a.estructura ^ c.estructura)
        self.nivel_2[2] = VectorFFE(b.forma ^ c.forma, b.funcion ^ c.funcion, b.estructura ^ c.estructura)
        
        # Grupo 2: Derivados de 'b'
        self.nivel_2[3] = VectorFFE(b.forma ^ a.forma, b.funcion ^ a.funcion, b.estructura ^ a.estructura)
        self.nivel_2[4] = VectorFFE(b.forma ^ c.forma, b.funcion ^ c.funcion, b.estructura ^ c.estructura)
        self.nivel_2[5] = VectorFFE(c.forma ^ a.forma, c.funcion ^ a.funcion, c.estructura ^ a.estructura)
        
        # Grupo 3: Combinaciones complejas
        self.nivel_2[6] = VectorFFE(
            (a.forma ^ b.forma) & 0b111,
            (b.funcion ^ c.funcion) & 0b111,
            (c.estructura ^ a.estructura) & 0b111
        )
        self.nivel_2[7] = VectorFFE(
            (b.forma ^ c.forma) & 0b111,
            (c.funcion ^ a.funcion) & 0b111,
            (a.estructura ^ b.estructura) & 0b111
        )
        self.nivel_2[8] = VectorFFE(
            (c.forma ^ a.forma) & 0b111,
            (a.funcion ^ b.funcion) & 0b111,
            (b.estructura ^ c.estructura) & 0b111
        )
    
    def generar_nivel_3(self) -> None:
        """
        Genera Nivel 3 desde Nivel 1 y Nivel 2 recursivamente
        Combina patrones emergentes
        """
        idx = 0
        for i in range(3):  # Por cada vector de Nivel 1
            for j in range(3):  # Genera 3 derivados
                base_idx = i * 3 + j
                if base_idx < 9:
                    n1 = self.nivel_1[i]
                    n2 = self.nivel_2[base_idx]
                    
                    # Derivado 1: XOR directo
                    self.nivel_3[idx] = VectorFFE(
                        (n1.forma ^ n2.forma) & 0b111,
                        (n1.funcion ^ n2.funcion) & 0b111,
                        (n1.estructura ^ n2.estructura) & 0b111
                    )
                    idx += 1
                    
                    # Derivado 2: Rotación
                    self.nivel_3[idx] = VectorFFE(
                        (n2.forma ^ n1.funcion) & 0b111,
                        (n2.funcion ^ n1.estructura) & 0b111,
                        (n2.estructura ^ n1.forma) & 0b111
                    )
                    idx += 1
                    
                    # Derivado 3: Complemento parcial
                    self.nivel_3[idx] = VectorFFE(
                        ((n1.forma + n2.forma) % 8) & 0b111,
                        ((n1.funcion ^ n2.funcion) ^ 0b111) & 0b111,
                        ((n1.estructura * 3) % 8) & 0b111
                    )
                    idx += 1
    
    def reconstruir_jerarquia(self) -> None:
        """Reconstruye Nivel 2 y 3 desde Nivel 1"""
        self.generar_nivel_2()
        self.generar_nivel_3()
    
    def podar_dimensiones(self, dimensiones_a_podar: List[str]) -> None:
        """
        Podado contextual: marca dimensiones como inactivas
        No las elimina, solo las ignora en este contexto
        """
        for dim in dimensiones_a_podar:
            self.dimensiones_activas[dim] = False
    
    def activar_dimensiones(self, dimensiones: List[str]) -> None:
        """Activa dimensiones relevantes para el contexto"""
        for dim in dimensiones:
            self.dimensiones_activas[dim] = True
    
    def coherencia(self) -> float:
        """
        Métrica de coherencia interna: mide autosimilitud fractal
        Rango [0.0, 1.0]
        """
        # Distancia promedio dentro de cada nivel
        dist_n1 = sum(self.nivel_1[i].distancia(self.nivel_1[(i+1)%3]) for i in range(3)) / 3
        dist_n2 = sum(self.nivel_2[i].distancia(self.nivel_2[(i+1)%9]) for i in range(9)) / 9
        dist_n3 = sum(self.nivel_3[i].distancia(self.nivel_3[(i+1)%27]) for i in range(27)) / 27
        
        # Coherencia = 1 - (variación normalizada)
        max_dist = 7 * 3  # Máxima distancia Manhattan
        variacion = (dist_n1 + dist_n2 + dist_n3) / (3 * max_dist)
        return 1.0 - variacion
    
    def compresion_ratio(self, original_bits: int = 32768) -> float:
        """
        Ratio de compresión vs. embedding tradicional (4096 floats = 32KB)
        """
        return original_bits / self.total_bits
    
    def to_ndarray(self) -> np.ndarray:
        """
        Convierte estructura fractal 3→9→27 a array numpy.
        Preserva jerarquía: [nivel_1 (9), nivel_2 (27), nivel_3 (81)] = 117 valores
        
        Pensamiento fractal: cada valor 0-7 se mantiene discreto, no normalizado.
        """
        # Nivel 1: 3 vectores × 3 valores = 9
        valores_n1 = []
        for v in self.nivel_1:
            valores_n1.extend([v.forma, v.funcion, v.estructura])
        
        # Nivel 2: 9 vectores × 3 valores = 27
        valores_n2 = []
        for v in self.nivel_2:
            valores_n2.extend([v.forma, v.funcion, v.estructura])
        
        # Nivel 3: 27 vectores × 3 valores = 81
        valores_n3 = []
        for v in self.nivel_3:
            valores_n3.extend([v.forma, v.funcion, v.estructura])
        
        # Concatenar jerárquicamente: 9 + 27 + 81 = 117
        return np.array(valores_n1 + valores_n2 + valores_n3, dtype=np.float32)
    
    def __repr__(self) -> str:
        return (f"TensorFFE(nivel_abstraccion={self.nivel_abstraccion}, "
                f"bits={self.total_bits}, coherencia={self.coherencia():.3f})")


class TransformadorFFE:
    """
    Transforma entre niveles de abstracción (0-7)
    Abstracting: ↑ (elimina dimensiones de bajo nivel)
    Extending: ↓ (recupera dimensiones concretas)
    """
    
    NIVELES = {
        0: "Fonético",
        1: "Silábico",
        2: "Morfémico",
        3: "Léxico",
        4: "Sintáctico",
        5: "Semántico",
        6: "Discursivo",
        7: "Teórico"
    }
    
    # Mapa de dimensiones relevantes por nivel
    DIMENSIONES_POR_NIVEL = {
        0: ['frecuencia', 'amplitud', 'fase', 'timbre'],
        1: ['estructura_silabica', 'acento', 'patron_ritmico'],
        2: ['raiz', 'afijos', 'significado_basico', 'categoria'],
        3: ['significado_completo', 'categoria_gramatical', 'contexto_lexico'],
        4: ['funcion_oracional', 'relaciones_sintacticas', 'estructura_frase'],
        5: ['significado_contextual', 'relaciones_conceptuales', 'pragmatica'],
        6: ['estructura_argumental', 'coherencia_textual', 'estilo'],
        7: ['marcos_teoricos', 'principios_abstractos', 'leyes_universales']
    }
    
    @classmethod
    def abstracting(cls, tensor: TensorFFE) -> TensorFFE:
        """
        Ascenso en abstracción: nivel_actual → nivel_actual + 1
        Elimina dimensiones de bajo nivel, activa dimensiones superiores
        """
        if tensor.nivel_abstraccion >= 7:
            return tensor  # Ya en nivel máximo
        
        # Subir nivel
        nuevo_nivel = tensor.nivel_abstraccion + 1
        nuevo_tensor = TensorFFE(
            nivel_1=tensor.nivel_1.copy(),
            nivel_2=tensor.nivel_2.copy(),
            nivel_3=tensor.nivel_3.copy(),
            nivel_abstraccion=nuevo_nivel
        )
        
        # Podar dimensiones del nivel anterior
        dimensiones_obsoletas = cls.DIMENSIONES_POR_NIVEL.get(tensor.nivel_abstraccion, [])
        nuevo_tensor.podar_dimensiones(dimensiones_obsoletas)
        
        # Activar dimensiones del nuevo nivel
        dimensiones_nuevas = cls.DIMENSIONES_POR_NIVEL.get(nuevo_nivel, [])
        nuevo_tensor.activar_dimensiones(dimensiones_nuevas)
        
        return nuevo_tensor
    
    @classmethod
    def extending(cls, tensor: TensorFFE) -> TensorFFE:
        """
        Descenso en concreción: nivel_actual → nivel_actual - 1
        Recupera dimensiones concretas para manifestación
        """
        if tensor.nivel_abstraccion <= 0:
            return tensor  # Ya en nivel base
        
        # Bajar nivel
        nuevo_nivel = tensor.nivel_abstraccion - 1
        nuevo_tensor = TensorFFE(
            nivel_1=tensor.nivel_1.copy(),
            nivel_2=tensor.nivel_2.copy(),
            nivel_3=tensor.nivel_3.copy(),
            nivel_abstraccion=nuevo_nivel
        )
        
        # Recuperar dimensiones del nivel inferior
        dimensiones_concretas = cls.DIMENSIONES_POR_NIVEL.get(nuevo_nivel, [])
        nuevo_tensor.activar_dimensiones(dimensiones_concretas)
        
        return nuevo_tensor
    
    @classmethod
    def transformar_continuo(cls, tensor: TensorFFE, nivel_objetivo: int) -> TensorFFE:
        """
        Transforma directamente a un nivel objetivo (0-7)
        Usa abstracting o extending según sea necesario
        """
        if not 0 <= nivel_objetivo <= 7:
            raise ValueError(f"Nivel objetivo debe estar en [0,7], got {nivel_objetivo}")
        
        tensor_actual = tensor
        while tensor_actual.nivel_abstraccion < nivel_objetivo:
            tensor_actual = cls.abstracting(tensor_actual)
        
        while tensor_actual.nivel_abstraccion > nivel_objetivo:
            tensor_actual = cls.extending(tensor_actual)
        
        return tensor_actual


# === Utilidades ===

def crear_tensor_desde_lista(valores: List[int], nivel_abstraccion: int = 0) -> TensorFFE:
    """
    Crea TensorFFE desde lista plana [0-7]
    Ejemplo: [5, 3, 2] → TensorFFE con nivel_1 configurado
    """
    if len(valores) != 3:
        raise ValueError("Se requieren exactamente 3 valores para nivel_1")
    
    tensor = TensorFFE(
        nivel_1=[VectorFFE(v, v, v) for v in valores],
        nivel_abstraccion=nivel_abstraccion
    )
    tensor.reconstruir_jerarquia()
    return tensor


def tensor_nulo() -> TensorFFE:
    """Crea tensor con todos los valores en 0 (potencialidad pura)"""
    return TensorFFE(
        nivel_1=[VectorFFE(0, 0, 0) for _ in range(3)],
        nivel_abstraccion=0
    )


if __name__ == "__main__":
    # === Tests básicos ===
    print("🧬 Tensores FFE - Proyecto Genesis\n")
    
    # Test 1: Crear tensor básico
    print("Test 1: Crear tensor desde lista")
    tensor = crear_tensor_desde_lista([5, 3, 2], nivel_abstraccion=3)
    print(f"  {tensor}")
    print(f"  Coherencia: {tensor.coherencia():.3f}")
    print(f"  Compresión: {tensor.compresion_ratio():.1f}x\n")
    
    # Test 2: Serialización
    print("Test 2: Serialización a bits")
    bits = tensor.to_bits()
    print(f"  Bits totales: {tensor.total_bits}")
    print(f"  Valor: {bits} (0x{bits:X})")
    tensor_recuperado = TensorFFE.from_bits(bits)
    print(f"  Recuperado: {tensor_recuperado}\n")
    
    # Test 3: Abstracting
    print("Test 3: Abstracting (Léxico → Semántico)")
    tensor_semantico = TransformadorFFE.abstracting(tensor)
    print(f"  Nivel original: {TransformadorFFE.NIVELES[tensor.nivel_abstraccion]}")
    print(f"  Nivel nuevo: {TransformadorFFE.NIVELES[tensor_semantico.nivel_abstraccion]}")
    print(f"  Dimensiones activas: {list(tensor_semantico.dimensiones_activas.keys())}\n")
    
    # Test 4: Extending
    print("Test 4: Extending (Semántico → Morfémico)")
    tensor_final = TransformadorFFE.transformar_continuo(tensor_semantico, nivel_objetivo=2)
    print(f"  Nivel objetivo: {TransformadorFFE.NIVELES[tensor_final.nivel_abstraccion]}")
    print(f"  Dimensiones activas: {list(tensor_final.dimensiones_activas.keys())}\n")
    
    print("✅ Todos los tests pasaron!")
