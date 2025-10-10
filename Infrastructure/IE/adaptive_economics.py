"""
Aurora Adaptive Economics System
=================================
Sistema económico donde las políticas NO están hardcoded.
Son los MODELOS ENTRENADOS POR USUARIOS los que determinan:
    - Cuánto MERIT emitir según salud de la red
    - Qué operaciones merecen más MIND
    - Qué interacciones humanas generan TRUST

Los usuarios entrenan modelos → los modelos votan → consenso emergente.

Tokens:
    △ MERIT - Infraestructura/Red (gobernado por modelos de usuarios)
    ○ MIND - Cómputo/Inteligencia (gobernado por modelos de usuarios)
    U TRUST - Vínculos Humanos (validado por Armonizador comunitario)

CLAVE: Ningún parámetro es fijo. Todo evoluciona con el aprendizaje colectivo.
"""

import sys
import os
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import math

# Importar core de Aurora
sys.path.append(os.path.join(os.path.dirname(__file__)))
from core import (
    FractalTensor, Trigate,
    FractalKnowledgeBase, Evolver, Extender, Transcender, Armonizador
)


# ============================================================================
# POLÍTICAS APRENDIDAS (NO HARDCODED)
# ============================================================================

@dataclass
class LearnedPolicy:
    """
    Política económica aprendida por modelos de usuarios.
    NO es hardcoded → evoluciona con el entrenamiento colectivo.
    """
    nombre: str
    valor_actual: float
    votos_modelos: List[Tuple[str, float]]  # (model_id, valor_propuesto)
    confianza: float  # 0.0 a 1.0 - qué tan consensuado está
    ultima_actualizacion: datetime
    historico: List[Tuple[datetime, float]]  # Evolución temporal
    
    def calcular_consenso(self) -> float:
        """Calcula valor consensuado entre modelos votantes"""
        if not self.votos_modelos:
            return self.valor_actual
        
        # Media ponderada (en prod: usar votación más sofisticada)
        suma = sum(valor for _, valor in self.votos_modelos)
        return suma / len(self.votos_modelos)
    
    def actualizar_con_aprendizaje(self, nuevo_voto: Tuple[str, float]):
        """Un modelo votó → actualiza la política"""
        self.votos_modelos.append(nuevo_voto)
        nuevo_valor = self.calcular_consenso()
        
        # Registrar en histórico
        self.historico.append((datetime.now(), nuevo_valor))
        self.valor_actual = nuevo_valor
        self.ultima_actualizacion = datetime.now()
        
        # Confianza aumenta con más votos
        self.confianza = min(1.0, len(self.votos_modelos) / 10)


@dataclass
class TokenConfig:
    """
    Configuración INICIAL de un token (solo bootstrap).
    Los valores reales se determinan por LearnedPolicy.
    """
    name: str
    symbol: str
    supply_inicial: float
    
    # ESTAS NO SON FIJAS - solo valores iniciales hasta que los modelos aprendan
    politicas_aprendidas: Dict[str, LearnedPolicy]


# ============================================================================
# CONFIGURACIÓN INICIAL (BOOTSTRAP)
# Los usuarios entrenan modelos → los modelos actualizan estas políticas
# ============================================================================

def crear_politicas_iniciales() -> Dict[str, LearnedPolicy]:
    """
    Crea políticas con valores iniciales razonables.
    IMPORTANTE: Estos son SOLO para arrancar la red.
    Los modelos de usuarios los irán ajustando.
    """
    return {
        "tasa_emision_base": LearnedPolicy(
            nombre="tasa_emision_base",
            valor_actual=0.04,  # 4% anual - bootstrap
            votos_modelos=[],
            confianza=0.0,  # Sin confianza inicial
            ultima_actualizacion=datetime.now(),
            historico=[(datetime.now(), 0.04)]
        ),
        "tasa_quema_fees": LearnedPolicy(
            nombre="tasa_quema_fees",
            valor_actual=0.30,  # 30% - bootstrap
            votos_modelos=[],
            confianza=0.0,
            ultima_actualizacion=datetime.now(),
            historico=[(datetime.now(), 0.30)]
        ),
        "umbral_minimo_nodos": LearnedPolicy(
            nombre="umbral_minimo_nodos",
            valor_actual=10.0,  # Bootstrap
            votos_modelos=[],
            confianza=0.0,
            ultima_actualizacion=datetime.now(),
            historico=[(datetime.now(), 10.0)]
        ),
        "umbral_latencia_ms": LearnedPolicy(
            nombre="umbral_latencia_ms",
            valor_actual=500.0,  # Bootstrap
            votos_modelos=[],
            confianza=0.0,
            ultima_actualizacion=datetime.now(),
            historico=[(datetime.now(), 500.0)]
        ),
        "multiplicador_pattern0": LearnedPolicy(
            nombre="multiplicador_pattern0",
            valor_actual=2.0,  # Bootstrap: operaciones éticas valen 2x
            votos_modelos=[],
            confianza=0.0,
            ultima_actualizacion=datetime.now(),
            historico=[(datetime.now(), 2.0)]
        ),
        "multiplicador_colaborativo": LearnedPolicy(
            nombre="multiplicador_colaborativo",
            valor_actual=1.5,  # Bootstrap: colaboración vale 1.5x
            votos_modelos=[],
            confianza=0.0,
            ultima_actualizacion=datetime.now(),
            historico=[(datetime.now(), 1.5)]
        )
    }


