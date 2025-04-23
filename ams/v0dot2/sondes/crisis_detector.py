import json
import subprocess
from cpu_info import get_cpu_usage
from ram_info import get_ram_usage

CRITICAL_THRESHOLD = 90

def get_storage_usage():
    output = subprocess.check_output(["bash", "storage_info.sh"]).decode().strip()
    storage_data = json.loads(output)
    return storage_data

def check_crisis():
    cpu_data = get_cpu_usage()
    ram_data = get_ram_usage()
    storage_data = get_storage_usage()

    cpu_value = cpu_data["cpu_usage"]
    ram_value = ram_data["percent"]
    storage_value = float(storage_data["percent"].replace("%", "").replace(",", "."))

    crisis = {
        "cpu": cpu_value > CRITICAL_THRESHOLD,
        "ram": ram_value > CRITICAL_THRESHOLD,
        "storage": storage_value > CRITICAL_THRESHOLD,
    }

    crisis["is_crisis"] = any(crisis.values())

    return crisis

if __name__ == "__main__":
    print(json.dumps(check_crisis()))
