"""
🐹 Aurora Reputation System - Intelligent Peer Evaluation

Sistema de reputación con Machine Learning que detecta patrones tóxicos
y da oportunidades de mejora, inspirado en la ética de Pepino.

Características:
- Detección de patrones (no eventos aislados)
- Sistema de segunda oportunidad
- Aprendizaje de consenso comunitario
- Transparencia en decisiones
- Integración con Pepino archetype

Author: Aurora Alliance
License: Apache-2.0
"""

import json
import time
import hashlib
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from collections import deque
import numpy as np


@dataclass
class Interaction:
    """Registro de una interacción entre peers"""
    timestamp: float
    peer_id: str
    interaction_type: str  # 'tensor_exchange', 'message', 'contract', etc.
    success: bool
    metadata: Dict
    reporter_id: Optional[str] = None  # Quien reporta (si es reporte negativo)
    

@dataclass
class ReputationScore:
    """Score de reputación de un peer"""
    peer_id: str
    score: float  # 0.0 (tóxico) a 1.0 (excelente)
    confidence: float  # Qué tan confiable es este score (basado en data)
    interaction_count: int
    positive_ratio: float
    warnings: int
    last_updated: float
    behavioral_patterns: Dict  # Patrones detectados por ML
    redemption_path: Optional[Dict] = None  # Cómo puede mejorar
    

