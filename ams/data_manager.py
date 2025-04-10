import sqlite3
from datetime import datetime, timedelta
import json
import os

# Connexion à SQLite
DB = "database.db"

def create_table():

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS archive (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            data TEXT
        )
    """)
    conn.commit()
    conn.close()


def data_time_limite():

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    
    # Date limite : aujourd'hui - 30 jours
    date_limite = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')
    
    # Suppression des logs trop anciens
    cursor.execute("DELETE FROM archive WHERE timestamp < ?", (date_limite,))
    
    conn.commit()
    conn.close()


def insert_json_to_db(json_file):

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    with open(json_file, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()  # Enlever les espaces et sauts de ligne
            if not line:
                continue  # Ignorer les lignes vides

            try:
                data = json.loads(line)  # Convertir la ligne en JSON
            except json.JSONDecodeError:
                print(f" Erreur JSON sur la ligne : {line}")
                continue  # Ignorer la ligne si elle est invalide

            cursor.execute("INSERT INTO archive (data) VALUES (?)", (json.dumps(data),))

    conn.commit()
    conn.close()

def clear_json_file(filename):
    with open(filename, "w") as file:
        file.write("")  # Écrit un fichier vide
    #print(f"Le fichier {filename} a été vidé.")