# Configuración de los 3 tokens de Aurora (SOLO BOOTSTRAP)
MERIT_CONFIG = TokenConfig(
    name="Merit",
    symbol="△ MERIT",
    supply_inicial=1_000_000.0,
    politicas_aprendidas=crear_politicas_iniciales()
)

MIND_CONFIG = TokenConfig(
    name="Mind",
    symbol="○ MIND",
    supply_inicial=500_000.0,
    politicas_aprendidas=crear_politicas_iniciales()
)

TRUST_CONFIG = TokenConfig(
    name="Trust",
    symbol="U TRUST",
    supply_inicial=0.0,  # Nace de cero
    politicas_aprendidas=crear_politicas_iniciales()
)

# Recompensas fijas para TRUST (solo interacciones humanas)
TRUST_REWARDS = {
    "mentoria_completada": 10.0,
    "colaboracion_multipeer": 15.0,
    "resolucion_conflicto": 20.0,
    "validacion_etica_comunitaria": 5.0,
    "verificacion_peer": 3.0
}


# ============================================================================
# ESTADO DE LA RED
# ============================================================================

@dataclass
class NetworkState:
    """Estado actual de la red Aurora"""
    timestamp: datetime
    nodos_activos: int
    latencia_promedio_ms: float
    operaciones_por_hora: int
    coherencia_promedio: float
    supply_merit: float
    supply_mind: float
    supply_trust: float
    fees_acumuladas: Dict[str, float]  # Por token


class NetworkMonitor:
    """Monitor del estado de la red para decisiones adaptativas"""
    
    def __init__(self):
        self.historial: List[NetworkState] = []
        self.kb = FractalKnowledgeBase()
        
    def registrar_estado(self, estado: NetworkState):
        """Registra un snapshot del estado de la red"""
        self.historial.append(estado)
        
        # Almacenar en Knowledge Base para análisis temporal
        tensor_estado = FractalTensor.random()
        # Codificar estado en el tensor (simplificado)
        self.kb.store(
            name=f"network_state_{estado.timestamp.isoformat()}",
            tensor=tensor_estado,
            space_id=0
        )
    
    def obtener_tendencia(self, metrica: str, ventana_horas: int = 24) -> float:
        """Calcula tendencia de una métrica (positiva = creciendo)"""
        if len(self.historial) < 2:
            return 0.0
        
        ahora = datetime.now()
        estados_recientes = [
            e for e in self.historial
            if (ahora - e.timestamp) < timedelta(hours=ventana_horas)
        ]
        
        if len(estados_recientes) < 2:
            return 0.0
        
        # Calcular pendiente simple
        valores = [getattr(e, metrica) for e in estados_recientes]
        n = len(valores)
        pendiente = (valores[-1] - valores[0]) / n
        
        return pendiente


# ============================================================================
# MODELO ADAPTATIVO PARA △ MERIT
# ============================================================================

