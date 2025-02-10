from TIMERS import TON  
from TRIGGERS import SRTrigger

import time

from TECHPTRC import TECHPTRC

# Параметры для тестирования
deltaT = 0.5
steps = 10  # Количество итераций
inputs = [(0, 0, 0, 0, 0, 0), (0, 0, 0, 1, 0, 0),
          (0, 0, 0, 1, 1, 0), (0, 1, 0, 1, 1, 0),
          (1, 0, 0, 1, 1, 0), (0, 0, 0, 1, 1, 0),
          (0, 0, 1, 0, 1, 0)]  # Примеры состояний входов

# Создаем объект класса
tech_ptrc = TECHPTRC(SGF1=1, SGF2=1, T=1.5)  # Таймер на 5 секунд

# Инициализируем таблицу истинности
truth_table = []

# Симуляция
for step in range(steps):
    # Получаем текущее состояние входов
    OV, VYVOD, NaSign, srabKont, srabKI, Sbros = inputs[step % len(inputs)]
    
    # Вызываем метод Step и получаем результаты
    results = tech_ptrc.Step(OV, VYVOD, NaSign, srabKont, srabKI, Sbros)
    
    # Записываем входы и их результаты
    truth_table.append({
        'OV': OV,
        'VYVOD': VYVOD,
        'NaSign': NaSign,
        'srabKont': srabKont,
        'srabKI': srabKI,
        'Sbros': Sbros,
        'vvod': results[0],
        'oper_vyvod': results[1],
        'srab': results[2],
        'srabsign': results[3],
        'zablok': results[4],
        'ET': results[5]
    })
    
    # Задержка по времени
    time.sleep(deltaT)

# Вывод таблицы истинности
print("Таблица истинности:")
for entry in truth_table:
    print(entry)