class ReputationSystem:
    """
    Sistema de reputación inteligente con ML.
    
    Filosofía (inspirada en Pepino):
    - "Todo ser merece una segunda oportunidad"
    - "Los patrones revelan la verdad, no los eventos aislados"
    - "La exclusión es el último recurso, no el primero"
    - "La transparencia construye confianza"
    """
    
    # Thresholds configurables
    TOXIC_THRESHOLD = 0.3  # Score bajo el cual se considera problemático
    WARNING_THRESHOLD = 0.5  # Score que genera advertencia
    EXCELLENT_THRESHOLD = 0.8  # Score para peers confiables
    
    MIN_INTERACTIONS = 10  # Mínimo de interacciones para score confiable
    PATTERN_WINDOW = 20  # Ventana de interacciones para detección de patrones
    REDEMPTION_PERIOD = 7 * 24 * 3600  # 7 días para demostrar mejora
    
    def __init__(self, peer_id: str):
        self.peer_id = peer_id
        self.interactions_history: Dict[str, deque] = {}  # peer_id -> deque de Interactions
        self.reputation_cache: Dict[str, ReputationScore] = {}
        self.community_reports: Dict[str, List[Dict]] = {}  # peer_id -> reportes
        self.redemption_tracking: Dict[str, Dict] = {}  # peers en periodo de redención
        
    def record_interaction(
        self, 
        peer_id: str, 
        interaction_type: str, 
        success: bool,
        metadata: Optional[Dict] = None
    ):
        """
        Registra una interacción con otro peer.
        
        Args:
            peer_id: ID del peer con quien interactuamos
            interaction_type: Tipo de interacción
            success: Si fue exitosa
            metadata: Info adicional
        """
        if peer_id not in self.interactions_history:
            self.interactions_history[peer_id] = deque(maxlen=self.PATTERN_WINDOW)
        
        interaction = Interaction(
            timestamp=time.time(),
            peer_id=peer_id,
            interaction_type=interaction_type,
            success=success,
            metadata=metadata or {}
        )
        
        self.interactions_history[peer_id].append(interaction)
        
        # Invalidar cache de reputación
        if peer_id in self.reputation_cache:
            del self.reputation_cache[peer_id]
    
    def report_toxic_behavior(
        self,
        peer_id: str,
        reason: str,
        evidence: Optional[Dict] = None,
        severity: str = 'medium'  # 'low', 'medium', 'high'
    ):
        """
        Reporta comportamiento tóxico de un peer.
        
        Nota: El reporte no causa ban inmediato, sino que alimenta el ML
        para detectar patrones.
        """
        if peer_id not in self.community_reports:
            self.community_reports[peer_id] = []
        
        report = {
            'reporter': self.peer_id,
            'timestamp': time.time(),
            'reason': reason,
            'severity': severity,
            'evidence': evidence or {}
        }
        
        self.community_reports[peer_id].append(report)
        
        # Invalidar cache
        if peer_id in self.reputation_cache:
            del self.reputation_cache[peer_id]
    
    def calculate_reputation(self, peer_id: str) -> ReputationScore:
        """
        Calcula el score de reputación usando ML para detectar patrones.
        
        Returns:
            ReputationScore con score, confianza, y patrones detectados
        """
        # Check cache
        if peer_id in self.reputation_cache:
            cached = self.reputation_cache[peer_id]
            # Cache válido por 5 minutos
            if time.time() - cached.last_updated < 300:
                return cached
        
        # Obtener interacciones
        interactions = list(self.interactions_history.get(peer_id, []))
        reports = self.community_reports.get(peer_id, [])
        
        if len(interactions) < 3 and len(reports) == 0:
            # Nuevo peer - benefit of the doubt (Pepino's principle)
            return ReputationScore(
                peer_id=peer_id,
                score=0.7,  # Start neutral-positive
                confidence=0.1,  # Baja confianza
                interaction_count=0,
                positive_ratio=0.0,
                warnings=0,
                last_updated=time.time(),
                behavioral_patterns={'status': 'new_peer'}
            )
        
        # === ANÁLISIS DE PATRONES ===
        patterns = self._detect_behavioral_patterns(interactions, reports)
        
        # === CALCULAR SCORE BASE ===
        base_score = self._calculate_base_score(interactions)
        
        # === AJUSTES POR PATRONES ML ===
        ml_adjustment = self._apply_ml_adjustments(patterns)
        
        # === FACTOR DE REPORTES COMUNITARIOS ===
        community_factor = self._calculate_community_factor(reports)
        
        # === SCORE FINAL ===
        final_score = base_score * ml_adjustment * community_factor
        final_score = max(0.0, min(1.0, final_score))  # Clamp [0, 1]
        
        # === CONFIANZA (basado en cantidad de data) ===
        confidence = min(1.0, len(interactions) / self.MIN_INTERACTIONS)
        
        # === RATIO POSITIVO ===
        positive_count = sum(1 for i in interactions if i.success)
        positive_ratio = positive_count / len(interactions) if interactions else 0.0
        
        # === ADVERTENCIAS ===
        warnings = self._count_warnings(patterns)
        
        # === PATH DE REDENCIÓN (si aplica) ===
        redemption_path = None
        if final_score < self.WARNING_THRESHOLD:
            redemption_path = self._generate_redemption_path(peer_id, patterns)
        
        reputation = ReputationScore(
            peer_id=peer_id,
            score=final_score,
            confidence=confidence,
            interaction_count=len(interactions),
            positive_ratio=positive_ratio,
            warnings=warnings,
            last_updated=time.time(),
            behavioral_patterns=patterns,
            redemption_path=redemption_path
        )
        
        # Cache
        self.reputation_cache[peer_id] = reputation
        
        return reputation
    
    def _detect_behavioral_patterns(
        self, 
        interactions: List[Interaction],
        reports: List[Dict]
    ) -> Dict:
        """
        Detecta patrones de comportamiento usando técnicas simples de ML.
        
        Patrones detectados:
        - Fallos consecutivos (posible sabotaje)
        - Horarios sospechosos (bot?)
        - Variabilidad en éxito (inconsistencia)
        - Reportes recurrentes de múltiples peers
        - Recovery patterns (mejora después de advertencia)
        """
        patterns = {}
        
        if len(interactions) < 3:
            patterns['status'] = 'insufficient_data'
            return patterns
        
        # 1. FALLOS CONSECUTIVOS
        consecutive_failures = 0
        max_consecutive = 0
        for i in interactions:
            if not i.success:
                consecutive_failures += 1
                max_consecutive = max(max_consecutive, consecutive_failures)
            else:
                consecutive_failures = 0
        
        patterns['max_consecutive_failures'] = max_consecutive
        if max_consecutive >= 5:
            patterns['alert_consecutive_failures'] = True
        
        # 2. PATRÓN TEMPORAL (detección de bots)
        timestamps = [i.timestamp for i in interactions]
        if len(timestamps) > 5:
            intervals = np.diff(timestamps)
            # Bot típicamente tiene intervalos muy regulares
            std_dev = np.std(intervals)
            mean_interval = np.mean(intervals)
            coefficient_of_variation = std_dev / mean_interval if mean_interval > 0 else 0
            
            patterns['temporal_regularity'] = coefficient_of_variation
            if coefficient_of_variation < 0.1:  # Muy regular
                patterns['alert_bot_like_behavior'] = True
        
        # 3. TENDENCIA DE MEJORA/EMPEORAMIENTO
        if len(interactions) >= 10:
            # Dividir en mitades y comparar
            mid = len(interactions) // 2
            first_half = interactions[:mid]
            second_half = interactions[mid:]
            
            first_success = sum(1 for i in first_half if i.success) / len(first_half)
            second_success = sum(1 for i in second_half if i.success) / len(second_half)
            
            patterns['trend'] = second_success - first_success
            if patterns['trend'] > 0.2:
                patterns['improving'] = True
            elif patterns['trend'] < -0.2:
                patterns['degrading'] = True
        
        # 4. ANÁLISIS DE REPORTES COMUNITARIOS
        if reports:
            patterns['community_reports_count'] = len(reports)
            
            # Contar reporteros únicos
            unique_reporters = len(set(r['reporter'] for r in reports))
            patterns['unique_reporters'] = unique_reporters
            
            # Si múltiples peers reportan, es más serio
            if unique_reporters >= 3:
                patterns['alert_multiple_reporters'] = True
            
            # Severidad predominante
            severities = [r['severity'] for r in reports]
            high_severity = sum(1 for s in severities if s == 'high')
            if high_severity >= 2:
                patterns['alert_high_severity_reports'] = True
        
        # 5. TIPO DE INTERACCIONES
        interaction_types = {}
        for i in interactions:
            itype = i.interaction_type
            if itype not in interaction_types:
                interaction_types[itype] = {'total': 0, 'success': 0}
            interaction_types[itype]['total'] += 1
            if i.success:
                interaction_types[itype]['success'] += 1
        
        patterns['interaction_type_breakdown'] = interaction_types
        
        return patterns
    
    def _calculate_base_score(self, interactions: List[Interaction]) -> float:
        """Calcula score base desde interacciones directas"""
        if not interactions:
            return 0.7  # Neutral
        
        positive = sum(1 for i in interactions if i.success)
        total = len(interactions)
        
        return positive / total
    
    def _apply_ml_adjustments(self, patterns: Dict) -> float:
        """Aplica ajustes basados en patrones ML detectados"""
        adjustment = 1.0
        
        # Penalizar fallos consecutivos
        if patterns.get('alert_consecutive_failures'):
            adjustment *= 0.7
        
        # Penalizar comportamiento tipo bot
        if patterns.get('alert_bot_like_behavior'):
            adjustment *= 0.8
        
        # Recompensar tendencia de mejora
        if patterns.get('improving'):
            adjustment *= 1.2
        
        # Penalizar degradación
        if patterns.get('degrading'):
            adjustment *= 0.8
        
        return adjustment
    
    def _calculate_community_factor(self, reports: List[Dict]) -> float:
        """Factor basado en reportes de la comunidad"""
        if not reports:
            return 1.0
        
        # Más reportes = menor factor
        factor = 1.0 - (len(reports) * 0.1)
        
        # Pero verificar si son de múltiples fuentes
        unique_reporters = len(set(r['reporter'] for r in reports))
        if unique_reporters >= 3:
            factor *= 0.7  # Penalizar más si múltiples peers reportan
        
        return max(0.3, factor)  # Nunca bajar de 0.3 por reportes solos
    
    def _count_warnings(self, patterns: Dict) -> int:
        """Cuenta warnings activos"""
        warnings = 0
        
        if patterns.get('alert_consecutive_failures'):
            warnings += 1
        if patterns.get('alert_bot_like_behavior'):
            warnings += 1
        if patterns.get('alert_multiple_reporters'):
            warnings += 1
        if patterns.get('alert_high_severity_reports'):
            warnings += 1
        
        return warnings
    
    def _generate_redemption_path(self, peer_id: str, patterns: Dict) -> Dict:
        """
        Genera un path de redención específico para el peer.
        
        Filosofía Pepino: "Toda criatura merece saber cómo puede mejorar"
        """
        path = {
            'created_at': time.time(),
            'expires_at': time.time() + self.REDEMPTION_PERIOD,
            'goals': [],
            'progress': 0.0,
            'explanation': ''
        }
        
        # Identificar problemas y generar goals
        if patterns.get('alert_consecutive_failures'):
            path['goals'].append({
                'type': 'reduce_failures',
                'target': 'Achieve 80% success rate in next 20 interactions',
                'metric': 'success_rate',
                'threshold': 0.8
            })
            path['explanation'] += 'Hemos detectado múltiples fallos consecutivos. '
        
        if patterns.get('alert_bot_like_behavior'):
            path['goals'].append({
                'type': 'vary_behavior',
                'target': 'Show more varied interaction patterns',
                'metric': 'temporal_regularity',
                'threshold': 0.2
            })
            path['explanation'] += 'Tu comportamiento parece muy automatizado. '
        
        if patterns.get('alert_multiple_reporters'):
            path['goals'].append({
                'type': 'community_trust',
                'target': 'Complete 30 successful interactions with no reports',
                'metric': 'clean_interactions',
                'threshold': 30
            })
            path['explanation'] += 'Múltiples peers han reportado problemas. '
        
        # Mensaje de esperanza
        path['explanation'] += '\n\n🐹 Pepino dice: "Todo ser merece una segunda oportunidad. '
        path['explanation'] += 'Completa estos objetivos para recuperar tu reputación en la comunidad Aurora."'
        
        # Track redemption
        self.redemption_tracking[peer_id] = {
            'started': time.time(),
            'path': path,
            'initial_score': self.reputation_cache.get(peer_id, ReputationScore(
                peer_id=peer_id, score=0.5, confidence=0.0, interaction_count=0,
                positive_ratio=0.0, warnings=0, last_updated=time.time(),
                behavioral_patterns={}
            )).score
        }
        
        return path
    
    def should_connect_to_peer(self, peer_id: str) -> Tuple[bool, str]:
        """
        Decide si debemos conectarnos a un peer basado en su reputación.
        
        Returns:
            (should_connect, reason)
        """
        reputation = self.calculate_reputation(peer_id)
        
        # Caso 1: Score alto - conectar sin problema
        if reputation.score >= self.EXCELLENT_THRESHOLD:
            return (True, f"Peer confiable (score: {reputation.score:.2f})")
        
        # Caso 2: Score medio - conectar con precaución
        if reputation.score >= self.WARNING_THRESHOLD:
            if reputation.confidence < 0.5:
                return (True, f"Nuevo peer, damos oportunidad (score: {reputation.score:.2f})")
            return (True, f"Score aceptable (score: {reputation.score:.2f})")
        
        # Caso 3: Score bajo pero en redención
        if peer_id in self.redemption_tracking:
            redemption = self.redemption_tracking[peer_id]
            if time.time() < redemption['path']['expires_at']:
                return (True, f"Peer en periodo de redención, damos oportunidad")
        
        # Caso 4: Score muy bajo con alta confianza - no conectar
        if reputation.score < self.TOXIC_THRESHOLD and reputation.confidence > 0.7:
            patterns_str = ', '.join([
                k for k in reputation.behavioral_patterns.keys() 
                if k.startswith('alert_')
            ])
            return (False, f"Score tóxico (score: {reputation.score:.2f}). Patrones: {patterns_str}")
        
        # Caso 5: Score bajo pero poca data - dar oportunidad
        if reputation.confidence < 0.5:
            return (True, f"Poca información, damos oportunidad (score: {reputation.score:.2f})")
        
        # Default: precaución pero sí conectar
        return (True, f"Conectar con precaución (score: {reputation.score:.2f})")
    
    def get_reputation_explanation(self, peer_id: str) -> str:
        """
        Genera explicación humana de la reputación.
        
        Transparencia es clave para confianza.
        """
        reputation = self.calculate_reputation(peer_id)
        
        explanation = f"""
🐹 Reputación de Peer {peer_id[:16]}...

Score: {reputation.score:.2f} / 1.00
Confianza: {reputation.confidence:.2f} (basada en {reputation.interaction_count} interacciones)
Ratio de éxito: {reputation.positive_ratio:.1%}
Advertencias activas: {reputation.warnings}

Patrones detectados:
"""
        
        patterns = reputation.behavioral_patterns
        
        if patterns.get('improving'):
            explanation += "✅ Tendencia de mejora detectada (+)\n"
        if patterns.get('degrading'):
            explanation += "⚠️ Tendencia de empeoramiento (-)\n"
        if patterns.get('alert_consecutive_failures'):
            explanation += f"❌ Fallos consecutivos: {patterns['max_consecutive_failures']}\n"
        if patterns.get('alert_bot_like_behavior'):
            explanation += "🤖 Comportamiento automatizado detectado\n"
        if patterns.get('alert_multiple_reporters'):
            explanation += f"⚠️ Reportado por {patterns['unique_reporters']} peers diferentes\n"
        
        if reputation.redemption_path:
            explanation += f"\n🔄 Path de redención activo:\n"
            explanation += reputation.redemption_path['explanation']
        
        if reputation.score >= self.EXCELLENT_THRESHOLD:
            explanation += "\n\n✨ Peer altamente confiable en la red Aurora"
        elif reputation.score >= self.WARNING_THRESHOLD:
            explanation += "\n\n👍 Peer con reputación aceptable"
        else:
            explanation += "\n\n⚠️ Interactuar con precaución"
        
        return explanation