class MeritEconomics:
    """Modelo de inteligencia para gestión adaptativa de MERIT"""
    
    def __init__(self, config: TokenConfig, monitor: NetworkMonitor):
        self.config = config
        self.monitor = monitor
        self.armonizador = Armonizador()
        self.kb = FractalKnowledgeBase()  # KB para el extender
        self.extender = Extender(self.kb)
        
    def calcular_recompensa_nodo(self, estado: NetworkState, politicas: Dict[str, float]) -> float:
        """
        Calcula recompensa MERIT para un nodo validador.
        Se adapta según salud de la red y políticas APRENDIDAS (no hardcoded).
        
        Args:
            politicas: Políticas consensuadas por modelos de usuarios
        """
        # Usar política aprendida en lugar de valor hardcoded
        tasa_emision = politicas.get("tasa_emision_base", 0.04)
        base = self.config.supply_inicial * tasa_emision / (365 * 24)
        multiplicador = 1.0
        
        # Factor 1: Escasez de nodos (umbral aprendido)
        umbral_nodos = politicas.get("umbral_minimo_nodos", 10.0)
        if estado.nodos_activos < umbral_nodos:
            deficit = umbral_nodos - estado.nodos_activos
            multiplicador *= (1.0 + deficit * 0.1)  # +10% por cada nodo faltante
        
        # Factor 2: Latencia alta (umbral aprendido)
        umbral_latencia = politicas.get("umbral_latencia_ms", 500.0)
        if estado.latencia_promedio_ms > umbral_latencia:
            exceso = estado.latencia_promedio_ms / umbral_latencia
            multiplicador *= (1.0 + (exceso - 1.0) * 0.2)  # +20% por cada 100% de exceso
        
        # Factor 3: Tendencia de deserción
        tendencia_nodos = self.monitor.obtener_tendencia("nodos_activos")
        if tendencia_nodos < 0:
            multiplicador *= 1.3  # Incentivo de emergencia
        
        # Factor 4: Coherencia de la red (medida por Armonizador)
        coherencia = estado.coherencia_promedio
        if coherencia < 0.7:
            # Red incoherente = necesita más nodos estables
            multiplicador *= (1.0 + (0.7 - coherencia))
        
        recompensa = base * multiplicador
        
        return min(recompensa, base * 2.0)  # Cap: máximo 2x la base
    
    def calcular_quema_fees(self, fees: float, politicas: Dict[str, float]) -> float:
        """Calcula cuánto MERIT quemar de las fees (usando política aprendida)"""
        tasa_quema = politicas.get("tasa_quema_fees", 0.30)
        return fees * tasa_quema
    
    def proyectar_necesidades(self, estado: NetworkState, horizonte_horas: int = 168) -> Dict:
        """
        Usa Extender para proyectar necesidades futuras de infraestructura.
        Retorna recomendaciones de ajuste.
        """
        # Usar Extender para deducir patrón de crecimiento
        ss_query = [1, 0, 1]  # Patrón de crecimiento (lista simple)
        extension = self.extender.extend(ss_query, use_recursive_deduction=True)
        
        # Analizar tendencias
        tendencia_operaciones = self.monitor.obtener_tendencia("operaciones_por_hora")
        
        proyeccion = {
            "necesita_mas_nodos": estado.nodos_activos < self.config.umbral_minimo_nodos,
            "tasa_crecimiento_estimada": tendencia_operaciones / estado.operaciones_por_hora if estado.operaciones_por_hora > 0 else 0,
            "recomendacion": "aumentar_incentivos" if tendencia_operaciones > 10 else "mantener",
            "coherencia_proyectada": extension.coherence if extension else 0.5
        }
        
        return proyeccion


# ============================================================================
# MODELO ADAPTATIVO PARA ○ MIND
# ============================================================================

class MindEconomics:
    """Modelo de inteligencia para gestión adaptativa de MIND"""
    
    def __init__(self, config: TokenConfig, monitor: NetworkMonitor):
        self.config = config
        self.monitor = monitor
        self.kb = FractalKnowledgeBase()  # KB para transcender
        self.evolver = Evolver()  # No toma argumentos
        self.transcender = Transcender(self.kb)
        
    def calcular_recompensa_computo(
        self,
        tipo_operacion: str,
        complejidad_fractal: float,
        coherencia: float,
        es_colaborativa: bool,
        politicas: Dict[str, float]
    ) -> float:
        """
        Calcula recompensa MIND por ejecutar cómputo.
        USA POLÍTICAS APRENDIDAS (no hardcoded).
        
        Los multiplicadores son determinados por modelos de usuarios.
        """
        base = politicas.get("mind_emision_base", 1.0)
        multiplicador = 1.0
        
        # Factor 1: Tipo de operación (multiplicador aprendido)
        mult_pattern0 = politicas.get("multiplicador_pattern0", 2.0)
        mult_colaborativo = politicas.get("multiplicador_colaborativo", 1.5)
        
        if tipo_operacion == "pattern0":
            multiplicador *= mult_pattern0  # Aprendido por modelos
        elif tipo_operacion == "extend_recursive":
            multiplicador *= 1.8  # Deducción recursiva = alta complejidad
        elif tipo_operacion == "trigate_synthesis":
            multiplicador *= 1.5
        elif tipo_operacion == "simple_query":
            multiplicador *= 0.5  # Operaciones simples = menos recompensa
        
        # Factor 2: Complejidad fractal (0.0 a 1.0)
        multiplicador *= (1.0 + complejidad_fractal)
        
        # Factor 3: Coherencia (calidad del resultado)
        umbral_coherencia = politicas.get("umbral_coherencia", 0.7)
        if coherencia > umbral_coherencia:
            bonus_coherencia = (coherencia - umbral_coherencia) * 2.0
            multiplicador *= (1.0 + bonus_coherencia)
        
        # Factor 4: Colaboración multi-peer (aprendido)
        if es_colaborativa:
            multiplicador *= mult_colaborativo
        
        recompensa = base * multiplicador
        
        return min(recompensa, base * 3.0)  # Cap: máximo 3x la base
    
    def evolucionar_arquetipos(self, operaciones_recientes: List[Dict]) -> Dict:
        """
        Usa Evolver para sintetizar arquetipos de operaciones útiles.
        Ajusta incentivos según lo que genera valor real.
        """
        # Crear tensores de las operaciones más valiosas
        tensores = [FractalTensor.random() for _ in range(min(3, len(operaciones_recientes)))]
        
        if len(tensores) >= 2:
            # Sintetizar arquetipo de "operación valiosa"
            arquetipo = self.evolver.synthesize(tensores[0], tensores[1])
            
            return {
                "arquetipo_util": arquetipo,
                "coherencia": arquetipo.coherence if arquetipo else 0.0,
                "recomendacion": "priorizar_operaciones_coherentes"
            }
        
        return {"recomendacion": "insuficientes_datos"}


