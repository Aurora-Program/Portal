"""
🌌 TEST RÁPIDO DE LA API AURORA
================================

Test simplificado para verificar que la API está operacional.
"""

import requests
import json

BASE_URL = "http://localhost:8080"

print("🌌 AURORA API - Quick Test")
print("=" * 60)

# Test 1: Registro de usuario
print("\n📌 Test 1: User Registration")
try:
    response = requests.post(f"{BASE_URL}/auth/register", json={
        "public_key": "test_user_quick",
        "peer_signature": "sig_123",
        "peer_id": "peer_001"
    })
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        token = data.get('token')
        print(f"✅ Registered! Token: {token[:20]}...")
        
        # Test 2: Aprendizaje
        print("\n📌 Test 2: Learn Patterns")
        response = requests.post(
            f"{BASE_URL}/ie/learn",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "patterns": [[1, 0, 1], [0, 1, 0], [1, 1, 0]],
                "space_id": "quick_test"
            }
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"✅ Learning successful: {response.json()}")
            
            # Test 3: Query
            print("\n📌 Test 3: Query Pattern")
            response = requests.post(
                f"{BASE_URL}/ie/query",
                headers={"Authorization": f"Bearer {token}"},
                json={
                    "pattern": [1, None, None],
                    "space_id": "quick_test"
                }
            )
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Query successful!")
                print(f"   Pattern: [1, None, None]")
                print(f"   Result: {result.get('result', 'N/A')}")
                
                # Test 4: KB Status
                print("\n📌 Test 4: Knowledge Base Status")
                response = requests.get(
                    f"{BASE_URL}/ie/kb/status",
                    headers={"Authorization": f"Bearer {token}"}
                )
                print(f"Status: {response.status_code}")
                if response.status_code == 200:
                    kb_status = response.json()
                    print(f"✅ KB Status retrieved:")
                    print(f"   Universes: {kb_status.get('total_universes', 0)}")
                    print(f"   Archetypes: {kb_status.get('total_archetypes', 0)}")
                    
                    # Test 5: Economics Balance
                    print("\n📌 Test 5: Economics Balance")
                    response = requests.get(
                        f"{BASE_URL}/economics/balance",
                        headers={"Authorization": f"Bearer {token}"}
                    )
                    print(f"Status: {response.status_code}")
                    if response.status_code == 200:
                        balance = response.json()
                        print(f"✅ Balance retrieved:")
                        print(f"   MERIT: {balance.get('MERIT', 0)}")
                        print(f"   MIND: {balance.get('MIND', 0)}")
                        print(f"   TRUST: {balance.get('TRUST', 0)}")
                        
                        print("\n" + "=" * 60)
                        print("✅ ALL TESTS PASSED!")
                        print("🌌 Aurora API is fully operational")
                        print(f"📡 Docs: http://localhost:8080/docs")
                        print("=" * 60)
                    else:
                        print(f"❌ Economics error: {response.text}")
                else:
                    print(f"❌ KB Status error: {response.text}")
            else:
                print(f"❌ Query error: {response.text}")
        else:
            print(f"❌ Learning error: {response.text}")
    else:
        print(f"❌ Registration failed: {response.text}")

except requests.exceptions.ConnectionError:
    print("❌ ERROR: Cannot connect to API")
    print("Make sure the API is running:")
    print("  python aurora_api.py")
except Exception as e:
    print(f"❌ ERROR: {e}")
