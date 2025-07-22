import os
import pandas as pd

# Корневая папка
root_path = 'pmi_mtzt'

# Поиск всех папок, содержащих строку 'modes'
for root, dirs, files in os.walk(root_path):
    if 'modes' in root:
        for filename in files:
            if filename.endswith(".xlsx"):
                file_path = os.path.join(root, filename)
                
                # Загрузка файла Excel
                with pd.ExcelFile(file_path) as xls:
                    # Создаем словарь для хранения данных всех листов
                    sheets_dict = {}
                    
                    # Обработка всех листов
                    for sheet_name in xls.sheet_names:
                        df = pd.read_excel(xls, sheet_name=sheet_name)
                        
                        # Если это лист SGF_Parameters, добавляем новые столбцы
                        #if sheet_name == 'SGF_Parameters':
                            #new_columns = ['SGF11_lvalh', 'SGF12_lvalh', 'SGF13_lvalh', 'SGF14_lvalh']
                            #for col in new_columns:
                                #df[col] = 0
                                
                        # Если это лист Settings, добавляем новый столбец
                        if sheet_name == 'Settings':
                            new_columns = ['T1_ptrc1_ttoclgc',]
                            for col in new_columns:
                                df[col] = 1



                        sheets_dict[sheet_name] = df
                    
                    # Сохраняем изменения обратно в файл Excel
                    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                        for sheet_name, df in sheets_dict.items():
                            df.to_excel(writer, sheet_name=sheet_name, index=False)