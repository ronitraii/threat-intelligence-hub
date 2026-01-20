# Configuration and Hardening Guide

## Configuration File Example

### config.yaml
```yaml
# Network IDS Configuration
network_ids:
  detection_threshold: 0.7
  models:
    isolation_forest:
      n_estimators: 100
      contamination: 0.1
      weight: 0.6
    autoencoder:
      input_dim: 5
      hidden_dims: [64, 32, 16]
      weight: 0.4
    xgboost:
      max_depth: 6
      learning_rate: 0.1
      weight: 0.0  # Can be enabled
  packet_capture:
    interface: "eth0"
    filter: "tcp port 22 or tcp port 443"

# Log Analysis Configuration
log_analyzer:
  sources:
    - type: "syslog"
      host: "syslog.example.com"
      port: 514
    - type: "file"
      path: "/var/log/auth.log"
    - type: "windows_event"
      host: "dc.example.com"
  patterns:
    brute_force_threshold: 5
    time_window: 300  # seconds
    privilege_escalation_keywords:
      - "sudo"
      - "admin"
      - "root"
      - "system"

# Malware Detection Configuration
malware_detector:
  scan_paths:
    - "C:\\Users"
    - "C:\\Windows\\Temp"
    - "/tmp"
    - "/home"
  features:
    static_weight: 0.6
    dynamic_weight: 0.4
    threshold: 0.7
  sandbox:
    timeout: 60  # seconds
    memory_limit: 2048  # MB
    api_call_monitoring: true

# Dashboard Configuration
dashboard:
  host: "0.0.0.0"
  port: 5000
  debug: false
  log_level: "INFO"
  max_connections: 500
  alert_retention: 7  # days
  incident_retention: 30  # days

# Security Configuration
security:
  ssl_enabled: true
  ssl_cert: "/etc/ssl/certs/server.crt"
  ssl_key: "/etc/ssl/private/server.key"
  auth_type: "oauth2"
  rate_limit: 1000  # requests per minute
  cors_origins:
    - "https://soc.example.com"
    - "https://dashboard.example.com"
```

## API Security Hardening

### Authentication Setup
```python
from flask_oauth import OAuth

oauth = OAuth()
oauth.init_app(app)

@app.before_request
def require_oauth():
    if request.path.startswith('/api/'):
        token = request.headers.get('Authorization')
        # Validate token
        ...
```

### CORS Configuration
```python
from flask_cors import CORS

CORS(app, 
     resources={
         r"/api/*": {
             "origins": ["https://soc.example.com"],
             "methods": ["GET", "POST", "PATCH"],
             "allow_headers": ["Authorization", "Content-Type"],
             "max_age": 3600
         }
     })
```

### Rate Limiting
```python
from flask_limiter import Limiter

limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route('/api/threats')
@limiter.limit("100 per minute")
def get_threats():
    ...
```

## Database Security

### PostgreSQL Hardening
```sql
-- Create dedicated database user
CREATE ROLE threat_hub_user WITH PASSWORD 'strong_password_here';

-- Grant minimal permissions
GRANT CONNECT ON DATABASE threat_hub TO threat_hub_user;
GRANT USAGE ON SCHEMA public TO threat_hub_user;
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO threat_hub_user;

-- Enable SSL
ALTER SYSTEM SET ssl = on;
ALTER SYSTEM SET ssl_cert_file = '/etc/ssl/certs/server.crt';
ALTER SYSTEM SET ssl_key_file = '/etc/ssl/private/server.key';
```

## Network Security

### Firewall Rules (UFW)
```bash
# Allow SSH
sudo ufw allow 22/tcp

# Allow HTTPS for Dashboard
sudo ufw allow 443/tcp

# Allow internal API (restricted)
sudo ufw allow from 10.0.0.0/8 to any port 5000

# Deny all other traffic
sudo ufw default deny incoming
sudo ufw default allow outgoing
```

### Network Segmentation
```
DMZ:
  - Incident Response Dashboard (exposed)
  - Load Balancer

Internal Network:
  - Network IDS engines
  - Log analysis servers
  - Malware detection sandbox
  - Database servers
  - Message queue (Kafka)

Management Network:
  - Admin console
  - Monitoring tools
  - Backup systems
```

## Monitoring and Alerting

### Prometheus Metrics
```python
from prometheus_client import Counter, Histogram, Gauge

threat_counter = Counter('threats_detected_total', 'Total threats detected', ['severity', 'module'])
processing_time = Histogram('processing_seconds', 'Processing time', ['module'])
active_incidents = Gauge('active_incidents', 'Number of active incidents')
```

### Logging Configuration
```python
import logging
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler('app.log', maxBytes=10485760, backupCount=10)
formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
handler.setFormatter(formatter)
app.logger.addHandler(handler)
```

## Backup and Disaster Recovery

### Daily Backup Script
```bash
#!/bin/bash
BACKUP_DIR="/backups/threat-hub"
DATE=$(date +%Y-%m-%d)

# Backup database
pg_dump threat_hub | gzip > $BACKUP_DIR/db_$DATE.sql.gz

# Backup configurations
tar -czf $BACKUP_DIR/config_$DATE.tar.gz /etc/threat-hub/

# Backup models
tar -czf $BACKUP_DIR/models_$DATE.tar.gz /opt/threat-hub/models/

# Sync to S3
aws s3 sync $BACKUP_DIR s3://threat-hub-backups/
```

### Disaster Recovery Plan
- RTO: Recovery Time Objective = 4 hours
- RPO: Recovery Point Objective = 1 hour
- Secondary site with hot standby
- Automated failover configuration
