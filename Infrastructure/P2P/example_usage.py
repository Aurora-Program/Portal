"""
🐹 Aurora P2P Client - Ejemplos de Uso

Ejemplos prácticos de cómo usar el cliente P2P de Aurora
con el Discovery Server serverless.

Author: Aurora Alliance
"""

import time
from aurora_p2p_client import AuroraP2PClient, PeerInfo


# ============================================================================
# EJEMPLO 1: Cliente Simple con Auto-registro
# ============================================================================

def example_1_simple_client():
    """Cliente básico que se registra y descubre peers"""
    print("\n" + "="*60)
    print("EJEMPLO 1: Cliente Simple")
    print("="*60)
    
    # Tu URL del API Gateway (después de desplegar CloudFormation)
    DISCOVERY_URL = "https://your-api-id.execute-api.us-east-1.amazonaws.com/dev"
    
    # Crear cliente (se registra automáticamente)
    client = AuroraP2PClient(
        discovery_url=DISCOVERY_URL,
        archetypes=['pepino', 'ethics'],
        port=9000
    )
    
    # Iniciar heartbeat automático
    client.start_heartbeat(interval=30)
    
    # Descubrir peers
    peers = client.discover()
    print(f"Found {len(peers)} peers")
    
    # Esperar un poco
    time.sleep(5)
    
    # Detener
    client.stop()


# ============================================================================
# EJEMPLO 2: Peer con Listener (Servidor)
# ============================================================================

def example_2_peer_server():
    """Peer que acepta conexiones entrantes"""
    print("\n" + "="*60)
    print("EJEMPLO 2: Peer Server (acepta conexiones)")
    print("="*60)
    
    DISCOVERY_URL = "https://your-api-id.execute-api.us-east-1.amazonaws.com/dev"
    
    client = AuroraP2PClient(
        discovery_url=DISCOVERY_URL,
        archetypes=['pepino', 'tensor-provider'],
        port=9001
    )
    
    # Handler personalizado para conexiones entrantes
    def handle_connection(sock, peer_info):
        print(f"📥 New connection from {peer_info['peer_id'][:8]}...")
        
        try:
            while True:
                data = sock.recv(4096)
                if not data:
                    break
                
                # Procesar datos recibidos
                message = data.decode()
                print(f"📨 Received: {message}")
                
                # Responder
                response = f"Echo from server: {message}"
                sock.sendall(response.encode())
        
        finally:
            sock.close()
            print(f"🔌 Connection closed")
    
    # Iniciar listener
    client.start_listener(handler=handle_connection)
    client.start_heartbeat()
    
    print("🎧 Server listening... Press Ctrl+C to stop")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        client.stop()


# ============================================================================
# EJEMPLO 3: Peer Client (Se conecta a otros)
# ============================================================================

def example_3_peer_client():
    """Peer que se conecta activamente a otros peers"""
    print("\n" + "="*60)
    print("EJEMPLO 3: Peer Client (busca y conecta)")
    print("="*60)
    
    DISCOVERY_URL = "https://your-api-id.execute-api.us-east-1.amazonaws.com/dev"
    
    client = AuroraP2PClient(
        discovery_url=DISCOVERY_URL,
        archetypes=['pepino', 'tensor-consumer'],
        port=9002
    )
    
    client.start_heartbeat()
    
    # Descubrir peers con arquetipo específico
    print("🔍 Discovering peers with 'tensor-provider' archetype...")
    peers = client.discover(archetype='tensor-provider')
    
    if peers:
        for peer in peers:
            print(f"\n🔗 Connecting to {peer.peer_id[:8]}...")
            sock = client.connect_to_peer(peer)
            
            if sock:
                # Enviar tensor (simulado)
                tensor_data = {
                    'type': 'FractalTensor',
                    'nivel_3': [[0, 1, 1]],  # Pepino tensor!
                    'archetype': 'pepino'
                }
                
                import json
                sock.sendall(json.dumps(tensor_data).encode())
                
                # Recibir respuesta
                response = sock.recv(4096)
                print(f"📬 Response: {response.decode()}")
                
                sock.close()
    else:
        print("❌ No tensor providers found")
    
    client.stop()


# ============================================================================
# EJEMPLO 4: Red de Pepino (Cluster de Peers)
# ============================================================================

