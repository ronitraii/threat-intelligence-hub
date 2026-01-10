# Deployment and Operations Guide

## Prerequisites
- Python 3.11+
- 4GB RAM minimum
- 1GB disk space for models and data
- Network access for threat intelligence feeds

## Production Deployment

### Step 1: Environment Setup
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Model Training (Optional)
```bash
python scripts/train_models.py --dataset UNSW-NB15
```

### Step 3: Start Service
```bash
python app.py --host 0.0.0.0 --port 5000
```

### Step 4: Configure Inputs
- Network IDS: Configure packet capture or flow data source
- Log Analyzer: Add log file paths or syslog endpoints
- Malware Detector: Set file monitoring directories
- Dashboard: Access at http://localhost:5000

## Monitoring and Alerts

### Health Checks
```bash
curl http://localhost:5000/api/health
```

### Threat Monitoring
```bash
# Real-time threats
curl http://localhost:5000/api/threats/all

# By module
curl http://localhost:5000/api/threats/network
curl http://localhost:5000/api/threats/logs
curl http://localhost:5000/api/threats/malware
```

### Statistics
```bash
curl http://localhost:5000/api/stats
```

## Incident Response Workflow

1. **Detection** → Module detects threat
2. **Alert** → Dashboard shows threat
3. **Investigation** → Review threat details
4. **Correlation** → Link related threats
5. **Escalation** → Create incident
6. **Response** → Execute response playbooks
7. **Resolution** → Close incident
8. **Documentation** → Record findings

## Scalability Considerations

- Horizontal scaling: Deploy multiple dashboard instances
- Load balancing: Use nginx/haproxy for distribution
- Database: Migrate to PostgreSQL for persistence
- Caching: Implement Redis for performance
- Message Queue: Use Kafka for event streaming
- Container: Docker/Kubernetes for orchestration

## Security Hardening

- ✅ Input validation on all API endpoints
- ✅ Rate limiting on HTTP endpoints
- ✅ SSL/TLS encryption for API communication
- ✅ Authentication: Implement OAuth 2.0
- ✅ Authorization: Role-based access control (RBAC)
- ✅ Audit logging for all operations
- ✅ Data encryption at rest and in transit
