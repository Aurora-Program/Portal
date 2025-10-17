"""
Evolver - Motor de Aprendizaje Fractal
Proyecto Genesis - Aurora Intelligence Engine

Aprende en tres dimensiones fractales:
1. Arquetipos: Patrones universales atemporales
2. Dinámicas: Evolución temporal de transformaciones
3. Relatores: Conexiones fractales entre conceptos

Usa TransformadorFFE y Transcender para aprender desde tensores emergentes.
"""

from typing import List, Dict, Tuple, Optional, Set
from dataclasses import dataclass, field
from collections import defaultdict
import numpy as np
from tensor_ffe import TensorFFE, VectorFFE, TransformadorFFE
from transcender import Transcender, Emergencia


@dataclass
class Arquetipo:
    """Patrón universal atemporal"""
    id: str
    tensor_prototipo: TensorFFE
    ejemplos: List[TensorFFE] = field(default_factory=list)
    frecuencia: int = 0
    nivel_abstraccion: int = 3
    
    def coherencia(self) -> float:
        """Mide qué tan consistente es el arquetipo"""
        if len(self.ejemplos) < 2:
            return 1.0
        
        # Distancia promedio entre ejemplos y prototipo
        distancias = [self._distancia(ej, self.tensor_prototipo) for ej in self.ejemplos]
        return 1.0 - (sum(distancias) / len(distancias))
    
    def _distancia(self, t1: TensorFFE, t2: TensorFFE) -> float:
        """Distancia normalizada entre tensores"""
        dist = sum(v1.distancia(v2) for v1, v2 in zip(t1.nivel_1, t2.nivel_1))
        return dist / (3 * 7 * 3)  # Normalizar


@dataclass
class Dinamica:
    """Patrón temporal de transformación"""
    id: str
    secuencia: List[TensorFFE]
    delta_promedio: VectorFFE  # Vector promedio de cambio
    periodicidad: Optional[int] = None
    
    def predecir_siguiente(self, actual: TensorFFE) -> TensorFFE:
        """Predice el próximo tensor en la secuencia"""
        siguiente = TensorFFE()
        
        for i in range(3):
            siguiente.nivel_1[i] = VectorFFE(
                forma=(actual.nivel_1[i].forma + self.delta_promedio.forma) % 8,
                funcion=(actual.nivel_1[i].funcion + self.delta_promedio.funcion) % 8,
                estructura=(actual.nivel_1[i].estructura + self.delta_promedio.estructura) % 8
            )
        
        siguiente.reconstruir_jerarquia()
        siguiente.nivel_abstraccion = actual.nivel_abstraccion
        return siguiente


@dataclass
class Relator:
    """Conexión fractal entre conceptos"""
    id: str
    origen: str  # ID de arquetipo origen
    destino: str  # ID de arquetipo destino
    tipo: str  # "causal", "analogico", "jerarquico"
    fuerza: float = 0.0  # [0.0, 1.0]
    transformacion: Optional[TensorFFE] = None  # Tensor de transformación


