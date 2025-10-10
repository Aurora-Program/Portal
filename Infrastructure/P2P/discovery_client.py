"""
🐹 Aurora P2P Discovery Client
Cliente Python para Discovery Server con sistema de reputación integrado
"""

import json
import requests
import time
import threading
from typing import List, Dict, Optional, Callable
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import uuid


@dataclass
class PeerInfo:
    """Información de un peer descubierto"""
    peer_id: str
    address: str
    port: int
    archetypes: List[str]
    last_seen: str
    metadata: Dict = None
    reputation_hint: Dict = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
        if isinstance(self.last_seen, str):
            self.last_seen_dt = datetime.fromisoformat(self.last_seen.replace('Z', '+00:00'))
        else:
            self.last_seen_dt = self.last_seen
    
    @property
    def age_seconds(self) -> float:
        """Edad del registro en segundos"""
        return (datetime.now() - self.last_seen_dt).total_seconds()
    
    def is_active(self, ttl_seconds: int = 300) -> bool:
        """Verifica si el peer está activo según TTL"""
        return self.age_seconds < ttl_seconds


@dataclass
class DiscoveryConfig:
    """Configuración del cliente Discovery"""
    endpoint: str
    peer_id: str = None
    archetypes: List[str] = None
    heartbeat_interval: int = 30
    ttl_seconds: int = 300
    enable_reputation: bool = True
    auto_heartbeat: bool = True
    
    def __post_init__(self):
        if self.peer_id is None:
            self.peer_id = f"aurora-peer-{uuid.uuid4().hex[:8]}"
        if self.archetypes is None:
            self.archetypes = []


