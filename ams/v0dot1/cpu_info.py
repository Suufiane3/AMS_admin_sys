import psutil
import time
import json


def get_cpu_usage(interval=1):
        cpu_info = {"cpu_usage" : psutil.cpu_percent(interval=interval)}
        return cpu_info

def dump_cpu_info():
        with open("data.json","a") as f:
                f.write(json.dumps(get_cpu_usage()) + "\n")


def show_cpu_usage(duration=10, interval=1):
        print("Surveillance de l'utilisation CPU :")
        print("-"*50)
        try:
                for _ in range(duration):
                        usage = get_cpu_usage(interval)
                        print(f"Utilisation du CPU : {usage}%")
        except KeyboardInterrupt:
                print("\n Fin de la surveillance")



#if __name__ == "__main__":



        #print("\n Veuillez insérer une durée : ")
        #duration = int(input())
        #show_cpu_usage(duration)