class ArchetypeLearner:
    """Detector de patrones universales con rotación Fibonacci"""
    
    def __init__(self, umbral_similitud: float = 0.7):
        self.arquetipos: Dict[str, Arquetipo] = {}
        self.umbral_similitud = umbral_similitud
        self.contador = 0
        
        # Secuencia Fibonacci para rotaciones (mod 8 para escala octal)
        self.fibonacci = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]
        self.paso_rotacion = 0  # Índice en secuencia Fibonacci
    
    def detectar_o_crear(self, tensor: TensorFFE) -> Arquetipo:
        """Detecta arquetipo existente o crea uno nuevo con rotación Fibonacci"""
        # Buscar arquetipo similar usando rotaciones Fibonacci
        mejor_match = None
        mejor_similitud = 0.0
        mejor_rotacion = 0
        
        # Probar tensor original + rotaciones Fibonacci
        rotaciones = [tensor] + self._generar_rotaciones_fibonacci(tensor)
        
        for arq in self.arquetipos.values():
            for rot_idx, tensor_rot in enumerate(rotaciones):
                similitud = self._similitud(tensor_rot, arq.tensor_prototipo)
                if similitud > mejor_similitud and similitud >= self.umbral_similitud:
                    mejor_similitud = similitud
                    mejor_match = arq
                    mejor_rotacion = rot_idx
        
        # Actualizar existente o crear nuevo
        if mejor_match:
            # Usar la rotación que mejor encaja
            tensor_a_usar = rotaciones[mejor_rotacion]
            mejor_match.ejemplos.append(tensor_a_usar)
            mejor_match.frecuencia += 1
            # Actualizar prototipo (promedio móvil)
            self._actualizar_prototipo(mejor_match)
            
            # Avanzar paso Fibonacci (exploración continua)
            self.paso_rotacion = (self.paso_rotacion + 1) % len(self.fibonacci)
            
            return mejor_match
        else:
            # Crear nuevo arquetipo
            self.contador += 1
            nuevo = Arquetipo(
                id=f"ARQ_{self.contador:04d}",
                tensor_prototipo=self._clonar_tensor(tensor),
                ejemplos=[tensor],
                frecuencia=1,
                nivel_abstraccion=tensor.nivel_abstraccion
            )
            self.arquetipos[nuevo.id] = nuevo
            
            # Avanzar paso Fibonacci
            self.paso_rotacion = (self.paso_rotacion + 1) % len(self.fibonacci)
            
            return nuevo
    
    def _generar_rotaciones_fibonacci(self, tensor: TensorFFE) -> List[TensorFFE]:
        """
        Genera rotaciones del tensor siguiendo secuencia Fibonacci
        Esto permite encontrar coherencia fractal en diferentes "ángulos"
        """
        rotaciones = []
        
        # Tomar 3 pasos Fibonacci (exploramos 3 rotaciones)
        for i in range(3):
            idx_fib = (self.paso_rotacion + i) % len(self.fibonacci)
            paso = self.fibonacci[idx_fib] % 8  # Octal
            
            # Rotar dimensiones FFE según paso Fibonacci
            tensor_rot = TensorFFE()
            
            for j in range(3):
                v_orig = tensor.nivel_1[j]
                
                # Rotación: F→Fn→E→F (circular) con desplazamiento Fibonacci
                tensor_rot.nivel_1[j] = VectorFFE(
                    forma=(v_orig.forma + paso) % 8,
                    funcion=(v_orig.funcion + paso) % 8,
                    estructura=(v_orig.estructura + paso) % 8
                )
            
            tensor_rot.reconstruir_jerarquia()
            tensor_rot.nivel_abstraccion = tensor.nivel_abstraccion
            rotaciones.append(tensor_rot)
        
        return rotaciones
    
    def _similitud(self, t1: TensorFFE, t2: TensorFFE) -> float:
        """Similitud coseno entre tensores [0.0, 1.0]"""
        dist = sum(v1.distancia(v2) for v1, v2 in zip(t1.nivel_1, t2.nivel_1))
        max_dist = 3 * 7 * 3
        return 1.0 - (dist / max_dist)
    
    def _actualizar_prototipo(self, arq: Arquetipo) -> None:
        """Actualiza prototipo con promedio móvil exponencial (α=0.2)"""
        if not arq.ejemplos:
            return
        
        ultimo = arq.ejemplos[-1]
        alpha = 0.2
        
        for i in range(3):
            arq.tensor_prototipo.nivel_1[i] = VectorFFE(
                forma=int((1 - alpha) * arq.tensor_prototipo.nivel_1[i].forma + alpha * ultimo.nivel_1[i].forma),
                funcion=int((1 - alpha) * arq.tensor_prototipo.nivel_1[i].funcion + alpha * ultimo.nivel_1[i].funcion),
                estructura=int((1 - alpha) * arq.tensor_prototipo.nivel_1[i].estructura + alpha * ultimo.nivel_1[i].estructura)
            )
        
        arq.tensor_prototipo.reconstruir_jerarquia()
    
    def _clonar_tensor(self, tensor: TensorFFE) -> TensorFFE:
        """Crea copia profunda de tensor"""
        clon = TensorFFE()
        for i in range(3):
            clon.nivel_1[i] = VectorFFE(
                forma=tensor.nivel_1[i].forma,
                funcion=tensor.nivel_1[i].funcion,
                estructura=tensor.nivel_1[i].estructura
            )
        clon.reconstruir_jerarquia()
        clon.nivel_abstraccion = tensor.nivel_abstraccion
        clon.dimensiones_activas = set(tensor.dimensiones_activas)
        return clon
    
    def top_arquetipos(self, n: int = 5) -> List[Arquetipo]:
        """Retorna top N arquetipos por frecuencia"""
        return sorted(self.arquetipos.values(), key=lambda a: a.frecuencia, reverse=True)[:n]


