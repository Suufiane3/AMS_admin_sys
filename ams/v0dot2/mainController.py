import os
import subprocess
import sqlite3
import json
from datetime import datetime, timedelta

# Configuration
SONDES_DIR = "/home/soso/ams2/AMS_admin_sys/ams/v0dot2/sondes"  # Dossier contenant les scripts de sondes
DB_PATH = "/home/soso/ams2/AMS_admin_sys/ams/v0dot2/database.db"  # Chemin vers la base de données
DATA_CONSERVATION_DAYS = 7 # Durée de conservation des données (en jours)

def create_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS archive (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            type TEXT,
            data TEXT
        )
    """)
    conn.commit()
    conn.close()

def determine_data_type(data):
    """Détermine le type de données basé sur les clés présentes"""
    if isinstance(data, dict):
        if "cpu_usage" in data:
            return "cpu"
        elif "total_ram" in data or ("percent" in data and "available" in data):
            return "ram"
        elif "total_storage" in data:
            return "storage"
        elif "Date" in data and "Alerte" in data:
            return "alerte"
        elif "is_crisis" in data:
            return "crisis"
    return "unknown"

def insert_data_to_db(data):
    """Insère les données JSON dans la base de données"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        data_type = determine_data_type(data)
        cursor.execute(
            "INSERT INTO archive (type, data) VALUES (?, ?)",
            (data_type, json.dumps(data))
        )
        conn.commit()
    except Exception as e:
        print(f"Erreur lors de l'insertion des données: {e}")
    finally:
        conn.close()


def clean_outdated_db():
    """Supprime les données plus anciennes que DATA_RETENTION_DAYS"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Calculer la date limite
        limit_date = (datetime.now() - timedelta(days=DATA_CONSERVATION_DAYS)).strftime('%Y-%m-%d %H:%M:%S')
        
        # Compter combien d'enregistrements seront supprimés
        cursor.execute("SELECT COUNT(*) FROM archive WHERE timestamp < ?", (limit_date,))
        count = cursor.fetchone()[0]
        
        # Supprimer les enregistrements anciens
        cursor.execute("DELETE FROM archive WHERE timestamp < ?", (limit_date,))
        conn.commit()
        
        if count > 0:
            print(f"Nettoyage: {count} enregistrements plus anciens que {DATA_CONSERVATION_DAYS} jours ont été supprimés.")
            
        # Optimiser la base de données après suppression
        cursor.execute("VACUUM")
        conn.commit()
        
    except Exception as e:
        print(f"Erreur lors du nettoyage des anciennes données: {e}")
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

def execute_sondes():
    """Exécute les sondes sur la machine locale et récupère les données"""
    print("Collecte des données...")

    # Récupérer la liste des scripts de sondes
    sonde_scripts = get_sonde_scripts()

    for script in sonde_scripts:
        script_path = os.path.join(SONDES_DIR, script)

        try:
            # Exécuter le script sur la machine locale
            if script.endswith('.py'):
                cmd = f"python3 {script_path}"
            else:  # script bash
                # S'assurer que le script est exécutable
                os.chmod(script_path, 0o755)
                cmd = f"{script_path}"

            # Exécuter le script et capturer la sortie
            output = subprocess.check_output(cmd, shell=True, universal_newlines=True)

            # Si le script a produit une sortie JSON, l'analyser et l'insérer dans la base de données
            if output.strip():
                try:
                    data = json.loads(output.strip())
                    insert_data_to_db(data)
                except json.JSONDecodeError:
                    print(f"Erreur JSON dans la sortie du script {script}: {output}")
        except subprocess.CalledProcessError as e:
            print(f"Erreur lors de l'exécution du script {script}: {e}")
        except Exception as e:
            print(f"Erreur inattendue avec le script {script}: {e}")

    clean_outdated_db()

def main():
    # Créer la table si elle n'existe pas
    create_table()

    # Exécuter les sondes localement
    execute_sondes()

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Collecte de données terminée")

if __name__ == "__main__":
    main()
