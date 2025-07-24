# Для тестирования генератора уставок
# потом удалить
import json

from docx.shared import RGBColor

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

        if 'switchdevice' in ld:
            ld = 'tsd'

        if 'signassembly' in ld:
            ld = 'tsa'
            ln = ''

        if 'lvalh' in ld:
            ld = 'lvalh'
            ln = ''

        key = alias + ln +'_'+ ld
        if alias !='-':
            #print('>>>>>',key)
            #print(modes_params)
            aa = modes_params[key]['Value']
            a = format_value_by_step(aa, row['Шаг'])
            row['Уставка'] = a
            row['IsChanged'] = modes_params[key]['IsChanged']
        else:
            row['Уставка'] = '*'
            row['IsChanged'] = 2            
        filled_template.append(row)
    return filled_template
    
def generate_settings(doc, parsed_assembly, part_of_modes_list, path_to_fsu):
    # загружаем словарь с расшифровками
    with open('description.json', 'r', encoding='utf-8') as f:
        descriptions = json.load(f)
    # загружаем шаблоны для уставок
    list_of_fbs = []
    for section in parsed_assembly:
        if section['section_name'] == 'settings_general':
            fbs = section.get('fbs', [])
            if fbs:
                list_of_fbs = create_fbs(fbs, path_to_fsu)
    #print(list_of_fbs)

    #doc.add_heading('ПАРАМЕТРЫ И УСТАВКИ РЕЖИМОВ', level=1) # Убран заголовок для генерации в приложение НЕ требуется

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
        #doc.add_heading(header, level=2)
        doc.add_heading(header, level=1) # для генерации в приложение повышаем уровень заголовка

        isFirstPass = True           
        for key in target_keys:
            #print('>>>>>>',key)
            #print(result[key])
            if not isFirstPass and all(item['IsChanged'] == 0 for item in result[key].values()):
                #doc.add_heading(f"{key.split('.')[-1]}", level=3)
                doc.add_heading(f"{key.split('.')[-1]}", level=2)  # для генерации в приложение повышаем уровень заголовка              
                # Создаем параграф и задаем стиль
                paragraph = doc.add_paragraph(style='ЮИ_Обычный')
                run = paragraph.add_run(f"Уставки и параметры задействованных функций идентичны предыдущему режиму.")
                run.font.color.rgb = RGBColor(0, 128, 0)  # Зеленый цвет (R, G, B)
                #run.bold = True  # Жирный шрифт (как заголовок)
                continue

            #doc.add_heading(f"{key.split('.')[-1]}. Уставки и параметры задействованных функций", level=3)  # Вывод номера режима в заголовке Режим №1 ...  
            doc.add_heading(f"{key.split('.')[-1]}", level=2)  # для генерации в приложение повышаем уровень заголовка 
            #paragraph = doc.add_paragraph(style='ЮИ_Обычный')
            #run = paragraph.add_run(f"Уставки и параметры задействованных функций.")  

            # выводим таблицы уставок
            for fb in list_of_fbs:
                #print(fb, fb.get_fb_name())
                fb_name = descriptions[fb.get_fb_iec_name().lower()]['fbname']
                fb_desc = descriptions[fb.get_fb_iec_name().lower()]['desc']
                #doc.add_heading(fb_desc + f' ({fb_name})', level=4)
                doc.add_heading(fb_desc + f' ({fb_name})', level=3) # для генерации в приложение повышаем уровень заголовка                
                t = fb.get_functions()

                check = False    
                for function in t:
                    #print(result[key])
                    f = function.settings_for_pmi

                    templ = fill_template(result[key], f)

                    if not isFirstPass and not(check_ischanged(templ)):
                        continue
                    check = True
                    doc = add_table_settings(doc, templ, descriptions)
                if not check:
                        paragraph = doc.add_paragraph(style='ЮИ_Обычный')
                        run = paragraph.add_run(f"Уставки и параметры функции идентичны предыдущему режиму.")
                        run.font.color.rgb = RGBColor(0, 0, 255)  # Зеленый цвет (R, G, B)                    
            isFirstPass = False
        #break # для целей тестирования

    return doc


def check_ischanged(data):
    #if not data:
        #print('Пустой список - False')
        #return False
    #print(data)
    for item in data:
        #print(item)
        #if not isinstance(item, dict):
            #print("В списке найден элемент, не являющийся словарём - False")
            #return False
        if item.get('IsChanged') == 1:
            #print("Найден элемент с IsChanged == 1")
            return True

    #print("нет IsChanged == 1")
    return False


if __name__ == "__main__":

    generate_settings()