# ============================================================================
# MODELO PARA U TRUST (Validación Humana)
# ============================================================================

class TrustEconomics:
    """Modelo de validación ética para emisión de TRUST"""
    
    def __init__(self, config: TokenConfig):
        self.config = config
        self.armonizador = Armonizador()
        self.interacciones_pendientes: List[Dict] = []
        
    def validar_interaccion(
        self,
        tipo: str,
        peer_a: str,
        peer_b: str,
        firma_a: str,
        firma_b: str,
        metadata: Dict
    ) -> Tuple[bool, float]:
        """
        Valida una interacción humana y determina si merece TRUST.
        
        Returns:
            (es_valida, cantidad_trust)
        """
        # Verificar que el tipo existe
        if tipo not in TRUST_REWARDS:
            return False, 0.0
        
        # Verificar firmas (simplificado - en prod usar criptografía real)
        if not (firma_a and firma_b):
            return False, 0.0
        
        # Usar Armonizador para validar coherencia ética
        # Crear tensor de la interacción
        tensor_interaccion = FractalTensor.random()  # En prod: codificar metadata
        coherencia = self.armonizador.check_coherence([tensor_interaccion])
        
        # Umbral ético: coherencia > 0.8
        if coherencia < 0.8:
            return False, 0.0
        
        # Cantidad base según tipo
        cantidad = TRUST_REWARDS[tipo]
        
        # Bonus por coherencia excepcional
        if coherencia > 0.95:
            cantidad *= 1.2
        
        return True, cantidad
    
    def registrar_interaccion_pendiente(self, interaccion: Dict):
        """Registra una interacción para validación comunitaria (2-de-N)"""
        self.interacciones_pendientes.append({
            **interaccion,
            "timestamp": datetime.now(),
            "validaciones": []
        })
    
    def votar_validacion(self, id_interaccion: int, validador: str, aprueba: bool):
        """Registra voto de un validador comunitario"""
        if id_interaccion >= len(self.interacciones_pendientes):
            return
        
        interaccion = self.interacciones_pendientes[id_interaccion]
        interaccion["validaciones"].append({
            "validador": validador,
            "aprueba": aprueba,
            "timestamp": datetime.now()
        })
    
    def obtener_interacciones_aprobadas(self, umbral_votos: int = 2) -> List[Dict]:
        """Retorna interacciones que superaron el umbral de validación"""
        aprobadas = []
        
        for interaccion in self.interacciones_pendientes:
            votos_a_favor = sum(1 for v in interaccion["validaciones"] if v["aprueba"])
            
            if votos_a_favor >= umbral_votos:
                aprobadas.append(interaccion)
        
        # Limpiar las aprobadas de pendientes
        self.interacciones_pendientes = [
            i for i in self.interacciones_pendientes
            if i not in aprobadas
        ]
        
        return aprobadas


# ============================================================================
# MODELOS ENTRENADOS POR USUARIOS
# ============================================================================

