import cpu_info.py
import ram_info.py
import data_manager.py
import subprocess


cpu_info.dump_cpu_info()
ram_info.dump_ram_info()

data_manager.create_table()
print("Aucune table existante, creation avec succès")
data_manager.insert_json_to_db()
print("Tâche terminé")


