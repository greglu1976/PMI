import os
import pandas as pd

# Корневая папка
root_path = 'pmi_tokzdzt'

# Поиск всех папок, содержащих строку 'modes'
for root, dirs, files in os.walk(root_path):
    if 'modes' in root:
        for filename in files:
            if filename.endswith(".xlsx"):
                file_path = os.path.join(root, filename)
                
                # Загрузка файла Excel
                with pd.ExcelFile(file_path) as xls:
                    # Обработка листа Outputs
                    if 'Outputs' in xls.sheet_names:
                        df = pd.read_excel(xls, sheet_name='Inputs')
                        
                        # Проверка наличия столбца для переименования
                        if 'NaOtkl_hvptoc1_tovctoc' in df.columns:
                            # Переименование столбца
                            df.rename(columns={'NaOtkl_hvptoc1_tovctoc': 'NaOtkl_tovctoc'}, inplace=True)
                            
                            # Сохранение изменений
                            with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', 
                                               if_sheet_exists='replace') as writer:
                                df.to_excel(writer, sheet_name='Inputs', index=False)
                            
                            print(f"Файл {file_path} (лист 'Inputs') обновлен:")
                            print("  NaOtkl_hvptoc1_tovctoc -> NaOtkl_tovctoc")
                        else:
                            print(f"В файле {file_path} (лист 'Inputs') не найден столбец 'NaOtkl_hvptoc1_tovctoc'.")
                    else:
                        print(f"Лист 'Inputs' не найден в файле {file_path}.")