class DynamicsLearner:
    """Detector de patrones temporales"""
    
    def __init__(self, ventana_minima: int = 3):
        self.dinamicas: Dict[str, Dinamica] = {}
        self.ventana_minima = ventana_minima
        self.contador = 0
    
    def aprender_secuencia(self, secuencia: List[TensorFFE]) -> Optional[Dinamica]:
        """Aprende patrón dinámico desde secuencia temporal"""
        if len(secuencia) < self.ventana_minima:
            return None
        
        # Calcular delta promedio
        deltas = []
        for i in range(len(secuencia) - 1):
            delta = self._calcular_delta(secuencia[i], secuencia[i+1])
            deltas.append(delta)
        
        delta_promedio = self._promediar_vectores(deltas)
        
        # Detectar periodicidad
        periodicidad = self._detectar_periodicidad(secuencia)
        
        # Crear dinámica
        self.contador += 1
        dinamica = Dinamica(
            id=f"DYN_{self.contador:04d}",
            secuencia=secuencia,
            delta_promedio=delta_promedio,
            periodicidad=periodicidad
        )
        
        self.dinamicas[dinamica.id] = dinamica
        return dinamica
    
    def _calcular_delta(self, t1: TensorFFE, t2: TensorFFE) -> VectorFFE:
        """Calcula vector de cambio entre dos tensores"""
        # Promedio de cambios en nivel_1
        delta_f = sum((t2.nivel_1[i].forma - t1.nivel_1[i].forma) % 8 for i in range(3)) // 3
        delta_fn = sum((t2.nivel_1[i].funcion - t1.nivel_1[i].funcion) % 8 for i in range(3)) // 3
        delta_e = sum((t2.nivel_1[i].estructura - t1.nivel_1[i].estructura) % 8 for i in range(3)) // 3
        
        return VectorFFE(forma=delta_f, funcion=delta_fn, estructura=delta_e)
    
    def _promediar_vectores(self, vectores: List[VectorFFE]) -> VectorFFE:
        """Promedia lista de vectores"""
        f = sum(v.forma for v in vectores) // len(vectores)
        fn = sum(v.funcion for v in vectores) // len(vectores)
        e = sum(v.estructura for v in vectores) // len(vectores)
        return VectorFFE(forma=f, funcion=fn, estructura=e)
    
    def _detectar_periodicidad(self, secuencia: List[TensorFFE]) -> Optional[int]:
        """Detecta periodicidad en la secuencia"""
        n = len(secuencia)
        if n < 6:
            return None
        
        # Probar períodos de 2 a n//2
        for periodo in range(2, n // 2 + 1):
            es_periodico = True
            for i in range(periodo, n):
                if self._distancia_tensor(secuencia[i], secuencia[i % periodo]) > 0.3:
                    es_periodico = False
                    break
            
            if es_periodico:
                return periodo
        
        return None
    
    def _distancia_tensor(self, t1: TensorFFE, t2: TensorFFE) -> float:
        """Distancia normalizada entre tensores"""
        dist = sum(v1.distancia(v2) for v1, v2 in zip(t1.nivel_1, t2.nivel_1))
        return dist / (3 * 7 * 3)


class RelatorNetwork:
    """Red de relaciones fractales con rotación Fibonacci"""
    
    def __init__(self, transcender: Transcender):
        self.relatores: Dict[str, Relator] = {}
        self.grafo: Dict[str, Set[str]] = defaultdict(set)  # Adyacencia
        self.transcender = transcender
        self.contador = 0
        
        # Secuencia Fibonacci para exploración de conexiones
        self.fibonacci = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]
        self.paso_conexion = 0
    
    def conectar(self, arq1: Arquetipo, arq2: Arquetipo, tipo: str = "analogico") -> Relator:
        """
        Crea o fortalece conexión entre arquetipos usando rotación Fibonacci
        para explorar múltiples perspectivas de la relación
        """
        # Sintetizar transformación emergente desde múltiples rotaciones
        mejor_emergencia = None
        mejor_score = 0.0
        
        # Probar 3 rotaciones Fibonacci del par de arquetipos
        for i in range(3):
            idx_fib = (self.paso_conexion + i) % len(self.fibonacci)
            paso = self.fibonacci[idx_fib] % 8
            
            # Rotar ambos arquetipos
            arq1_rot = self._rotar_arquetipo(arq1, paso)
            arq2_rot = self._rotar_arquetipo(arq2, paso)
            
            # Sintetizar con rotación
            dummy = TensorFFE()  # Tensor neutral
            emergencia = self.transcender.sintetizar(
                arq1_rot.tensor_prototipo, 
                arq2_rot.tensor_prototipo, 
                dummy
            )
            
            if emergencia.score_emergencia > mejor_score:
                mejor_score = emergencia.score_emergencia
                mejor_emergencia = emergencia
        
        # Crear relator con la mejor síntesis emergente completa
        # El tensor del relator ES la emergencia (Ms, Ss, MetaM)
        # No solo Ms - incluimos toda la síntesis fractal
        self.contador += 1
        relator = Relator(
            id=f"REL_{self.contador:04d}",
            origen=arq1.id,
            destino=arq2.id,
            tipo=tipo,
            fuerza=mejor_emergencia.score_emergencia,
            transformacion=mejor_emergencia.Ms  # La emergencia Ms es la transformación
        )
        
        self.relatores[relator.id] = relator
        self.grafo[arq1.id].add(arq2.id)
        
        # Avanzar paso Fibonacci
        self.paso_conexion = (self.paso_conexion + 1) % len(self.fibonacci)
        
        return relator
    
    def _rotar_arquetipo(self, arq: Arquetipo, paso: int) -> Arquetipo:
        """Crea copia del arquetipo con tensor rotado"""
        tensor_rot = TensorFFE()
        
        for i in range(3):
            v = arq.tensor_prototipo.nivel_1[i]
            tensor_rot.nivel_1[i] = VectorFFE(
                forma=(v.forma + paso) % 8,
                funcion=(v.funcion + paso) % 8,
                estructura=(v.estructura + paso) % 8
            )
        
        tensor_rot.reconstruir_jerarquia()
        tensor_rot.nivel_abstraccion = arq.tensor_prototipo.nivel_abstraccion
        
        # Crear arquetipo temporal con tensor rotado
        arq_rot = Arquetipo(
            id=arq.id,
            tensor_prototipo=tensor_rot,
            frecuencia=arq.frecuencia,
            nivel_abstraccion=arq.nivel_abstraccion
        )
        
        return arq_rot
    
    def camino_mas_corto(self, id_origen: str, id_destino: str) -> Optional[List[str]]:
        """BFS para encontrar camino entre arquetipos"""
        if id_origen == id_destino:
            return [id_origen]
        
        visitados = {id_origen}
        cola = [(id_origen, [id_origen])]
        
        while cola:
            actual, camino = cola.pop(0)
            
            for vecino in self.grafo.get(actual, []):
                if vecino in visitados:
                    continue
                
                nuevo_camino = camino + [vecino]
                
                if vecino == id_destino:
                    return nuevo_camino
                
                visitados.add(vecino)
                cola.append((vecino, nuevo_camino))
        
        return None
    
    def conexiones_fuertes(self, umbral: float = 0.7) -> List[Relator]:
        """Retorna relatores con fuerza >= umbral"""
        return [r for r in self.relatores.values() if r.fuerza >= umbral]


