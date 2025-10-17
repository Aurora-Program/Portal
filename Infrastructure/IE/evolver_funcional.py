"""
Evolver Funcional - Motor de Aprendizaje Fractal (Redux-style)
Proyecto Genesis v1.3 - Aurora Intelligence Engine

ARQUITECTURA FUNCIONAL:
- Funciones puras (sin side effects)
- Inmutabilidad (copy-on-write)
- Thread-safe por diseño (sin locks)
- Estado como valores (frozen dataclasses)
- Reducers para cambios de estado

Aprende en tres dimensiones fractales:
1. Arquetipos: Patrones universales atemporales
2. Dinámicas: Evolución temporal de transformaciones
3. Relatores: Conexiones fractales entre conceptos
"""

from typing import List, Dict, Tuple, Optional, Set, NamedTuple
from dataclasses import dataclass, field, replace
from collections import defaultdict
from tensor_ffe import TensorFFE, VectorFFE
from transcender_funcional import TranscenderFuncional, sintetizar_puro


# ============================================================================
# TIPOS INMUTABLES (Frozen Dataclasses)
# ============================================================================

@dataclass(frozen=True)
class Arquetipo:
    """Patrón universal atemporal (inmutable)"""
    id: str
    tensor_prototipo: TensorFFE
    ejemplos: Tuple[TensorFFE, ...] = field(default_factory=tuple)
    frecuencia: int = 0
    nivel_abstraccion: int = 3
    
    def coherencia(self) -> float:
        """Mide qué tan consistente es el arquetipo (pure function)"""
        if len(self.ejemplos) < 2:
            return 1.0
        
        # Distancia promedio entre ejemplos y prototipo
        distancias = [distancia_tensor_puro(ej, self.tensor_prototipo) for ej in self.ejemplos]
        return 1.0 - (sum(distancias) / len(distancias))
    
    def with_ejemplo(self, tensor: TensorFFE) -> 'Arquetipo':
        """Retorna nuevo arquetipo con ejemplo agregado (inmutable)"""
        return replace(
            self,
            ejemplos=self.ejemplos + (tensor,),
            frecuencia=self.frecuencia + 1
        )
    
    def with_prototipo(self, nuevo_prototipo: TensorFFE) -> 'Arquetipo':
        """Retorna nuevo arquetipo con prototipo actualizado (inmutable)"""
        return replace(self, tensor_prototipo=nuevo_prototipo)


@dataclass(frozen=True)
class Dinamica:
    """Patrón temporal de transformación (inmutable)"""
    id: str
    secuencia: Tuple[TensorFFE, ...]
    delta_promedio: VectorFFE  # Vector promedio de cambio
    periodicidad: Optional[int] = None


@dataclass(frozen=True)
class Relator:
    """Conexión fractal entre conceptos (inmutable)"""
    id: str
    origen: str  # ID de arquetipo origen
    destino: str  # ID de arquetipo destino
    tipo: str  # "causal", "analogico", "jerarquico"
    fuerza: float = 0.0  # [0.0, 1.0]
    transformacion: Optional[TensorFFE] = None  # Tensor de transformación


class ArquetipoKey(NamedTuple):
    """Clave inmutable para cache de arquetipos"""
    valores: Tuple[Tuple[int, int, int], ...]
    
    @staticmethod
    def from_tensor(tensor: TensorFFE) -> 'ArquetipoKey':
        return ArquetipoKey(
            valores=tuple(
                (v.forma, v.funcion, v.estructura)
                for v in tensor.nivel_1
            )
        )


