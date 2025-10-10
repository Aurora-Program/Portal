"""
🐹 Aurora P2P Client

Cliente para conectar agentes Aurora a través del Discovery Server serverless.
Maneja registro, descubrimiento, heartbeat y conexiones P2P directas.

Author: Aurora Alliance
License: Apache-2.0
Version: 1.0.0
"""

import requests
import socket
import threading
import time
import uuid
import json
import logging
from typing import List, Dict, Optional, Callable
from datetime import datetime
from dataclasses import dataclass, asdict

# Logger setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("aurora.p2p")


@dataclass
class PeerInfo:
    """Información de un peer en la red Aurora"""
    peer_id: str
    address: str
    port: int
    archetypes: List[str]
    last_seen: str
    metadata: Dict = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
    
    def to_dict(self) -> Dict:
        """Convierte a diccionario para JSON"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'PeerInfo':
        """Crea PeerInfo desde diccionario"""
        return cls(
            peer_id=data['peer_id'],
            address=data['address'],
            port=int(data['port']),
            archetypes=data.get('archetypes', []),
            last_seen=data['last_seen'],
            metadata=data.get('metadata', {})
        )


class AuroraP2PClient:
    """
    Cliente P2P para Aurora que usa Discovery Server serverless.
    
    Funcionalidades:
    - Registro automático en la red
    - Descubrimiento de peers activos
    - Heartbeat automático
    - Conexiones P2P directas
    - Filtrado por arquetipos
    
    Uso:
        client = AuroraP2PClient(discovery_url="https://api.aws.../dev")
        client.register(archetypes=['pepino', 'ethics'])
        client.start_heartbeat()
        
        peers = client.discover(archetype='pepino')
        for peer in peers:
            client.connect_to_peer(peer)
    """
    
    def __init__(
        self, 
        discovery_url: str,
        peer_id: Optional[str] = None,
        port: int = 9000,
        archetypes: List[str] = None,
        auto_register: bool = True,
        heartbeat_interval: int = 30
    ):
        """
        Inicializa el cliente P2P.
        
        Args:
            discovery_url: URL del Discovery Server (Lambda API Gateway)
            peer_id: ID único del peer (genera uno si no se provee)
            port: Puerto para conexiones P2P directas
            archetypes: Lista de arquetipos que maneja este peer
            auto_register: Registrarse automáticamente al iniciar
            heartbeat_interval: Intervalo de heartbeat en segundos
        """
        self.discovery_url = discovery_url.rstrip('/')
        self.peer_id = peer_id or str(uuid.uuid4())
        self.port = port
        self.archetypes = archetypes or []
        self.heartbeat_interval = heartbeat_interval
        
        # Estado interno
        self._running = False
        self._heartbeat_thread = None
        self._socket = None
        self._callbacks: Dict[str, List[Callable]] = {
            'on_peer_discovered': [],
            'on_peer_connected': [],
            'on_peer_disconnected': [],
            'on_data_received': []
        }
        
        # Obtener IP local
        self.local_ip = self._get_local_ip()
        
        logger.info(f"🐹 Aurora P2P Client initialized: {self.peer_id}")
        logger.info(f"   Local IP: {self.local_ip}:{self.port}")
        logger.info(f"   Archetypes: {self.archetypes}")
        
        # Auto-registro
        if auto_register:
            self.register()
    
    def _get_local_ip(self) -> str:
        """Obtiene la IP local para conexiones P2P"""
        try:
            # Truco: conectar a un servidor externo para obtener IP local
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except Exception as e:
            logger.warning(f"No se pudo obtener IP local: {e}")
            return '127.0.0.1'
    
    def register(self, archetypes: Optional[List[str]] = None, metadata: Optional[Dict] = None) -> Dict:
        """
        Registra este peer en el Discovery Server.
        
        Args:
            archetypes: Lista de arquetipos (usa self.archetypes si no se provee)
            metadata: Metadata adicional del peer
        
        Returns:
            Respuesta del servidor con confirmación
        """
        if archetypes:
            self.archetypes = archetypes
        
        data = {
            'peer_id': self.peer_id,
            'address': self.local_ip,
            'port': self.port,
            'archetypes': self.archetypes,
            'metadata': metadata or {
                'version': '1.0.0',
                'client': 'aurora-p2p-python',
                'capabilities': ['tensor-exchange', 'archetype-sync']
            }
        }
        
        try:
            response = requests.post(
                f"{self.discovery_url}/register",
                json=data,
                timeout=10
            )
            response.raise_for_status()
            result = response.json()
            
            logger.info(f"✅ Peer registered: {self.peer_id}")
            logger.info(f"   TTL expires: {result.get('ttl_expires', 'unknown')}")
            
            return result
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Registration failed: {e}")
            raise
    
    def discover(self, archetype: Optional[str] = None) -> List[PeerInfo]:
        """
        Descubre peers activos en la red.
        
        Args:
            archetype: Filtrar solo peers con este arquetipo
        
        Returns:
            Lista de PeerInfo con peers activos
        """
        try:
            params = {'archetype': archetype} if archetype else {}
            response = requests.get(
                f"{self.discovery_url}/discover",
                params=params,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            peers = [
                PeerInfo.from_dict(p) 
                for p in data['peers']
                if p['peer_id'] != self.peer_id  # No incluirse a sí mismo
            ]
            
            logger.info(f"🔍 Discovered {len(peers)} peers")
            if archetype:
                logger.info(f"   Filtered by archetype: {archetype}")
            
            # Trigger callbacks
            for peer in peers:
                self._trigger_callback('on_peer_discovered', peer)
            
            return peers
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Discovery failed: {e}")
            return []
    
    def heartbeat(self) -> bool:
        """
        Envía un heartbeat al Discovery Server para mantener el registro activo.
        
        Returns:
            True si el heartbeat fue exitoso
        """
        try:
            response = requests.post(
                f"{self.discovery_url}/heartbeat",
                json={'peer_id': self.peer_id},
                timeout=5
            )
            response.raise_for_status()
            logger.debug(f"💓 Heartbeat sent: {self.peer_id}")
            return True
        except requests.exceptions.RequestException as e:
            logger.warning(f"⚠️ Heartbeat failed: {e}")
            return False
    
    def start_heartbeat(self, interval: Optional[int] = None):
        """
        Inicia el envío automático de heartbeats en background.
        
        Args:
            interval: Intervalo en segundos (usa self.heartbeat_interval si no se provee)
        """
        if self._running:
            logger.warning("Heartbeat already running")
            return
        
        interval = interval or self.heartbeat_interval
        self._running = True
        
        def heartbeat_loop():
            logger.info(f"💓 Starting heartbeat (interval: {interval}s)")
            while self._running:
                try:
                    self.heartbeat()
                    time.sleep(interval)
                except Exception as e:
                    logger.error(f"Heartbeat loop error: {e}")
                    time.sleep(interval)
        
        self._heartbeat_thread = threading.Thread(
            target=heartbeat_loop,
            daemon=True,
            name="aurora-heartbeat"
        )
        self._heartbeat_thread.start()
        logger.info("✅ Heartbeat started")
    
    def stop_heartbeat(self):
        """Detiene el envío automático de heartbeats"""
        if not self._running:
            return
        
        self._running = False
        if self._heartbeat_thread:
            self._heartbeat_thread.join(timeout=5)
        logger.info("🛑 Heartbeat stopped")
    
    def connect_to_peer(self, peer: PeerInfo, timeout: int = 10) -> Optional[socket.socket]:
        """
        Establece una conexión P2P directa con otro peer.
        
        Args:
            peer: PeerInfo del peer destino
            timeout: Timeout de conexión en segundos
        
        Returns:
            Socket conectado o None si falla
        """
        try:
            logger.info(f"🔗 Connecting to peer {peer.peer_id[:8]}... at {peer.address}:{peer.port}")
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            sock.connect((peer.address, peer.port))
            
            # Handshake simple
            handshake = {
                'peer_id': self.peer_id,
                'archetypes': self.archetypes,
                'timestamp': datetime.now().isoformat()
            }
            sock.sendall(json.dumps(handshake).encode() + b'\n')
            
            logger.info(f"✅ Connected to peer {peer.peer_id[:8]}...")
            self._trigger_callback('on_peer_connected', peer, sock)
            
            return sock
        except Exception as e:
            logger.error(f"❌ Connection failed to {peer.peer_id[:8]}...: {e}")
            return None
    
    def start_listener(self, handler: Optional[Callable] = None):
        """
        Inicia un servidor socket para aceptar conexiones P2P entrantes.
        
        Args:
            handler: Función callback para manejar conexiones entrantes
        """
        if self._socket:
            logger.warning("Listener already running")
            return
        
        def listener_loop():
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self._socket.bind(('0.0.0.0', self.port))
            self._socket.listen(5)
            
            logger.info(f"👂 Listening for P2P connections on port {self.port}")
            
            while self._running:
                try:
                    client_socket, address = self._socket.accept()
                    logger.info(f"📥 Incoming connection from {address}")
                    
                    # Leer handshake
                    data = client_socket.recv(1024).decode().strip()
                    peer_info = json.loads(data)
                    
                    logger.info(f"   Peer ID: {peer_info['peer_id'][:8]}...")
                    logger.info(f"   Archetypes: {peer_info['archetypes']}")
                    
                    if handler:
                        threading.Thread(
                            target=handler,
                            args=(client_socket, peer_info),
                            daemon=True
                        ).start()
                    else:
                        # Handler por defecto: echo
                        self._default_handler(client_socket, peer_info)
                
                except Exception as e:
                    if self._running:
                        logger.error(f"Listener error: {e}")
        
        threading.Thread(
            target=listener_loop,
            daemon=True,
            name="aurora-listener"
        ).start()
        logger.info("✅ Listener started")
    
    def _default_handler(self, sock: socket.socket, peer_info: Dict):
        """Handler por defecto para conexiones entrantes"""
        try:
            while True:
                data = sock.recv(4096)
                if not data:
                    break
                
                logger.info(f"📨 Received {len(data)} bytes from {peer_info['peer_id'][:8]}...")
                self._trigger_callback('on_data_received', data, peer_info)
                
                # Echo back
                sock.sendall(data)
        except Exception as e:
            logger.error(f"Handler error: {e}")
        finally:
            sock.close()
            logger.info(f"🔌 Connection closed with {peer_info['peer_id'][:8]}...")
    
    def on(self, event: str, callback: Callable):
        """
        Registra un callback para eventos.
        
        Eventos disponibles:
        - on_peer_discovered: Cuando se descubre un nuevo peer
        - on_peer_connected: Cuando se establece conexión con un peer
        - on_peer_disconnected: Cuando se pierde conexión con un peer
        - on_data_received: Cuando se reciben datos de un peer
        
        Args:
            event: Nombre del evento
            callback: Función a llamar cuando ocurra el evento
        """
        if event not in self._callbacks:
            raise ValueError(f"Unknown event: {event}")
        self._callbacks[event].append(callback)
        logger.debug(f"Callback registered for event: {event}")
    
    def _trigger_callback(self, event: str, *args, **kwargs):
        """Dispara callbacks registrados para un evento"""
        for callback in self._callbacks.get(event, []):
            try:
                callback(*args, **kwargs)
            except Exception as e:
                logger.error(f"Callback error for {event}: {e}")
    
    def health_check(self) -> Dict:
        """
        Verifica el estado del Discovery Server.
        
        Returns:
            Estado del servidor
        """
        try:
            response = requests.get(
                f"{self.discovery_url}/health",
                timeout=5
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Health check failed: {e}")
            return {'status': 'unhealthy', 'error': str(e)}
    
    def stop(self):
        """Detiene el cliente y limpia recursos"""
        logger.info("🛑 Stopping Aurora P2P Client...")
        
        self.stop_heartbeat()
        
        if self._socket:
            try:
                self._socket.close()
            except:
                pass
        
        logger.info("✅ Client stopped")
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.stop()


# ============================================================================
# EJEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    # Configuración (reemplazar con tu API Gateway URL)
    DISCOVERY_URL = "https://your-api-id.execute-api.us-east-1.amazonaws.com/dev"
    
    print("🐹 Aurora P2P Client Demo")
    print("=" * 50)
    
    # Crear cliente
    client = AuroraP2PClient(
        discovery_url=DISCOVERY_URL,
        archetypes=['pepino', 'ethics'],
        port=9000
    )
    
    # Registrar callbacks
    def on_peer_discovered(peer: PeerInfo):
        print(f"✨ Discovered peer: {peer.peer_id[:8]}... with archetypes {peer.archetypes}")
    
    def on_data_received(data: bytes, peer_info: Dict):
        print(f"📨 Received: {data.decode()} from {peer_info['peer_id'][:8]}...")
    
    client.on('on_peer_discovered', on_peer_discovered)
    client.on('on_data_received', on_data_received)
    
    # Iniciar heartbeat
    client.start_heartbeat()
    
    # Iniciar listener para conexiones entrantes
    client.start_listener()
    
    # Descubrir peers periódicamente
    print("\n🔍 Starting peer discovery loop...")
    print("Press Ctrl+C to stop\n")
    
    try:
        while True:
            # Descubrir todos los peers
            peers = client.discover()
            
            if peers:
                print(f"\n📡 Found {len(peers)} active peers:")
                for peer in peers:
                    print(f"  - {peer.peer_id[:8]}... at {peer.address}:{peer.port}")
                    print(f"    Archetypes: {peer.archetypes}")
                
                # Conectar al primer peer con arquetipo 'pepino'
                pepino_peers = [p for p in peers if 'pepino' in p.archetypes]
                if pepino_peers:
                    peer = pepino_peers[0]
                    sock = client.connect_to_peer(peer)
                    if sock:
                        # Enviar mensaje de prueba
                        message = f"Hello from {client.peer_id[:8]}! 🐹"
                        sock.sendall(message.encode())
                        
                        # Recibir respuesta
                        response = sock.recv(1024)
                        print(f"📬 Response: {response.decode()}")
                        
                        sock.close()
            else:
                print("No peers found yet...")
            
            # Esperar antes de la siguiente búsqueda
            time.sleep(10)
    
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down...")
        client.stop()
        print("✅ Goodbye!")