def example_4_pepino_network():
    """Crea una red de peers que comparten el arquetipo de Pepino"""
    print("\n" + "="*60)
    print("EJEMPLO 4: Red de Pepino (Ethical Network)")
    print("="*60)
    
    DISCOVERY_URL = "https://your-api-id.execute-api.us-east-1.amazonaws.com/dev"
    
    # Crear múltiples peers en la misma máquina (puertos diferentes)
    peers = []
    for i in range(3):
        client = AuroraP2PClient(
            discovery_url=DISCOVERY_URL,
            archetypes=['pepino', 'ethics', f'node-{i}'],
            port=9010 + i,
            auto_register=True
        )
        client.start_heartbeat()
        peers.append(client)
        print(f"✅ Peer {i} registered: {client.peer_id[:8]}...")
    
    time.sleep(2)  # Esperar registro
    
    # Cada peer descubre a los demás
    print("\n🔍 Discovering Pepino network...")
    for i, client in enumerate(peers):
        discovered = client.discover(archetype='pepino')
        print(f"Peer {i} discovered {len(discovered)} other peers")
    
    # Peer 0 envía mensaje a todos
    print("\n📡 Broadcasting from Peer 0...")
    sender = peers[0]
    others = sender.discover()
    
    for peer in others:
        sock = sender.connect_to_peer(peer)
        if sock:
            message = "🐹 Pepino's lesson: Empathy for all beings!"
            sock.sendall(message.encode())
            sock.close()
    
    # Cleanup
    time.sleep(2)
    for client in peers:
        client.stop()
    
    print("\n✅ Pepino network demo complete!")


# ============================================================================
# EJEMPLO 5: Context Manager
# ============================================================================

def example_5_context_manager():
    """Uso con context manager (auto-cleanup)"""
    print("\n" + "="*60)
    print("EJEMPLO 5: Context Manager")
    print("="*60)
    
    DISCOVERY_URL = "https://your-api-id.execute-api.us-east-1.amazonaws.com/dev"
    
    # Uso con 'with' - auto-cleanup al salir
    with AuroraP2PClient(
        discovery_url=DISCOVERY_URL,
        archetypes=['pepino'],
        port=9020
    ) as client:
        
        client.start_heartbeat()
        
        # Health check
        health = client.health_check()
        print(f"Server health: {health}")
        
        # Discover
        peers = client.discover()
        print(f"Found {len(peers)} peers")
        
        time.sleep(5)
    
    # Client se detiene automáticamente aquí
    print("✅ Client auto-stopped")


# ============================================================================
# EJEMPLO 6: Callbacks y Eventos
# ============================================================================

def example_6_callbacks():
    """Uso avanzado con callbacks para eventos"""
    print("\n" + "="*60)
    print("EJEMPLO 6: Callbacks y Eventos")
    print("="*60)
    
    DISCOVERY_URL = "https://your-api-id.execute-api.us-east-1.amazonaws.com/dev"
    
    client = AuroraP2PClient(
        discovery_url=DISCOVERY_URL,
        archetypes=['pepino', 'observer'],
        port=9030
    )
    
    # Callback cuando se descubre un peer
    def on_peer_discovered(peer: PeerInfo):
        print(f"🎉 NEW PEER: {peer.peer_id[:8]}... with {peer.archetypes}")
        
        # Auto-conectar si tiene arquetipo 'pepino'
        if 'pepino' in peer.archetypes:
            print(f"   → Has Pepino archetype! Connecting...")
            sock = client.connect_to_peer(peer)
            if sock:
                sock.sendall(b"Hello fellow Pepino peer!")
                sock.close()
    
    # Callback cuando se conecta exitosamente
    def on_peer_connected(peer: PeerInfo, sock):
        print(f"✅ CONNECTED: {peer.peer_id[:8]}...")
    
    # Callback cuando se reciben datos
    def on_data_received(data: bytes, peer_info: dict):
        print(f"📨 DATA: {data.decode()} from {peer_info['peer_id'][:8]}...")
    
    # Registrar callbacks
    client.on('on_peer_discovered', on_peer_discovered)
    client.on('on_peer_connected', on_peer_connected)
    client.on('on_data_received', on_data_received)
    
    # Iniciar
    client.start_heartbeat()
    client.start_listener()
    
    # Loop de descubrimiento
    print("\n👂 Listening for events... (10 seconds)")
    for _ in range(2):
        client.discover()
        time.sleep(5)
    
    client.stop()


# ============================================================================
# MAIN - Ejecutar Ejemplos
# ============================================================================

if __name__ == "__main__":
    print("\n" + "🐹"*30)
    print("AURORA P2P CLIENT - EJEMPLOS DE USO")
    print("🐹"*30)
    
    print("\nAntes de ejecutar, actualiza DISCOVERY_URL con tu API Gateway endpoint")
    print("(Obtenido después de desplegar con deploy.ps1)\n")
    
    # Descomentar el ejemplo que quieras ejecutar:
    
    # example_1_simple_client()
    # example_2_peer_server()
    # example_3_peer_client()
    # example_4_pepino_network()
    # example_5_context_manager()
    # example_6_callbacks()
    
    print("\n✨ Para ejecutar un ejemplo, descomenta la línea correspondiente")
    print("   y actualiza DISCOVERY_URL con tu endpoint real\n")
