"""
Threat Intelligence Hub - Main Application
Integrated threat detection platform
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from web_ui.api import api
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)
app.register_blueprint(api)

# Global state for threat data
threat_data = {
    'network_alerts': [],
    'log_events': [],
    'malware_detections': [],
    'incidents': []
}


@app.route('/')
def index():
    """Main dashboard"""
    return render_template('dashboard.html')


@app.route('/api/health')
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
    })


@app.route('/api/threats', methods=['GET'])
def get_threats():
    """Get all detected threats"""
    threat_type = request.args.get('type', 'all')
    
    response = {
        'timestamp': datetime.now().isoformat(),
        'total_threats': len(threat_data['network_alerts']) + 
                        len(threat_data['log_events']) + 
                        len(threat_data['malware_detections'])
    }
    
    if threat_type == 'all':
        response['network_alerts'] = threat_data['network_alerts']
        response['log_events'] = threat_data['log_events']
        response['malware_detections'] = threat_data['malware_detections']
    elif threat_type == 'network':
        response['data'] = threat_data['network_alerts']
    elif threat_type == 'logs':
        response['data'] = threat_data['log_events']
    elif threat_type == 'malware':
        response['data'] = threat_data['malware_detections']
    
    return jsonify(response)


@app.route('/api/incidents', methods=['GET'])
def get_incidents():
    """Get incident response data"""
    return jsonify({
        'timestamp': datetime.now().isoformat(),
        'incidents': threat_data['incidents'],
        'total_incidents': len(threat_data['incidents'])
    })


@app.route('/api/scan/network', methods=['POST'])
def scan_network():
    """Trigger network IDS scan"""
    logger.info("Network IDS scan triggered")
    # TODO: Implement network scanning logic
    return jsonify({
        'status': 'scan_started',
        'module': 'network_ids',
        'timestamp': datetime.now().isoformat()
    }), 202


@app.route('/api/scan/logs', methods=['POST'])
def scan_logs():
    """Trigger log analysis"""
    logger.info("Log analysis scan triggered")
    # TODO: Implement log analysis logic
    return jsonify({
        'status': 'scan_started',
        'module': 'log_analyzer',
        'timestamp': datetime.now().isoformat()
    }), 202


@app.route('/api/scan/malware', methods=['POST'])
def scan_malware():
    """Trigger malware detection"""
    logger.info("Malware detection scan triggered")
    # TODO: Implement malware detection logic
    return jsonify({
        'status': 'scan_started',
        'module': 'malware_detector',
        'timestamp': datetime.now().isoformat()
    }), 202


@app.route('/api/stats')
def get_stats():
    """Get platform statistics"""
    return jsonify({
        'timestamp': datetime.now().isoformat(),
        'network_alerts': len(threat_data['network_alerts']),
        'log_events': len(threat_data['log_events']),
        'malware_detections': len(threat_data['malware_detections']),
        'incidents': len(threat_data['incidents']),
        'threat_level': calculate_threat_level()
    })


def calculate_threat_level():
    """Calculate overall threat level"""
    total_threats = (len(threat_data['network_alerts']) + 
                    len(threat_data['log_events']) + 
                    len(threat_data['malware_detections']))
    
    if total_threats == 0:
        return 'LOW'
    elif total_threats < 5:
        return 'MEDIUM'
    else:
        return 'HIGH'


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {error}")
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    logger.info("Starting Threat Intelligence Hub")
    app.run(debug=True, host='0.0.0.0', port=5000)
