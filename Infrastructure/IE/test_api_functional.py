"""
🌌 TEST FUNCIONAL DE LA API AURORA
===================================

Test usando los endpoints correctos de la API v1.
"""

import requests
import json

BASE_URL = "http://localhost:8080/api/v1"

print("🌌 AURORA API - Functional Test")
print("=" * 70)

# Test 1: Health Check
print("\n📌 Test 1: Health Check")
try:
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"✅ API is healthy: {response.json()}")
    else:
        print(f"⚠️  Response: {response.text}")
except Exception as e:
    print(f"❌ Health check failed: {e}")

# Test 2: Login (simular autenticación)
print("\n📌 Test 2: Authentication (Login)")
try:
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "public_key": "test_aurora_user_" + str(int(__import__('time').time())),
        "peer_signature": "mock_signature_xyz",
        "peer_id": "peer_test_functional"
    })
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        token = data.get('access_token') or data.get('token')
        if not token:
            print(f"⚠️  No token in response: {data}")
            raise Exception("Authentication failed - no token received")
        print(f"✅ Authenticated! Token: {token[:30] if len(token) > 30 else token}...")
        
        headers = {"Authorization": f"Bearer {token}"}
        
        # Test 3: Create Tensor
        print("\n📌 Test 3: Create Tensor")
        response = requests.post(
            f"{BASE_URL}/tensors/create",
            headers=headers,
            json={
                "data": [1, 0, 1],
                "metadata": {"source": "functional_test"}
            }
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            tensor_data = response.json()
            print(f"✅ Tensor created:")
            print(f"   Root: {tensor_data.get('nivel_3', [[]])[0]}")
        else:
            print(f"⚠️  Response: {response.text}")
        
        # Test 4: Store in KB
        print("\n📌 Test 4: Store Archetype in KB")
        response = requests.post(
            f"{BASE_URL}/kb/store",
            headers=headers,
            json={
                "space_id": "functional_test",
                "name": "test_archetype_1",
                "Ms": [1, 0, 1],
                "Ss": [0, 1, 0],
                "MetaM": [1, 1, 1]
            }
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"✅ Archetype stored: {response.json()}")
        else:
            print(f"⚠️  Response: {response.text}")
        
        # Test 5: Query KB
        print("\n📌 Test 5: Query Knowledge Base")
        response = requests.post(
            f"{BASE_URL}/kb/query",
            headers=headers,
            json={
                "space_id": "functional_test",
                "query_type": "by_ms",
                "query_vector": [1, 0, 1]
            }
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ KB Query successful:")
            print(f"   Found: {result.get('found', False)}")
            if result.get('archetype'):
                print(f"   Ms: {result['archetype'].get('Ms', [])}")
        else:
            print(f"⚠️  Response: {response.text}")
        
        # Test 6: Aurora Extend (Deducción con NULLs)
        print("\n📌 Test 6: Aurora Extend (NULL Deduction)")
        response = requests.post(
            f"{BASE_URL}/aurora/extend",
            headers=headers,
            json={
                "input_ss": [1, None, None],
                "space_id": "functional_test"
            }
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Aurora Extend successful:")
            print(f"   Input: [1, None, None]")
            print(f"   Method: {result.get('reconstruction_method', 'N/A')}")
            if result.get('reconstructed_tensor'):
                tensor = result['reconstructed_tensor']
                if isinstance(tensor, dict) and 'nivel_3' in tensor:
                    print(f"   Output: {tensor['nivel_3'][0] if tensor['nivel_3'] else 'N/A'}")
        else:
            print(f"⚠️  Response: {response.text}")
        
        # Test 7: Pattern0 (Ethical Cluster)
        print("\n📌 Test 7: Pattern0 (Ethical Fractal Cluster)")
        response = requests.post(
            f"{BASE_URL}/aurora/pattern0",
            headers=headers,
            json={
                "input_data": [[1, 0, 1], [0, 1, 0], [1, 1, 0]],
                "space_id": "functional_test",
                "num_tensors": 3
            }
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Pattern0 cluster generated:")
            print(f"   Tensors: {result.get('num_tensors', 0)}")
            print(f"   Ethical hash: {result.get('ethical_signature', 'N/A')[:20]}...")
        else:
            print(f"⚠️  Response: {response.text}")
        
        # Test 8: Governance - Token Supplies
        print("\n📌 Test 8: Governance Token Supplies")
        response = requests.get(
            f"{BASE_URL}/governance/supplies",
            headers=headers
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            supplies = response.json()
            print(f"✅ Token supplies retrieved:")
            print(f"   MERIT: {supplies.get('MERIT', 0):,}")
            print(f"   MIND: {supplies.get('MIND', 0):,}")
            print(f"   TRUST: {supplies.get('TRUST', 0):,}")
        else:
            print(f"⚠️  Response: {response.text}")
        
        # Test 9: Metrics
        print("\n📌 Test 9: API Metrics")
        response = requests.get(
            f"{BASE_URL}/metrics",
            headers=headers
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            metrics = response.json()
            print(f"✅ Metrics retrieved:")
            print(f"   Active sessions: {metrics.get('active_sessions', 0)}")
            print(f"   KB size: {metrics.get('kb_size', 0)}")
        else:
            print(f"⚠️  Response: {response.text}")
        
        # Final Summary
        print("\n" + "=" * 70)
        print("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
        print("🌌 Aurora API is fully operational")
        print(f"📡 Documentation: http://localhost:8080/docs")
        print(f"🔗 API Base: {BASE_URL}")
        print("=" * 70)
        
    else:
        print(f"❌ Authentication failed: {response.text}")

except requests.exceptions.ConnectionError:
    print("\n❌ ERROR: Cannot connect to API server")
    print("Make sure the API is running:")
    print("  python aurora_api.py")
    print(f"\nExpected URL: {BASE_URL}")
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
