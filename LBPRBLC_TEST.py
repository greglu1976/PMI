# Орган блокировки ЛЗШ (БЛЗШ) (LBPRBLC) RBLC1
# SGF1 - БлокЛЗШ_выбор_ст - Выбор ступени блокировки (Не предусмотрено/ 1 ступень/ 2 ступень/ 3 ступень)

import time
import pandas as pd
from openpyxl import Workbook
from LBPRBLC import LBPRBLC

# Создаем экземпляр класса LBPRBLC
lbprblc = LBPRBLC(SGF1=3)

# Определяем возможные входные значения для тестирования
input_values = {
    "mtz1_pusk": [0, 1],
    "mtz2_pusk": [0, 1 ],
    "mtz3_pusk": [0, 1],
}

# Генерация всех возможных комбинаций входных значений
import itertools

# Создаем DataFrame для хранения результатов
columns = list(input_values.keys()) + [
     "blok", 
]

results = []

# Перебираем все комбинации входных значений
for inputs in itertools.product(*input_values.values()):
    input_dict = dict(zip(input_values.keys(), inputs))
    
    # Вызываем метод Step
    result =lbprblc.Step(
        mtz1_pusk=input_dict["mtz1_pusk"],
        mtz2_pusk=input_dict["mtz2_pusk"],
        mtz3_pusk=input_dict["mtz3_pusk"],
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