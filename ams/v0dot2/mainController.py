import os
import subprocess
import sqlite3
import json
import time
import platform
from datetime import datetime

# Détection du système d'exploitation
IS_WINDOWS = platform.system() == "Windows"

# Configuration
SONDES_DIR = "sondes"  # Dossier contenant les scripts de sondes
DB_PATH = "database.db"  # Chemin vers la base de données
REMOTE_MACHINES = [
    {"name": "pc1", "ip": "192.168.1.101", "user": "ubuntu", "key_path": "~/.ssh/id_rsa"},
    {"name": "local_vm", "ip": "127.0.0.1", "user": "ubuntu", "key_path": "~/.ssh/id_rsa", "port": 2222},
    # Ajoutez d'autres machines selon vos besoins
]

def create_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS archive (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            machine_name TEXT,
            machine_ip TEXT,
            data TEXT
        )
    """)
    conn.commit()
    conn.close()

def clear_json_file(filename):
    with open(filename, "w") as file:
        file.write("")

def insert_json_to_db(json_file, machine_name, machine_ip):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        with open(json_file, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                try:
                    data = json.loads(line)
                except json.JSONDecodeError:
                    print(f"Erreur JSON sur la ligne : {line}")
                    continue

                cursor.execute(
                    "INSERT INTO archive (machine_name, machine_ip, data) VALUES (?, ?, ?)",
                    (machine_name, machine_ip, json.dumps(data))
                )
        
        conn.commit()
    except Exception as e:
        print(f"Erreur lors de l'insertion des données: {e}")
    finally:
        conn.close()

def get_sonde_scripts():
    """Récupère la liste de tous les scripts dans le dossier des sondes"""
    sonde_scripts = []
    
    if os.path.exists(SONDES_DIR) and os.path.isdir(SONDES_DIR):
        for filename in os.listdir(SONDES_DIR):
            file_path = os.path.join(SONDES_DIR, filename)
            if os.path.isfile(file_path):
                # Vérifier si c'est un script Python ou Bash
                if filename.endswith('.py') or filename.endswith('.sh'):
                    sonde_scripts.append(filename)
    
    return sonde_scripts

def execute_remote_sondes(machine):
    """Exécute les sondes sur une machine distante et récupère les données"""
    machine_name = machine["name"]
    machine_ip = machine["ip"]
    user = machine["user"]
    key_path = machine["key_path"]
    port = machine.get("port", 22)  # Port SSH par défaut ou spécifié
    
    print(f"Collecte des données pour {machine_name} ({machine_ip})...")
    
    # Créer un répertoire temporaire pour les données de cette machine
    temp_dir = f"temp_{machine_name}"
    os.makedirs(temp_dir, exist_ok=True)
    
    # Nom du fichier temporaire pour stocker les données
    temp_json = os.path.join(temp_dir, "data.json")
    clear_json_file(temp_json)
    
    # Récupérer la liste des scripts de sondes
    sonde_scripts = get_sonde_scripts()
    
    for script in sonde_scripts:
        script_path = os.path.join(SONDES_DIR, script)
        remote_script_path = f"/tmp/{script}"
        
        # Commandes adaptées pour Windows/Linux
        if IS_WINDOWS:
            scp_cmd = f"scp -P {port} -i \"{key_path}\" \"{script_path}\" {user}@{machine_ip}:{remote_script_path}"
        else:
            scp_cmd = f"scp -P {port} -i {key_path} {script_path} {user}@{machine_ip}:{remote_script_path}"
        
        try:
            subprocess.run(scp_cmd, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Erreur lors de la copie du script {script} vers {machine_name}: {e}")
            continue
        
        # Exécuter le script sur la machine distante
        if script.endswith('.py'):
            if IS_WINDOWS:
                ssh_cmd = f"ssh -p {port} -i \"{key_path}\" {user}@{machine_ip} \"python3 {remote_script_path}\""
            else:
                ssh_cmd = f"ssh -p {port} -i {key_path} {user}@{machine_ip} 'python3 {remote_script_path}'"
        else:  # script bash
            if IS_WINDOWS:
                ssh_cmd = f"ssh -p {port} -i \"{key_path}\" {user}@{machine_ip} \"chmod +x {remote_script_path} && {remote_script_path}\""
            else:
                ssh_cmd = f"ssh -p {port} -i {key_path} {user}@{machine_ip} 'chmod +x {remote_script_path} && {remote_script_path}'"
        
        try:
            # Exécuter le script et capturer la sortie
            output = subprocess.check_output(ssh_cmd, shell=True, universal_newlines=True)
            
            # Si le script a produit une sortie JSON, l'ajouter au fichier de données
            if output.strip():
                with open(temp_json, "a") as f:
                    f.write(output.strip() + "\n")
        except subprocess.CalledProcessError as e:
            print(f"Erreur lors de l'exécution du script {script} sur {machine_name}: {e}")
    
    # Insérer les données dans la base de données
    insert_json_to_db(temp_json, machine_name, machine_ip)
    
    # Nettoyer
    clear_json_file(temp_json)
    
    # Sur Windows, rmdir ne fonctionne que si le répertoire est vide
    try:
        os.rmdir(temp_dir)
    except OSError as e:
        print(f"Avertissement: impossible de supprimer le dossier temporaire {temp_dir}: {e}")

def main():
    # Créer la table si elle n'existe pas
    create_table()
    
    # Pour chaque machine, exécuter les sondes et collecter les données
    for machine in REMOTE_MACHINES:
        try:
            execute_remote_sondes(machine)
        except Exception as e:
            print(f"Erreur lors de la collecte pour {machine['name']}: {e}")
    
    print("Collecte de données terminée")

if __name__ == "__main__":
    main()