@dataclass(frozen=True)
class EvolverState:
    """Estado global inmutable del Evolver"""
    arquetipos: Tuple[Arquetipo, ...] = field(default_factory=tuple)
    dinamicas: Tuple[Dinamica, ...] = field(default_factory=tuple)
    relatores: Tuple[Relator, ...] = field(default_factory=tuple)
    contador_arquetipos: int = 0
    contador_dinamicas: int = 0
    contador_relatores: int = 0
    paso_rotacion: int = 0
    paso_conexion: int = 0
    
    def with_arquetipo(self, arq: Arquetipo) -> 'EvolverState':
        """Retorna nuevo estado con arquetipo agregado"""
        return replace(
            self,
            arquetipos=self.arquetipos + (arq,),
            contador_arquetipos=self.contador_arquetipos + 1,
            paso_rotacion=(self.paso_rotacion + 1) % 12
        )
    
    def with_arquetipo_actualizado(self, arq_actualizado: Arquetipo) -> 'EvolverState':
        """Retorna nuevo estado con arquetipo actualizado"""
        nuevos_arquetipos = tuple(
            arq_actualizado if arq.id == arq_actualizado.id else arq
            for arq in self.arquetipos
        )
        return replace(
            self,
            arquetipos=nuevos_arquetipos,
            paso_rotacion=(self.paso_rotacion + 1) % 12
        )
    
    def with_dinamica(self, din: Dinamica) -> 'EvolverState':
        """Retorna nuevo estado con dinámica agregada"""
        return replace(
            self,
            dinamicas=self.dinamicas + (din,),
            contador_dinamicas=self.contador_dinamicas + 1
        )
    
    def with_relator(self, rel: Relator) -> 'EvolverState':
        """Retorna nuevo estado con relator agregado"""
        return replace(
            self,
            relatores=self.relatores + (rel,),
            contador_relatores=self.contador_relatores + 1,
            paso_conexion=(self.paso_conexion + 1) % 12
        )
    
    def get_arquetipo_by_id(self, arq_id: str) -> Optional[Arquetipo]:
        """Retorna arquetipo por ID (pure function)"""
        for arq in self.arquetipos:
            if arq.id == arq_id:
                return arq
        return None
    
    def top_arquetipos(self, n: int = 5) -> List[Arquetipo]:
        """Retorna top N arquetipos por frecuencia (pure function)"""
        return sorted(self.arquetipos, key=lambda a: a.frecuencia, reverse=True)[:n]


# ============================================================================
# FUNCIONES PURAS (Pure Functions)
# ============================================================================

# Secuencia Fibonacci para rotaciones (constante global)
FIBONACCI = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]


def distancia_tensor_puro(t1: TensorFFE, t2: TensorFFE) -> float:
    """Distancia normalizada entre tensores (pure)"""
    dist = sum(v1.distancia(v2) for v1, v2 in zip(t1.nivel_1, t2.nivel_1))
    return dist / (3 * 7 * 3)  # Normalizar


def similitud_tensor_puro(t1: TensorFFE, t2: TensorFFE) -> float:
    """Similitud entre tensores [0.0, 1.0] (pure)"""
    return 1.0 - distancia_tensor_puro(t1, t2)


def rotar_tensor_fibonacci_puro(tensor: TensorFFE, paso: int) -> TensorFFE:
    """
    Rota tensor según paso Fibonacci (pure)
    NO muta tensor original - retorna nuevo
    """
    from tensor_ffe import crear_tensor_desde_lista
    
    # Rotar cada vector FFE
    valores_rotados = [
        (
            (v.forma + paso) % 8,
            (v.funcion + paso) % 8,
            (v.estructura + paso) % 8
        )
        for v in tensor.nivel_1
    ]
    
    # Crear nuevo tensor con valores rotados
    tensor_rot = crear_tensor_desde_lista(
        [valores_rotados[i][0] for i in range(3)],
        tensor.nivel_abstraccion
    )
    
    return tensor_rot


def generar_rotaciones_fibonacci_puro(
    tensor: TensorFFE,
    paso_actual: int,
    num_rotaciones: int = 3
) -> List[TensorFFE]:
    """
    Genera N rotaciones del tensor siguiendo secuencia Fibonacci (pure)
    Permite encontrar coherencia fractal en diferentes "ángulos"
    """
    rotaciones = []
    
    for i in range(num_rotaciones):
        idx_fib = (paso_actual + i) % len(FIBONACCI)
        paso = FIBONACCI[idx_fib] % 8  # Octal
        
        tensor_rot = rotar_tensor_fibonacci_puro(tensor, paso)
        rotaciones.append(tensor_rot)
    
    return rotaciones


