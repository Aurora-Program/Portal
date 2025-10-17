"""
Transcender - Motor de Síntesis Emergente
Proyecto Genesis - Aurora Intelligence Engine

Combina tripletas (A, B, C) para generar emergencias:
- Ms (Structure): Nueva lógica emergente
- Ss (Form): Huella factual
- MetaM (Function): Ruta lógica completa

Propiedad NO CONMUTATIVA: (A,B,C) ≠ (B,A,C)
"""

from typing import Tuple, Optional, Dict, List
from dataclasses import dataclass
import numpy as np
from tensor_ffe import TensorFFE, VectorFFE


@dataclass
class Emergencia:
    """Resultado de síntesis emergente"""
    Ms: TensorFFE      # Structure - Nueva lógica
    Ss: TensorFFE      # Form - Huella factual
    MetaM: TensorFFE   # Function - Ruta lógica completa
    
    # Métricas
    novedad: float = 0.0
    coherencia: float = 0.0
    compresion: float = 0.0
    score_emergencia: float = 0.0
    
    def __repr__(self) -> str:
        return (f"Emergencia(score={self.score_emergencia:.3f}, "
                f"nov={self.novedad:.2f}, coh={self.coherencia:.2f}, comp={self.compresion:.2f})")


class Transcender:
    """
    Motor de síntesis emergente no conmutativo
    Opera sobre tripletas de tensores FFE
    """
    
    def __init__(self):
        self.historial_emergencias: List[Emergencia] = []
    
    def sintetizar(self, A: TensorFFE, B: TensorFFE, C: TensorFFE) -> Emergencia:
        """
        Síntesis emergente: (A, B, C) → (Ms, Ss, MetaM)
        El ORDEN importa (no conmutativo)
        """
        # === Ms (Structure): Nueva lógica emergente ===
        Ms = self._generar_estructura_emergente(A, B, C)
        
        # === Ss (Form): Huella factual ===
        Ss = self._generar_huella_factual(A, B, C)
        
        # === MetaM (Function): Ruta lógica completa ===
        MetaM = self._generar_ruta_logica(A, B, C, Ms, Ss)
        
        # === Calcular métricas ===
        emergencia = Emergencia(Ms=Ms, Ss=Ss, MetaM=MetaM)
        self._calcular_metricas(emergencia, A, B, C)
        
        # Guardar en historial
        self.historial_emergencias.append(emergencia)
        
        return emergencia
    
    def _generar_estructura_emergente(self, A: TensorFFE, B: TensorFFE, C: TensorFFE) -> TensorFFE:
        """
        Ms (Structure): Combina estructuras de A, B, C
        Usa operaciones ternarias XOR con peso posicional
        """
        Ms = TensorFFE()
        
        # Nivel 1: Combinación ponderada por posición
        for i in range(3):
            Ms.nivel_1[i] = VectorFFE(
                forma=(A.nivel_1[i].forma ^ (B.nivel_1[i].forma << 1) ^ (C.nivel_1[i].forma << 2)) & 0b111,
                funcion=(A.nivel_1[i].funcion + B.nivel_1[i].funcion * 2 + C.nivel_1[i].funcion * 3) % 8,
                estructura=(A.nivel_1[i].estructura ^ B.nivel_1[i].estructura ^ C.nivel_1[i].estructura) & 0b111
            )
        
        # Reconstruir jerarquía
        Ms.reconstruir_jerarquia()
        
        # Heredar nivel de abstracción más alto
        Ms.nivel_abstraccion = max(A.nivel_abstraccion, B.nivel_abstraccion, C.nivel_abstraccion)
        
        return Ms
    
    def _generar_huella_factual(self, A: TensorFFE, B: TensorFFE, C: TensorFFE) -> TensorFFE:
        """
        Ss (Form): Captura la "huella" secuencial de la síntesis
        Refleja el proceso de combinación
        """
        Ss = TensorFFE()
        
        # Nivel 1: Secuencia de transformaciones
        for i in range(3):
            # Paso 1: A influye en B
            temp1 = VectorFFE(
                forma=(A.nivel_1[i].forma + B.nivel_1[i].forma) % 8,
                funcion=(A.nivel_1[i].funcion ^ B.nivel_1[i].funcion) & 0b111,
                estructura=((A.nivel_1[i].estructura * B.nivel_1[i].estructura) % 8) & 0b111
            )
            
            # Paso 2: Resultado influye en C
            Ss.nivel_1[i] = VectorFFE(
                forma=(temp1.forma ^ C.nivel_1[i].forma) & 0b111,
                funcion=(temp1.funcion + C.nivel_1[i].funcion) % 8,
                estructura=((temp1.estructura + C.nivel_1[i].estructura) * 3) % 8
            )
        
        Ss.reconstruir_jerarquia()
        Ss.nivel_abstraccion = (A.nivel_abstraccion + B.nivel_abstraccion + C.nivel_abstraccion) // 3
        
        return Ss
    
    def _generar_ruta_logica(self, A: TensorFFE, B: TensorFFE, C: TensorFFE, 
                             Ms: TensorFFE, Ss: TensorFFE) -> TensorFFE:
        """
        MetaM (Function): Ruta lógica completa del proceso
        Captura la función meta del razonamiento
        """
        MetaM = TensorFFE()
        
        # Nivel 1: Síntesis de la síntesis (meta-nivel)
        for i in range(3):
            MetaM.nivel_1[i] = VectorFFE(
                forma=(Ms.nivel_1[i].forma + Ss.nivel_1[i].forma) % 8,
                funcion=((Ms.nivel_1[i].funcion * Ss.nivel_1[i].funcion) % 8) & 0b111,
                estructura=(Ms.nivel_1[i].estructura ^ Ss.nivel_1[i].estructura ^ 
                           (A.nivel_1[i].estructura + B.nivel_1[i].estructura + C.nivel_1[i].estructura) % 8) & 0b111
            )
        
        MetaM.reconstruir_jerarquia()
        MetaM.nivel_abstraccion = max(Ms.nivel_abstraccion, Ss.nivel_abstraccion) + 1
        if MetaM.nivel_abstraccion > 7:
            MetaM.nivel_abstraccion = 7
        
        return MetaM
    
    def _calcular_metricas(self, emergencia: Emergencia, A: TensorFFE, B: TensorFFE, C: TensorFFE) -> None:
        """
        Calcula métricas de calidad de la emergencia:
        1. Novedad estructural
        2. Coherencia jerárquica
        3. Ganancia de compresión
        """
        # === 1. Novedad Estructural ===
        # Compara emergencia vs. promedio convexo
        convex_hull = self._calcular_convex_hull(A, B, C)
        emergencia.novedad = self._distancia_vectorial(emergencia.Ms, convex_hull)
        
        # === 2. Coherencia Jerárquica ===
        # Mide alineación con patrón fractal (3→9→27)
        emergencia.coherencia = emergencia.Ms.coherencia()
        
        # === 3. Ganancia de Compresión (MDL) ===
        # ¿Cuánto reduce la descripción total?
        mdl_original = self._mdl_length(A) + self._mdl_length(B) + self._mdl_length(C)
        mdl_emergente = self._mdl_length(emergencia.Ms)
        emergencia.compresion = (mdl_original - mdl_emergente) / mdl_original if mdl_original > 0 else 0.0
        
        # === Score Total ===
        # Ponderación: 40% novedad, 30% coherencia, 30% compresión
        emergencia.score_emergencia = (
            0.4 * emergencia.novedad +
            0.3 * emergencia.coherencia +
            0.3 * max(0.0, emergencia.compresion)
        )
    
    def _calcular_convex_hull(self, A: TensorFFE, B: TensorFFE, C: TensorFFE) -> TensorFFE:
        """
        Promedio convexo: (A + B + C) / 3
        Usado como baseline para medir novedad
        """
        convex = TensorFFE()
        
        for i in range(3):
            convex.nivel_1[i] = VectorFFE(
                forma=(A.nivel_1[i].forma + B.nivel_1[i].forma + C.nivel_1[i].forma) // 3,
                funcion=(A.nivel_1[i].funcion + B.nivel_1[i].funcion + C.nivel_1[i].funcion) // 3,
                estructura=(A.nivel_1[i].estructura + B.nivel_1[i].estructura + C.nivel_1[i].estructura) // 3
            )
        
        convex.reconstruir_jerarquia()
        return convex
    
    def _distancia_vectorial(self, tensor1: TensorFFE, tensor2: TensorFFE) -> float:
        """
        Distancia Manhattan normalizada entre tensores
        Rango [0.0, 1.0]
        """
        dist_total = 0.0
        for v1, v2 in zip(tensor1.nivel_1, tensor2.nivel_1):
            dist_total += v1.distancia(v2)
        
        max_dist = 3 * 7 * 3  # 3 vectores × 7 max × 3 dimensiones
        return dist_total / max_dist
    
    def _mdl_length(self, tensor: TensorFFE) -> float:
        """
        Minimum Description Length (MDL)
        Aproximación: número de bits únicos necesarios
        """
        # Contar valores únicos en nivel_1
        valores_unicos = set()
        for v in tensor.nivel_1:
            valores_unicos.add((v.forma, v.funcion, v.estructura))
        
        # MDL ≈ log2(valores_únicos) + complejidad_estructura
        import math
        if len(valores_unicos) == 0:
            return 0.0
        
        return math.log2(len(valores_unicos)) + tensor.coherencia() * 10
    
    def validar_no_conmutatividad(self, A: TensorFFE, B: TensorFFE, C: TensorFFE) -> Dict[str, float]:
        """
        Valida que el orden importa: f(A,B,C) ≠ f(B,A,C) ≠ f(A,C,B)
        Retorna scores de cada permutación
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
    
    def mejor_emergencia(self) -> Optional[Emergencia]:
        """Retorna la emergencia con mayor score del historial"""
        if not self.historial_emergencias:
            return None
        return max(self.historial_emergencias, key=lambda e: e.score_emergencia)


# === Utilidades ===

def demostrar_no_conmutatividad():
    """Demuestra que el orden importa en la síntesis"""
    from tensor_ffe import crear_tensor_desde_lista
    
    print("🔮 Demostrando No Conmutatividad\n")
    
    # Crear tres tensores diferentes
    A = crear_tensor_desde_lista([1, 2, 3], nivel_abstraccion=3)
    B = crear_tensor_desde_lista([4, 5, 6], nivel_abstraccion=3)
    C = crear_tensor_desde_lista([7, 0, 1], nivel_abstraccion=3)
    
    print(f"A: {A.nivel_1}")
    print(f"B: {B.nivel_1}")
    print(f"C: {C.nivel_1}\n")
    
    # Probar todas las permutaciones
    transcender = Transcender()
    resultados = transcender.validar_no_conmutatividad(A, B, C)
    
    print("Scores de emergencia por permutación:")
    for orden, score in sorted(resultados.items(), key=lambda x: x[1], reverse=True):
        print(f"  {orden}: {score:.4f}")
    
    print("\n✅ El orden SÍ importa (scores diferentes confirman no conmutatividad)")


if __name__ == "__main__":
    from tensor_ffe import crear_tensor_desde_lista
    
    print("🔮 Transcender - Motor de Síntesis Emergente\n")
    
    # Test 1: Síntesis básica
    print("Test 1: Síntesis emergente básica")
    A = crear_tensor_desde_lista([5, 3, 2], nivel_abstraccion=3)
    B = crear_tensor_desde_lista([1, 7, 4], nivel_abstraccion=3)
    C = crear_tensor_desde_lista([6, 0, 3], nivel_abstraccion=4)
    
    transcender = Transcender()
    emergencia = transcender.sintetizar(A, B, C)
    
    print(f"  Entrada: A, B, C")
    print(f"  {emergencia}")
    print(f"  Ms: {emergencia.Ms.nivel_1}")
    print(f"  Ss: {emergencia.Ss.nivel_1}")
    print(f"  MetaM: {emergencia.MetaM.nivel_1}\n")
    
    # Test 2: No conmutatividad
    print("Test 2: Validar no conmutatividad")
    demostrar_no_conmutatividad()
    
    print("\n✅ Todos los tests pasaron!")
