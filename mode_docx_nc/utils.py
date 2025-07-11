import configparser
import json
from io import StringIO

from tables import add_table_infuences


def parse_assembly_ini(assemply_path):
    # Создаем объект ConfigParser
    config = configparser.ConfigParser()
    
    # Читаем содержимое файла
    config.read(assemply_path, encoding="utf-8")  
    
    # Преобразуем в список словарей
    sections = []
    for section_name in config.sections():
        section_data = {
            'section_name': section_name,
            'heading': config.get(section_name, 'heading', fallback=''),
            'intro_text': config.get(section_name, 'intro_text', fallback=''),
            'func_modes_dir': config.get(section_name, 'func_modes_dir', fallback=''),
            'needed_inputs': config.get(section_name, 'needed_inputs', fallback=''),
            'needed_outputs': config.get(section_name, 'needed_outputs', fallback=''),
            'result_heading': config.get(section_name, 'result_heading', fallback=''),
            'result_text': config.get(section_name, 'result_text', fallback='')
        }
        sections.append(section_data)
    #print(sections)
    return sections

# Автоматическая генерация раздела с проверкой функций из режимов
def add_checking_funcs_par(doc, assembly, path_to_pmi, modes_list):

    for section in assembly:

        # Ищем описание режимов для данного режима
        curr_modes = None
        for item in modes_list:
            if item.modes.modes_name == section['section_name']:
                curr_modes = item.modes.data
                break
        if not curr_modes:
            continue  # Пропускаем секцию, если режим не найден

        # Проставляем заголовки
        doc.add_heading(section['heading'], level=2)
        doc.add_heading(section['intro_text'], level=3)

        # Загружаем необходимые входы
        path_to_inputs = path_to_pmi / section['needed_inputs']
        with open(path_to_inputs, 'r', encoding='utf-8') as file:
            data_dict = json.load(file)
        #print(data_dict)  # Выводим полученный словарь - это фактически заголовки таблицы

        # Создаем заголовок
        header = ['Номер режима']
        header.extend(value for key, value in data_dict.items())
        table_rows = [header] # модель таблицы для сборки

        for i, mode in enumerate(curr_modes, start=1):
            # Получаем значения для текущего режима
            mode_values = mode.mode_data.inputs
            
            # Формируем строку: номер режима + значения в порядке заголовков
            row = [str(i)]  # Номер режима
            for key in data_dict:
                row.append(str(mode_values.get(key, '')))
            
            table_rows.append(row)

        print(table_rows)
        doc = add_table_infuences(doc, table_rows)

    return doc

