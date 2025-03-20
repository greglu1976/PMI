# Орган КПОН в составе МТЗ трансформатора - VCPTUV
# SGF1 - Реж_пуска - Режим пуска (По Uмин/ Комбинированный/ Внешний)

import time
import pandas as pd
from openpyxl import Workbook
from VCPTUV import VCPTUV

# Создаем экземпляр класса VCPTUV
vcptuv = VCPTUV(SGF1=2, Uop=40, U2op=5)

# Определяем возможные входные значения для тестирования
input_values = {
    "VVOD": [1,],
    "KPONvnesh": [1, ],
    "UAB": [50, ],
    "UBC": [50,],
    "UCA": [50, ],
    "U2": [4, 10, 50 ],
}

# Генерация всех возможных комбинаций входных значений
import itertools

# Создаем DataFrame для хранения результатов
columns = list(input_values.keys()) + [
     "kpon_pusk", 
]

results = []

# Перебираем все комбинации входных значений
for inputs in itertools.product(*input_values.values()):
    input_dict = dict(zip(input_values.keys(), inputs))
    
    # Вызываем метод Step
    result = vcptuv.Step(
        VVOD=input_dict["VVOD"],
        KPONvnesh=input_dict["KPONvnesh"],
        UAB=input_dict["UAB"],
        UBC=input_dict["UBC"],
        UCA=input_dict["UCA"],
        U2=input_dict["U2"],
    )
    
    # Сохраняем результаты
    results.append(list(input_dict.values()) + list(result))
    # Добавление временной задержки между итерациями
    time.sleep(0.1)

# Создаем DataFrame из результатов
df = pd.DataFrame(results, columns=columns)

# Сохраняем результаты в файл Excel
output_file = "test_results.xlsx"
df.to_excel(output_file, index=False, engine="openpyxl")

print(f"Результаты сохранены в файл: {output_file}")