# ============================================================================
# INTEGRACIÓN CON DISCOVERY SERVER
# ============================================================================

def enrich_peer_with_reputation(peer_data: Dict, reputation: ReputationScore) -> Dict:
    """
    Enriquece los datos de peer con información de reputación.
    Para incluir en respuestas del Discovery Server.
    """
    peer_data['reputation'] = {
        'score': reputation.score,
        'confidence': reputation.confidence,
        'warnings': reputation.warnings,
        'is_trusted': reputation.score >= ReputationSystem.EXCELLENT_THRESHOLD,
        'needs_caution': reputation.score < ReputationSystem.WARNING_THRESHOLD,
        'in_redemption': reputation.redemption_path is not None
    }
    return peer_data


# ============================================================================
# EJEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    print("🐹 Aurora Reputation System Demo")
    print("="*60)
    
    # Sistema para nuestro peer
    my_system = ReputationSystem(peer_id="peer-alice")
    
    # Simular interacciones con otro peer
    peer_bob = "peer-bob"
    
    print(f"\nSimulando interacciones con {peer_bob}...")
    
    # Interacciones normales
    for i in range(15):
        success = True if i % 4 != 0 else False  # 75% éxito
        my_system.record_interaction(peer_bob, 'tensor_exchange', success)
    
    reputation = my_system.calculate_reputation(peer_bob)
    print(f"\nScore: {reputation.score:.2f}")
    print(f"Confidence: {reputation.confidence:.2f}")
    print(f"Patterns: {reputation.behavioral_patterns}")
    
    should_connect, reason = my_system.should_connect_to_peer(peer_bob)
    print(f"\n¿Conectar? {should_connect}")
    print(f"Razón: {reason}")
    
    # Simular peer tóxico
    print("\n" + "="*60)
    print("Simulando peer con comportamiento tóxico...")
    
    peer_toxic = "peer-toxic"
    
    # Muchos fallos consecutivos
    for i in range(20):
        my_system.record_interaction(peer_toxic, 'tensor_exchange', False)
    
    # Múltiples reportes
    my_system.report_toxic_behavior(peer_toxic, "Envía tensors corruptos", severity='high')
    my_system.report_toxic_behavior(peer_toxic, "No responde a mensajes", severity='medium')
    
    reputation_toxic = my_system.calculate_reputation(peer_toxic)
    print(f"\nScore: {reputation_toxic.score:.2f}")
    print(f"Warnings: {reputation_toxic.warnings}")
    
    should_connect, reason = my_system.should_connect_to_peer(peer_toxic)
    print(f"\n¿Conectar? {should_connect}")
    print(f"Razón: {reason}")
    
    if reputation_toxic.redemption_path:
        print("\n📋 Path de Redención:")
        print(reputation_toxic.redemption_path['explanation'])
        print(f"\nGoals: {len(reputation_toxic.redemption_path['goals'])}")
    
    print("\n" + "="*60)
    print("🐹 Pepino's Wisdom:")
    print("   'Los patrones revelan la verdad.'")
    print("   'Toda criatura merece una segunda oportunidad.'")
    print("   'La exclusión es el último recurso, no el primero.'")
