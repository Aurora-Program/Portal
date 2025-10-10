"""
🐹 Aurora P2P Client - Tests

Tests básicos para el cliente P2P (sin necesidad de servidor real).

Author: Aurora Alliance
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from aurora_p2p_client import AuroraP2PClient, PeerInfo


class TestPeerInfo(unittest.TestCase):
    """Tests para la clase PeerInfo"""
    
    def test_peer_info_creation(self):
        """Test creación básica de PeerInfo"""
        peer = PeerInfo(
            peer_id="test-peer-123",
            address="192.168.1.100",
            port=9000,
            archetypes=['pepino', 'ethics'],
            last_seen="2025-10-02T12:00:00"
        )
        
        self.assertEqual(peer.peer_id, "test-peer-123")
        self.assertEqual(peer.address, "192.168.1.100")
        self.assertEqual(peer.port, 9000)
        self.assertIn('pepino', peer.archetypes)
    
    def test_peer_info_to_dict(self):
        """Test conversión a diccionario"""
        peer = PeerInfo(
            peer_id="test-123",
            address="10.0.0.1",
            port=8000,
            archetypes=['test'],
            last_seen="2025-10-02T12:00:00"
        )
        
        data = peer.to_dict()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['peer_id'], "test-123")
        self.assertEqual(data['port'], 8000)
    
    def test_peer_info_from_dict(self):
        """Test creación desde diccionario"""
        data = {
            'peer_id': 'peer-456',
            'address': '172.16.0.1',
            'port': 7000,
            'archetypes': ['pepino'],
            'last_seen': '2025-10-02T12:00:00',
            'metadata': {'version': '1.0'}
        }
        
        peer = PeerInfo.from_dict(data)
        self.assertEqual(peer.peer_id, 'peer-456')
        self.assertIn('pepino', peer.archetypes)
        self.assertEqual(peer.metadata['version'], '1.0')


class TestAuroraP2PClient(unittest.TestCase):
    """Tests para el cliente P2P"""
    
    @patch('aurora_p2p_client.requests.post')
    def test_register(self, mock_post):
        """Test registro de peer"""
        # Mock response
        mock_response = Mock()
        mock_response.json.return_value = {
            'message': 'Peer registered',
            'peer_id': 'test-123',
            'ttl_expires': '2025-10-02T12:05:00'
        }
        mock_post.return_value = mock_response
        
        # Crear cliente sin auto-registro
        client = AuroraP2PClient(
            discovery_url="http://test.local",
            archetypes=['test'],
            auto_register=False
        )
        
        # Registrar
        result = client.register()
        
        # Verificar
        self.assertEqual(result['message'], 'Peer registered')
        mock_post.assert_called_once()
    
    @patch('aurora_p2p_client.requests.get')
    def test_discover(self, mock_get):
        """Test descubrimiento de peers"""
        # Mock response
        mock_response = Mock()
        mock_response.json.return_value = {
            'peers': [
                {
                    'peer_id': 'peer-1',
                    'address': '192.168.1.100',
                    'port': 9000,
                    'archetypes': ['pepino'],
                    'last_seen': '2025-10-02T12:00:00'
                },
                {
                    'peer_id': 'peer-2',
                    'address': '192.168.1.101',
                    'port': 9001,
                    'archetypes': ['ethics'],
                    'last_seen': '2025-10-02T12:00:00'
                }
            ],
            'count': 2
        }
        mock_get.return_value = mock_response
        
        # Crear cliente
        client = AuroraP2PClient(
            discovery_url="http://test.local",
            auto_register=False
        )
        
        # Descubrir
        peers = client.discover()
        
        # Verificar
        self.assertEqual(len(peers), 2)
        self.assertIsInstance(peers[0], PeerInfo)
        self.assertEqual(peers[0].peer_id, 'peer-1')
    
    @patch('aurora_p2p_client.requests.post')
    def test_heartbeat(self, mock_post):
        """Test envío de heartbeat"""
        mock_response = Mock()
        mock_response.json.return_value = {'message': 'Heartbeat updated'}
        mock_post.return_value = mock_response
        
        client = AuroraP2PClient(
            discovery_url="http://test.local",
            auto_register=False
        )
        
        result = client.heartbeat()
        
        self.assertTrue(result)
        mock_post.assert_called()
    
    @patch('aurora_p2p_client.requests.get')
    def test_health_check(self, mock_get):
        """Test health check del servidor"""
        mock_response = Mock()
        mock_response.json.return_value = {'status': 'healthy'}
        mock_get.return_value = mock_response
        
        client = AuroraP2PClient(
            discovery_url="http://test.local",
            auto_register=False
        )
        
        health = client.health_check()
        
        self.assertEqual(health['status'], 'healthy')
    
    def test_callbacks(self):
        """Test sistema de callbacks"""
        client = AuroraP2PClient(
            discovery_url="http://test.local",
            auto_register=False
        )
        
        callback_called = []
        
        def test_callback(peer):
            callback_called.append(peer)
        
        # Registrar callback
        client.on('on_peer_discovered', test_callback)
        
        # Trigger callback manualmente
        test_peer = PeerInfo(
            peer_id='test',
            address='1.2.3.4',
            port=9000,
            archetypes=['test'],
            last_seen='2025-10-02T12:00:00'
        )
        client._trigger_callback('on_peer_discovered', test_peer)
        
        # Verificar
        self.assertEqual(len(callback_called), 1)
        self.assertEqual(callback_called[0].peer_id, 'test')
    
    def test_context_manager(self):
        """Test uso como context manager"""
        with AuroraP2PClient(
            discovery_url="http://test.local",
            auto_register=False
        ) as client:
            self.assertIsNotNone(client.peer_id)
        
        # Verificar que se detuvo
        self.assertFalse(client._running)


def run_tests():
    """Ejecuta todos los tests"""
    print("🐹 Running Aurora P2P Client Tests...\n")
    
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Cargar tests
    suite.addTests(loader.loadTestsFromTestCase(TestPeerInfo))
    suite.addTests(loader.loadTestsFromTestCase(TestAuroraP2PClient))
    
    # Ejecutar
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Resumen
    print("\n" + "="*60)
    if result.wasSuccessful():
        print("✅ ALL TESTS PASSED!")
    else:
        print("❌ SOME TESTS FAILED")
    print("="*60)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
