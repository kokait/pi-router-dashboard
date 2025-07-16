from flask import Flask, render_template_string
import subprocess
import socket
import os

app = Flask(__name__)

def get_tailscale_status():
    try:
        output = subprocess.check_output(["tailscale", "status"], text=True)
        return "Connected" if "100." in output or "fd7a:" in output else "Disconnected"
    except:
        return "Error"

def get_public_ip():
    try:
        return subprocess.check_output(["curl", "-s", "ifconfig.me"], text=True).strip()
    except:
        return "Unavailable"

@app.route("/")
def dashboard():
    tailscale = get_tailscale_status()
    ip = get_public_ip()
    hostname = socket.gethostname()
    return render_template_string("""
    <h1>🛡️ Pi Router Dashboard</h1>
    <ul>
        <li><strong>Hostname:</strong> {{ hostname }}</li>
        <li><strong>Tailscale:</strong> {{ tailscale }}</li>
        <li><strong>Public IP:</strong> {{ ip }}</li>
    </ul>
    <form method="POST" action="/backup">
        <button type="submit">📦 Manual Backup to GitHub</button>
    </form>
    """, hostname=hostname, tailscale=tailscale, ip=ip)

@app.route("/backup", methods=["POST"])
def manual_backup():
    os.system("cd ~/rpi-router-backup && git add . && git commit -m 'Manual backup' && git push")
    return "✅ Backup complete. <a href='/'>Go back</a>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
from flask import Flask, render_template
from airgradient import fetch_airgradient_metrics

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/air")
def air_status():
    data = fetch_airgradient_metrics()
    return render_template("air.html", data=data)

#if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
