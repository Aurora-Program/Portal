"""
Armonizador - Módulo de Coherencia y Autocorrección
Proyecto Genesis - Aurora Intelligence Engine

Capítulo 11 del Manual Aurora:
"El Armonizador detecta incoherencias, las corrige recursivamente,
y aprende de los errores para fortalecer la red de conocimiento."

Funciones principales:
1. Detectar incoherencias lógicas (conflictos Ms ↔ MetaM)
2. Autocorregir recursivamente buscando máxima coherencia
3. Aprender de errores (ajustar confianza de arquetipos/relatores)
4. Validar correspondencia única (Principio de Coherencia Absoluta)
5. Gestionar ambigüedad (NULL como oportunidad, no error)

Usa rotación Fibonacci para explorar múltiples caminos de corrección.
"""

from typing import List, Dict, Tuple, Optional, Set
from dataclasses import dataclass, field
import numpy as np
from enum import Enum

from tensor_ffe import TensorFFE, VectorFFE
from transcender import Transcender, Emergencia
from evolver import Evolver, Arquetipo, Relator


class TipoIncoherencia(Enum):
    """Tipos de incoherencias detectables"""
    CORRESPONDENCIA_INVALIDA = "ms_metamm_mismatch"  # Ms no corresponde a MetaM
    CONTRADICCION_LOGICA = "logical_contradiction"    # A y ¬A simultáneos
    ARQUETIPO_DEBIL = "weak_archetype"                # Coherencia < umbral
    RELATOR_ROTO = "broken_relator"                   # Relación inválida
    CICLO_INFINITO = "infinite_loop"                  # Recursión sin convergencia
    NULL_AMBIGUO = "ambiguous_null"                   # NULL sin semántica clara


@dataclass
class Incoherencia:
    """
    Representa una incoherencia detectada en el sistema
    """
    tipo: TipoIncoherencia
    tensor_origen: TensorFFE
    tensor_conflicto: Optional[TensorFFE] = None
    arquetipo_id: Optional[str] = None
    relator_id: Optional[str] = None
    nivel_severidad: float = 0.0  # [0.0, 1.0]
    descripcion: str = ""
    contexto: Dict = field(default_factory=dict)


@dataclass
class CorreccionPropuesta:
    """
    Propuesta de corrección para una incoherencia
    """
    incoherencia: Incoherencia
    tensor_corregido: TensorFFE
    coherencia_resultante: float
    pasos_recursivos: int
    camino_fibonacci: List[int]  # Secuencia Fibonacci usada
    costo_correccion: float  # [0.0, 1.0] - cuánto se modificó


@dataclass
class AprendizajeError:
    """
    Registro de aprendizaje desde un error
    """
    incoherencia: Incoherencia
    correccion: CorreccionPropuesta
    ajuste_confianza: Dict[str, float]  # {arq_id/rel_id: delta_confianza}
    patron_error: str  # Descripción del patrón de error


