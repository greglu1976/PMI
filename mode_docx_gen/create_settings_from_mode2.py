import pandas as pd
import json
import glob
import os
import re
import numpy as np  # Для проверки типов данных

def parse_sgf(input_str):
    # Проверяем наличие '__' для выделения part
    if '__' in input_str:
        # Разделяем строку на две части по '__'
        main_part, part = input_str.rsplit('__', 1)  # Берём последнее вхождение '__'
        part = part.strip('_')  # Удаляем лишние '_'
    else:
        # Если '__' нет, то part пустой
        main_part = input_str
        part = ''

    result = main_part.split('_')
    
    if len(result)==3:
        switch = result[0]
        func = result[1]
        fb = result[2]
    else:
        switch = result[0]
        func = ''
        fb = result[1]

    return {'switch': switch, 'func': func, 'fb': fb, 'part': part}

def load_and_find_data(data, result_dict, set_value, root_dir = ''):
    # Извлекаем значения из словаря
    switch = data['switch']
    func = data['func']
    fb = data['fb']
    part = data['part'] if data['part'] != '' else root_dir+'part'

    # Формируем путь к файлу
    file_path = os.path.join(part, fb, func, '*.xlsx')
    #print(f"Ищем файл по пути: {file_path}")
    
    # Ищем файл по шаблону
    files = glob.glob(file_path)
    if not files:
        print('>>>>', data)
        print(f"Файл не найден по пути: {file_path}")
        return

    # Загружаем первый найденный файл
    file_path = files[0]
    df = pd.read_excel(file_path, sheet_name='Signals')

    if 'SGF' in switch:
        # Ищем значение в столбце 'AppliedDescription'
        row = df[df['AppliedDescription'] == switch]
        if row.empty:
            print(f"Значение '{switch}' не найдено в столбце 'AppliedDescription'")
            return
    else:
        row = df[df['alias'] == switch]
        if row.empty:
            print(f"Значение '{switch}' не найдено в столбце 'alias'{file_path}")
            return
    # Извлекаем нужные столбцы и преобразуем numpy.int64 в стандартные типы Python
    result = {
        'ShortDescription': str(row['ShortDescription'].values[0]),  # Преобразуем в строку
        'FullDescription': str(row['FullDescription (Описание параметра для пояснения в ПО ЮНИТ Сервис)'].values[0]),
        'Note': str(row['Note (Справочная информация)'].values[0]),
        'DefaultValue': str(row['DefaultValue'].values[0]),
        'AppliedDescription': str(row['AppliedDescription'].values[0]),
        'units': str(row['units'].values[0]),
        'minValue': str(row['minValue'].values[0]),
        'maxValue': str(row['maxValue'].values[0]),
        'step': str(row['step'].values[0]),        
        'SetValue': str(set_value) if pd.notna(set_value) else None,
        'Color': 'norm'
    }

    # Добавляем данные в структуру словарей
    if fb not in result_dict:
        result_dict[fb] = {}
    if func not in result_dict[fb]:
        result_dict[fb][func] = {}
    result_dict[fb][func][switch] = result

# Функция для преобразования numpy.int64 в стандартные типы Python
def convert_numpy_types(obj):
    if isinstance(obj, (np.int64, np.int32)):
        return int(obj)
    elif isinstance(obj, (np.float64, np.float32)):
        return float(obj)
    elif isinstance(obj, dict):
        return {k: convert_numpy_types(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy_types(v) for v in obj]
    else:
        return obj

def merge_dicts(dict1, dict2):
    for key, value in dict2.items():
        # Если ключ уже есть в dict1 и значение является словарём
        if key in dict1 and isinstance(dict1[key], dict) and isinstance(value, dict):
            merge_dicts(dict1[key], value)
        else:
            # Добавляем ключ с его значением (или перезаписываем, если ключ совпадает)
            dict1[key] = value
    return dict1

def start_proceed_modes(xlsx_file, root_dir=''):

    # Извлекаем базовое имя файла без расширения
    base_name = os.path.splitext(os.path.basename(xlsx_file))[0]
    output_dir = os.path.dirname(xlsx_file)  # Директория входного файла
    output_file = os.path.join(output_dir, f"{base_name}.json")  # Формируем путь к выходному файлу

    # Путь к файлу Excel
    #xlsx_file = '1.xlsx'
    #sheet_name = 'SGF_Parameters'
    sheet_name = 'Settings'

    # Считываем заголовки и первую строку данных
    df = pd.read_excel(xlsx_file, sheet_name=sheet_name, nrows=1)

    # Создаем структуру для хранения результатов
    result_dict = {}

    # Обрабатываем каждый заголовок и соответствующее значение из первой строки
    for column in df.columns:
        parsed_data = parse_sgf(column)
        set_value = df[column].values[0]  # Значение из первой строки
        #print(f"Обрабатываем заголовок: {column}, значение: {set_value}")
        #print(f"Результат парсинга: {parsed_data}")
        load_and_find_data(parsed_data, result_dict, set_value, root_dir)

    # Преобразуем все numpy.int64 в стандартные типы Python
    settings_result_dict = convert_numpy_types(result_dict)

    # Выводим итоговую структуру
    #print(json.dumps(settings_result_dict, indent=4, ensure_ascii=False))

    # Сохраняем результат в JSON-файл
    #with open('settings.json', 'w', encoding='utf-8') as f:
        #json.dump(settings_result_dict, f, indent=4, ensure_ascii=False)

    #print("Результат сохранен в файл 'settings.json'")

    sheet_name = 'SGF_Parameters'

    # Считываем заголовки и первую строку данных
    df = pd.read_excel(xlsx_file, sheet_name=sheet_name, nrows=1)

    # Создаем структуру для хранения результатов
    result_dict = {}

    # Обрабатываем каждый заголовок и соответствующее значение из первой строки
    for column in df.columns:
        parsed_data = parse_sgf(column)
        set_value = df[column].values[0]  # Значение из первой строки
        #print(f"Обрабатываем заголовок: {column}, значение: {set_value}")
        #print(f"Результат парсинга: {parsed_data}")
        load_and_find_data(parsed_data, result_dict, set_value, root_dir)

    # Преобразуем все numpy.int64 в стандартные типы Python
    sgfs_result_dict = convert_numpy_types(result_dict)

    # Выводим итоговую структуру
    #print(json.dumps(sgfs_result_dict, indent=4, ensure_ascii=False))

    # Сохраняем результат в JSON-файл
    #with open('sgfs.json', 'w', encoding='utf-8') as f:
        #json.dump(sgfs_result_dict, f, indent=4, ensure_ascii=False)

    #print("Результат сохранен в файл 'sgfs.json'")

    result_dict = merge_dicts(sgfs_result_dict, settings_result_dict)

    # Сохраняем результат в JSON-файл
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result_dict, f, indent=4, ensure_ascii=False)

    print(f"Результат сохранен в файл {output_file}")

    #print(json.dumps(data, indent=4, ensure_ascii=False))  # Выводим данные с форматированием

