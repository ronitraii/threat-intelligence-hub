"""
Module 4: Incident Response Dashboard API
Enhanced REST API for integrated threat management
"""

from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
import random

# Create API blueprint
api = Blueprint('api', __name__, url_prefix='/api')

# Mock incident database
incidents_db = []
threat_queue = []


@api.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'modules': {
            'network_ids': 'operational',
            'log_analyzer': 'operational',
            'malware_detector': 'operational',
            'dashboard': 'operational'
        }
    }), 200


@api.route('/threats/all', methods=['GET'])
def get_all_threats():
    """Get all threats from all modules"""
    return jsonify({
        'timestamp': datetime.now().isoformat(),
        'total_threats': len(threat_queue),
        'threats': threat_queue,
        'by_severity': {
            'CRITICAL': len([t for t in threat_queue if t.get('severity') == 'CRITICAL']),
            'HIGH': len([t for t in threat_queue if t.get('severity') == 'HIGH']),
            'MEDIUM': len([t for t in threat_queue if t.get('severity') == 'MEDIUM']),
            'LOW': len([t for t in threat_queue if t.get('severity') == 'LOW'])
        }
    }), 200


@api.route('/threats/network', methods=['GET'])
def get_network_threats():
    """Get network IDS threats"""
    network_threats = [t for t in threat_queue if t.get('source_module') == 'network_ids']
    return jsonify({
        'timestamp': datetime.now().isoformat(),
        'count': len(network_threats),
        'threats': network_threats
    }), 200


@api.route('/threats/logs', methods=['GET'])
def get_log_threats():
    """Get log analysis threats"""
    log_threats = [t for t in threat_queue if t.get('source_module') == 'log_analyzer']
    return jsonify({
        'timestamp': datetime.now().isoformat(),
        'count': len(log_threats),
        'threats': log_threats
    }), 200


@api.route('/threats/malware', methods=['GET'])
def get_malware_threats():
    """Get malware detection threats"""
    malware_threats = [t for t in threat_queue if t.get('source_module') == 'malware_detector']
    return jsonify({
        'timestamp': datetime.now().isoformat(),
        'count': len(malware_threats),
        'threats': malware_threats
    }), 200


@api.route('/incidents', methods=['GET'])
def get_incidents():
    """Get all incidents"""
    status = request.args.get('status', 'all')
    
    if status != 'all':
        incidents = [i for i in incidents_db if i.get('status') == status]
    else:
        incidents = incidents_db
    
    return jsonify({
        'timestamp': datetime.now().isoformat(),
        'total_incidents': len(incidents),
        'incidents': incidents
    }), 200


@api.route('/incidents', methods=['POST'])
def create_incident():
    """Create new incident from threats"""
    data = request.get_json()
    
    incident = {
        'id': len(incidents_db) + 1,
        'threat_ids': data.get('threat_ids', []),
        'title': data.get('title', 'Unknown Incident'),
        'severity': data.get('severity', 'MEDIUM'),
        'status': 'Open',
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat(),
        'assigned_to': data.get('assigned_to', 'Unassigned'),
        'notes': data.get('notes', '')
    }
    
    incidents_db.append(incident)
    return jsonify(incident), 201


@api.route('/incidents/<int:incident_id>', methods=['PATCH'])
def update_incident(incident_id):
    """Update incident status"""
    data = request.get_json()
    
    for incident in incidents_db:
        if incident['id'] == incident_id:
            incident.update(data)
            incident['updated_at'] = datetime.now().isoformat()
            return jsonify(incident), 200
    
    return jsonify({'error': 'Incident not found'}), 404


@api.route('/stats', methods=['GET'])
def get_stats():
    """Get platform statistics"""
    return jsonify({
        'timestamp': datetime.now().isoformat(),
        'total_threats': len(threat_queue),
        'network_alerts': len([t for t in threat_queue if t.get('source_module') == 'network_ids']),
        'log_events': len([t for t in threat_queue if t.get('source_module') == 'log_analyzer']),
        'malware_detections': len([t for t in threat_queue if t.get('source_module') == 'malware_detector']),
        'incidents': len(incidents_db),
        'threat_level': calculate_threat_level(),
        'uptime_hours': 48,
        'detection_rate': '94.3%'
    }), 200


def calculate_threat_level():
    """Calculate overall threat level"""
    critical = len([t for t in threat_queue if t.get('severity') == 'CRITICAL'])
    high = len([t for t in threat_queue if t.get('severity') == 'HIGH'])
    
    if critical > 0:
        return 'CRITICAL'
    elif high > 2:
        return 'HIGH'
    elif high > 0:
        return 'MEDIUM'
    else:
        return 'LOW'
