# airgradient.py
import requests

def fetch_airgradient_metrics():
    try:
        response = requests.get("http://192.168.13.22/metrics", timeout=5)
        lines = response.text.strip().splitlines()

        def get_value(metric):
            for line in lines:
                if line.startswith(metric):
                    return float(line.split()[-1])
            return None

        return {
            "pm2_5": get_value("airgradient_pm2d5_ugm3"),
            "temp": get_value("airgradient_temperature_celsius"),
            "humidity": get_value("airgradient_humidity_percent"),
            "co2": get_value("airgradient_co2_ppm"),
            "tvoc": get_value("airgradient_tvoc_index"),
            "nox": get_value("airgradient_nox_index"),
        }

    except Exception as e:
        return {"error": str(e)}
