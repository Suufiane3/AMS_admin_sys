import psutil
import json

def get_cpu_usage(interval=1):
    cpu_info = {"cpu_usage": psutil.cpu_percent(interval=interval)}
    return cpu_info

if __name__ == "__main__":
    print(json.dumps(get_cpu_usage()))
