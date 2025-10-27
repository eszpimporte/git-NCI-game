import time, datetime
from infos.infos_prog import *

logs : list[str]
logs = []

def write_logs()->None:
    with open("logs.txt", "+a", encoding="utf-8") as file_logs:
        logs.append(f"Enregsitrement des logs à {datetime.datetime.now().strftime("%H:%M:%S le %d/%m/%Y")}, version du programme : {version}\n")
        file_logs.write("\n".join(logs)+"\n_______________________________________\n")