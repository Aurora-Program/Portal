"""
🐹 Aurora P2P Network - Ejemplo Completo
Demuestra una red P2P con múltiples peers, discovery y reputación
"""

import time
import threading
from discovery_client import DiscoveryClient, DiscoveryConfig, PeerInfo
from reputation_system import ReputationSystem
import random
from datetime import datetime


class AuroraPeer:
    """
    Representa un peer completo en la red Aurora
    Combina Discovery Client + Reputation System + lógica de negocio
    """
    
    def __init__(self, peer_id: str, archetypes: list, endpoint: str):
        self.peer_id = peer_id
        self.archetypes = archetypes
        self.endpoint = endpoint
        
        # Sistema de reputación local
        self.reputation = ReputationSystem()
        
        # Cliente de Discovery
        self.config = DiscoveryConfig(
            endpoint=endpoint,
            peer_id=peer_id,
            archetypes=archetypes,
            heartbeat_interval=30,
            auto_heartbeat=True,
            enable_reputation=True
        )
        
        self.client = DiscoveryClient(self.config, reputation_system=self.reputation)
        
        # Estado del peer
        self.is_running = False
        self.connections = {}  # peer_id -> connection info
        self.work_done = 0
        
    def start(self, address: str = "127.0.0.1", port: int = None):
        """Inicia el peer en la red"""
        if port is None:
            port = random.randint(8000, 9000)
        
        print(f"\n🚀 Iniciando peer {self.peer_id}")
        print(f"   Archetypes: {', '.join(self.archetypes)}")
        print(f"   Address: {address}:{port}")
        
        try:
            # Registrar en Discovery Server
            result = self.client.register(
                address=address,
                port=port,
                metadata={
                    "version": "1.0.0",
                    "capabilities": ["training", "inference", "tensor_exchange"]
                }
            )
            
            self.is_running = True
            print(f"   ✅ Registrado (TTL: {result['ttl_expires']})")
            
            # Callbacks
            self.client.on_heartbeat_success = lambda: None  # Silencioso
            self.client.on_peer_discovered = self._on_peer_discovered
            
            return True
            
        except Exception as e:
            print(f"   ❌ Error al iniciar: {e}")
            return False
    
    def discover_and_connect(self, archetype: str = None):
        """Descubre peers y establece conexiones"""
        print(f"\n🔍 {self.peer_id} buscando peers...")
        
        try:
            peers = self.client.discover(archetype=archetype, include_reputation=True)
            print(f"   Encontrados: {len(peers)} peers")
            
            for peer in peers:
                self._try_connect(peer)
            
            return peers
            
        except Exception as e:
            print(f"   ❌ Error en discovery: {e}")
            return []
    
    def _try_connect(self, peer: PeerInfo):
        """Intenta conectar con un peer"""
        # Verificar reputación
        decision = self.reputation.should_connect_to_peer(peer.peer_id)
        
        if not decision['should_connect']:
            print(f"   🚫 {peer.peer_id} rechazado: {decision['reason']}")
            return False
        
        # Simular conexión
        self.connections[peer.peer_id] = {
            'peer': peer,
            'connected_at': datetime.now(),
            'interactions': 0,
            'warnings': decision.get('warning', False)
        }
        
        status = "⚠️ " if decision.get('warning') else "✅"
        print(f"   {status} Conectado a {peer.peer_id}")
        
        if decision.get('warning'):
            print(f"      Razón: {decision['reason']}")
        
        return True
    
    def _on_peer_discovered(self, peer: PeerInfo):
        """Callback cuando se descubre un peer"""
        if peer.peer_id not in self.connections:
            print(f"   🆕 Nuevo peer disponible: {peer.peer_id}")
    
    def simulate_work(self, peer_id: str, success_rate: float = 0.9):
        """
        Simula trabajo colaborativo con otro peer
        
        Args:
            peer_id: ID del peer con quien trabajar
            success_rate: Probabilidad de éxito (0.0-1.0)
        """
        if peer_id not in self.connections:
            print(f"   ⚠️  No conectado a {peer_id}")
            return
        
        # Simular interacción
        success = random.random() < success_rate
        interaction_type = random.choice(['tensor_exchange', 'training', 'inference'])
        
        # Reportar al sistema de reputación
        self.client.report_interaction(peer_id, success, interaction_type)
        
        # Actualizar stats
        self.connections[peer_id]['interactions'] += 1
        self.work_done += 1
        
        status = "✅" if success else "❌"
        print(f"   {status} {self.peer_id} ↔️  {peer_id}: {interaction_type} {'OK' if success else 'FAIL'}")
        
        return success
    
    def get_reputation_report(self, peer_id: str):
        """Obtiene reporte de reputación de un peer"""
        rep = self.reputation.calculate_reputation(peer_id)
        
        print(f"\n📊 Reputación de {peer_id}:")
        print(f"   Score: {rep.score:.2f}")
        print(f"   Confidence: {rep.confidence:.2f}")
        print(f"   Patterns: {rep.patterns_detected}")
        
        if rep.warnings:
            print(f"   ⚠️  Warnings: {len(rep.warnings)}")
            for warning in rep.warnings:
                print(f"      - {warning}")
        
        if rep.redemption_path:
            print(f"   🔄 En periodo de redención")
    
    def get_stats(self):
        """Estadísticas del peer"""
        client_stats = self.client.get_stats()
        
        return {
            'peer_id': self.peer_id,
            'connections': len(self.connections),
            'work_done': self.work_done,
            'uptime': client_stats['uptime_formatted'],
            'heartbeats': client_stats['heartbeats_sent'],
            'peers_known': client_stats['peers_discovered']
        }
    
    def stop(self):
        """Detiene el peer"""
        print(f"\n🛑 Deteniendo {self.peer_id}")
        self.client.stop_heartbeat()
        self.is_running = False


