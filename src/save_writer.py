import datetime
from src.logs_writer import logs, write_logs

save : dict

def to_save()->None:
    logs.append(f"Save à {datetime.datetime.now().strftime("%H:%M:%S le %d/%m/%Y")}")
    with open("save.py", "w", encoding="utf-8") as save_file:
        save_to_write = "{" + (",".join(map(str,save.items()))).replace("(","").replace(")","").replace(";",":") + "}"
        save_file.write(save_to_write)
    write_logs()

def get_save()->dict:
    with open("save.py", "r", encoding="utf-8") as save_file:
        save : dict
        save = eval(save_file.readline())
        assert type(save) == dict
    return save

def init_save():
    global save
    try:
        save = get_save()
    except AssertionError or FileNotFoundError:
        save = {}
    except:
        logs.append("An unknown error occured !")
        save = {}