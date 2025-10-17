"""
Extender - Módulo de Comunicación Fractal
Proyecto Genesis - Aurora Intelligence Engine

Proceso INVERSO al Transcender:
- Transcender: Texto → Tensor abstracto (síntesis emergente)
- Extender: Tensor abstracto → Texto concreto (despliegue fractal)

Capítulo 10 del Manual Aurora:
"El Extender navega desde idea → frases → palabras → morfemas,
guiado por las 'migas de pan' del contexto original"

Usa rotación Fibonacci para explorar múltiples perspectivas de despliegue.
"""

from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field
import numpy as np

from tensor_ffe import TensorFFE, VectorFFE, TransformadorFFE
from evolver import Evolver, Arquetipo


@dataclass
class MigaDePan:
    """
    'Breadcrumb' contextual para guiar el despliegue
    Preserva información del camino de abstracción original
    """
    nivel: int  # 0-7 del continuum (Fonético → Teórico)
    tensor_contexto: Optional[TensorFFE] = None
    arquetipos_vecinos: List[str] = field(default_factory=list)
    palabras_originales: List[str] = field(default_factory=list)


@dataclass
class ResultadoDespliegue:
    """
    Resultado de desplegar un tensor abstracto a texto concreto
    """
    texto_generado: str
    nivel_coherencia: float  # [0.0, 1.0]
    migas_usadas: List[MigaDePan]
    tensores_intermedios: List[TensorFFE]
    nivel_final: int  # Nivel del continuum alcanzado


