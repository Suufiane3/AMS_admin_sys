import sqlite3
import json

# Connexion à SQLite
conn = sqlite3.connect("database.db")
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
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO archive (data) VALUES (?)", (json.dumps(data),))

    conn.commit()
    conn.close()

# Exemple d'utilisation
insert_json_to_db("data.json")
