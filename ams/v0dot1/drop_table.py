import sqlite3
DB = "database.db"

def drop_table():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS archive")
    conn.commit()
    conn.close()
    print("Table 'archive' supprimé avec succès")

if __name__ == "__main__":
    drop_table()
    