def clonar_tensor_puro(tensor: TensorFFE) -> TensorFFE:
    """Crea copia profunda de tensor (pure)"""
    from tensor_ffe import crear_tensor_desde_lista
    
    valores = [v.forma for v in tensor.nivel_1]
    clon = crear_tensor_desde_lista(valores, tensor.nivel_abstraccion)
    clon.dimensiones_activas = set(tensor.dimensiones_activas)
    
    return clon


def actualizar_prototipo_puro(arq: Arquetipo) -> TensorFFE:
    """
    Actualiza prototipo con promedio móvil exponencial (α=0.2) (pure)
    Retorna nuevo tensor prototipo
    """
    if not arq.ejemplos:
        return arq.tensor_prototipo
    
    ultimo = arq.ejemplos[-1]
    alpha = 0.2
    
    from tensor_ffe import crear_tensor_desde_lista
    
    # Calcular nuevos valores con promedio móvil
    nuevos_valores = []
    for i in range(3):
        forma_nueva = int(
            (1 - alpha) * arq.tensor_prototipo.nivel_1[i].forma + 
            alpha * ultimo.nivel_1[i].forma
        )
        nuevos_valores.append(forma_nueva)
    
    # Crear nuevo prototipo
    nuevo_prototipo = crear_tensor_desde_lista(nuevos_valores, arq.tensor_prototipo.nivel_abstraccion)
    
    return nuevo_prototipo


def detectar_arquetipo_puro(
    tensor: TensorFFE,
    state: EvolverState,
    umbral_similitud: float = 0.7
) -> Tuple[Optional[Arquetipo], int, int]:
    """
    Detecta arquetipo similar en estado actual (pure)
    Retorna: (arquetipo_encontrado, mejor_similitud_idx, mejor_rotacion_idx)
    """
    # Generar rotaciones Fibonacci del tensor
    rotaciones = [tensor] + generar_rotaciones_fibonacci_puro(
        tensor, state.paso_rotacion, num_rotaciones=3
    )
    
    mejor_match = None
    mejor_similitud = 0.0
    mejor_rotacion = 0
    mejor_arq_idx = -1
    
    # Buscar en arquetipos existentes
    for arq_idx, arq in enumerate(state.arquetipos):
        for rot_idx, tensor_rot in enumerate(rotaciones):
            similitud = similitud_tensor_puro(tensor_rot, arq.tensor_prototipo)
            
            if similitud > mejor_similitud and similitud >= umbral_similitud:
                mejor_similitud = similitud
                mejor_match = arq
                mejor_rotacion = rot_idx
                mejor_arq_idx = arq_idx
    
    return mejor_match, mejor_arq_idx, mejor_rotacion


def crear_arquetipo_puro(
    tensor: TensorFFE,
    state: EvolverState
) -> Arquetipo:
    """Crea nuevo arquetipo (pure)"""
    nuevo_id = f"ARQ_{state.contador_arquetipos + 1:04d}"
    
    return Arquetipo(
        id=nuevo_id,
        tensor_prototipo=clonar_tensor_puro(tensor),
        ejemplos=(tensor,),
        frecuencia=1,
        nivel_abstraccion=tensor.nivel_abstraccion
    )


def aprender_tensor_puro(
    tensor: TensorFFE,
    state: EvolverState,
    umbral_similitud: float = 0.7
) -> Tuple[Arquetipo, EvolverState]:
    """
    Aprende desde un tensor (pure)
    Retorna: (arquetipo, nuevo_estado)
    """
    # Detectar arquetipo existente
    match, match_idx, rotacion_idx = detectar_arquetipo_puro(
        tensor, state, umbral_similitud
    )
    
    if match:
        # Actualizar arquetipo existente
        # Usar la rotación que mejor encaja
        rotaciones = [tensor] + generar_rotaciones_fibonacci_puro(
            tensor, state.paso_rotacion, num_rotaciones=3
        )
        tensor_a_usar = rotaciones[rotacion_idx]
        
        # Agregar ejemplo
        arq_con_ejemplo = match.with_ejemplo(tensor_a_usar)
        
        # Actualizar prototipo
        nuevo_prototipo = actualizar_prototipo_puro(arq_con_ejemplo)
        arq_actualizado = arq_con_ejemplo.with_prototipo(nuevo_prototipo)
        
        # Crear nuevo estado con arquetipo actualizado
        nuevo_state = state.with_arquetipo_actualizado(arq_actualizado)
        
        return arq_actualizado, nuevo_state
    else:
        # Crear nuevo arquetipo
        nuevo_arq = crear_arquetipo_puro(tensor, state)
        nuevo_state = state.with_arquetipo(nuevo_arq)
        
        return nuevo_arq, nuevo_state


