from flask import Flask, jsonify, request
from flask_cors import CORS
import time
import random

app = Flask(__name__)
# Enable CORS for all domains, crucial for front-end development
CORS(app)

# This is where your actual backend logic will go.
# For this example, we'll use dummy data to simulate the results.

def run_security_scan():
    """Simulates a security scan and returns a list of detected threats."""
    possible_threats = [
        {
            "id": 1,
            "name": "Suspicious Registry Entry",
            "type": "Registry Persistence",
            "severity": "High",
            "icon": "📝",
            "location": "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run",
            "description": "Unauthorized startup entry detected",
            "details": "Detected suspicious registry modification in Windows startup location. This could indicate malware persistence mechanism.",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "selected": False
        },
        {
            "id": 2,
            "name": "Unknown Service Installation",
            "type": "Service Persistence",
            "severity": "Medium",
            "icon": "⚙️",
            "location": "Services.msc",
            "description": "New service with suspicious behavior patterns",
            "details": "A new Windows service was installed with unusual characteristics and network communication patterns.",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "selected": False
        },
        {
            "id": 3,
            "name": "Scheduled Task Anomaly",
            "type": "Task Scheduler",
            "severity": "High",
            "icon": "⏰",
            "location": "Task Scheduler Library",
            "description": "Malicious scheduled task for persistence",
            "details": "Suspicious scheduled task detected that executes PowerShell commands at system startup.",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "selected": False
        },
        {
            "id": 4,
            "name": "Suspicious PowerShell Activity",
            "type": "Command Execution",
            "severity": "Critical",
            "icon": "⚠️",
            "location": "PowerShell.exe",
            "description": "Obfuscated PowerShell commands detected",
            "details": "Detected obfuscated PowerShell commands attempting to download external payloads from suspicious domains.",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "selected": False
        },
        {
            "id": 5,
            "name": "Unauthorized Network Connection",
            "type": "Network Activity",
            "severity": "High",
            "icon": "🌐",
            "location": "Network Interface",
            "description": "Connection to known malicious IP address",
            "details": "Process attempting to connect to known malicious IP address 192.168.1.100 on suspicious port.",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "selected": False
        },
        {
            "id": 6,
            "name": "Process Injection Detected",
            "type": "Code Injection",
            "severity": "Critical",
            "icon": "💉",
            "location": "System Process",
            "description": "Code injection attempt in legitimate process",
            "details": "Code injection attempt detected in legitimate system process, indicating advanced malware techniques.",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "selected": False
        }
    ]
    # Randomly select a few threats to simulate a scan result
    num_threats = random.randint(0, len(possible_threats))
    return random.sample(possible_threats, num_threats)

def mitigate_threats_on_backend(threat_ids):
    """Simulates mitigating threats on the backend."""
    # In a real application, you would implement the logic to remove
    # registry keys, stop services, delete files, etc.
    print(f"Mitigating threats with IDs: {threat_ids}")
    return {"status": "success", "message": f"Successfully mitigated {len(threat_ids)} threats."}

@app.route('/api/scan', methods=['POST'])
def scan_endpoint():
    # Simulate a delay for the scan process
    time.sleep(2)
    threats = run_security_scan()
    return jsonify(threats)

@app.route('/api/mitigate', methods=['POST'])
def mitigate_endpoint():
    try:
        data = request.get_json()
        threat_ids = data.get('threat_ids', [])
        if not threat_ids:
            return jsonify({"status": "error", "message": "No threat IDs provided."}), 400
        
        result = mitigate_threats_on_backend(threat_ids)
        return jsonify(result)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
