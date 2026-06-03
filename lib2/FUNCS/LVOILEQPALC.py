# Логика ступени ЗПО (ЗПО) (LVOILEQPALC) PALC1

# SGF1 - Ввод _функции - Ввод функции в работу (Не предусмотрено/ Предусмотрено)
# SGF2 - Контр_тока - Контроль тока от токовых органов ЗПО (Не предусмотрено/ Предусмотрено)
# SGF3 - Контр_темп - Контроль температуры от датчика температуры (Не предусмотрено/ Предусмотрено)
# Т1 - Тср - Выдержка времени срабатывания 

from lib2.TIMERS.TIMERS import TON

class LVOILEQPALC:
    def __init__(self, SGF1, SGF2, SGF3, T1):
        self.SGF1 = SGF1
        self.SGF2 = SGF2
        self.SGF3 = SGF3              
        self.T1 = TON()
        self.T1.set_PT(T1)

    def Step(self, VYVOD, OV, NaSign, otkaz_so, ToZpoPusk, t_masla_zpo):

        vvod = (not(OV or VYVOD)) and (self.SGF1==1) # ЗПО: Ввод
        oper_vyvod = (OV or VYVOD) and (self.SGF1==1) # ЗПО: Оперативный вывод

        pusk = vvod and otkaz_so and (1 if self.SGF2==0 else ToZpoPusk) and (1 if self.SGF3==0 else t_masla_zpo)
           
        self.T1.IN = pusk
        srabsign, ET = self.T1.start()  # Запускаем таймер и получаем выход и прошедшее время 
        srab = not(NaSign) and srabsign

        return vvod, oper_vyvod, pusk, srabsign, srab, ET
 
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
    def set_T1(self, T):
        self.T1.set_PT(T)  # Устанавливаем предустановленное время таймера

if __name__ == "__main__":
    f = LVOILEQPALC(SGF1=1, T1=0, Iset=1)
    res = f.Step(0,0,0,0,0,0)
    print(res)