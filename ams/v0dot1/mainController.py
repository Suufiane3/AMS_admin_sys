import cpu_info
import ram_info
import data_manager
import scraper
import subprocess
import crisis_detector

f = "data.json"

cpu_info.dump_cpu_info()
ram_info.dump_ram_info()
subprocess.run(["bash", "storage_info.sh"])

crisis_detector.dump_crisis_status()
scraper.dump_alerte()

data_manager.create_table()
data_manager.insert_json_to_db(f)
data_manager.clear_json_file(f)
print("Tâche terminée")
