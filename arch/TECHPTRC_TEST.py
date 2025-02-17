# тестирование TECHPTRC

import pandas as pd
import itertools
import time
from lib._TIMERS.TIMERS import TON  
from lib.TECHPTRC.TECHPTRC import TECHPTRC

def generate_truth_table_to_excel(filename):
    inputs = ["ОВ ГЗоткл", "Вывод терминала", "ГЗоткл на сигн", "Откл.конт.газ. реле", "Сраб. КИ ГЗ_откл", "Сброс блок. ГЗ,ТЗ"]
    combinations = list(itertools.product([0, 1], repeat=len(inputs)))  # Используем 0 и 1

    # Создание списка для хранения результатов
    results_data = []

    # Инициализация класса для тестирования
    ptrc = TECHPTRC(SGF1=1, SGF2=1, T=0)

    for combination in combinations:
        results = ptrc.Step(*combination)
        # Преобразуем логические значения в 0 и 1
        results_data.append(list(combination) + [int(val) for val in results])
        
        # Добавление временной задержки между итерациями (например, 1 секунда)
        time.sleep(0.1)  # Задержка на 1 секунду

    # Создание DataFrame из данных
    columns = inputs + ["ЛО: Ввод", "ЛО: Оперативный вывод", "ЛО: Срабатывание", "ЛО: Срабатывание сигн", "Заблокировано", "ET"]
    df = pd.DataFrame(results_data, columns=columns)

    # Сохранение в файл Excel
    df.to_excel(filename, index=False, engine='openpyxl')
    print(f"Таблица истинности сохранена в {filename}")

def generate_truth_table_from_excel(input_filename, output_filename):
    # Читаем входные данные из Excel файла
    try:
        df_input = pd.read_excel(input_filename)
        inputs = df_input.columns.tolist()[:6]  # Получаем названия входных сигналов
    except Exception as e:
        print(f"Ошибка при чтении входного файла: {e}")
        return

    # Создание списка для хранения результатов
    results_data = []

    # Инициализация класса для тестирования
    ptrc = TECHPTRC(SGF1=1, SGF2=1, T=0)

    # Обработка каждой строки из входного файла
    for index, row in df_input.iterrows():
        try:
            # Получаем значения входов из текущей строки
            input_values = [row[input_name] for input_name in inputs]
            
            # Вызываем Step с значениями из файла
            results = ptrc.Step(*input_values)
            
            # Преобразуем логические значения в 0 и 1
            results_data.append(list(input_values) + [int(val) for val in results])
            
            # Добавление временной задержки между итерациями
            time.sleep(0.1)
        except Exception as e:
            print(f"Ошибка при обработке строки {index}: {e}")
            continue

    # Создание DataFrame из данных
    columns = inputs + ["ЛО: Ввод", "ЛО: Оперативный вывод", "ЛО: Срабатывание", 
                       "ЛО: Срабатывание сигн", "Заблокировано", "ET"]
    
    try:
        df_output = pd.DataFrame(results_data, columns=columns)
        # Сохранение в файл Excel
        df_output.to_excel(output_filename, index=False, engine='openpyxl')
        print(f"Таблица истинности сохранена в {output_filename}")
    except Exception as e:
        print(f"Ошибка при сохранении результатов: {e}")



# Вызов функции для генерации и сохранения таблицы истинности в XLSX
#generate_truth_table_to_excel('techptrc.xlsx')
generate_truth_table_from_excel('techptrc.xlsx', 'techptrc_truth_table.xlsx')