class Evolver:
    """Motor completo de aprendizaje fractal"""
    
    def __init__(self):
        self.archetype_learner = ArchetypeLearner()
        self.dynamics_learner = DynamicsLearner()
        self.transcender = Transcender()
        self.relator_network = RelatorNetwork(self.transcender)
        self.transformador = TransformadorFFE()
    
    def aprender(self, tensor: TensorFFE) -> Dict[str, any]:
        """Aprende desde un tensor FFE (entrada principal)"""
        resultados = {}
        
        # 1. Detectar/crear arquetipo
        arq = self.archetype_learner.detectar_o_crear(tensor)
        resultados['arquetipo'] = arq.id
        
        # 2. Buscar relaciones con otros arquetipos (top 3)
        top_arqs = self.archetype_learner.top_arquetipos(n=3)
        for otro_arq in top_arqs:
            if otro_arq.id != arq.id:
                relator = self.relator_network.conectar(arq, otro_arq)
                if relator.fuerza > 0.5:
                    resultados.setdefault('relaciones', []).append(relator.id)
        
        return resultados
    
    def aprender_secuencia(self, secuencia: List[TensorFFE]) -> Optional[Dinamica]:
        """Aprende dinámica desde secuencia temporal"""
        return self.dynamics_learner.aprender_secuencia(secuencia)
    
    def estadisticas(self) -> Dict[str, any]:
        """Estadísticas del sistema de aprendizaje"""
        return {
            'arquetipos': len(self.archetype_learner.arquetipos),
            'dinamicas': len(self.dynamics_learner.dinamicas),
            'relatores': len(self.relator_network.relatores),
            'top_arquetipos': [(a.id, a.frecuencia) for a in self.archetype_learner.top_arquetipos(3)],
            'conexiones_fuertes': len(self.relator_network.conexiones_fuertes())
        }


