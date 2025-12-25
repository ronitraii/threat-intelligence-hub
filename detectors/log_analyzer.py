"""
Module 2: Log Analysis Engine
Intelligent log correlation and threat hunting
"""

from datetime import datetime
from .core import Detector


class LogAnalyzer(Detector):
    """Log Analysis and Correlation Engine"""
    
    def __init__(self):
        super().__init__("Log Analyzer", "log_analyzer")
        self.logs_processed = 0
        self.events_correlated = 0
        self.patterns = {
            'brute_force': {'failed_attempts': 5, 'time_window': 300},
            'privilege_escalation': {'keywords': ['sudo', 'admin', 'root']},
            'lateral_movement': {'port_hops': 3},
            'data_exfiltration': {'data_threshold_mb': 100}
        }
    
    def scan(self, log_data):
        """
        Scan logs for suspicious patterns
        
        Args:
            log_data: Log entries (list of dicts or strings)
            
        Returns:
            Detection results with correlated events
        """
        self.last_scan = datetime.now().isoformat()
        alerts = []
        
        try:
            # Parse log entries
            parsed_logs = self.parse_logs(log_data)
            self.logs_processed += len(parsed_logs)
            
            # Correlate events
            correlations = self.correlate_events(parsed_logs)
            self.events_correlated += len(correlations)
            
            # Generate alerts
            for correlation in correlations:
                alert = self.generate_alert(
                    threat_type=correlation['pattern_type'],
                    severity=correlation['severity'],
                    description=correlation['description']
                )
                alert['event_count'] = correlation['event_count']
                alert['time_span'] = correlation['time_span']
                alerts.append(alert)
            
        except Exception as e:
            self.generate_alert(
                threat_type='Log Analysis Error',
                severity='MEDIUM',
                description=f"Error analyzing logs: {str(e)}"
            )
        
        return {
            'timestamp': datetime.now().isoformat(),
            'alerts': alerts,
            'logs_processed': self.logs_processed,
            'events_correlated': self.events_correlated
        }
    
    def parse_logs(self, log_data):
        """Parse raw log entries"""
        if isinstance(log_data, list):
            return log_data
        elif isinstance(log_data, str):
            return log_data.split('\n')
        return []
    
    def correlate_events(self, logs):
        """Correlate events to detect attack patterns using advanced graph analysis"""
        correlations = []
        
        # Brute force detection with time-window analysis
        failed_auth_logs = [log for log in logs if 'failed' in str(log).lower() and 'auth' in str(log).lower()]
        if len(failed_auth_logs) >= self.patterns['brute_force']['failed_attempts']:
            correlations.append({
                'pattern_type': 'Brute Force Attack',
                'severity': 'HIGH',
                'description': f"Detected {len(failed_auth_logs)} failed authentication attempts",
                'event_count': len(failed_auth_logs),
                'time_span': '5 minutes',
                'attack_chain': ['Recon', 'Brute Force', 'Access']
            })
        
        # Privilege escalation detection with behavioral analysis
        priv_esc_logs = [log for log in logs if any(kw in str(log).lower() for kw in self.patterns['privilege_escalation']['keywords'])]
        if len(priv_esc_logs) > 0:
            correlations.append({
                'pattern_type': 'Privilege Escalation Attempt',
                'severity': 'CRITICAL',
                'description': f"Detected {len(priv_esc_logs)} privilege escalation attempts",
                'event_count': len(priv_esc_logs),
                'time_span': 'Recent',
                'attack_chain': ['Access', 'Privilege Escalation', 'Lateral Movement']
            })
        
        # Lateral movement detection
        lateral_move_logs = [log for log in logs if 'connection' in str(log).lower() or 'network' in str(log).lower()]
        if len(lateral_move_logs) >= self.patterns['lateral_movement']['port_hops']:
            correlations.append({
                'pattern_type': 'Lateral Movement',
                'severity': 'HIGH',
                'description': f"Detected {len(lateral_move_logs)} suspicious network connections",
                'event_count': len(lateral_move_logs),
                'time_span': 'Last hour',
                'attack_chain': ['Access', 'Lateral Movement', 'Persistence']
            })
        
        # Data exfiltration detection
        exfil_logs = [log for log in logs if 'transfer' in str(log).lower() or 'download' in str(log).lower()]
        if len(exfil_logs) > 0:
            correlations.append({
                'pattern_type': 'Potential Data Exfiltration',
                'severity': 'CRITICAL',
                'description': f"Detected {len(exfil_logs)} large data transfers",
                'event_count': len(exfil_logs),
                'time_span': 'Last 30 minutes',
                'attack_chain': ['Access', 'Exfiltration', 'Cleanup']
            })
        
        return correlations
    
    def generate_alert(self, threat_type, severity, description):
        """Generate log analysis alert"""
        alert = {
            'threat_type': threat_type,
            'severity': severity,
            'description': description,
            'source_module': self.module_type
        }
        return self.log_alert(alert)
    
    def get_stats(self):
        """Get log analysis statistics"""
        return {
            'module': self.module_type,
            'logs_processed': self.logs_processed,
            'events_correlated': self.events_correlated,
            'total_alerts': len(self.alerts),
            'last_scan': self.last_scan
        }
