import pandas as pd
import openpyxl
import pathlib
from typing import NamedTuple
from pathlib import Path

class ModeData(NamedTuple):
    mode_name: str
    sgf_parameters: dict
    settings: dict
    inputs: dict
    outputs: dict


class Mode:
    """
    Класс, представляющий отдельный режим ПМИ.
    Содержит данные и логику для работы с конкретным режимом.
    """
    def __init__(self, mode_path):
        """
        :param mode_data: данные режима, распарсенные из xlsx
        """
        self._mode_path = mode_path # путь с именем файла к xlsx файлу описания режима
        self._mode_name = Path(mode_path).stem  
        self._sgf_parameters_dict = {}
        self._settings_dict = {}
        self._inputs_dict = {}
        self._outputs_dict = {}

        self._load_mode()

    def _load_mode(self):
        """
        Загружает данные из xlsx файла режима в Series (если на листе одна строка данных).
        Читает листы: SGF_Parameters, Settings, Inputs, Outputs.
        """
        try:
            xls = pd.ExcelFile(self._mode_path, engine='openpyxl')
            
            # Загружаем каждый лист в Series (если там одна строка данных)
            if 'SGF_Parameters' in xls.sheet_names:
                df = pd.read_excel(xls, sheet_name='SGF_Parameters')
                self._sgf_parameters_dict = df.iloc[0].to_dict() if not df.empty else {}
            
            if 'Settings' in xls.sheet_names:
                df = pd.read_excel(xls, sheet_name='Settings')
                self._settings_dict = df.iloc[0].to_dict() if not df.empty else {}
            
            if 'Inputs' in xls.sheet_names:
                df = pd.read_excel(xls, sheet_name='Inputs')
                self._inputs_dict = df.iloc[0].to_dict() if not df.empty else {}
            
            if 'Outputs' in xls.sheet_names:
                df = pd.read_excel(xls, sheet_name='Outputs')
                self._outputs_dict = df.iloc[0].to_dict() if not df.empty else {}
                
        except Exception as e:
            print(f"Ошибка при загрузке файла режима {self._mode_path}: {str(e)}")
            raise
        
    @property
    def mode_data(self) -> ModeData:
        """Возвращает все данные режима в виде именованного кортежа."""
        return ModeData(
            mode_name = self._mode_name,
            sgf_parameters=self._sgf_parameters_dict,
            settings=self._settings_dict,
            inputs=self._inputs_dict,
            outputs=self._outputs_dict
        )

    @property
    def name(self) -> str:
        """Возвращает название режима (имя файла без .xlsx)."""
        return Path(self._mode_path).stem


if __name__ == "__main__":

    # автоматическое построение
    current_dir = pathlib.Path(__file__).parent
    mode_path = current_dir / "pmi_dzt" / "dtz1_modes" / "ДТЗ_2.xlsx"

    mode = Mode(str(mode_path))
    print(mode.get_mode_data())

