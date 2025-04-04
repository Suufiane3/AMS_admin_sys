import json
import os

# Seuil critique (90%)
CRITICAL_THRESHOLD = 90

def read_json_file():

    try:
        with open("data.json", "r") as f:
            lines = f.readlines()

        cpu_data = None
        ram_data = None
        storage_data = None
        
        # Parcourt les lignes en commençant par la fin pour trouver les données les plus récentes
        for line in reversed(lines):
            if line.strip():
                data = json.loads(line.strip())
                
                # Identifie le type de donnée par ses clés caractéristiques
                if "cpu_usage" in data:
                    cpu_data = data
                elif "total_ram" in data and "percent" in data:
                    ram_data = data
                elif "total_storage" in data and "percent" in data:
                    storage_data = data
                
                # Si on a trouvé toutes les données, on s'arrête
                if cpu_data and ram_data and storage_data:
                    break
                    
        return cpu_data, ram_data, storage_data
    
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Erreur lors de la lecture des données: {e}")
        return None, None, None

def check_crisis():

    cpu_data, ram_data, storage_data = read_json_file()
    
    # Valeurs par défaut
    cpu_value = 0
    ram_value = 0
    storage_value = 0
    
    if cpu_data:
        cpu_value = cpu_data["cpu_usage"]
        
    if ram_data:
        ram_value = ram_data["percent"]
        
    if storage_data:
        # Convertit le pourcentage stocké sous forme de chaîne (ex: "75%") en nombre
        storage_value = float(storage_data["percent"].replace("%", ""))
    
    crisis = {
        "cpu": cpu_value > CRITICAL_THRESHOLD,
        "ram": ram_value > CRITICAL_THRESHOLD,
        "storage": storage_value > CRITICAL_THRESHOLD,
    }
    
    # Situation de crise si au moins un des systèmes est critique
    crisis["is_crisis"] = any([crisis["cpu"], crisis["ram"], crisis["storage"]])
    
    return crisis

def dump_crisis_status():

    crisis_data = check_crisis()
    with open("data.json", "a") as f:
        f.write(json.dumps(crisis_data) + "\n")
    return crisis_data
  