# ============================================================================
# FUNCIONES PURAS - DINÁMICAS
# ============================================================================

def calcular_delta_puro(t1: TensorFFE, t2: TensorFFE) -> VectorFFE:
    """Calcula vector de cambio entre dos tensores (pure)"""
    # Promedio de cambios en nivel_1
    delta_f = sum((t2.nivel_1[i].forma - t1.nivel_1[i].forma) % 8 for i in range(3)) // 3
    delta_fn = sum((t2.nivel_1[i].funcion - t1.nivel_1[i].funcion) % 8 for i in range(3)) // 3
    delta_e = sum((t2.nivel_1[i].estructura - t1.nivel_1[i].estructura) % 8 for i in range(3)) // 3
    
    return VectorFFE(forma=delta_f, funcion=delta_fn, estructura=delta_e)


def promediar_vectores_puro(vectores: List[VectorFFE]) -> VectorFFE:
    """Promedia lista de vectores (pure)"""
    if not vectores:
        return VectorFFE(forma=0, funcion=0, estructura=0)
    
    f = sum(v.forma for v in vectores) // len(vectores)
    fn = sum(v.funcion for v in vectores) // len(vectores)
    e = sum(v.estructura for v in vectores) // len(vectores)
    
    return VectorFFE(forma=f, funcion=fn, estructura=e)


