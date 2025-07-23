
# 1. Для работы с режимами pmi_gz требуется переименовать столбцы в файлах режимов - _rblc1_tofflvlgc в _lvcbrblc1_tofflvlgc. 
# Либо доработать файл генерации режимов auto_part_TECH_T.py и все перегенерировать заново. 

# 2. Для работы с режимами pmi_gzt2 требуется переименовать столбцы в файлах режимов - _rblc1_tofflvlgc в _lvcbrblc1_tofflvlgc. 
# Либо доработать файл генерации режимов auto_part_TECH_T2.py и все перегенерировать заново. 

# 3. Для работы с режимами pmi_ka требуется переименовать столбцы в файлах режимов _rbrf1_ в _genrbrf1_ с помощью changer_xlsx2.py
# Либо доработать файл генерации режимов auto_part_SWITCH3.py и все перегенерировать заново.

# 4. Для работы с режимами pmi_ka требуется добавить столбцы в файлах режимов _lvalh со значением =0. по SGF14 (SGF13 уже есть)
# Либо доработать файл генерации режимов auto_part_SWITCH3.py и все перегенерировать заново. Сделана версия 2 учитывающая пп. 3,4. Но режиме НЕ перегенерировались - были добавлены столбцы для lvalh

# 5. Для работы с режимами pmi_ka2 требуется добавить столбцы в файлах режимов _lvalh со значением =0. по SGF10 (SGF9 уже есть)
# Либо доработать файл генерации режимов auto_part_SWITCH3.py и все перегенерировать заново. Сделана версия 2 учитывающая пп. 3,4. Но режиме НЕ перегенерировались - были добавлены столбцы для lvalh

#6. Для работы с режимами pmi_lo требуется обновить по пп.1,3 (changer_xlsx.py, changer_xlsx2.py).

#7. Почему то для ЛО ДЗТ pmi_lodzt. В качестве ЛО НН1, НН2 взят узел lvtcboff1. Хотя должен быть LVTPRMCBOFF. Оставлен LVTPRMCBOFF. Изменить auto_part_LO_DZT.py. Так же _rbrf1_ в _genrbrf1_ с помощью changer_xlsx2.py

#8. Для работы с режимами pmi_lot2 требуется переименовать столбцы в файлах режимов - _rblc1_tofflvlgc в _lvcbrblc1_tofflvlgc. Таже логика отключениея НН1, НН2 и ЛО Т

#9 В режимах pmi_mtz нет столбца T1_ptrc1_ttoclgc = 1. Добавлялся вручную!!!

#10 В режимах pmi_mtzt столбцов SGF11_lvalh ... SGF14_lvalh. Добавлялся вручную!!!

#11 В режимах pmi_todzt есть столбец _lvoileqpalc_eqpalc (!!! исправить в генераторе режимов), должен быть _palc1_eqpalc. Почему то вместо strtpalc в сигналах обозначение strpalc!!!

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
    def __init__(self, part_of_modes_dir, settings):

        self._part_of_modes_dir = part_of_modes_dir
        self._part_of_modes_list = []

        self.GENERATE_SETTINGS = settings

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



        if self.GENERATE_SETTINGS == 1:
            #path_to_docx_templ_apx = self._part_of_modes_dir / "template_apx.docx"
            path_to_docx_templ_apx = "template_apx.docx"
            doc_apx = Document(path_to_docx_templ_apx)
            doc_apx = generate_settings(doc_apx, parsed_assembly, self._part_of_modes_list)
            doc_apx.save('Бланки уставок.docx')
        else: # Вариант в котором бланки уставок генерятся прямо в общем документе ПМИ
            doc = generate_settings(doc, parsed_assembly, self._part_of_modes_list)     

        # Сохраняем документ ПМИ
        doc.save('ПМИ.docx')
    


if __name__ == "__main__":
    # НАСТРОЙКИ
    # GENERATE_SETTINGS = 1 - генерация в отдельный файл Приложение - полностью все таблицы. Больше пока ничего не предусмотрено - По 1 самая урезанная версия!!!
    GENERATE_SETTINGS = 1

    # автоматическое построение
    current_dir = pathlib.Path(__file__).parent
    part_of_modes_dir = current_dir / "pmi_tokzdzt" 

    pmi = PMI(part_of_modes_dir, GENERATE_SETTINGS)