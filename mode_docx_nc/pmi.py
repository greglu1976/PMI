from typing import Optional, List  # Для Python 3.8 и ниже
import pathlib
from modes import Modes

from docx import Document

from utils import parse_assembly_ini, add_checking_funcs_par, add_results_funcs_par

from _test import generate_settings


class PMI:
    """
    Класс для работы с документацией ПМИ.
    При инициализации загружает все режимы из указанной директории.
    """
    def __init__(self, part_of_modes_dir):

        self._part_of_modes_dir = part_of_modes_dir
        self._part_of_modes_list = []

        self._load_part_of_modes()

        self.get_docx()
    
    def _load_part_of_modes(self):
        """Приватный метод для загрузки режимов из директории"""
        self._part_of_modes_list = []  # Очищаем список перед загрузкой

        # Ищем все поддиректории (игнорируем файлы)
        for mode_dir in self._part_of_modes_dir.iterdir():
            if mode_dir.is_dir() and mode_dir.name.endswith('_modes'):
                try:
                    modes = Modes(mode_dir)
                    self._part_of_modes_list.append(modes)
                    #print(f"Загружена группа режимов из: {mode_dir.name}")
                except Exception as e:
                    print(f"Ошибка при загрузке режимов из {mode_dir}: {str(e)}")

    def get_docx(self) -> bytes:
        """
        Генерирует отчет в формате DOCX
        """
        # Парсим _assembly.ini
        path_to_assembly = self._part_of_modes_dir / "_assembly.ini"
        parsed_assembly = parse_assembly_ini(path_to_assembly)
        # Создаем docx файл из шаблона, загружаем шаблон
        path_to_docx_templ = self._part_of_modes_dir / "template.docx"
        doc = Document(path_to_docx_templ)

        # Добавляем заголовок раздела (РАЗДЕЛ 2)       
        doc.add_heading('МЕТОДИКИ ПРОВЕДЕНИЯ ИСПЫТАНИЙ', level=1)
        # Добавляем подразделы с описанием режимов
        doc = add_checking_funcs_par(doc, parsed_assembly, self._part_of_modes_dir, self._part_of_modes_list)

        # Добавляем заголовок раздела (РАЗДЕЛ 3)       
        doc.add_heading('РЕЗУЛЬТАТ ИСПЫТАНИЙ', level=1)
        # Добавляем подразделы с результатами
        doc = add_results_funcs_par(doc, parsed_assembly, self._part_of_modes_dir, self._part_of_modes_list)

        # Тестируем генератор уставок
        doc = generate_settings(doc, parsed_assembly, self._part_of_modes_dir, self._part_of_modes_list)     

        # Сохраняем документ ПМИ
        doc.save('_pmi.docx')
    






if __name__ == "__main__":

    # автоматическое построение
    current_dir = pathlib.Path(__file__).parent
    part_of_modes_dir = current_dir / "pmi_dzt" 

    pmi = PMI(part_of_modes_dir)