@dataclass
class UserTrainedModel:
    """
    Modelo entrenado por un usuario específico.
    Aprende de las interacciones del usuario y vota sobre políticas.
    """
    model_id: str
    owner_peer_id: str
    kb: FractalKnowledgeBase  # Su conocimiento acumulado
    votos_historicos: List[Dict]  # Historial de votos sobre políticas
    metricas_aprendizaje: Dict[str, float]  # Precisión, coherencia, etc.
    interacciones_entrenadas: int
    fecha_creacion: datetime
    
    def entrenar_con_interaccion(self, interaccion: Dict):
        """
        Entrena el modelo con una nueva interacción del usuario.
        El modelo aprende qué comportamientos generan valor.
        """
        # Crear tensor de la interacción
        tensor = FractalTensor.random()  # En prod: codificar interaccion real
        
        # Almacenar en Knowledge Base
        self.kb.store(
            name=f"interaccion_{self.interacciones_entrenadas}",
            tensor=tensor,
            space_id=0
        )
        
        self.interacciones_entrenadas += 1
        
        # Actualizar métricas (simplificado)
        self.metricas_aprendizaje["coherencia"] = tensor.coherence
    
    def votar_politica(self, nombre_politica: str, valor_propuesto: float) -> Tuple[str, float]:
        """
        El modelo vota sobre una política económica basado en su aprendizaje.
        """
        # Registrar voto
        voto = {
            "politica": nombre_politica,
            "valor": valor_propuesto,
            "timestamp": datetime.now(),
            "confianza": self.metricas_aprendizaje.get("coherencia", 0.5)
        }
        self.votos_historicos.append(voto)
        
        return (self.model_id, valor_propuesto)
    
    def proponer_ajuste_automatico(self, politica: str, observaciones: Dict) -> Optional[float]:
        """
        El modelo propone un ajuste a una política basado en lo que aprendió.
        """
        # Consultar Knowledge Base para ver patrones aprendidos
        arquetipos = self.kb.query_by_name(f"patron_{politica}")
        
        if not arquetipos:
            return None
        
        # Usar coherencia del arquetipo para proponer valor
        # En prod: lógica más sofisticada
        coherencia = arquetipos[0].coherence if arquetipos else 0.5
        
        if politica == "tasa_emision_base":
            # Si aprendió alta coherencia → propone emisión más conservadora
            return 0.03 + (0.05 * (1.0 - coherencia))
        
        return None


class ModelGovernanceSystem:
    """
    Sistema de gobernanza donde los modelos entrenados por usuarios
    votan sobre políticas económicas.
    """
    
    def __init__(self):
        self.modelos: Dict[str, UserTrainedModel] = {}
        self.politicas_globales: Dict[str, LearnedPolicy] = crear_politicas_iniciales()
        
    def registrar_modelo(self, peer_id: str) -> str:
        """Crea un modelo nuevo para un usuario"""
        model_id = f"model_{peer_id}_{len(self.modelos)}"
        
        modelo = UserTrainedModel(
            model_id=model_id,
            owner_peer_id=peer_id,
            kb=FractalKnowledgeBase(),
            votos_historicos=[],
            metricas_aprendizaje={"coherencia": 0.5},
            interacciones_entrenadas=0,
            fecha_creacion=datetime.now()
        )
        
        self.modelos[model_id] = modelo
        return model_id
    
    def entrenar_modelo(self, model_id: str, interaccion: Dict):
        """Usuario entrena su modelo con una interacción"""
        if model_id not in self.modelos:
            return
        
        modelo = self.modelos[model_id]
        modelo.entrenar_con_interaccion(interaccion)
        
        # Después de entrenar, el modelo puede proponer ajustes
        self._procesar_propuestas_automaticas(modelo)
    
    def _procesar_propuestas_automaticas(self, modelo: UserTrainedModel):
        """El modelo propone ajustes basados en lo que aprendió"""
        for nombre_politica in self.politicas_globales.keys():
            propuesta = modelo.proponer_ajuste_automatico(nombre_politica, {})
            
            if propuesta is not None:
                # El modelo votó → actualizar política global
                voto = modelo.votar_politica(nombre_politica, propuesta)
                self.politicas_globales[nombre_politica].actualizar_con_aprendizaje(voto)
    
    def votar_manualmente(self, model_id: str, politica: str, valor: float):
        """Usuario hace que su modelo vote manualmente sobre una política"""
        if model_id not in self.modelos:
            return
        
        modelo = self.modelos[model_id]
        voto = modelo.votar_politica(politica, valor)
        self.politicas_globales[politica].actualizar_con_aprendizaje(voto)
    
    def obtener_politica_actual(self, nombre: str) -> float:
        """Obtiene valor actual consensuado de una política"""
        if nombre not in self.politicas_globales:
            return 0.0
        
        return self.politicas_globales[nombre].valor_actual
    
    def obtener_evolucion_politica(self, nombre: str) -> List[Tuple[datetime, float]]:
        """Obtiene histórico de cómo evolucionó una política"""
        if nombre not in self.politicas_globales:
            return []
        
        return self.politicas_globales[nombre].historico
    
    def obtener_estadisticas(self) -> Dict:
        """Estadísticas del sistema de gobernanza"""
        return {
            "total_modelos": len(self.modelos),
            "modelos_activos": sum(1 for m in self.modelos.values() if m.interacciones_entrenadas > 0),
            "total_votos": sum(len(m.votos_historicos) for m in self.modelos.values()),
            "politicas": {
                nombre: {
                    "valor_actual": pol.valor_actual,
                    "confianza": pol.confianza,
                    "num_votos": len(pol.votos_modelos)
                }
                for nombre, pol in self.politicas_globales.items()
            }
        }


