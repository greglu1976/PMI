# Для тестирования генератора уставок
# потом удалить
import json

from tables import add_table_settings
from _fb2 import create_fbs

def _get_dict(modes, section_name):
    result = {}
    previous_mode_params = {}  # Для хранения параметров предыдущего режима
    
    #for item in curr_modes:
    for datum in modes:
        mode_name = datum.mode_data.mode_name
        sgf_parameters = datum.mode_data.sgf_parameters
        settings = datum.mode_data.settings
        
        # Формируем ключ для режима
        mode_key = f"{section_name}. Режим №{mode_name.split('_')[1]}"
        result[mode_key] = {}
        
        # Обрабатываем sgf_parameters
        for param, value in sgf_parameters.items():
            param_dict = {
                'Value': value,
                'IsChanged': 0  # По умолчанию изменений нет
            }
            
            # Проверяем, было ли изменение по сравнению с предыдущим режимом
            if previous_mode_params and param in previous_mode_params['sgf']:
                if previous_mode_params['sgf'][param] != value:
                    param_dict['IsChanged'] = 1
            
            result[mode_key][param] = param_dict
        
        # Обрабатываем settings
        for param, value in settings.items():
            param_dict = {
                'Value': value,
                'IsChanged': 0  # По умолчанию изменений нет
            }
            
            # Проверяем, было ли изменение по сравнению с предыдущим режимом
            if previous_mode_params and param in previous_mode_params['settings']:
                if previous_mode_params['settings'][param] != value:
                    param_dict['IsChanged'] = 1
            
            result[mode_key][param] = param_dict
        
        # Сохраняем параметры текущего режима для сравнения со следующим
        previous_mode_params = {
            'sgf': sgf_parameters.copy(),
            'settings': settings.copy()
        }
    return result


def format_value_by_step(value, step):
    if step == '-':
        return value
    # Заменяем запятую на точку для парсинга
    step = float(step.replace(',', '.'))
    
    # Определяем число знаков после запятой
    if step == 1.0:
        decimals = 0
    else:
        parts = str(step).split('.')
        decimals = len(parts[1]) if len(parts) > 1 else 0

    # Форматируем число с точкой, затем заменяем точку на запятую
    formatted = f"{value:.{decimals}f}"
    formatted = formatted.replace('.', ',')
    
    return formatted

# Рендер шаблона таблиц - заполнение данными режима
def fill_template(modes_params, template_list):
    filled_template = []
    #print(modes_params)
    for row in template_list:
        #print(row['Шаг'])
        ld = row['LD'].lower()
        if '_' in ld:
            temp = ld.split('_')
            if temp[1] == 'uirz':
                ld = temp[0]
            else:
                ld = temp[1]
        ln =f"_{row['LN'].lower()}"
        if ln == '_lln0':
            ln =''
        alias = row['alias']
        key = alias + ln +'_'+ ld
        if alias !='-':
            #print(modes_params[key])
            aa = modes_params[key]['Value']
            a = format_value_by_step(aa, row['Шаг'])
            row['Уставка'] = a
            row['IsChanged'] = modes_params[key]['IsChanged']
        else:
            row['Уставка'] = '*'
            row['IsChanged'] = 2            
        filled_template.append(row)
    return filled_template
    




def generate_settings(doc, parsed_assembly, part_of_modes_dir, part_of_modes_list):
    # загружаем словарь с расшифровками
    with open('description.json', 'r', encoding='utf-8') as f:
        descriptions = json.load(f)
    # загружаем шаблоны для уставок
    list_of_fbs = []
    for section in parsed_assembly:
        if section['section_name'] == 'settings_general':
            fbs = section.get('fbs', [])
            if fbs:
                list_of_fbs = create_fbs(fbs)
    #print(list_of_fbs)

    doc.add_heading('ПАРАМЕТРЫ И УСТАВКИ РЕЖИМОВ', level=1)

    for section in parsed_assembly:
    # Ищем описание режимов для данного режима
        curr_modes = None
        for item in part_of_modes_list:
            if item.modes.modes_name == section['section_name']:
                curr_modes = item.modes.data
                break
        if not curr_modes:
            continue  # Пропускаем секцию, если режим не найден

        result = _get_dict(curr_modes, section['setting_heading'])
        # Находим все ключи, содержащие нужную фразу
        target_keys = [key for key in result.keys() 
                    if "Параметры для проверки" in key]
        header_list = target_keys[0].split('.')
        if len(header_list) == 3:
            header = header_list[0] + '.' + header_list[1]
        else:
            header = header_list[0]
        doc.add_heading(header, level=2)            
        for key in target_keys:
            #print('>>>>>>',key)
            #print(result[key])
            doc.add_heading(key.split('.')[-1], level=3)             
            # выводим таблицы уставок
            for fb in list_of_fbs:
                fb_name = descriptions[fb.get_fb_iec_name().lower()]['fbname']
                fb_desc = descriptions[fb.get_fb_iec_name().lower()]['desc']
                doc.add_heading(fb_desc + f' ({fb_name})', level=4)
                t = fb.get_functions()
                for function in t:
                    #print(function.settings_for_pmi)
                    templ = fill_template(result[key], function.settings_for_pmi)
                    doc = add_table_settings(doc, templ, descriptions)

        break

    return doc




if __name__ == "__main__":

    generate_settings()
