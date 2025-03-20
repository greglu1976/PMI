# Орган выявления бросков тока намагничивания (БНТ) (TOCPHAR) PHAR1
# SGF1 - Перекрест_блок - Перекрестная блокировка (Не предусмотрено/ Предусмотрено)

import time
import pandas as pd
from openpyxl import Workbook
from TOCPHAR import TOCPHAR

# Создаем экземпляр класса TOCPHAR
tocphar = TOCPHAR(SGF1=1, Imax=2, Ratio=0.3)

# Определяем возможные входные значения для тестирования
input_values = {
    "VVOD": [1,],
    "mtz_ioA": [(1,), ],
    "mtz_ioB": [(0,), ],
    "mtz_ioC": [(0,), ],
    "IA": [1, 3 ],
    "IA2harm": [0.5, 2],
    "IB": [1, ],
    "IB2harm": [0,],
    "IC": [1, ],
    "IC2harm": [0,],
}

# Генерация всех возможных комбинаций входных значений
import itertools

# Создаем DataFrame для хранения результатов
columns = list(input_values.keys()) + [
     "ia_start_out", "ib_start_out", "ic_start_out", "start"
]

results = []

# Перебираем все комбинации входных значений
for inputs in itertools.product(*input_values.values()):
    input_dict = dict(zip(input_values.keys(), inputs))
    
    # Вызываем метод Step
    result = tocphar.Step(
        VVOD=input_dict["VVOD"],
        mtz_ioA=input_dict["mtz_ioA"],
        mtz_ioB=input_dict["mtz_ioB"],
        mtz_ioC=input_dict["mtz_ioC"],                
        IA=input_dict["IA"],
        IA2harm=input_dict["IA2harm"],
        IB=input_dict["IB"],
        IB2harm=input_dict["IB2harm"],
        IC=input_dict["IC"],
        IC2harm=input_dict["IC2harm"],
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