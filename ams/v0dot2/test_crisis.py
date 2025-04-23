import json
from datetime import datetime

# Importer la fonction que tu veux tester
from mainController import insert_data_to_db  # Remplace "ton_script" par le nom réel de ton fichier Python

# Simuler un jeu de données de crise
data = {"cpu": False, "ram": False, "storage": True, "is_crisis": True}

# Appeler la fonction avec les données simulées
insert_data_to_db(data)