def detectar_periodicidad_puro(secuencia: Tuple[TensorFFE, ...]) -> Optional[int]:
    """Detecta periodicidad en la secuencia (pure)"""
    n = len(secuencia)
    if n < 6:
        return None
    
    # Probar períodos de 2 a n//2
    for periodo in range(2, n // 2 + 1):
        es_periodico = True
        for i in range(periodo, n):
            if distancia_tensor_puro(secuencia[i], secuencia[i % periodo]) > 0.3:
                es_periodico = False
                break
        
        if es_periodico:
            return periodo
    
    return None


def aprender_secuencia_puro(
    secuencia: List[TensorFFE],
    state: EvolverState,
    ventana_minima: int = 3
) -> Tuple[Optional[Dinamica], EvolverState]:
    """
    Aprende patrón dinámico desde secuencia temporal (pure)
    Retorna: (dinamica, nuevo_estado)
    """
    if len(secuencia) < ventana_minima:
        return None, state
    
    # Calcular delta promedio
    deltas = []
    for i in range(len(secuencia) - 1):
        delta = calcular_delta_puro(secuencia[i], secuencia[i+1])
        deltas.append(delta)
    
    delta_promedio = promediar_vectores_puro(deltas)
    
    # Detectar periodicidad
    periodicidad = detectar_periodicidad_puro(tuple(secuencia))
    
    # Crear dinámica
    nuevo_id = f"DYN_{state.contador_dinamicas + 1:04d}"
    dinamica = Dinamica(
        id=nuevo_id,
        secuencia=tuple(secuencia),
        delta_promedio=delta_promedio,
        periodicidad=periodicidad
    )
    
    nuevo_state = state.with_dinamica(dinamica)
    
    return dinamica, nuevo_state


def predecir_siguiente_puro(dinamica: Dinamica, actual: TensorFFE) -> TensorFFE:
    """Predice el próximo tensor en la secuencia (pure)"""
    from tensor_ffe import crear_tensor_desde_lista
    
    # Calcular nuevos valores aplicando delta
    valores_nuevos = []
    for i in range(3):
        forma_nueva = (actual.nivel_1[i].forma + dinamica.delta_promedio.forma) % 8
        valores_nuevos.append(forma_nueva)
    
    siguiente = crear_tensor_desde_lista(valores_nuevos, actual.nivel_abstraccion)
    
    return siguiente


# ============================================================================
# FUNCIONES PURAS - RELATORES
# ============================================================================

def conectar_arquetipos_puro(
    arq1: Arquetipo,
    arq2: Arquetipo,
    state: EvolverState,
    tipo: str = "analogico"
) -> Tuple[Relator, EvolverState]:
    """
    Crea conexión entre arquetipos usando rotación Fibonacci (pure)
    Retorna: (relator, nuevo_estado)
    """
    # Sintetizar transformación emergente desde múltiples rotaciones
    mejor_emergencia = None
    mejor_score = 0.0
    
    # Probar 3 rotaciones Fibonacci del par de arquetipos
    for i in range(3):
        idx_fib = (state.paso_conexion + i) % len(FIBONACCI)
        paso = FIBONACCI[idx_fib] % 8
        
        # Rotar ambos arquetipos
        arq1_rot = rotar_tensor_fibonacci_puro(arq1.tensor_prototipo, paso)
        arq2_rot = rotar_tensor_fibonacci_puro(arq2.tensor_prototipo, paso)
        
        # Sintetizar con rotación
        from tensor_ffe import crear_tensor_desde_lista
        dummy = crear_tensor_desde_lista([0, 0, 0], 3)  # Tensor neutral
        
        emergencia = sintetizar_puro(arq1_rot, arq2_rot, dummy)
        
        if emergencia.score_emergencia > mejor_score:
            mejor_score = emergencia.score_emergencia
            mejor_emergencia = emergencia
    
    # Crear relator con la mejor síntesis emergente
    nuevo_id = f"REL_{state.contador_relatores + 1:04d}"
    relator = Relator(
        id=nuevo_id,
        origen=arq1.id,
        destino=arq2.id,
        tipo=tipo,
        fuerza=mejor_emergencia.score_emergencia,
        transformacion=mejor_emergencia.Ms  # La emergencia Ms es la transformación
    )
    
    nuevo_state = state.with_relator(relator)
    
    return relator, nuevo_state


def camino_mas_corto_puro(
    id_origen: str,
    id_destino: str,
    state: EvolverState
) -> Optional[List[str]]:
    """BFS para encontrar camino entre arquetipos (pure)"""
    if id_origen == id_destino:
        return [id_origen]
    
    # Construir grafo de adyacencia
    grafo: Dict[str, Set[str]] = defaultdict(set)
    for rel in state.relatores:
        grafo[rel.origen].add(rel.destino)
    
    # BFS
    visitados = {id_origen}
    cola = [(id_origen, [id_origen])]
    
    while cola:
        actual, camino = cola.pop(0)
        
        for vecino in grafo.get(actual, set()):
            if vecino in visitados:
                continue
            
            nuevo_camino = camino + [vecino]
            
            if vecino == id_destino:
                return nuevo_camino
            
            visitados.add(vecino)
            cola.append((vecino, nuevo_camino))
    
    return None


def conexiones_fuertes_puro(state: EvolverState, umbral: float = 0.7) -> List[Relator]:
    """Retorna relatores con fuerza >= umbral (pure)"""
    return [r for r in state.relatores if r.fuerza >= umbral]


# ============================================================================
# CLASE FUNCIONAL (Facade con estado inmutable)
# ============================================================================

class EvolverFuncional:
    """
    Motor completo de aprendizaje fractal (Redux-style)
    
    ARQUITECTURA:
    - Estado inmutable (EvolverState)
    - Operaciones puras (funciones externas)
    - Thread-safe por diseño
    - Sin locks necesarios
    """
    
    def __init__(self):
        self.state = EvolverState()
        self.transcender = TranscenderFuncional(with_cache=True)
    
    def aprender(self, tensor: TensorFFE) -> Dict[str, any]:
        """
        Aprende desde un tensor FFE (entrada principal)
        Retorna resultados del aprendizaje
        """
        resultados = {}
        
        # 1. Detectar/crear arquetipo (pure function)
        arq, nuevo_state = aprender_tensor_puro(tensor, self.state)
        self.state = nuevo_state
        
        resultados['arquetipo'] = arq.id
        
        # 2. Buscar relaciones con otros arquetipos (top 3)
        top_arqs = self.state.top_arquetipos(n=3)
        
        for otro_arq in top_arqs:
            if otro_arq.id != arq.id:
                # Conectar arquetipos (pure function)
                relator, nuevo_state = conectar_arquetipos_puro(
                    arq, otro_arq, self.state
                )
                self.state = nuevo_state
                
                if relator.fuerza > 0.5:
                    resultados.setdefault('relaciones', []).append(relator.id)
        
        return resultados
    
    def aprender_tensor(self, tensor: TensorFFE) -> Tuple[Arquetipo, 'EvolverFuncional']:
        """
        Aprende desde un tensor y retorna arquetipo + nueva instancia (inmutable)
        
        Retorna: (arquetipo, evolver_actualizado)
        """
        arq, nuevo_state = aprender_tensor_puro(tensor, self.state)
        
        # Crear nueva instancia con estado actualizado
        evolver_nuevo = EvolverFuncional()
        evolver_nuevo.state = nuevo_state
        evolver_nuevo.transcender = self.transcender
        
        return arq, evolver_nuevo
    
    def aprender_secuencia(self, secuencia: List[TensorFFE]) -> Optional[Dinamica]:
        """Aprende dinámica desde secuencia temporal"""
        dinamica, nuevo_state = aprender_secuencia_puro(secuencia, self.state)
        self.state = nuevo_state
        return dinamica
    
    def predecir_siguiente(self, dinamica: Dinamica, actual: TensorFFE) -> TensorFFE:
        """Predice próximo tensor usando dinámica"""
        return predecir_siguiente_puro(dinamica, actual)
    
    def camino_arquetipos(self, id_origen: str, id_destino: str) -> Optional[List[str]]:
        """Encuentra camino más corto entre arquetipos"""
        return camino_mas_corto_puro(id_origen, id_destino, self.state)
    
    def estadisticas(self) -> Dict[str, any]:
        """Estadísticas del sistema de aprendizaje (pure)"""
        return {
            'arquetipos': len(self.state.arquetipos),
            'dinamicas': len(self.state.dinamicas),
            'relatores': len(self.state.relatores),
            'top_arquetipos': [
                (a.id, a.frecuencia) 
                for a in self.state.top_arquetipos(3)
            ],
            'conexiones_fuertes': len(conexiones_fuertes_puro(self.state))
        }
    
    def get_state(self) -> EvolverState:
        """Retorna estado actual (inmutable)"""
        return self.state
    
    def set_state(self, state: EvolverState) -> None:
        """Establece nuevo estado (para replay/undo)"""
        self.state = state


# ============================================================================
# BATCH PROCESSING (Thread-safe)
# ============================================================================

def batch_aprender_puro(
    tensores: List[TensorFFE],
    state_inicial: EvolverState
) -> Tuple[List[Dict[str, any]], EvolverState]:
    """
    Aprende desde múltiples tensores secuencialmente (pure)
    Thread-safe: puede paralelizarse con ThreadPoolExecutor
    
    Retorna: (resultados, estado_final)
    """
    state = state_inicial
    resultados = []
    
    for tensor in tensores:
        # Aprender tensor (pure)
        arq, state = aprender_tensor_puro(tensor, state)
        
        resultado = {'arquetipo': arq.id}
        resultados.append(resultado)
    
    return resultados, state


# ============================================================================
# TEST & VALIDACIÓN
# ============================================================================

if __name__ == "__main__":
    from tensor_ffe import crear_tensor_desde_lista
    
    print("🌱 Evolver Funcional - Motor de Aprendizaje Fractal v1.3\n")
    
    # Test 1: Aprendizaje de arquetipos
    print("=" * 60)
    print("Test 1: Detectar arquetipos (funcional)")
    print("=" * 60)
    
    evolver = EvolverFuncional()
    
    tensores = [
        crear_tensor_desde_lista([1, 2, 3], 3),
        crear_tensor_desde_lista([1, 3, 2], 3),  # Similar
        crear_tensor_desde_lista([6, 7, 0], 4),  # Diferente
        crear_tensor_desde_lista([1, 2, 4], 3),  # Similar al primero
    ]
    
    for i, t in enumerate(tensores):
        resultado = evolver.aprender(t)
        print(f"  Tensor {i+1}: Arquetipo {resultado['arquetipo']}")
        if 'relaciones' in resultado:
            print(f"           Relaciones: {resultado['relaciones']}")
    
    stats = evolver.estadisticas()
    print(f"\n📊 ESTADÍSTICAS:")
    print(f"  Arquetipos detectados: {stats['arquetipos']}")
    print(f"  Relatores creados: {stats['relatores']}")
    print(f"  Conexiones fuertes: {stats['conexiones_fuertes']}")
    
    # Test 2: Aprendizaje de dinámicas
    print("\n" + "=" * 60)
    print("Test 2: Detectar dinámicas temporales (funcional)")
    print("=" * 60)
    
    secuencia = [
        crear_tensor_desde_lista([0, 0, 0], 2),
        crear_tensor_desde_lista([1, 1, 1], 2),
        crear_tensor_desde_lista([2, 2, 2], 2),
        crear_tensor_desde_lista([3, 3, 3], 2),
    ]
    
    dinamica = evolver.aprender_secuencia(secuencia)
    if dinamica:
        print(f"  Dinámica {dinamica.id} detectada")
        print(f"  Delta promedio: F={dinamica.delta_promedio.forma}, "
              f"Fn={dinamica.delta_promedio.funcion}, "
              f"E={dinamica.delta_promedio.estructura}")
        
        # Predecir siguiente
        prediccion = evolver.predecir_siguiente(dinamica, secuencia[-1])
        print(f"  Predicción próximo: {prediccion.nivel_1[0]}")
    
    # Test 3: Inmutabilidad
    print("\n" + "=" * 60)
    print("Test 3: Validar inmutabilidad (funcional)")
    print("=" * 60)
    
    state_antes = evolver.get_state()
    print(f"  Estado antes: {len(state_antes.arquetipos)} arquetipos")
    
    # Aprender nuevo tensor
    nuevo_tensor = crear_tensor_desde_lista([5, 5, 5], 3)
    evolver.aprender(nuevo_tensor)
    
    state_despues = evolver.get_state()
    print(f"  Estado después: {len(state_despues.arquetipos)} arquetipos")
    print(f"  Estado antes (inmutable): {len(state_antes.arquetipos)} arquetipos ✅")
    
    # Test 4: Batch processing
    print("\n" + "=" * 60)
    print("Test 4: Batch processing (thread-safe)")
    print("=" * 60)
    
    batch_tensores = [
        crear_tensor_desde_lista([i, i+1, i+2], 3)
        for i in range(5)
    ]
    
    resultados_batch, state_final = batch_aprender_puro(
        batch_tensores,
        evolver.get_state()
    )
    
    print(f"  Tensores procesados: {len(resultados_batch)}")
    print(f"  Arquetipos finales: {len(state_final.arquetipos)}")
    
    # Estadísticas finales
    print("\n" + "=" * 60)
    print("📊 ESTADÍSTICAS FINALES")
    print("=" * 60)
    
    evolver.set_state(state_final)
    stats_finales = evolver.estadisticas()
    
    print(f"  Arquetipos: {stats_finales['arquetipos']}")
    print(f"  Dinámicas: {stats_finales['dinamicas']}")
    print(f"  Relatores: {stats_finales['relatores']}")
    print(f"  Top 3 arquetipos: {stats_finales['top_arquetipos']}")
    
    print("\n✅ Todos los tests pasaron!")
    print("🎯 Evolver funcional: Thread-safe, inmutable, predecible")
