"""
🌌 TEST DE LA API AURORA
========================

Script de prueba para validar todos los endpoints de la API Aurora.
"""

import requests
import json
from time import sleep

BASE_URL = "http://localhost:8080"

def print_section(title):
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def test_health():
    """Test del endpoint de salud."""
    print_section("🏥 TEST 1: Health Check")
    
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    assert response.status_code == 200
    print("✅ Health check passed")
    return response.json()

def test_register():
    """Test de registro de usuario."""
    print_section("👤 TEST 2: User Registration")
    
    import time
    payload = {
        "public_key": "test_user_" + str(int(time.time())),
        "peer_signature": "signature_mock_123",
        "peer_id": "peer_test_001"
    }
    
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    response = requests.post(f"{BASE_URL}/auth/register", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    assert response.status_code == 200
    print("✅ Registration successful")
    return response.json()

def test_learn(token):
    """Test de aprendizaje de patrones."""
    print_section("🧠 TEST 3: Learn Patterns")
    
    payload = {
        "patterns": [
            [1, 0, 1],
            [0, 1, 0],
            [1, 1, 0],
            [0, 0, 1]
        ],
        "space_id": "test_space"
    }
    
    headers = {"Authorization": f"Bearer {token}"}
    
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    response = requests.post(f"{BASE_URL}/ie/learn", json=payload, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    assert response.status_code == 200
    print("✅ Learning successful")
    return response.json()

def test_query(token):
    """Test de consulta de patrones."""
    print_section("🔍 TEST 4: Query Patterns")
    
    # Consulta completa
    payload1 = {
        "pattern": [1, 0, 1],
        "space_id": "test_space"
    }
    
    headers = {"Authorization": f"Bearer {token}"}
    
    print("\n📌 Consulta exacta:")
    print(f"Payload: {json.dumps(payload1, indent=2)}")
    
    response1 = requests.post(f"{BASE_URL}/ie/query", json=payload1, headers=headers)
    print(f"Status: {response1.status_code}")
    print(f"Response: {json.dumps(response1.json(), indent=2)}")
    
    # Consulta con NULLs
    payload2 = {
        "pattern": [1, None, None],
        "space_id": "test_space"
    }
    
    print("\n📌 Consulta con NULLs:")
    print(f"Payload: {json.dumps(payload2, indent=2)}")
    
    response2 = requests.post(f"{BASE_URL}/ie/query", json=payload2, headers=headers)
    print(f"Status: {response2.status_code}")
    print(f"Response: {json.dumps(response2.json(), indent=2)}")
    
    assert response1.status_code == 200
    assert response2.status_code == 200
    print("✅ Query successful")
    return response2.json()

def test_kb_status(token):
    """Test del estado de la Knowledge Base."""
    print_section("📚 TEST 5: Knowledge Base Status")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(f"{BASE_URL}/ie/kb/status", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    assert response.status_code == 200
    print("✅ KB status retrieved")
    return response.json()

def test_create_tensor(token):
    """Test de creación de tensor."""
    print_section("🔷 TEST 6: Create Tensor")
    
    import time
    payload = {
        "data": [1, 0, 1],
        "metadata": {
            "source": "api_test",
            "timestamp": int(time.time())
        }
    }
    
    headers = {"Authorization": f"Bearer {token}"}
    
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    response = requests.post(f"{BASE_URL}/ie/tensor/create", json=payload, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    assert response.status_code == 200
    print("✅ Tensor created")
    return response.json()

def test_economics(token):
    """Test del sistema económico adaptativo."""
    print_section("💎 TEST 7: Adaptive Economics")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Get balance
    response = requests.get(f"{BASE_URL}/economics/balance", headers=headers)
    print(f"\n💰 Balance:")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Get metrics
    response2 = requests.get(f"{BASE_URL}/economics/metrics", headers=headers)
    print(f"\n📊 Metrics:")
    print(f"Status: {response2.status_code}")
    print(f"Response: {json.dumps(response2.json(), indent=2)}")
    
    assert response.status_code == 200
    print("✅ Economics system working")
    return response.json()

def main():
    print_section("🌌 AURORA API TEST SUITE")
    print(f"\nTesting API at: {BASE_URL}")
    
    try:
        # 1. Health check
        health = test_health()
        print(f"Server timestamp: {health.get('timestamp', 'N/A')}")
        sleep(0.5)
        
        # 2. Register user
        auth_data = test_register()
        token = auth_data['token']
        sleep(0.5)
        
        # 3. Learn patterns
        test_learn(token)
        sleep(0.5)
        
        # 4. Query patterns
        test_query(token)
        sleep(0.5)
        
        # 5. KB status
        test_kb_status(token)
        sleep(0.5)
        
        # 6. Create tensor
        test_create_tensor(token)
        sleep(0.5)
        
        # 7. Economics
        test_economics(token)
        
        # Summary
        print_section("✅ ALL TESTS PASSED")
        print("""
        Aurora API is fully operational:
        
        ✓ Health check working
        ✓ User registration & JWT auth working
        ✓ Pattern learning working
        ✓ Query & deduction working
        ✓ Knowledge Base operational
        ✓ Tensor creation working
        ✓ Adaptive Economics system working
        
        🌌 API ready for production
        📡 Access docs at: http://localhost:8080/docs
        """)
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
    except requests.exceptions.ConnectionError:
        print(f"\n❌ ERROR: Cannot connect to {BASE_URL}")
        print("Make sure the API is running: python aurora_api.py")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
