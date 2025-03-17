import time

from lib._TIMERS.TIMERS import TP_with_R

# Создаем таймер
tp = TP_with_R()
tp.set_PT(5)  # Устанавливаем время импульса 5 секунд

# Пример работы таймера
tp.IN = True  # Включаем вход
tp.R = False  # Сброс не активен

mode = ((0,0), (0,0), (1,0), (1,0), (1,0), (1,0), (0,0), (0,0), (0,0), (0,1), (0,1), (1,1), (1,1), (1,1), (1,0), (0,0), (0,0), (1,0), (1,0), (0,0), (0,0), (0,0), (0,0), (0,0))


for item in mode:
    tp.IN = item[0]
    tp.R = item[1]
    q, et = tp.start()
    print(f"Q: {q}, ET: {et}")
    time.sleep(1)    

