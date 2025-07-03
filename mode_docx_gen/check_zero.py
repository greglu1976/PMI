# Вспомогательный скрипт для просмотра файлов режимов и выдачи отчета , какие входы и выходы изменяются

import os
import pandas as pd
from collections import defaultdict

def check_non_zero_columns(dir_path, report_file='report.txt'):
    # Словарь для хранения данных: {путь_к_папке: {'Inputs': set(), 'Outputs': set()}}
    folder_report = defaultdict(lambda: {'Inputs': set(), 'Outputs': set()})
    
    for root, dirs, files in os.walk(dir_path):
        if 'modes' in root.lower():
            for file in files:
                if file.endswith('.xlsx'):
                    file_path = os.path.join(root, file)
                    try:
                        # Проверяем оба листа
                        for sheet_name in ['Inputs', 'Outputs']:
                            try:
                                df = pd.read_excel(file_path, sheet_name=sheet_name)
                                
                                # Находим ненулевые столбцы
                                non_zero_cols = [col for col in df.columns if (df[col] != 0).any()]
                                
                                # Добавляем в отчёт
                                if non_zero_cols:
                                    folder_report[root][sheet_name].update(non_zero_cols)
                            
                            except Exception as e:
                                print(f"Лист '{sheet_name}' не найден в файле {file_path} или ошибка чтения: {e}")
                    
                    except Exception as e:
                        print(f"Ошибка при обработке файла {file_path}: {e}")
    
    # Записываем отчёт
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("Отчет о ненулевых столбцах (сгруппировано по папкам):\n")
        f.write("=" * 70 + "\n")
        
        for folder, sheets in folder_report.items():
            f.write(f"Папка: {folder}\n")
            
            for sheet_name, columns in sheets.items():
                if columns:  # Выводим только если есть ненулевые столбцы
                    f.write(f"Лист '{sheet_name}': {', '.join(sorted(columns))}\n")
            
            f.write("-" * 70 + "\n")
    
    print(f"Отчёт сохранён в файл: {report_file}")

# Запуск
dir_path = 'pmi_lot2'
check_non_zero_columns(dir_path)