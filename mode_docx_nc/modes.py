import pandas as pd
import openpyxl
import pathlib
from natsort import natsorted  # Импортируем natural sort
from mode import Mode
from pathlib import Path
from typing import NamedTuple

class ModesData(NamedTuple):
    modes_name: str
    data: list

class Modes:
    """
    Класс, представляющий совокупность режимов ПМИ.
    Содержит данные и логику для работы с группой режимов.
    """
    def __init__(self, modes_path):
        self._modes_path = pathlib.Path(modes_path)
        self._list_of_modes = []
        self._load_modes()  # Автоматическая загрузка при инициализации
        self._modes_name = Path(modes_path).name # имя папки будет именем блока режимов

    def _load_modes(self):
        """Загружает все режимы (.xlsx файлы) из указанной директории"""
        try:
            # Ищем все xlsx файлы в директории
            xlsx_files = list(self._modes_path.glob("*.xlsx"))
            
            # Сортируем файлы в естественном порядке
            xlsx_files_sorted = natsorted(xlsx_files, key=lambda x: x.stem)
            
            for xlsx_file in xlsx_files_sorted:
                try:
                    mode = Mode(xlsx_file)
                    self._list_of_modes.append(mode)
                    #print(f"Загружен режим: {mode.name}")
                except Exception as e:
                    print(f"Ошибка при загрузке файла {xlsx_file}: {str(e)}")
                    
        except Exception as e:
            print(f"Ошибка при чтении директории режимов: {str(e)}")
            raise


    @property
    def modes(self):
        """Возвращает список всех режимов в виде именованного кортежа"""
        return ModesData(
            modes_name = self._modes_name,
            data=self._list_of_modes
        )

if __name__ == "__main__":

    # автоматическое построение
    current_dir = pathlib.Path(__file__).parent
    modes_dir = current_dir / "pmi_dzt" / "dtz1_modes" 

    modes = Modes(modes_dir)