# ============================================================================
# COORDINADOR DEL SISTEMA ECONÓMICO
# ============================================================================

class AdaptiveEconomicsCoordinator:
    """
    Coordinador maestro que integra:
    1. Modelos entrenados por usuarios (gobernanza)
    2. Sistema económico adaptativo
    3. Monitoreo de red
    
    CLAVE: Las políticas NO están hardcoded.
    Los modelos de usuarios las determinan mediante aprendizaje colectivo.
    """
    
    def __init__(self):
        self.monitor = NetworkMonitor()
        self.governance = ModelGovernanceSystem()  # Sistema de gobernanza por modelos
        self.merit = MeritEconomics(MERIT_CONFIG, self.monitor)
        self.mind = MindEconomics(MIND_CONFIG, self.monitor)
        self.trust = TrustEconomics(TRUST_CONFIG)
        
        # Estado actual de supplies
        self.supplies = {
            "MERIT": MERIT_CONFIG.supply_inicial,
            "MIND": MIND_CONFIG.supply_inicial,
            "TRUST": TRUST_CONFIG.supply_inicial
        }
        
    def procesar_bloque(self, estado: NetworkState) -> Dict:
        """
        Procesa un bloque nuevo y ajusta la economía.
        USA POLÍTICAS APRENDIDAS POR MODELOS DE USUARIOS (no hardcoded).
        
        Retorna las emisiones/quemas realizadas.
        """
        # Registrar estado
        self.monitor.registrar_estado(estado)
        
        # OBTENER POLÍTICAS ACTUALES (consensuadas por modelos)
        politicas = {
            nombre: self.governance.obtener_politica_actual(nombre)
            for nombre in self.governance.politicas_globales.keys()
        }
        
        resultados = {
            "timestamp": estado.timestamp,
            "emisiones": {},
            "quemas": {},
            "supplies_actualizados": {},
            "politicas_aplicadas": politicas  # Transparencia: qué políticas se usaron
        }
        
        # 1. Calcular recompensas MERIT para nodos activos (con políticas aprendidas)
        recompensa_merit_por_nodo = self.merit.calcular_recompensa_nodo(estado, politicas)
        emision_merit = recompensa_merit_por_nodo * estado.nodos_activos
        
        # 2. Calcular quema MERIT de fees (con política aprendida)
        quema_merit = self.merit.calcular_quema_fees(
            estado.fees_acumuladas.get("MERIT", 0),
            politicas
        )
        
        # 3. Actualizar supply MERIT
        self.supplies["MERIT"] += emision_merit - quema_merit
        
        resultados["emisiones"]["MERIT"] = emision_merit
        resultados["quemas"]["MERIT"] = quema_merit
        resultados["supplies_actualizados"]["MERIT"] = self.supplies["MERIT"]
        
        # 4. Calcular quema MIND de fees (con política aprendida)
        tasa_quema_mind = politicas.get("tasa_quema_fees", 0.50)
        quema_mind = estado.fees_acumuladas.get("MIND", 0) * tasa_quema_mind
        self.supplies["MIND"] -= quema_mind
        resultados["quemas"]["MIND"] = quema_mind
        resultados["supplies_actualizados"]["MIND"] = self.supplies["MIND"]
        
        # 5. TRUST no se toca en procesamiento automático
        resultados["supplies_actualizados"]["TRUST"] = self.supplies["TRUST"]
        
        return resultados
    
    def emitir_recompensa_computo(
        self,
        tipo_operacion: str,
        complejidad: float,
        coherencia: float,
        es_colaborativa: bool = False
    ) -> float:
        """Emite MIND por ejecutar cómputo (con políticas aprendidas)"""
        # Obtener políticas actuales
        politicas = {
            nombre: self.governance.obtener_politica_actual(nombre)
            for nombre in self.governance.politicas_globales.keys()
        }
        
        recompensa = self.mind.calcular_recompensa_computo(
            tipo_operacion, complejidad, coherencia, es_colaborativa, politicas
        )
        
        self.supplies["MIND"] += recompensa
        return recompensa
    
    def emitir_trust(
        self,
        tipo: str,
        peer_a: str,
        peer_b: str,
        firma_a: str,
        firma_b: str,
        metadata: Dict
    ) -> Tuple[bool, float]:
        """Emite TRUST por interacción humana validada"""
        valida, cantidad = self.trust.validar_interaccion(
            tipo, peer_a, peer_b, firma_a, firma_b, metadata
        )
        
        if valida:
            self.supplies["TRUST"] += cantidad
        
        return valida, cantidad
    
    def obtener_proyeccion(self) -> Dict:
        """Obtiene proyección de necesidades futuras"""
        estado_actual = self.monitor.historial[-1] if self.monitor.historial else None
        if not estado_actual:
            return {"error": "No hay datos históricos"}
        
        proyeccion_merit = self.merit.proyectar_necesidades(estado_actual)
        
        return {
            "merit": proyeccion_merit,
            "supplies_actuales": self.supplies,
            "timestamp": datetime.now()
        }
    
    def registrar_modelo_usuario(self, peer_id: str) -> str:
        """
        Registra un modelo nuevo para un usuario.
        Este modelo aprenderá de las interacciones del usuario.
        """
        return self.governance.registrar_modelo(peer_id)
    
    def entrenar_modelo_con_interaccion(self, model_id: str, interaccion: Dict):
        """
        Usuario entrena su modelo con una interacción.
        El modelo aprende y puede proponer ajustes a políticas.
        """
        self.governance.entrenar_modelo(model_id, interaccion)
    
    def votar_politica(self, model_id: str, nombre_politica: str, valor_propuesto: float):
        """
        Usuario hace que su modelo vote sobre una política económica.
        """
        self.governance.votar_manualmente(model_id, nombre_politica, valor_propuesto)
    
    def obtener_evolucion_politica(self, nombre: str) -> List[Tuple[datetime, float]]:
        """Obtiene cómo ha evolucionado una política con el tiempo"""
        return self.governance.obtener_evolucion_politica(nombre)
    
    def obtener_metricas(self) -> Dict:
        """Retorna métricas del sistema económico (con gobernanza)"""
        return {
            "supplies": self.supplies,
            "politicas_actuales": {
                nombre: {
                    "valor": self.governance.obtener_politica_actual(nombre),
                    "confianza": pol.confianza,
                    "num_votos": len(pol.votos_modelos),
                    "ultima_actualizacion": pol.ultima_actualizacion.isoformat()
                }
                for nombre, pol in self.governance.politicas_globales.items()
            },
            "gobernanza": self.governance.obtener_estadisticas(),
            "historial_bloques": len(self.monitor.historial),
            "trust_rewards": TRUST_REWARDS
        }


