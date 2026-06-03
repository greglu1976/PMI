# Функция защиты от перегрузки ДЗТ2

#SGF1 - Ввод_функции - Ввод функции в работу (Не предусмотрено/ Предусмотрено)

from lib2.TIMERS.TIMERS import TON  
from lib2.TRIGGERS.TRIGGERS import RSTrigger

class PHPTOC:
    def __init__(self, SGF1, T1, Iset):
        self.SGF1 = SGF1
        self.Iset = Iset
        self.T1 = TON()
        self.T1.set_PT(T1)
        self.RS = RSTrigger(state=0)

    def Step(self, VYVOD, OV, OVst, NaOtkl, IA, IB, IC):

        vvod = (not(OV or VYVOD or OVst)) and (self.SGF1==1) # ТО: Ввод
        oper_vyvod = (OV or VYVOD or OVst) and (self.SGF1==1) # ТО: Оперативный вывод

        I = max(IA, IB, IC)
        io = (self.SGF1==1) and (self.RS.run((I>=self.Iset), (I<0.95*self.Iset)))
        pusk = vvod and io

        self.T1.IN = pusk
        srab, ET = self.T1.start()  # Запускаем таймер и получаем выход и прошедшее время   
        srabotkl = srab and NaOtkl     

        return vvod, oper_vyvod, pusk, io, srab, srabotkl, ET
 
    # Геттеры и сеттеры
    def get_SGF1(self):
        return self.SGF1
    def set_SGF1(self, value):
        self.SGF1 = value

    def get_T1(self):
        return self.T1.PT  # Предустановленное время таймера
    # Сеттер для времени таймера
    def set_T1(self, T):
        self.T1.set_PT(T)  # Устанавливаем предустановленное время таймера

if __name__ == "__main__":
    ptoc1 = PHPTOC(SGF1=1, T1=0, Iset=1)
    res = ptoc1.Step(0,0,0,0,0,0)
    print(res)