"""
Core detector base class
"""

from abc import ABC, abstractmethod
from datetime import datetime


class Detector(ABC):
    """Base class for all threat detectors"""
    
    def __init__(self, name, module_type):
        self.name = name
        self.module_type = module_type
        self.alerts = []
        self.last_scan = None
    
    @abstractmethod
    def scan(self, data):
        """Perform threat scan on input data"""
        pass
    
    @abstractmethod
    def generate_alert(self, threat_type, severity, description):
        """Generate threat alert"""
        pass
    
    def log_alert(self, alert):
        """Log alert to internal storage"""
        alert['timestamp'] = datetime.now().isoformat()
        alert['module'] = self.module_type
        self.alerts.append(alert)
        return alert
    
    def get_alerts(self):
        """Get all alerts"""
        return self.alerts
    
    def clear_alerts(self):
        """Clear alert history"""
        self.alerts = []
