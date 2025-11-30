import datetime
from src.logs_writer import logs, write_logs
from saves.save1 import save as save1
from saves.save2 import save as save2
from saves.save3 import save as save3


class Save():
    save_numb_open = 0
    save : dict


    def choice_save(numb:int)->None:
        assert numb in [1,2,3]
        Save.save_numb_open = numb

        if numb == 1:
            Save.save = save1
        elif numb == 2:
            Save.save = save2
        elif numb == 3:
            Save.save = save3


    def to_save(new_save)->None:
        logs.append(f"Save à {datetime.datetime.now().strftime("%H:%M:%S le %d/%m/%Y")}")
        with open(f"saves/save{Save.save_numb_open}.py", "w", encoding="utf-8") as save_file:
            save_to_write = "save = " + str(new_save)
            save_file.write(save_to_write)
        write_logs()


    def get_save()->dict:
        return Save.save