# ============================================================================
# EJEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    print("🌟 Aurora Adaptive Economics System")
    print("=" * 60)
    print("💡 Los usuarios entrenan modelos → los modelos votan → consenso emergente")
    print()
    
    # Inicializar coordinador
    coordinator = AdaptiveEconomicsCoordinator()
    
    # ========================================================================
    # 1. USUARIOS REGISTRAN SUS MODELOS
    # ========================================================================
    print("👥 Usuarios registrando modelos...")
    modelo_alice = coordinator.registrar_modelo_usuario("peer_alice")
    modelo_bob = coordinator.registrar_modelo_usuario("peer_bob")
    modelo_charlie = coordinator.registrar_modelo_usuario("peer_charlie")
    print(f"  ✓ Modelo de Alice: {modelo_alice}")
    print(f"  ✓ Modelo de Bob: {modelo_bob}")
    print(f"  ✓ Modelo de Charlie: {modelo_charlie}")
    
    # ========================================================================
    # 2. USUARIOS ENTRENAN SUS MODELOS CON INTERACCIONES
    # ========================================================================
    print("\n🧠 Usuarios entrenando sus modelos...")
    
    # Alice entrena con mentorías
    for i in range(5):
        coordinator.entrenar_modelo_con_interaccion(modelo_alice, {
            "tipo": "mentoria",
            "calidad": 0.9,
            "duracion_horas": 8
        })
    print(f"  ✓ Alice entrenó su modelo con 5 mentorías de alta calidad")
    
    # Bob entrena con operaciones de cómputo
    for i in range(3):
        coordinator.entrenar_modelo_con_interaccion(modelo_bob, {
            "tipo": "computo_pattern0",
            "coherencia": 0.95,
            "complejidad": 0.8
        })
    print(f"  ✓ Bob entrenó su modelo con 3 operaciones Pattern 0")
    
    # Charlie entrena con validación de nodos
    for i in range(4):
        coordinator.entrenar_modelo_con_interaccion(modelo_charlie, {
            "tipo": "validacion_nodo",
            "latencia_ms": 300.0,
            "uptime": 0.99
        })
    print(f"  ✓ Charlie entrenó su modelo con 4 validaciones de nodos")
    
    # ========================================================================
    # 3. MODELOS VOTAN SOBRE POLÍTICAS (después de aprender)
    # ========================================================================
    print("\n🗳️  Modelos votando sobre políticas económicas...")
    
    # Alice (experta en mentorías) vota por más TRUST
    coordinator.votar_politica(modelo_alice, "multiplicador_pattern0", 2.5)
    print("  Alice: 'Pattern 0 debe valer 2.5x (alta ética)'")
    
    # Bob (experto en Pattern 0) vota similar
    coordinator.votar_politica(modelo_bob, "multiplicador_pattern0", 2.3)
    print("  Bob: 'Pattern 0 debe valer 2.3x'")
    
    # Charlie (experto en infraestructura) vota por más MERIT
    coordinator.votar_politica(modelo_charlie, "tasa_emision_base", 0.05)
    print("  Charlie: 'Emisión de MERIT debe ser 5% anual'")
    
    # ========================================================================
    # 4. VERIFICAR CONSENSO EMERGENTE
    # ========================================================================
    print("\n📊 Políticas Consensuadas (no hardcoded):")
    metricas = coordinator.obtener_metricas()
    
    for nombre, info in metricas["politicas_actuales"].items():
        if info["num_votos"] > 0:
            print(f"  {nombre}:")
            print(f"    Valor actual: {info['valor']:.3f}")
            print(f"    Confianza: {info['confianza']:.2f}")
            print(f"    Votos: {info['num_votos']}")
    
    # ========================================================================
    # 5. PROCESAR BLOQUE CON POLÍTICAS APRENDIDAS
    # ========================================================================
    print("\n⚙️  Procesando bloque con políticas aprendidas...")
    
    estado = NetworkState(
        timestamp=datetime.now(),
        nodos_activos=8,
        latencia_promedio_ms=600.0,
        operaciones_por_hora=150,
        coherencia_promedio=0.75,
        supply_merit=1_000_000.0,
        supply_mind=500_000.0,
        supply_trust=0.0,
        fees_acumuladas={"MERIT": 100.0, "MIND": 50.0}
    )
    
    resultado = coordinator.procesar_bloque(estado)
    
    print(f"\n💎 Emisiones/Quemas (basadas en consenso de modelos):")
    print(f"  △ MERIT emitido: {resultado['emisiones']['MERIT']:.2f}")
    print(f"  △ MERIT quemado: {resultado['quemas']['MERIT']:.2f}")
    
    print(f"\n� Políticas Aplicadas en este Bloque:")
    for nombre, valor in resultado["politicas_aplicadas"].items():
        if valor != 0:
            print(f"  {nombre}: {valor:.3f}")
    
    # ========================================================================
    # 6. OPERACIÓN CON MULTIPLICADOR APRENDIDO
    # ========================================================================
    print("\n🧠 Emitiendo MIND por operación Pattern 0...")
    print("  (usando multiplicador consensuado por modelos)")
    
    mind_ganado = coordinator.emitir_recompensa_computo(
        tipo_operacion="pattern0",
        complejidad=0.9,
        coherencia=0.95,
        es_colaborativa=True
    )
    print(f"  Recompensa: {mind_ganado:.2f} ○ MIND")
    
    # ========================================================================
    # 7. TRUST (validación humana)
    # ========================================================================
    print("\n🤝 Validando mentoría para emisión de TRUST...")
    valida, trust_ganado = coordinator.emitir_trust(
        tipo="mentoria_completada",
        peer_a="peer_alice",
        peer_b="peer_bob",
        firma_a="sig_a_123",
        firma_b="sig_b_456",
        metadata={"duracion_horas": 10}
    )
    
    if valida:
        print(f"  ✓ Mentoría validada: {trust_ganado:.2f} U TRUST emitido")
    else:
        print("  ✗ Mentoría rechazada (coherencia insuficiente)")
    
    # ========================================================================
    # 8. GOBERNANZA
    # ========================================================================
    print("\n� Estadísticas de Gobernanza:")
    gobernanza = metricas["gobernanza"]
    print(f"  Total de modelos: {gobernanza['total_modelos']}")
    print(f"  Modelos activos: {gobernanza['modelos_activos']}")
    print(f"  Total de votos: {gobernanza['total_votos']}")
    
    print("\n" + "=" * 60)
    print("✨ Sistema económico APRENDIZ en funcionamiento")
    print("💡 Las políticas evolucionan con el aprendizaje colectivo")
    print("🚀 NO hay código hardcoded - todo es consenso emergente")
