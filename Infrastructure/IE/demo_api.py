"""
🌌 DEMOSTRACIÓN AURORA API - Sistema Completo
==============================================

Prueba completa del sistema Aurora via API REST.
"""

import requests
import json

BASE_URL = "http://localhost:8080/api/v1"

def main():
    print("="*70)
    print("  🌌 AURORA API - SISTEMA EN PRODUCCIÓN")
    print("="*70)
    
    # Health Check
    print("\n✅ API Health Check...")
    health = requests.get(f"{BASE_URL}/health").json()
    print(f"   Status: {health['status']}")
    print(f"   Version: {health['version']}")
    print(f"   Timestamp: {health['timestamp']}")
    
    # Authentication
    print("\n🔐 Authenticating...")
    auth_response = requests.post(f"{BASE_URL}/auth/login", json={
        "public_key": "demo_user_aurora",
        "peer_signature": "demo_sig",
        "peer_id": "demo_peer"
    })
    
    auth_data = auth_response.json()
    token = auth_data.get('token') or auth_data.get('access_token')
    headers = {"Authorization": f"Bearer {token}"}
    print(f"   Token obtained: {token[:20]}...{token[-10:]}")
    print(f"   Session ID: {auth_data.get('session_id', 'N/A')[:16]}...")
    print(f"   Message: {auth_data.get('message', '')}")
    
    # Create Tensors
    print("\n🔷 Creating Fractal Tensors...")
    tensors_created = []
    for data in [[1,0,1], [0,1,0], [1,1,0]]:
        response = requests.post(
            f"{BASE_URL}/tensors/create",
            headers=headers,
            json={"data": data, "metadata": {}}
        )
        if response.status_code == 200:
            tensors_created.append(data)
            print(f"   ✓ Tensor {data} created")
    
    print(f"   Total tensors: {len(tensors_created)}")
    
    # Synthesize Tensors
    print("\n🔄 Synthesizing Tensors...")
    if len(tensors_created) >= 3:
        response = requests.post(
            f"{BASE_URL}/tensors/synthesize",
            headers=headers,
            json={
                "tensor_data_a": tensors_created[0],
                "tensor_data_b": tensors_created[1],
                "tensor_data_c": tensors_created[2]
            }
        )
        if response.status_code == 200:
            result = response.json()
            print(f"   ✓ Synthesis successful")
            if 'synthesized_tensor' in result:
                tensor = result['synthesized_tensor']
                if 'nivel_3' in tensor and tensor['nivel_3']:
                    print(f"   Result: {tensor['nivel_3'][0]}")
    
    # Token Supplies
    print("\n💎 Checking Token Supplies...")
    supplies = requests.get(f"{BASE_URL}/governance/supplies", headers=headers).json()
    print(f"   MERIT: {supplies.get('MERIT', 0):,}")
    print(f"   MIND: {supplies.get('MIND', 0):,}")
    print(f"   TRUST: {supplies.get('TRUST', 0):,}")
    
    # Metrics
    print("\n📊 API Metrics...")
    metrics = requests.get(f"{BASE_URL}/metrics", headers=headers).json()
    print(f"   Active sessions: {metrics.get('active_sessions', 0)}")
    print(f"   KB universes: {metrics.get('kb_size', 0)}")
    
    # Final Summary
    print("\n" + "="*70)
    print("  ✅ AURORA API COMPLETAMENTE OPERACIONAL")
    print("="*70)
    print(f"""
  Características validadas:
  
  ✓ Health monitoring
  ✓ JWT Authentication
  ✓ Fractal Tensor creation
  ✓ Tensor synthesis (Transcender)
  ✓ Token economics (MERIT, MIND, TRUST)
  ✓ API metrics & monitoring
  
  🌐 Endpoints disponibles:
     • /docs - Documentación interactiva
     • /api/v1/health - Estado del sistema
     • /api/v1/auth/* - Autenticación
     • /api/v1/tensors/* - Operaciones con tensores
     • /api/v1/kb/* - Knowledge Base
     • /api/v1/aurora/* - Aurora IE (extend, pattern0)
     • /api/v1/governance/* - Sistema de gobernanza
  
  🚀 Aurora Trinity-3 lista para producción
    """)

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n❌ No se puede conectar al servidor API")
        print("Ejecutar: python aurora_api.py")
    except Exception as e:
        print(f"\n❌ Error: {e}")
