from flask import Flask, render_template
import subprocess
import socket
import requests

app = Flask(__name__)

# ฟังก์ชันดึงรายชื่ออุปกรณ์ที่เชื่อมกับ Wi-Fi Hotspot (MAC Address)
def get_wifi_clients():
    try:
        output = subprocess.check_output(['iw', 'dev', 'wlan0', 'station', 'dump'], text=True)
        macs = []
        for line in output.splitlines():
            if line.strip().startswith("Station"):
                mac = line.split()[1]
                macs.append(mac)
        return macs
    except Exception as e:
        return [f"Error: {e}"]

# ดึง Public IP จากภายนอก
def get_public_ip():
    try:
        return requests.get("https://ifconfig.me", timeout=3).text.strip()
    except:
        return "Unavailable"

# ดึงสถานะ Tailscale
def get_tailscale_status():
    try:
        return subprocess.check_output(["tailscale", "status"], text=True)
    except:
        return "Not Connected"

@app.route("/")
def index():
    hostname = socket.gethostname()
    public_ip = get_public_ip()
    tailscale_status = get_tailscale_status()
    wifi_clients = get_wifi_clients()

    return render_template("dashboard.html",
                           hostname=hostname,
                           public_ip=public_ip,
                           tailscale_status=tailscale_status,
                           wifi_clients=wifi_clients)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