class DiscoveryClient:
    """
    Cliente para Aurora P2P Discovery Server
    
    Features:
    - Registro automático de peer
    - Heartbeat automático en background
    - Descubrimiento de peers por archetype
    - Integración con sistema de reputación
    - Retry automático con backoff exponencial
    - Thread-safe
    """
    
    def __init__(self, config: DiscoveryConfig, reputation_system=None):
        """
        Args:
            config: Configuración del cliente
            reputation_system: Sistema de reputación (opcional)
        """
        self.config = config
        self.reputation_system = reputation_system
        self.registered = False
        self.heartbeat_thread = None
        self.heartbeat_stop = threading.Event()
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': f'Aurora-Discovery-Client/1.0 ({self.config.peer_id})'
        })
        
        # Callbacks
        self.on_peer_discovered: Optional[Callable] = None
        self.on_heartbeat_success: Optional[Callable] = None
        self.on_heartbeat_failure: Optional[Callable] = None
        
        # Stats
        self.stats = {
            'heartbeats_sent': 0,
            'heartbeats_failed': 0,
            'peers_discovered': 0,
            'last_discovery': None,
            'uptime_start': datetime.now()
        }
    
    def register(self, address: str, port: int, metadata: Dict = None) -> Dict:
        """
        Registra este peer en el Discovery Server
        
        Args:
            address: Dirección IP/hostname del peer
            port: Puerto del peer
            metadata: Metadata adicional (opcional)
            
        Returns:
            Respuesta del servidor con confirmación y TTL
        """
        payload = {
            'peer_id': self.config.peer_id,
            'address': address,
            'port': port,
            'archetypes': self.config.archetypes,
            'metadata': metadata or {}
        }
        
        response = self._post(f"{self.config.endpoint}/register", payload)
        
        if response.status_code == 200:
            self.registered = True
            
            # Auto-start heartbeat
            if self.config.auto_heartbeat and not self.heartbeat_thread:
                self.start_heartbeat()
            
            print(f"✅ Peer {self.config.peer_id} registrado exitosamente")
            return response.json()
        else:
            raise Exception(f"Error al registrar peer: {response.status_code} - {response.text}")
    
    def discover(self, archetype: str = None, include_reputation: bool = None) -> List[PeerInfo]:
        """
        Descubre peers activos en la red
        
        Args:
            archetype: Filtrar por archetype específico (opcional)
            include_reputation: Incluir hints de reputación del servidor (opcional)
            
        Returns:
            Lista de peers descubiertos
        """
        if include_reputation is None:
            include_reputation = self.config.enable_reputation
        
        params = {}
        if archetype:
            params['archetype'] = archetype
        if include_reputation:
            params['reputation'] = 'true'
        
        response = self._get(f"{self.config.endpoint}/discover", params=params)
        
        if response.status_code == 200:
            data = response.json()
            peers = [PeerInfo(**peer) for peer in data['peers']]
            
            # Filtrar peers activos
            active_peers = [p for p in peers if p.is_active(self.config.ttl_seconds)]
            
            # Excluir este peer
            active_peers = [p for p in active_peers if p.peer_id != self.config.peer_id]
            
            # Aplicar reputación local si está disponible
            if self.reputation_system:
                active_peers = self._filter_by_reputation(active_peers)
            
            self.stats['peers_discovered'] = len(active_peers)
            self.stats['last_discovery'] = datetime.now()
            
            if self.on_peer_discovered:
                for peer in active_peers:
                    self.on_peer_discovered(peer)
            
            return active_peers
        else:
            raise Exception(f"Error al descubrir peers: {response.status_code} - {response.text}")
    
    def heartbeat(self) -> Dict:
        """
        Envía heartbeat para mantener registro activo
        
        Returns:
            Respuesta del servidor con timestamp actualizado
        """
        if not self.registered:
            raise Exception("Peer no registrado. Llama a register() primero.")
        
        payload = {'peer_id': self.config.peer_id}
        response = self._post(f"{self.config.endpoint}/heartbeat", payload)
        
        if response.status_code == 200:
            self.stats['heartbeats_sent'] += 1
            if self.on_heartbeat_success:
                self.on_heartbeat_success()
            return response.json()
        else:
            self.stats['heartbeats_failed'] += 1
            if self.on_heartbeat_failure:
                self.on_heartbeat_failure(response)
            raise Exception(f"Error en heartbeat: {response.status_code} - {response.text}")
    
    def health_check(self) -> Dict:
        """
        Verifica estado del Discovery Server
        
        Returns:
            Estado del servidor
        """
        response = self._get(f"{self.config.endpoint}/health")
        return response.json()
    
    def start_heartbeat(self):
        """Inicia heartbeat automático en background thread"""
        if self.heartbeat_thread and self.heartbeat_thread.is_alive():
            print("⚠️  Heartbeat ya está corriendo")
            return
        
        self.heartbeat_stop.clear()
        self.heartbeat_thread = threading.Thread(target=self._heartbeat_loop, daemon=True)
        self.heartbeat_thread.start()
        print(f"💓 Heartbeat iniciado (intervalo: {self.config.heartbeat_interval}s)")
    
    def stop_heartbeat(self):
        """Detiene heartbeat automático"""
        if self.heartbeat_thread:
            self.heartbeat_stop.set()
            self.heartbeat_thread.join(timeout=5)
            print("💔 Heartbeat detenido")
    
    def _heartbeat_loop(self):
        """Loop de heartbeat en background"""
        while not self.heartbeat_stop.is_set():
            try:
                self.heartbeat()
            except Exception as e:
                print(f"⚠️  Error en heartbeat automático: {e}")
            
            # Sleep con check periódico para poder interrumpir
            for _ in range(self.config.heartbeat_interval):
                if self.heartbeat_stop.is_set():
                    break
                time.sleep(1)
    
    def _filter_by_reputation(self, peers: List[PeerInfo]) -> List[PeerInfo]:
        """
        Filtra peers usando el sistema de reputación local
        
        Args:
            peers: Lista de peers descubiertos
            
        Returns:
            Lista filtrada de peers confiables
        """
        if not self.reputation_system:
            return peers
        
        trusted_peers = []
        for peer in peers:
            decision = self.reputation_system.should_connect_to_peer(peer.peer_id)
            
            if decision['should_connect']:
                trusted_peers.append(peer)
                if decision.get('warning'):
                    print(f"⚠️  Peer {peer.peer_id}: {decision['reason']}")
            else:
                print(f"🚫 Peer {peer.peer_id} filtrado: {decision['reason']}")
        
        return trusted_peers
    
    def report_interaction(self, peer_id: str, success: bool, interaction_type: str = 'general'):
        """
        Reporta interacción con peer al sistema de reputación
        
        Args:
            peer_id: ID del peer
            success: Si la interacción fue exitosa
            interaction_type: Tipo de interacción (tensor_exchange, training, etc.)
        """
        if self.reputation_system:
            self.reputation_system.record_interaction(
                peer_id=peer_id,
                success=success,
                interaction_type=interaction_type
            )
    
    def get_stats(self) -> Dict:
        """Obtiene estadísticas del cliente"""
        uptime = (datetime.now() - self.stats['uptime_start']).total_seconds()
        return {
            **self.stats,
            'uptime_seconds': uptime,
            'uptime_formatted': str(timedelta(seconds=int(uptime))),
            'heartbeat_success_rate': (
                self.stats['heartbeats_sent'] / 
                (self.stats['heartbeats_sent'] + self.stats['heartbeats_failed'])
                if self.stats['heartbeats_sent'] + self.stats['heartbeats_failed'] > 0
                else 0.0
            )
        }
    
    def _get(self, url: str, params: Dict = None, retry: int = 3) -> requests.Response:
        """GET request con retry exponencial"""
        for attempt in range(retry):
            try:
                response = self.session.get(url, params=params, timeout=10)
                return response
            except requests.RequestException as e:
                if attempt == retry - 1:
                    raise
                wait_time = 2 ** attempt
                print(f"⚠️  Request falló, reintentando en {wait_time}s... ({attempt + 1}/{retry})")
                time.sleep(wait_time)
    
    def _post(self, url: str, data: Dict, retry: int = 3) -> requests.Response:
        """POST request con retry exponencial"""
        for attempt in range(retry):
            try:
                response = self.session.post(url, json=data, timeout=10)
                return response
            except requests.RequestException as e:
                if attempt == retry - 1:
                    raise
                wait_time = 2 ** attempt
                print(f"⚠️  Request falló, reintentando en {wait_time}s... ({attempt + 1}/{retry})")
                time.sleep(wait_time)
    
    def __enter__(self):
        """Context manager support"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Cleanup al salir del context"""
        self.stop_heartbeat()
        self.session.close()