def demo_simple():
    """Demo simple con 2 peers"""
    print("=" * 70)
    print("🐹 DEMO 1: Red Simple (2 Peers)")
    print("=" * 70)
    
    # Configurar endpoint (actualiza con tu API Gateway URL)
    ENDPOINT = "https://YOUR-API-ID.execute-api.us-east-1.amazonaws.com/dev"
    
    # Crear peers
    pepino = AuroraPeer("pepino-001", ["Pepino", "Teacher"], ENDPOINT)
    researcher = AuroraPeer("researcher-001", ["Researcher"], ENDPOINT)
    
    # Iniciar peers
    if not pepino.start(port=8001):
        return
    if not researcher.start(port=8002):
        return
    
    # Esperar un poco para que se registren
    time.sleep(2)
    
    # Descubrir peers
    pepino.discover_and_connect()
    researcher.discover_and_connect()
    
    # Simular trabajo colaborativo
    print("\n💼 Simulando trabajo colaborativo...")
    for i in range(10):
        if "researcher-001" in pepino.connections:
            pepino.simulate_work("researcher-001", success_rate=0.8)
        
        if "pepino-001" in researcher.connections:
            researcher.simulate_work("pepino-001", success_rate=0.9)
        
        time.sleep(1)
    
    # Ver reputación mutua
    pepino.get_reputation_report("researcher-001")
    researcher.get_reputation_report("pepino-001")
    
    # Stats
    print("\n📊 Estadísticas:")
    print(f"   Pepino: {pepino.get_stats()}")
    print(f"   Researcher: {researcher.get_stats()}")
    
    # Cleanup
    pepino.stop()
    researcher.stop()