class Extender:
    """
    Motor de despliegue fractal: Tensor abstracto → Texto concreto
    
    Navega jerárquicamente:
    1. Idea (Teórico, nivel 7)
    2. → Conceptos (Semántico, nivel 5)
    3. → Frases (Sintáctico, nivel 4)
    4. → Palabras (Léxico, nivel 3)
    5. → Morfemas (Morfémico, nivel 2)
    6. → Fonemas (Fonético, nivel 0)
    
    Usa rotación Fibonacci para explorar múltiples ángulos de expresión.
    """
    
    def __init__(self, evolver: Evolver, transformador: Optional[TransformadorFFE] = None):
        """
        Inicializa Extender
        
        Args:
            evolver: Evolver con arquetipos y relatores aprendidos
            transformador: Transformador FFE para niveles del continuum
        """
        self.evolver = evolver
        self.transformador = transformador or TransformadorFFE()
        
        # Secuencia Fibonacci para rotaciones
        self.fibonacci = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]
        self.paso_despliegue = 0
        
        # Vocabulario inverso: arquetipo → palabras
        self.vocabulario_inverso: Dict[str, List[str]] = {}
    
    def registrar_vocabulario(self, vocabulario: Dict[str, Arquetipo]):
        """
        Construye índice inverso: arquetipo → palabras
        Necesario para generar texto desde arquetipos
        """
        self.vocabulario_inverso = {}
        
        for palabra, arq in vocabulario.items():
            if arq.id not in self.vocabulario_inverso:
                self.vocabulario_inverso[arq.id] = []
            self.vocabulario_inverso[arq.id].append(palabra)
        
        print(f"  ✅ Vocabulario inverso: {len(self.vocabulario_inverso)} arquetipos")
    
    def desplegar(
        self, 
        tensor_abstracto: TensorFFE,
        migas_de_pan: Optional[List[MigaDePan]] = None,
        nivel_objetivo: int = 3  # Léxico por defecto
    ) -> ResultadoDespliegue:
        """
        Despliega tensor abstracto a texto concreto
        
        Args:
            tensor_abstracto: Tensor emergente de Transcender (nivel alto)
            migas_de_pan: Contexto del camino de abstracción original
            nivel_objetivo: Nivel del continuum a alcanzar (3=Léxico, 0=Fonético)
        
        Returns:
            ResultadoDespliegue con texto generado y métricas
        """
        if migas_de_pan is None:
            migas_de_pan = []
        
        # 1. Identificar arquetipo del tensor abstracto
        arq = self.evolver.archetype_learner.detectar_o_crear(tensor_abstracto)
        
        # 2. Explorar rotaciones Fibonacci para encontrar mejor expresión
        mejor_expresion = None
        mejor_coherencia = 0.0
        tensores_explorados = []
        
        for i in range(3):  # Probar 3 rotaciones
            idx_fib = (self.paso_despliegue + i) % len(self.fibonacci)
            paso = self.fibonacci[idx_fib] % 8
            
            # Rotar tensor para explorar diferentes perspectivas
            tensor_rot = self._rotar_tensor(tensor_abstracto, paso)
            tensores_explorados.append(tensor_rot)
            
            # Buscar arquetipo de esta rotación
            arq_rot = self.evolver.archetype_learner.detectar_o_crear(tensor_rot)
            
            # Generar expresión desde este arquetipo
            if arq_rot.id in self.vocabulario_inverso:
                palabras_candidatas = self.vocabulario_inverso[arq_rot.id]
                
                # Evaluar coherencia con migas de pan
                coherencia = self._evaluar_coherencia(
                    palabras_candidatas, 
                    migas_de_pan, 
                    tensor_rot
                )
                
                if coherencia > mejor_coherencia:
                    mejor_coherencia = coherencia
                    mejor_expresion = palabras_candidatas[0]  # Primera palabra del arquetipo
        
        # 3. Si no hay expresión directa, navegar por relatores
        if mejor_expresion is None:
            mejor_expresion = self._navegar_relatores(arq, migas_de_pan)
            mejor_coherencia = 0.5  # Coherencia media (inferida)
        
        # 4. Expandir a frase si nivel objetivo < 3
        if nivel_objetivo < 3:
            mejor_expresion = self._expandir_a_frase(
                mejor_expresion, 
                arq, 
                migas_de_pan
            )
        
        # Avanzar paso Fibonacci
        self.paso_despliegue = (self.paso_despliegue + 1) % len(self.fibonacci)
        
        return ResultadoDespliegue(
            texto_generado=mejor_expresion,
            nivel_coherencia=mejor_coherencia,
            migas_usadas=migas_de_pan,
            tensores_intermedios=tensores_explorados,
            nivel_final=nivel_objetivo
        )
    
    def desplegar_jerarquico(
        self,
        emergencia_Ms: TensorFFE,  # Structure (lógica emergente)
        emergencia_Ss: TensorFFE,  # Form (huella factual)
        emergencia_MetaM: TensorFFE,  # Function (ruta completa)
        migas_de_pan: Optional[List[MigaDePan]] = None
    ) -> ResultadoDespliegue:
        """
        Despliegue jerárquico usando los 3 tensores de Emergencia
        Ms, Ss, MetaM representan diferentes niveles de la jerarquía
        
        Proceso:
        1. MetaM (nivel 1) → Idea general
        2. Ms (nivel 2) → Estructura lógica
        3. Ss (nivel 3) → Detalles concretos
        """
        if migas_de_pan is None:
            migas_de_pan = []
        
        # Nivel 1: Idea desde MetaM
        resultado_idea = self.desplegar(emergencia_MetaM, migas_de_pan, nivel_objetivo=5)
        
        # Nivel 2: Estructura desde Ms
        migas_estructura = migas_de_pan + [MigaDePan(
            nivel=5,
            tensor_contexto=emergencia_MetaM,
            palabras_originales=[resultado_idea.texto_generado]
        )]
        resultado_estructura = self.desplegar(emergencia_Ms, migas_estructura, nivel_objetivo=4)
        
        # Nivel 3: Detalles desde Ss
        migas_detalles = migas_estructura + [MigaDePan(
            nivel=4,
            tensor_contexto=emergencia_Ms,
            palabras_originales=[resultado_estructura.texto_generado]
        )]
        resultado_detalles = self.desplegar(emergencia_Ss, migas_detalles, nivel_objetivo=3)
        
        # Combinar los 3 niveles
        texto_final = f"{resultado_idea.texto_generado} {resultado_estructura.texto_generado} {resultado_detalles.texto_generado}"
        
        coherencia_promedio = (
            resultado_idea.nivel_coherencia +
            resultado_estructura.nivel_coherencia +
            resultado_detalles.nivel_coherencia
        ) / 3
        
        return ResultadoDespliegue(
            texto_generado=texto_final.strip(),
            nivel_coherencia=coherencia_promedio,
            migas_usadas=migas_detalles,
            tensores_intermedios=(
                resultado_idea.tensores_intermedios +
                resultado_estructura.tensores_intermedios +
                resultado_detalles.tensores_intermedios
            ),
            nivel_final=3
        )
    
    def _rotar_tensor(self, tensor: TensorFFE, paso: int) -> TensorFFE:
        """Rota tensor con paso Fibonacci"""
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
    
    def _evaluar_coherencia(
        self, 
        palabras: List[str], 
        migas: List[MigaDePan],
        tensor: TensorFFE
    ) -> float:
        """
        Evalúa qué tan coherente es una expresión con el contexto
        """
        if not migas:
            return 0.5  # Sin contexto, coherencia neutral
        
        coherencia = 0.0
        
        # 1. Coherencia por nivel del continuum
        nivel_tensor = tensor.nivel_abstraccion
        niveles_migas = [m.nivel for m in migas]
        
        if niveles_migas:
            distancia_nivel = abs(nivel_tensor - np.mean(niveles_migas))
            coherencia += 0.3 * (1.0 - distancia_nivel / 7.0)
        
        # 2. Coherencia semántica (palabras en migas)
        palabras_migas = []
        for miga in migas:
            palabras_migas.extend(miga.palabras_originales)
        
        if palabras_migas:
            # Si alguna palabra candidata aparece en migas → coherencia alta
            overlap = len(set(palabras) & set(palabras_migas))
            coherencia += 0.4 * (overlap / len(palabras))
        
        # 3. Coherencia estructural (similitud de tensores)
        tensores_migas = [m.tensor_contexto for m in migas if m.tensor_contexto]
        
        if tensores_migas:
            similitud = max(
                self._similitud_tensores(tensor, t_miga)
                for t_miga in tensores_migas
            )
            coherencia += 0.3 * similitud
        
        return min(coherencia, 1.0)
    
    def _similitud_tensores(self, t1: TensorFFE, t2: TensorFFE) -> float:
        """Similitud entre dos tensores [0.0, 1.0]"""
        dist = sum(v1.distancia(v2) for v1, v2 in zip(t1.nivel_1, t2.nivel_1))
        return 1.0 - (dist / (3 * 7 * 3))
    
    def _navegar_relatores(
        self, 
        arq: Arquetipo, 
        migas: List[MigaDePan]
    ) -> str:
        """
        Si no hay expresión directa, navega por relatores para encontrar
        un arquetipo cercano que tenga palabras
        """
        # Buscar arquetipos vecinos por relatores
        arquetipos_vecinos = self.evolver.relator_network.grafo.get(arq.id, set())
        
        for arq_vecino_id in arquetipos_vecinos:
            if arq_vecino_id in self.vocabulario_inverso:
                palabras = self.vocabulario_inverso[arq_vecino_id]
                return palabras[0]  # Primera palabra del vecino
        
        # Fallback: usar arquetipos de migas
        for miga in reversed(migas):
            if miga.arquetipos_vecinos:
                for arq_id in miga.arquetipos_vecinos:
                    if arq_id in self.vocabulario_inverso:
                        return self.vocabulario_inverso[arq_id][0]
        
        return "<desconocido>"  # No se pudo desplegar
    
    def _expandir_a_frase(
        self, 
        palabra_base: str, 
        arq: Arquetipo,
        migas: List[MigaDePan]
    ) -> str:
        """
        Expande una palabra a frase usando arquetipos relacionados
        """
        # Buscar arquetipos conectados por relatores fuertes
        relatores_fuertes = [
            rel for rel in self.evolver.relator_network.relatores.values()
            if rel.origen == arq.id and rel.fuerza > 0.5
        ]
        
        if not relatores_fuertes:
            return palabra_base  # Sin expansión posible
        
        # Tomar top 2 relatores más fuertes
        relatores_top = sorted(relatores_fuertes, key=lambda r: r.fuerza, reverse=True)[:2]
        
        palabras_adicionales = []
        for rel in relatores_top:
            if rel.destino in self.vocabulario_inverso:
                palabras_adicionales.append(self.vocabulario_inverso[rel.destino][0])
        
        # Construir frase simple
        if len(palabras_adicionales) == 0:
            return palabra_base
        elif len(palabras_adicionales) == 1:
            return f"{palabra_base} {palabras_adicionales[0]}"
        else:
            return f"{palabra_base} {palabras_adicionales[0]} {palabras_adicionales[1]}"


# ============================================================================
# UTILIDADES
# ============================================================================

def crear_migas_desde_frases(frases: List[str], tensores: List[TensorFFE]) -> List[MigaDePan]:
    """
    Crea migas de pan desde frases originales y sus tensores
    Útil para preservar contexto durante abstracción
    """
    migas = []
    
    for i, (frase, tensor) in enumerate(zip(frases, tensores)):
        miga = MigaDePan(
            nivel=tensor.nivel_abstraccion,
            tensor_contexto=tensor,
            palabras_originales=frase.split()[:5]  # Primeras 5 palabras
        )
        migas.append(miga)
    
    return migas
