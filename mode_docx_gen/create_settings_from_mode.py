#
# Получаем файл 1.xlsx
# считываем заголовки и ищем искомое значение каждого столбца

import pandas as pd
import json

import glob, os
import re

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

    # Регулярное выражение для парсинга оставшейся части (switch, func, fb)
    pattern = r'^(?P<switch>SGF\d+)_?(?P<func>\w+)?_(?P<fb>\w+)$'
    
    # Поиск совпадений с игнорированием регистра
    match = re.match(pattern, main_part, re.IGNORECASE)
    
    if match:
        # Извлечение групп
        result = {
            'switch': match.group('switch').upper(),  # Преобразуем switch в верхний регистр
            'func': match.group('func') or '',       # Если func отсутствует, вернуть пустую строку
            'fb': match.group('fb') or '',          # Например, 'toc'
            'part': part                            # Добавляем part
        }
        return result
    else:
        # Если строка не соответствует шаблону, вернуть пустой словарь или обработать ошибку
        return {'switch': '', 'func': '', 'fb': '', 'part': ''}

def load_and_find_data(data):
    # Извлекаем значения из словаря
    switch = data['switch']
    func = data['func']
    fb = data['fb']
    part = part if data['part']!='' else 'part'

    # Формируем путь к файлу
    file_path = os.path.join(part, fb, func, '*.xlsx')
    print(file_path)
    # Ищем файл по шаблону
    files = glob.glob(file_path)
    if not files:
        print(f"Файл не найден по пути: {file_path}")
        return

    # Загружаем первый найденный файл
    file_path = files[0]
    df = pd.read_excel(file_path, sheet_name='Signals')

    # Ищем значение в столбце 'AppliedDescription'
    row = df[df['AppliedDescription'] == switch]
    if row.empty:
        print(f"Значение '{switch}' не найдено в столбце 'AppliedDescription'")
        return

    # Извлекаем нужные столбцы
    result = {
        'ShortDescription': row['ShortDescription'].values[0],
        'FullDescription': row['FullDescription (Описание параметра для пояснения в ПО ЮНИТ Сервис)'].values[0],
        'Note': row['Note (Справочная информация)'].values[0]
    }

    # Выводим результат на экран
    print(result)


# Путь к файлу Excel
xlsx_file = '1.xlsx'

sheet_name='SGF_Parameters' 

# Функция для чтения заголовков с указанного листа и сохранения их в JSON-файл
# Считываем только строку заголовков с указанного листа
df = pd.read_excel(xlsx_file, sheet_name=sheet_name, nrows=0)
# Преобразуем заголовки в словарь, где значения равны пустой строке
headers_dict = {column: "" for column in df.columns}

for column in df.columns:
    #print(column)
    print(parse_sgf(column))
    t = parse_sgf(column)
    load_and_find_data(t)




