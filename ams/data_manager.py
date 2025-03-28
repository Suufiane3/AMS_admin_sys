import sqlite3
import json
import os

# Connexion à SQLite
DB = "database.db"

conn = sqlite3.connect(DB)
cursor = conn.cursor()

# Création d'une table avec une colonne JSON
cursor.execute("""
CREATE TABLE IF NOT EXISTS archive (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    data JSON
)
""")
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
    
        cursor.execute("INSERT INTO data_archive (data) VALUES (?)", (json.dumps(data),))
    
    conn.commit()
    conn.close()


insert_json_to_db("data.json")
