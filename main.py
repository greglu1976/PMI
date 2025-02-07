import time
from TECHPTRC import TECHPTRC

PTRC1 = TECHPTRC(SGF1=1, SGF2=0)

try:
    while True:
        # Здесь можно задать значения для входных параметров
        OVGZ = 0           # Пример значения
        VYVOD = 0          # Пример значения
        GZnasign = 0       # Пример значения
        otklKontGazRele = 1 # Пример значения
        srabKI = 1         # Пример значения
        Sbros = 0          # Пример значения

        # Выполнить шаг PLC
        outputs = PTRC1.Step(OVGZ, VYVOD, GZnasign, otklKontGazRele, srabKI, Sbros)
        print("Выходы:", 'ЛО ГЗоткл / ЛО: Ввод>', outputs[0])  # Печать выходных значений
        
        time.sleep(1)  # Задержка на 1 секунду для имитации циклической работы
except KeyboardInterrupt:
    print("Остановка....")