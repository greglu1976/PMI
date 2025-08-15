import pandas as pd
import json

# Путь к файлу Excel
xlsx_file = '1.xlsx'

# Функция для чтения заголовков с указанного листа и сохранения их в JSON-файл
def save_headers_to_json(sheet_name, output_file):
    # Считываем только строку заголовков с указанного листа
    df = pd.read_excel(xlsx_file, sheet_name=sheet_name, nrows=0)
    
    # Преобразуем заголовки в словарь, где значения равны пустой строке
    headers_dict = {column: "" for column in df.columns}
    
    # Сохраняем словарь в JSON-файл
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(headers_dict, f, ensure_ascii=False, indent=4)

# Обработка листа "Inputs"
save_headers_to_json(sheet_name='Inputs', output_file='inputs.json')

# Обработка листа "Outputs"
save_headers_to_json(sheet_name='Outputs', output_file='outputs.json')

# Обработка листа "SGF"
save_headers_to_json(sheet_name='SGF_Parameters', output_file='sgfs.json')

# Обработка листа "SGF"
save_headers_to_json(sheet_name='Settings', output_file='settings.json')

print("Заголовки успешно сохранены...")