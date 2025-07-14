# Для тестирования генератора уставок
# потом удалить

def generate_settings2(doc, parsed_assembly, part_of_modes_dir, part_of_modes_list):
    

    for item in part_of_modes_list:
        #print(item.modes.data)
        for datum in item.modes.data:
            print(datum.mode_data.mode_name) 
            print(datum.mode_data.sgf_parameters)            
            print(datum.mode_data.settings)   


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

def generate_settings(doc, parsed_assembly, part_of_modes_dir, part_of_modes_list):

    final_result = {}  # Итоговый результат для всех секций

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
        print(result)
        break

        final_result[section['section_name']] = result  # Добавляем результат секции в общий словарь
    #print(final_result)
    return final_result




if __name__ == "__main__":

    generate_settings()
