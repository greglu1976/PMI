import configparser
import json

from tables import add_table_infuences, add_table_results


def parse_assembly_ini(assembly_path):
    config = configparser.ConfigParser()
    config.read(assembly_path, encoding="utf-8")
    
    sections = []
    
    for section_name in config.sections():
        section_data = {'section_name': section_name}
        
        # Обрабатываем секцию [settings_general] особым образом
        if section_name == 'settings_general':
            # Получаем список FBS из строки
            fbs_str = config.get(section_name, 'fbs', fallback='')
            # Преобразуем строку вида "['CTR_UIRZ', 'TDIF', 'TPRMOFFLVLGC']" в список
            fbs_list = [item.strip("' ") for item in fbs_str.strip("[]").split(',')]
            section_data['fbs'] = fbs_list
        else:
            # Обрабатываем остальные секции как раньше
            section_data.update({
                'heading': config.get(section_name, 'heading', fallback=''),
                'intro_text': config.get(section_name, 'intro_text', fallback=''),
                'func_modes_dir': config.get(section_name, 'func_modes_dir', fallback=''),
                'needed_inputs': config.get(section_name, 'needed_inputs', fallback=''),
                'needed_outputs': config.get(section_name, 'needed_outputs', fallback=''),
                'result_heading': config.get(section_name, 'result_heading', fallback=''),
                'result_text': config.get(section_name, 'result_text', fallback=''),
                'setting_heading': config.get(section_name, 'setting_heading', fallback='')
            })
        
        sections.append(section_data)
    
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

        #print(table_rows)
        doc = add_table_infuences(doc, table_rows)

    return doc

######################## РАЗДЕЛ 3 ###################################
# Автоматическая генерация раздела с результатами
def add_results_funcs_par(doc, assembly, path_to_pmi, modes_list):

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
        doc.add_heading(section['result_heading'], level=2)
        doc.add_heading(section['result_text'], level=3)

        # Загружаем необходимые входы
        path_to_inputs = path_to_pmi / section['needed_outputs']
        with open(path_to_inputs, 'r', encoding='utf-8') as file:
            data_dict = json.load(file)
        #print(data_dict)  # Выводим полученный словарь - это фактически заголовки таблицы

        # Создаем заголовок
        header = ['Номер режима']
        header.extend(value for key, value in data_dict.items())
        table_rows = [header] # модель таблицы для сборки

        for i, mode in enumerate(curr_modes, start=1):
            # Получаем значения для текущего режима
            mode_values = mode.mode_data.outputs
            
            # Формируем строку: номер режима + значения в порядке заголовков
            row = [str(i)]  # Номер режима
            for key in data_dict:
                row.append(str(mode_values.get(key, '')))
            
            table_rows.append(row)

        #print(table_rows)
        doc = add_table_results(doc, table_rows)

    return doc