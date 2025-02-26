import os
import json
from natsort import natsorted  # Для естественной сортировки

def compare_and_update(prev_data, curr_data):
    """
    Сравнивает два словаря и обновляет поле 'Color' при необходимости.
    """
    def recursive_compare(prev, curr):
        for key in curr:
            if key not in prev:  # Если ключа нет в предыдущих данных, пропускаем
                continue
            
            if isinstance(curr[key], dict):  # Рекурсивный спуск для вложенных словарей
                recursive_compare(prev[key], curr[key])
            else:
                # Сравниваем значения полей
                if key == "SetValue" and prev.get(key) != curr.get(key):
                    # Если значение изменилось, меняем цвет
                    curr["Color"] = "changed"
    
    # Вызываем рекурсивное сравнение
    recursive_compare(prev_data, curr_data)

def start_analyze(folder_path):
# Путь к папке с файлами
#folder_path = 'modes2'

    # Получаем список файлов в папке и сортируем их в естественном порядке
    file_list = [f for f in os.listdir(folder_path) if f.endswith('.json')]
    file_list = natsorted(file_list)

    # Переменная для хранения предыдущего состояния данных
    previous_data = None

    # Обработка каждого файла
    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)
        
        # Считываем данные из файла
        with open(file_path, 'r', encoding='utf-8') as file:
            current_data = json.load(file)
        
        # Если есть предыдущие данные, сравниваем их с текущими
        if previous_data:
            compare_and_update(previous_data, current_data)
        
        # Сохраняем измененные данные обратно в файл
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(current_data, file, ensure_ascii=False, indent=4)
        
        # Обновляем предыдущее состояние
        previous_data = current_data

