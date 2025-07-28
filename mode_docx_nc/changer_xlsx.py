import os
import pandas as pd

# Корневая папка
root_path = 'pmi_lot2'

# Поиск всех папок, содержащих строку 'modes'
for root, dirs, files in os.walk(root_path):
    if 'modes' in root:
        for filename in files:
            if filename.endswith(".xlsx"):
                file_path = os.path.join(root, filename)
                
                # Загрузка файла Excel
                with pd.ExcelFile(file_path) as xls:
                    # Обработка обоих листов
                    for sheet_name in ['SGF_Parameters', 'Settings']:
                        if sheet_name in xls.sheet_names:
                            df = pd.read_excel(xls, sheet_name=sheet_name)
                            
                            # Поиск столбцов содержащих '_rblc1_tofflvlgc'
                            target_columns = [col for col in df.columns 
                                            if '_lvtcboff2' in col]
                            
                            if target_columns:
                                # Переименование столбцов
                                renamed_columns = {
                                    col: col.replace('_lvtcboff2', '_lvtrescboff2') 
                                    for col in target_columns
                                }
                                
                                df.rename(columns=renamed_columns, inplace=True)
                                
                                # Сохранение изменений
                                with pd.ExcelWriter(file_path, engine='openpyxl', mode='a',
                                                  if_sheet_exists='replace') as writer:
                                    df.to_excel(writer, sheet_name=sheet_name, index=False)
                                    
                                print(f"Файл {file_path} (лист '{sheet_name}') обновлен:")
                                for old, new in renamed_columns.items():
                                    print(f"  {old} -> {new}")
                            else:
                                print(f"В файле {file_path} (лист '{sheet_name}') не найдены целевые столбцы.")
                        else:
                            print(f"Лист '{sheet_name}' не найден в файле {file_path}.")