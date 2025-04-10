import psutil
import json

def get_ram_usage():
    mem = psutil.virtual_memory()

    def bytes_to_gb(bytes_val):
        return bytes_val / (1024 ** 3)  # nb d'octets dans 1gb

    ram_info = {
        "total_ram": round(bytes_to_gb(mem.total), 3),
        "available": round(bytes_to_gb(mem.available), 3),
        "used": round(bytes_to_gb(mem.used), 3),
        "percent": mem.percent
    }

    return ram_info

if __name__ == "__main__":
    # Au lieu d'écrire dans un fichier, on imprime le résultat JSON
    print(json.dumps(get_ram_usage()))
