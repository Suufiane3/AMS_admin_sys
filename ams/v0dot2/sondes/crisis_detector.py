import json
import psutil
import os
import subprocess

# Seuil critique (90%)
CRITICAL_THRESHOLD = 90

def get_cpu_usage():
    return {"cpu_usage": psutil.cpu_percent(interval=1)}

def get_ram_usage():
    mem = psutil.virtual_memory()
    return {
        "percent": mem.percent
    }

def get_storage_usage():
    if os.name == 'posix':  # Pour Linux/Unix
        try:
            cmd = "df -h / | grep -v 'Filesystem' | tr -s ' ' | cut -d' ' -f5"
            storage_percent = subprocess.check_output(cmd, shell=True).decode().strip()
            return {"percent": storage_percent}
        except:
            return {"percent": "0%"}
    else:
        return {"percent": "0%"}

def check_crisis():
    # Récupère les données en temps réel
    cpu_data = get_cpu_usage()
    ram_data = get_ram_usage()
    storage_data = get_storage_usage()
    
    # Valeurs par défaut
    cpu_value = cpu_data["cpu_usage"]
    ram_value = ram_data["percent"]
    
    # Convertit le pourcentage stocké sous forme de chaîne (ex: "75%") en nombre
    storage_string = storage_data["percent"]
    storage_value = float(storage_string.replace("%", ""))
    
    crisis = {
        "cpu": cpu_value > CRITICAL_THRESHOLD,
        "ram": ram_value > CRITICAL_THRESHOLD,
        "storage": storage_value > CRITICAL_THRESHOLD,
    }
    
    # Situation de crise si au moins un des systèmes est critique
    crisis["is_crisis"] = any([crisis["cpu"], crisis["ram"], crisis["storage"]])
    
    return crisis

if __name__ == "__main__":
    # Au lieu d'écrire dans un fichier, on imprime le résultat JSON
    print(json.dumps(check_crisis()))
