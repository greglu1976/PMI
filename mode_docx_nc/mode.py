import pandas as pd
import openpyxl
import pathlib

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

        self._sgf_parameters_dict = {}
        self._settings_dict = {}
        self._inputs_dict = {}
        self._outputs_dict = {}

        _load_mode(self)
        print(self._sgf_parameters_dict)

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
    def name(self) -> str:
        """Возвращает название режима"""
        return self._data.get('name', '')


if __name__ == "__main__":

    # автоматическое построение
    current_dir = pathlib.Path(__file__).parent
    mode_path = current_dir / "pmi_dzt" / "dtz1_modes" / "ДТЗ_2.xlsx"
    print(str(mode_path))
    mode = Mode(str(mode_path))