if __name__ == "__main__":
    from tensor_ffe import crear_tensor_desde_lista
    
    print("🌱 Evolver - Motor de Aprendizaje Fractal\n")
    
    # Test 1: Aprendizaje de arquetipos
    print("Test 1: Detectar arquetipos")
    evolver = Evolver()
    
    tensores = [
        crear_tensor_desde_lista([1, 2, 3], 3),
        crear_tensor_desde_lista([1, 3, 2], 3),  # Similar
        crear_tensor_desde_lista([6, 7, 0], 4),  # Diferente
        crear_tensor_desde_lista([1, 2, 4], 3),  # Similar al primero
    ]
    
    for i, t in enumerate(tensores):
        resultado = evolver.aprender(t)
        print(f"  Tensor {i+1}: Arquetipo {resultado['arquetipo']}")
    
    stats = evolver.estadisticas()
    print(f"\n  Arquetipos detectados: {stats['arquetipos']}")
    print(f"  Relatores creados: {stats['relatores']}\n")
    
    # Test 2: Aprendizaje de dinámicas
    print("Test 2: Detectar dinámicas temporales")
    secuencia = [
        crear_tensor_desde_lista([0, 0, 0], 2),
        crear_tensor_desde_lista([1, 1, 1], 2),
        crear_tensor_desde_lista([2, 2, 2], 2),
        crear_tensor_desde_lista([3, 3, 3], 2),
    ]
    
    dinamica = evolver.aprender_secuencia(secuencia)
    if dinamica:
        print(f"  Dinámica {dinamica.id} detectada")
        print(f"  Delta promedio: {dinamica.delta_promedio}")
        
        # Predecir siguiente
        prediccion = dinamica.predecir_siguiente(secuencia[-1])
        print(f"  Predicción próximo: {prediccion.nivel_1[0]}")
    
    print("\n✅ Todos los tests pasaron!")
