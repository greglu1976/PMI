import pandas as pd
import itertools
import time
from TIMERS import TON  

class TECHPTRC:
    def __init__(self, state=0, SGF1=0, SGF2=0, T=0):
        self.state = state  # Начальное состояние триггера
        self.SGF1 = SGF1
        self.SGF2 = SGF2
        self.T1 = TON()
        self.T1.set_PT(T)

    def RS(self, set, reset):
        if set and not reset:
            self.state = 1
        elif reset:
            self.state = 0
        return self.state

    def Step(self, OVGZ, VYVOD, GZnasign, otklKontGazRele, srabKI, Sbros):
        self.T1.IN = srabKI
        Q, ET = self.T1.start()

        vvod = (not(OVGZ or VYVOD)) and (self.SGF1 == 1)
        oper_vyvod = (OVGZ or VYVOD) and (self.SGF1 == 1)

        zablok = 0 if (self.SGF2 == 0) else self.RS(Q and vvod, not(vvod) or Sbros)
        srabsign = vvod and otklKontGazRele and not(zablok)
        srab = not(GZnasign) and srabsign

        return vvod, oper_vyvod, srab, srabsign, zablok, ET

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
        #time.sleep(1)  # Задержка на 1 секунду

    # Создание DataFrame из данных
    columns = inputs + ["ЛО: Ввод", "ЛО: Оперативный вывод", "ЛО: Срабатывание", "ЛО: Срабатывание сигн", "Заблокировано", "ET"]
    df = pd.DataFrame(results_data, columns=columns)

    # Сохранение в файл Excel
    df.to_excel(filename, index=False, engine='openpyxl')
    print(f"Таблица истинности сохранена в {filename}")

# Вызов функции для генерации и сохранения таблицы истинности в XLSX
generate_truth_table_to_excel('truth_table.xlsx')