def demo_toxic_peer():
    """Demo con peer tóxico y sistema de redención"""
    print("\n" + "=" * 70)
    print("🐹 DEMO 2: Peer Tóxico + Sistema de Redención")
    print("=" * 70)
    
    ENDPOINT = "https://YOUR-API-ID.execute-api.us-east-1.amazonaws.com/dev"
    
    # Crear peers
    good_peer = AuroraPeer("good-peer", ["Pepino"], ENDPOINT)
    toxic_peer = AuroraPeer("toxic-peer", ["Researcher"], ENDPOINT)
    
    # Iniciar
    if not good_peer.start(port=8001):
        return
    if not toxic_peer.start(port=8002):
        return
    
    time.sleep(2)
    
    # Descubrir
    good_peer.discover_and_connect()
    toxic_peer.discover_and_connect()
    
    # Fase 1: Toxic peer falla constantemente
    print("\n⚠️  FASE 1: Toxic peer fallando constantemente...")
    for i in range(15):
        if "toxic-peer" in good_peer.connections:
            good_peer.simulate_work("toxic-peer", success_rate=0.0)  # Siempre falla
        time.sleep(0.5)
    
    # Ver reputación (debería ser muy baja)
    print("\n📊 Reputación después de fallos:")
    good_peer.get_reputation_report("toxic-peer")
    
    # Fase 2: Sistema da segunda oportunidad
    decision = good_peer.reputation.should_connect_to_peer("toxic-peer")
    print(f"\n🔄 Decisión del sistema: {decision['reason']}")
    
    if decision.get('redemption_path'):
        path = decision['redemption_path']
        print(f"\n📋 Path de Redención:")
        print(f"   Mensaje: {path['message']}")
        print(f"   Periodo: {path['period_days']} días")
        print(f"   Goals:")
        for goal in path['goals']:
            print(f"      - {goal}")
    
    # Fase 3: Toxic peer mejora
    print("\n✅ FASE 2: Toxic peer mejorando...")
    for i in range(20):
        if "toxic-peer" in good_peer.connections:
            good_peer.simulate_work("toxic-peer", success_rate=0.85)  # Mejor comportamiento
        time.sleep(0.5)
    
    # Ver reputación recuperada
    print("\n📊 Reputación después de mejorar:")
    good_peer.get_reputation_report("toxic-peer")
    
    # Cleanup
    good_peer.stop()
    toxic_peer.stop()


def demo_network():
    """Demo con red de múltiples peers"""
    print("\n" + "=" * 70)
    print("🐹 DEMO 3: Red P2P Completa (5 Peers)")
    print("=" * 70)
    
    ENDPOINT = "https://YOUR-API-ID.execute-api.us-east-1.amazonaws.com/dev"
    
    # Crear red de peers
    peers = [
        AuroraPeer(f"pepino-{i}", ["Pepino", "Teacher"], ENDPOINT) 
        for i in range(2)
    ] + [
        AuroraPeer(f"researcher-{i}", ["Researcher"], ENDPOINT) 
        for i in range(3)
    ]
    
    # Iniciar todos
    print("\n🚀 Iniciando red...")
    for i, peer in enumerate(peers):
        if not peer.start(port=8000 + i):
            return
        time.sleep(0.5)
    
    # Esperar registro
    time.sleep(3)
    
    # Todos descubren la red
    print("\n🔍 Discovery phase...")
    for peer in peers:
        peer.discover_and_connect()
        time.sleep(1)
    
    # Simulación de trabajo en red
    print("\n💼 Simulando red activa (30 segundos)...")
    start_time = time.time()
    
    while time.time() - start_time < 30:
        # Cada peer trabaja con un peer aleatorio
        for peer in peers:
            if peer.connections:
                partner_id = random.choice(list(peer.connections.keys()))
                success_rate = random.uniform(0.7, 0.95)
                peer.simulate_work(partner_id, success_rate)
        
        time.sleep(2)
    
    # Resumen final
    print("\n" + "=" * 70)
    print("📊 RESUMEN DE LA RED")
    print("=" * 70)
    
    for peer in peers:
        stats = peer.get_stats()
        print(f"\n{stats['peer_id']}:")
        print(f"   Conexiones: {stats['connections']}")
        print(f"   Trabajo realizado: {stats['work_done']}")
        print(f"   Uptime: {stats['uptime']}")
        print(f"   Heartbeats: {stats['heartbeats']}")
    
    # Cleanup
    print("\n🛑 Deteniendo red...")
    for peer in peers:
        peer.stop()


if __name__ == "__main__":
    import sys
    
    print("🐹 Aurora P2P Network - Ejemplos Interactivos")
    print()
    print("NOTA: Actualiza la variable ENDPOINT en el código con tu API Gateway URL")
    print()
    print("Selecciona un demo:")
    print("1. Red simple (2 peers)")
    print("2. Peer tóxico + redención")
    print("3. Red completa (5 peers)")
    print("4. Todos los demos")
    print()
    
    choice = input("Opción (1-4): ").strip()
    
    if choice == "1":
        demo_simple()
    elif choice == "2":
        demo_toxic_peer()
    elif choice == "3":
        demo_network()
    elif choice == "4":
        demo_simple()
        time.sleep(2)
        demo_toxic_peer()
        time.sleep(2)
        demo_network()
    else:
        print("❌ Opción inválida")
