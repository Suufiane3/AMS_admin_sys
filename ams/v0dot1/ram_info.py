import psutil
import time
import json
import os



def get_ram_usage():
        mem = psutil.virtual_memory()

        def bytes_to_gb(bytes_val):
                return bytes_val / (1024 ** 3) #nb d'octets dans 1gb


        ram_info = {

        "total_ram": round(bytes_to_gb(mem.total), 3),
        "available": round(bytes_to_gb(mem.available), 3),
        "used": round(bytes_to_gb(mem.used), 3),
        "percent": mem.percent

        }

        return ram_info

def dump_ram_info():
        with open("data.json", "a") as f:
                f.write(json.dumps(get_ram_usage()) + "\n")


def show_ram_usage():
        ram_info = get_ram_usage()
        os.system("clear")

        print("-"*50)
        print(ram_info)

        time.sleep(1)


#if __name__ == "__main__":




        #print("Surveiller pendant : (secondes)")
        #for _ in range(int(input())):
        #       show_ram_usage()
        #print("FIN")
