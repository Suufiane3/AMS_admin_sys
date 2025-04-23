import sqlite3
import json
import pygal
from datetime import datetime

DB_PATH = "database.db"

def load_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cpu_data, ram_data, storage_data = [], [], []
    timestamps = []

    cursor.execute("SELECT timestamp, type, data FROM archive WHERE type IN ('cpu', 'ram', 'storage') ORDER BY timestamp ASC")
    rows = cursor.fetchall()

    for ts, typ, raw_data in rows:
        data = json.loads(raw_data)

        if typ == "cpu":
            cpu_data.append(data["cpu_usage"])
        elif typ == "ram":
            ram_data.append(data["percent"])
        elif typ == "storage":
            percent_str = data["percent"].replace("%", "").replace(",", ".")
            storage_data.append(float(percent_str))

        # Ajoute le timestamp une seule fois par cycle de 3 mesures
        if typ == "cpu":
            timestamps.append(datetime.strptime(ts, "%Y-%m-%d %H:%M:%S").strftime("%H:%M"))

    conn.close()
    return timestamps, cpu_data, ram_data, storage_data

def generate_chart():
    timestamps, cpu, ram, storage = load_data()

    chart = pygal.Line(title="Utilisation des ressources système", x_label_rotation=20, show_minor_x_labels=False)
    chart.x_labels = timestamps
    chart.x_labels_major = timestamps[::2]

    chart.add("CPU (%)", cpu)
    chart.add("RAM (%)", ram)
    chart.add("Stockage (%)", storage)

    chart.render_to_file("system_usage.svg")
    print("Graphique généré : system_usage.svg")

if __name__ == "__main__":
    generate_chart()
