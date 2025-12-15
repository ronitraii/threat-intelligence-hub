"""
Test suite for Network IDS module
"""

import unittest
from detectors.network_ids import NetworkIDS


class TestNetworkIDS(unittest.TestCase):
    """Test cases for Network Intrusion Detection System"""
    
    def setUp(self):
        """Initialize IDS for each test"""
        self.ids = NetworkIDS()
    
    def test_initialization(self):
        """Test IDS initialization"""
        self.assertEqual(self.ids.name, "Network IDS")
        self.assertEqual(self.ids.module_type, "network_ids")
        self.assertEqual(self.ids.detection_threshold, 0.7)
    
    def test_feature_extraction(self):
        """Test feature extraction from network data"""
        network_data = {
            'packet_rate': 100,
            'byte_rate': 5000,
            'flow_duration': 60,
            'unique_ports': 5,
            'protocol_variety': 3
        }
        features = self.ids.extract_features(network_data)
        self.assertEqual(len(features), 5)
    
    def test_severity_calculation(self):
        """Test severity level calculation"""
        self.assertEqual(self.ids.calculate_severity(0.95), 'CRITICAL')
        self.assertEqual(self.ids.calculate_severity(0.8), 'HIGH')
        self.assertEqual(self.ids.calculate_severity(0.65), 'MEDIUM')
        self.assertEqual(self.ids.calculate_severity(0.5), 'LOW')
    
    def test_scan_operation(self):
        """Test basic scan operation"""
        result = self.ids.scan({'packet_rate': 100})
        self.assertIn('timestamp', result)
        self.assertIn('alerts', result)
        self.assertIn('stats', result)


if __name__ == '__main__':
    unittest.main()
