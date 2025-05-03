# Вспомогательный скрипт зля замены определенного значения опряделенной ячейки в файле режима

import os
import pandas as pd

# Корневая папка
root_path = 'pmi_dzt'

# Поиск всех папок, содержащих строку 'modes'
for root, dirs, files in os.walk(root_path):
    if 'modes' in root:  # Проверка, содержит ли путь папки строку 'modes'
        # Поиск всех файлов .xlsx в текущей папке
        for filename in files:
            if filename.endswith(".xlsx"):
                file_path = os.path.join(root, filename)
                
                # Загрузка файла Excel
                with pd.ExcelFile(file_path) as xls:
                    if 'Settings' in xls.sheet_names:  # Проверка наличия листа 'Settings'
                        # Чтение листа 'Settings' в DataFrame
                        df = pd.read_excel(xls, sheet_name='Settings')
                        
                        # Проверка наличия столбца 'Ratio_phar1_lvttoc'
                        if 'Ubaz_rmxu1_tdif' in df.columns:
                            # Изменение значений в столбце 'Ratio_phar1_lvttoc' на 40
                            df['Ubaz_rmxu1_tdif'] = 35
                            
                            # Сохранение изменений обратно в файл
                            with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                                df.to_excel(writer, sheet_name='Settings', index=False)
                            
                            print(f"Файл {file_path} обновлен: столбец 'Ubaz_rmxu1_tdif' изменен.")
                        else:
                            print(f"Столбец 'Ubaz_rmxu1_tdif' не найден в файле {file_path}.")
                    else:
                        print(f"Лист 'Settings' не найден в файле {file_path}.")