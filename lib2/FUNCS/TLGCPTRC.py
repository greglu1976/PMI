# Логическая защита трансформатора (ЛЗТ) (TLGCPTRC) PTRC1

# SGF1 - Ввод _функции - Ввод функции в работу (Не предусмотрено/ Предусмотрено)
# SGF2 - Пуск_от_МТЗ-2 - Пуск от МТЗ 2 ступени (Не предусмотрено/ Предусмотрено)
# SGF3 - Пуск_от_МТЗ-3 - Пуск от МТЗ 3 ступени (Не предусмотрено/ Предусмотрено)
# Т1 - Тср - Выдержка времени срабатывания 

from lib2.TIMERS.TIMERS import TON

class PHSTRPTOC_T:
    def __init__(self, SGF1, SGF2, SGF3, T1):
        self.SGF1 = SGF1
        self.SGF2 = SGF2
        self.SGF3 = SGF3              
        self.T1 = TON()
        self.T1.set_PT(T1)

    def Step(self, VYVOD, OV, vnesh_pusk, mtz2_pusk, mtz3_pusk, blok_lzt):

        vvod = (not(OV or VYVOD)) and (self.SGF1==1) # ЛЗТ: Ввод
        oper_vyvod = (OV or VYVOD) and (self.SGF1==1) # ЛЗТ: Оперативный вывод

        pusk = vvod and not(blok_lzt) and (vnesh_pusk or (mtz2_pusk if self.SGF2==1 else 0) or (mtz3_pusk if self.SGF3==1 else 0))     
        self.T1.IN = pusk
        srab, ET = self.T1.start()  # Запускаем таймер и получаем выход и прошедшее время  
        return vvod, oper_vyvod, pusk, srab, ET
 
    # Геттеры и сеттеры
    def get_SGF1(self):
        return self.SGF1
    def set_SGF1(self, value):
        self.SGF1 = value
    def get_SGF2(self):
        return self.SGF2
    def set_SGF2(self, value):
        self.SGF2 = value
    def get_SGF3(self):
        return self.SGF3
    def set_SGF3(self, value):
        self.SGF3 = value

    def get_T1(self):
        return self.T1.PT  # Предустановленное время таймера
    # Сеттер для времени таймера
    def set_T1(self, T):
        self.T1.set_PT(T)  # Устанавливаем предустановленное время таймера

if __name__ == "__main__":
    f = PHSTRPTOC_T(SGF1=1, T1=0, Iset=1)
    res = f.Step(0,0,0,0,0,0)
    print(res)