# ============================================================================
# Ejemplo de uso
# ============================================================================

def main():
    """Ejemplo completo de uso del Discovery Client"""
    
    print("🐹 Aurora P2P Discovery Client - Demo")
    print("=" * 60)
    
    # Configuración
    config = DiscoveryConfig(
        endpoint="https://YOUR-API-ID.execute-api.us-east-1.amazonaws.com/dev",
        peer_id="demo-peer-001",
        archetypes=["Pepino", "Researcher"],
        heartbeat_interval=30,
        auto_heartbeat=True,
        enable_reputation=True
    )
    
    # Opcional: Integrar sistema de reputación
    try:
        from reputation_system import ReputationSystem
        reputation = ReputationSystem()
        print("✅ Sistema de reputación cargado")
    except ImportError:
        reputation = None
        print("⚠️  Sistema de reputación no disponible")
    
    # Crear cliente
    with DiscoveryClient(config, reputation_system=reputation) as client:
        
        # Health check
        print("\n1️⃣  Verificando servidor...")
        try:
            health = client.health_check()
            print(f"   Status: {health['status']}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return
        
        # Registrar peer
        print("\n2️⃣  Registrando peer...")
        try:
            result = client.register(
                address="192.168.1.100",
                port=8080,
                metadata={
                    "version": "1.0.0",
                    "capabilities": ["training", "inference"]
                }
            )
            print(f"   Peer ID: {result['peer_id']}")
            print(f"   TTL expira: {result['ttl_expires']}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return
        
        # Callbacks para heartbeat
        def on_heartbeat_ok():
            print("   💚 Heartbeat OK")
        
        def on_heartbeat_fail(response):
            print(f"   💔 Heartbeat falló: {response.status_code}")
        
        client.on_heartbeat_success = on_heartbeat_ok
        client.on_heartbeat_failure = on_heartbeat_fail
        
        # Descubrir peers
        print("\n3️⃣  Descubriendo peers...")
        try:
            peers = client.discover(include_reputation=True)
            print(f"   Encontrados: {len(peers)} peers activos")
            
            for peer in peers:
                print(f"\n   📍 Peer: {peer.peer_id}")
                print(f"      Address: {peer.address}:{peer.port}")
                print(f"      Archetypes: {', '.join(peer.archetypes)}")
                print(f"      Age: {peer.age_seconds:.1f}s")
                
                if peer.reputation_hint:
                    hint = peer.reputation_hint
                    print(f"      Reputation Hint: {hint['score']} {'🆕' if hint.get('is_new') else '👍'}")
        
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # Simular interacciones
        if peers and reputation:
            print("\n4️⃣  Simulando interacciones...")
            peer = peers[0]
            
            # Interacción exitosa
            client.report_interaction(peer.peer_id, success=True, interaction_type='tensor_exchange')
            print(f"   ✅ Interacción exitosa con {peer.peer_id}")
            
            # Verificar reputación actualizada
            rep = reputation.calculate_reputation(peer.peer_id)
            print(f"   Score: {rep.score:.2f} (confidence: {rep.confidence:.2f})")
        
        # Stats
        print("\n5️⃣  Estadísticas:")
        stats = client.get_stats()
        print(f"   Uptime: {stats['uptime_formatted']}")
        print(f"   Heartbeats: {stats['heartbeats_sent']} (exitosos)")
        print(f"   Heartbeats fallidos: {stats['heartbeats_failed']}")
        print(f"   Peers descubiertos: {stats['peers_discovered']}")
        print(f"   Success rate: {stats['heartbeat_success_rate']:.1%}")
        
        # Mantener vivo para ver heartbeats
        print("\n6️⃣  Monitoreando heartbeats (Ctrl+C para salir)...")
        try:
            while True:
                time.sleep(5)
                stats = client.get_stats()
                print(f"   💓 Heartbeats: {stats['heartbeats_sent']} | Peers: {stats['peers_discovered']}")
        except KeyboardInterrupt:
            print("\n\n👋 Saliendo...")


if __name__ == "__main__":
    main()