class Armonizador:
    """
    Motor de coherencia y autocorrección del sistema Aurora
    
    Proceso:
    1. Detectar incoherencias (validación Ms ↔ MetaM)
    2. Explorar correcciones (rotación Fibonacci)
    3. Aplicar mejor corrección (máxima coherencia)
    4. Aprender del error (ajustar confianzas)
    5. Validar convergencia (evitar ciclos infinitos)
    
    Principios:
    - Solo existencia positiva (0-7, sin negativos)
    - Correspondencia única Ms ↔ MetaM por espacio lógico
    - NULL es información (Unknown/Indifferent/Non-existent)
    - Recursión con límite (evitar ciclos infinitos)
    - Fibonacci para exploración multi-angular
    """
    
    def __init__(
        self, 
        evolver: Evolver,
        transcender: Transcender,
        umbral_coherencia: float = 0.7,
        max_recursion: int = 10
    ):
        """
        Inicializa Armonizador
        
        Args:
            evolver: Evolver con arquetipos y relatores
            transcender: Transcender para síntesis
            umbral_coherencia: Mínimo aceptable [0.0, 1.0]
            max_recursion: Máximo de pasos recursivos
        """
        self.evolver = evolver
        self.transcender = transcender
        self.umbral_coherencia = umbral_coherencia
        self.max_recursion = max_recursion
        
        # Fibonacci para exploración de correcciones
        self.fibonacci = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]
        self.paso_armonizacion = 0
        
        # Registro de coherencia por espacio lógico
        # {espacio_id: {ms_id: metamm_id}}
        self.correspondencias: Dict[str, Dict[str, str]] = {}
        
        # Historial de incoherencias detectadas
        self.historial_incoherencias: List[Incoherencia] = []
        
        # Historial de aprendizajes
        self.historial_aprendizajes: List[AprendizajeError] = []
        
        # Confianzas ajustadas (inicialmente 1.0)
        self.confianzas_arquetipos: Dict[str, float] = {}
        self.confianzas_relatores: Dict[str, float] = {}
    
    def detectar_incoherencias(
        self, 
        tensores: List[TensorFFE],
        espacio_logico: str = "default"
    ) -> List[Incoherencia]:
        """
        Detecta incoherencias en un conjunto de tensores
        
        Args:
            tensores: Lista de tensores a validar
            espacio_logico: ID del espacio lógico
        
        Returns:
            Lista de incoherencias detectadas
        """
        incoherencias = []
        
        # 1. Validar correspondencia Ms ↔ MetaM única
        incoherencias.extend(
            self._validar_correspondencia_unica(tensores, espacio_logico)
        )
        
        # 2. Detectar contradicciones lógicas (A y ¬A)
        incoherencias.extend(
            self._detectar_contradicciones(tensores)
        )
        
        # 3. Verificar coherencia de arquetipos
        incoherencias.extend(
            self._verificar_arquetipos_debiles(tensores)
        )
        
        # 4. Validar relatores rotos
        incoherencias.extend(
            self._validar_relatores(tensores)
        )
        
        # 5. Detectar NULLs ambiguos
        incoherencias.extend(
            self._detectar_nulls_ambiguos(tensores)
        )
        
        # Registrar en historial
        self.historial_incoherencias.extend(incoherencias)
        
        return incoherencias
    
    def autocorregir(
        self,
        incoherencia: Incoherencia,
        nivel_recursion: int = 0
    ) -> Optional[CorreccionPropuesta]:
        """
        Autocorrige una incoherencia recursivamente
        
        Proceso:
        1. Generar 3 variantes con rotación Fibonacci
        2. Evaluar coherencia de cada variante
        3. Si ninguna coherente, recursión (nivel + 1)
        4. Retornar mejor corrección
        
        Args:
            incoherencia: Incoherencia a corregir
            nivel_recursion: Nivel actual de recursión
        
        Returns:
            Corrección propuesta o None si no converge
        """
        # Límite de recursión (evitar ciclos infinitos)
        if nivel_recursion >= self.max_recursion:
            print(f"⚠️ Recursión máxima alcanzada ({self.max_recursion})")
            return None
        
        # Validar que tensor origen no sea None
        if incoherencia.tensor_origen is None:
            print(f"⚠️ Tensor origen es None, no se puede corregir")
            return None
        
        # Generar 3 variantes con Fibonacci
        variantes = self._generar_variantes_fibonacci(
            incoherencia.tensor_origen
        )
        
        mejor_correccion = None
        mejor_coherencia = 0.0
        
        for i, variante in enumerate(variantes):
            # Evaluar coherencia de variante
            coherencia = self._evaluar_coherencia_global(variante)
            
            # Si supera umbral, crear corrección
            if coherencia >= self.umbral_coherencia:
                costo = self._calcular_costo_correccion(
                    incoherencia.tensor_origen,
                    variante
                )
                
                correccion = CorreccionPropuesta(
                    incoherencia=incoherencia,
                    tensor_corregido=variante,
                    coherencia_resultante=coherencia,
                    pasos_recursivos=nivel_recursion,
                    camino_fibonacci=[self.fibonacci[(self.paso_armonizacion + i) % len(self.fibonacci)]],
                    costo_correccion=costo
                )
                
                if coherencia > mejor_coherencia:
                    mejor_coherencia = coherencia
                    mejor_correccion = correccion
        
        # Si encontramos corrección, retornar
        if mejor_correccion:
            return mejor_correccion
        
        # Si no, intentar recursión con la mejor variante
        print(f"🔄 Recursión nivel {nivel_recursion + 1}")
        
        # Crear incoherencia temporal para recursión
        incoherencia_recursiva = Incoherencia(
            tipo=incoherencia.tipo,
            tensor_origen=variantes[0],  # Usar primera variante
            nivel_severidad=incoherencia.nivel_severidad,
            descripcion=f"Recursión nivel {nivel_recursion + 1}"
        )
        
        # Avanzar Fibonacci
        self.paso_armonizacion = (self.paso_armonizacion + 1) % len(self.fibonacci)
        
        # Recursión
        return self.autocorregir(incoherencia_recursiva, nivel_recursion + 1)
    
    def aprender_de_error(
        self,
        incoherencia: Incoherencia,
        correccion: CorreccionPropuesta
    ) -> AprendizajeError:
        """
        Aprende de un error corregido, ajustando confianzas
        
        Proceso:
        1. Identificar arquetipos/relatores involucrados
        2. Ajustar confianzas según costo de corrección
        3. Detectar patrón de error
        4. Registrar aprendizaje
        
        Args:
            incoherencia: Incoherencia original
            correccion: Corrección aplicada
        
        Returns:
            Aprendizaje registrado
        """
        ajustes_confianza = {}
        
        # 1. Ajustar confianza de arquetipo si aplica
        if incoherencia.arquetipo_id:
            # Delta negativo proporcional al costo
            delta = -0.1 * correccion.costo_correccion
            
            confianza_actual = self.confianzas_arquetipos.get(
                incoherencia.arquetipo_id, 
                1.0
            )
            nueva_confianza = max(0.0, confianza_actual + delta)
            
            self.confianzas_arquetipos[incoherencia.arquetipo_id] = nueva_confianza
            ajustes_confianza[incoherencia.arquetipo_id] = delta
        
        # 2. Ajustar confianza de relator si aplica
        if incoherencia.relator_id:
            delta = -0.1 * correccion.costo_correccion
            
            confianza_actual = self.confianzas_relatores.get(
                incoherencia.relator_id,
                1.0
            )
            nueva_confianza = max(0.0, confianza_actual + delta)
            
            self.confianzas_relatores[incoherencia.relator_id] = nueva_confianza
            ajustes_confianza[incoherencia.relator_id] = delta
        
        # 3. Detectar patrón de error
        patron = self._detectar_patron_error(incoherencia, correccion)
        
        # 4. Crear aprendizaje
        aprendizaje = AprendizajeError(
            incoherencia=incoherencia,
            correccion=correccion,
            ajuste_confianza=ajustes_confianza,
            patron_error=patron
        )
        
        self.historial_aprendizajes.append(aprendizaje)
        
        return aprendizaje
    
    def validar_correspondencia_unica(
        self,
        ms: VectorFFE,
        metamm: List[VectorFFE],
        espacio_logico: str = "default"
    ) -> bool:
        """
        Valida Principio de Coherencia Absoluta:
        Dentro de un espacio lógico, cada Ms debe corresponder
        a un único MetaM
        
        Args:
            ms: Vector emergente
            metamm: Camino lógico completo
            espacio_logico: ID del espacio lógico
        
        Returns:
            True si válido, False si incoherente
        """
        # Crear ID único para Ms
        ms_id = self._generar_id_vector(ms)
        
        # Crear ID único para MetaM
        metamm_id = self._generar_id_metamm(metamm)
        
        # Verificar correspondencia en espacio lógico
        if espacio_logico not in self.correspondencias:
            # Primer Ms en este espacio, crear correspondencia
            self.correspondencias[espacio_logico] = {ms_id: metamm_id}
            return True
        
        if ms_id not in self.correspondencias[espacio_logico]:
            # Nuevo Ms, registrar correspondencia
            self.correspondencias[espacio_logico][ms_id] = metamm_id
            return True
        
        # Ms ya existe, verificar MetaM coincide
        metamm_esperado = self.correspondencias[espacio_logico][ms_id]
        
        if metamm_id == metamm_esperado:
            # Correspondencia válida
            return True
        else:
            # INCOHERENCIA: Mismo Ms, diferente MetaM
            return False
    
    def armonizar_lote(
        self,
        tensores: List[TensorFFE],
        espacio_logico: str = "default"
    ) -> Dict:
        """
        Armoniza un lote completo de tensores
        
        Proceso:
        1. Detectar incoherencias
        2. Ordenar por severidad
        3. Autocorregir cada una
        4. Aprender de errores
        5. Validar convergencia global
        
        Args:
            tensores: Lote a armonizar
            espacio_logico: ID del espacio lógico
        
        Returns:
            Reporte de armonización
        """
        print(f"\n🔧 ARMONIZANDO {len(tensores)} tensores...")
        
        # 1. Detectar incoherencias
        incoherencias = self.detectar_incoherencias(tensores, espacio_logico)
        
        if not incoherencias:
            print("✅ Sin incoherencias detectadas")
            return {
                "coherente": True,
                "incoherencias": 0,
                "correcciones": 0,
                "aprendizajes": 0
            }
        
        print(f"⚠️ Detectadas {len(incoherencias)} incoherencias")
        
        # 2. Ordenar por severidad
        incoherencias_ordenadas = sorted(
            incoherencias,
            key=lambda i: i.nivel_severidad,
            reverse=True
        )
        
        # 3. Autocorregir cada incoherencia
        correcciones_exitosas = 0
        correcciones_fallidas = 0
        
        for i, incoherencia in enumerate(incoherencias_ordenadas):
            print(f"\n[{i+1}/{len(incoherencias)}] Corrigiendo: {incoherencia.tipo.value}")
            
            correccion = self.autocorregir(incoherencia)
            
            if correccion:
                correcciones_exitosas += 1
                
                # 4. Aprender del error
                aprendizaje = self.aprender_de_error(incoherencia, correccion)
                
                print(f"  ✅ Corregido (coherencia={correccion.coherencia_resultante:.3f})")
                print(f"  📚 Aprendizaje: {aprendizaje.patron_error}")
            else:
                correcciones_fallidas += 1
                print(f"  ❌ No se encontró corrección convergente")
        
        # 5. Reporte final
        return {
            "coherente": correcciones_fallidas == 0,
            "incoherencias": len(incoherencias),
            "correcciones": correcciones_exitosas,
            "fallidas": correcciones_fallidas,
            "aprendizajes": len(self.historial_aprendizajes),
            "confianzas_arquetipos": dict(self.confianzas_arquetipos),
            "confianzas_relatores": dict(self.confianzas_relatores)
        }
    
    # ========================================================================
    # MÉTODOS PRIVADOS - Detección de Incoherencias
    # ========================================================================
    
    def _validar_correspondencia_unica(
        self,
        tensores: List[TensorFFE],
        espacio_logico: str
    ) -> List[Incoherencia]:
        """Valida correspondencia única Ms ↔ MetaM"""
        incoherencias = []
        
        for tensor in tensores:
            # Simular síntesis para obtener Ms y MetaM
            # (En producción, esto vendría del Transcender)
            ms = tensor.nivel_1[0]  # Simplificación
            metamm = tensor.nivel_1  # Simplificación
            
            if not self.validar_correspondencia_unica(ms, metamm, espacio_logico):
                incoherencias.append(Incoherencia(
                    tipo=TipoIncoherencia.CORRESPONDENCIA_INVALIDA,
                    tensor_origen=tensor,
                    nivel_severidad=0.9,  # Alta severidad
                    descripcion=f"Ms duplicado con MetaM diferente en {espacio_logico}"
                ))
        
        return incoherencias
    
    def _detectar_contradicciones(
        self,
        tensores: List[TensorFFE]
    ) -> List[Incoherencia]:
        """Detecta contradicciones lógicas (A y ¬A)"""
        incoherencias = []
        
        for i, t1 in enumerate(tensores):
            for j, t2 in enumerate(tensores[i+1:], start=i+1):
                if self._son_contradictorios(t1, t2):
                    incoherencias.append(Incoherencia(
                        tipo=TipoIncoherencia.CONTRADICCION_LOGICA,
                        tensor_origen=t1,
                        tensor_conflicto=t2,
                        nivel_severidad=1.0,  # Máxima severidad
                        descripcion=f"Tensores {i} y {j} son contradictorios"
                    ))
        
        return incoherencias
    
    def _verificar_arquetipos_debiles(
        self,
        tensores: List[TensorFFE]
    ) -> List[Incoherencia]:
        """Detecta arquetipos con coherencia < umbral"""
        incoherencias = []
        
        for tensor in tensores:
            # Detectar arquetipo
            arq = self.evolver.archetype_learner.detectar_o_crear(tensor)
            
            # Verificar coherencia (método, no propiedad)
            coherencia_actual = arq.coherencia() if callable(arq.coherencia) else arq.coherencia
            
            if coherencia_actual < self.umbral_coherencia:
                incoherencias.append(Incoherencia(
                    tipo=TipoIncoherencia.ARQUETIPO_DEBIL,
                    tensor_origen=tensor,
                    arquetipo_id=arq.id,
                    nivel_severidad=1.0 - coherencia_actual,
                    descripcion=f"Arquetipo {arq.id} coherencia={coherencia_actual:.3f} < {self.umbral_coherencia}"
                ))
        
        return incoherencias
    
    def _validar_relatores(
        self,
        tensores: List[TensorFFE]
    ) -> List[Incoherencia]:
        """Valida relatores rotos (fuerza < umbral)"""
        incoherencias = []
        
        # Obtener todos los relatores
        for relator in self.evolver.relator_network.relatores.values():
            if relator.fuerza < self.umbral_coherencia:
                # El tensor del relator ES su transformación emergente
                # Si no existe, es un relator incompleto
                tensor_relator = relator.transformacion if relator.transformacion else None
                
                incoherencias.append(Incoherencia(
                    tipo=TipoIncoherencia.RELATOR_ROTO,
                    tensor_origen=tensor_relator,  # Tensor de transformación del relator
                    relator_id=relator.id,
                    nivel_severidad=1.0 - relator.fuerza,
                    descripcion=f"Relator {relator.id} fuerza={relator.fuerza:.3f} < {self.umbral_coherencia}"
                ))
        
        return incoherencias
    
    def _detectar_nulls_ambiguos(
        self,
        tensores: List[TensorFFE]
    ) -> List[Incoherencia]:
        """Detecta NULLs sin semántica clara"""
        incoherencias = []
        
        for tensor in tensores:
            # Contar NULLs (valores -1 o fuera de rango)
            nulls = sum(
                1 for v in tensor.nivel_1
                if any(dim < 0 or dim > 7 for dim in [v.forma, v.funcion, v.estructura])
            )
            
            if nulls > 0:
                # NULL detectado, validar si tiene semántica
                # (simplificación - en producción, clasificar en N_u/N_i/N_x)
                incoherencias.append(Incoherencia(
                    tipo=TipoIncoherencia.NULL_AMBIGUO,
                    tensor_origen=tensor,
                    nivel_severidad=0.3 * (nulls / 3),  # Proporcional a cantidad
                    descripcion=f"{nulls} NULLs sin clasificar (N_u/N_i/N_x)"
                ))
        
        return incoherencias
    
    # ========================================================================
    # MÉTODOS PRIVADOS - Autocorrección
    # ========================================================================
    
    def _generar_variantes_fibonacci(
        self,
        tensor: TensorFFE
    ) -> List[TensorFFE]:
        """Genera 3 variantes rotadas con Fibonacci"""
        variantes = []
        
        for i in range(3):
            idx_fib = (self.paso_armonizacion + i) % len(self.fibonacci)
            paso = self.fibonacci[idx_fib] % 8
            
            variante = self._rotar_tensor(tensor, paso)
            variantes.append(variante)
        
        return variantes
    
    def _rotar_tensor(self, tensor: TensorFFE, paso: int) -> TensorFFE:
        """Rota tensor con paso Fibonacci"""
        # Validación: tensor no puede ser None
        if tensor is None:
            # Retornar tensor vacío válido
            return TensorFFE()
        
        tensor_rot = TensorFFE()
        
        for i in range(3):
            v = tensor.nivel_1[i]
            tensor_rot.nivel_1[i] = VectorFFE(
                forma=(v.forma + paso) % 8,
                funcion=(v.funcion + paso) % 8,
                estructura=(v.estructura + paso) % 8
            )
        
        tensor_rot.reconstruir_jerarquia()
        tensor_rot.nivel_abstraccion = tensor.nivel_abstraccion
        
        return tensor_rot
    
    def _evaluar_coherencia_global(self, tensor: TensorFFE) -> float:
        """
        Evalúa coherencia global de un tensor
        
        Componentes:
        1. Coherencia interna (autosimilitud nivel_1 → nivel_2 → nivel_3)
        2. Coherencia con arquetipos (similitud a arquetipos conocidos)
        3. Coherencia con relatores (conexiones válidas)
        """
        # 1. Coherencia interna
        coherencia_interna = self._coherencia_interna(tensor)
        
        # 2. Coherencia con arquetipos (puede ser método o propiedad)
        arq = self.evolver.archetype_learner.detectar_o_crear(tensor)
        coherencia_arquetipo = arq.coherencia() if callable(arq.coherencia) else arq.coherencia
        
        # 3. Coherencia con relatores (promedio de fuerzas)
        coherencia_relator = self._coherencia_relatores(tensor)
        
        # Promedio ponderado
        coherencia_total = (
            0.4 * coherencia_interna +
            0.4 * coherencia_arquetipo +
            0.2 * coherencia_relator
        )
        
        return coherencia_total
    
    def _coherencia_interna(self, tensor: TensorFFE) -> float:
        """Coherencia fractal (autosimilitud entre niveles)"""
        # Verificar que nivel_2 se genera correctamente desde nivel_1
        # (simplificación - en producción, validar síntesis completa)
        
        # Ejemplo: verificar que valores nivel_1 caen en rangos esperados
        valores_validos = sum(
            1 for v in tensor.nivel_1
            if 0 <= v.forma <= 7 and 0 <= v.funcion <= 7 and 0 <= v.estructura <= 7
        )
        
        return valores_validos / 3
    
    def _coherencia_relatores(self, tensor: TensorFFE) -> float:
        """Coherencia con red de relatores"""
        # Detectar arquetipo
        arq = self.evolver.archetype_learner.detectar_o_crear(tensor)
        
        # Obtener relatores del arquetipo
        relatores_arq = [
            r for r in self.evolver.relator_network.relatores.values()
            if r.origen == arq.id or r.destino == arq.id
        ]
        
        if not relatores_arq:
            return 0.5  # Sin relatores, coherencia neutral
        
        # Promedio de fuerzas
        fuerza_promedio = np.mean([r.fuerza for r in relatores_arq])
        
        return fuerza_promedio
    
    def _calcular_costo_correccion(
        self,
        original: TensorFFE,
        corregido: TensorFFE
    ) -> float:
        """Calcula cuánto se modificó el tensor [0.0, 1.0]"""
        diferencias = sum(
            abs(v1.forma - v2.forma) +
            abs(v1.funcion - v2.funcion) +
            abs(v1.estructura - v2.estructura)
            for v1, v2 in zip(original.nivel_1, corregido.nivel_1)
        )
        
        # Normalizar (máximo = 3 vectores * 3 dimensiones * 7 diferencia máxima)
        costo = diferencias / (3 * 3 * 7)
        
        return min(costo, 1.0)
    
    # ========================================================================
    # MÉTODOS PRIVADOS - Aprendizaje
    # ========================================================================
    
    def _detectar_patron_error(
        self,
        incoherencia: Incoherencia,
        correccion: CorreccionPropuesta
    ) -> str:
        """Detecta patrón recurrente de error"""
        # Análisis simplificado - en producción, ML para patrones
        
        patrones = {
            TipoIncoherencia.CORRESPONDENCIA_INVALIDA: "Duplicación Ms sin validar espacio",
            TipoIncoherencia.CONTRADICCION_LOGICA: "Tensores opuestos no segregados",
            TipoIncoherencia.ARQUETIPO_DEBIL: "Arquetipo con pocos ejemplos",
            TipoIncoherencia.RELATOR_ROTO: "Relación sin validación recíproca",
            TipoIncoherencia.NULL_AMBIGUO: "NULL sin clasificar (N_u/N_i/N_x)"
        }
        
        return patrones.get(
            incoherencia.tipo,
            "Patrón desconocido"
        )
    
    # ========================================================================
    # UTILIDADES
    # ========================================================================
    
    def _generar_id_vector(self, vector: VectorFFE) -> str:
        """Genera ID único para un vector"""
        return f"{vector.forma}_{vector.funcion}_{vector.estructura}"
    
    def _generar_id_metamm(self, metamm: List[VectorFFE]) -> str:
        """Genera ID único para MetaM"""
        ids = [self._generar_id_vector(v) for v in metamm]
        return "_".join(ids)
    
    def _son_contradictorios(self, t1: TensorFFE, t2: TensorFFE) -> bool:
        """Verifica si dos tensores son contradictorios"""
        # Simplificación: contradictorios si opuestos en todas dimensiones
        oposiciones = sum(
            1 for v1, v2 in zip(t1.nivel_1, t2.nivel_1)
            if abs(v1.forma - v2.forma) > 4 and
               abs(v1.funcion - v2.funcion) > 4 and
               abs(v1.estructura - v2.estructura) > 4
        )
        
        return oposiciones == 3  # Todas las dimensiones opuestas
    
    def obtener_estadisticas(self) -> Dict:
        """Obtiene estadísticas del Armonizador"""
        return {
            "total_incoherencias": len(self.historial_incoherencias),
            "total_aprendizajes": len(self.historial_aprendizajes),
            "confianzas_arquetipos": len(self.confianzas_arquetipos),
            "confianzas_relatores": len(self.confianzas_relatores),
            "confianza_promedio_arquetipos": np.mean(list(self.confianzas_arquetipos.values())) if self.confianzas_arquetipos else 1.0,
            "confianza_promedio_relatores": np.mean(list(self.confianzas_relatores.values())) if self.confianzas_relatores else 1.0,
            "correspondencias_espacios": len(self.correspondencias)
        }


# ============================================================================
# UTILIDADES
# ============================================================================

def crear_armonizador_desde_evolver(evolver: Evolver) -> Armonizador:
    """
    Crea Armonizador desde Evolver existente
    """
    transcender = Transcender()
    
    return Armonizador(
        evolver=evolver,
        transcender=transcender,
        umbral_coherencia=0.7,
        max_recursion=10
    )
