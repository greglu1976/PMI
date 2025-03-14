# Функция токовой отсечки

#SGF1 - Ввод_функции - Ввод функции в работу (Не предусмотрено/ Предусмотрено)
#SGF2 - Сборка_ток_цепей - Сборка токовых цепей (Звезда/ Треугольник)

from lib._TIMERS.TIMERS import TON  
from lib._TRIGGERS.TRIGGERS import RSTrigger

class LVPTOC:
    def __init__(self, SGF1, SGF2, T1, Iset):
        self.SGF1 = SGF1
        self.SGF2 = SGF2
        self.Iset = Iset
        self.T1 = TON()
        self.T1.set_PT(T1)
        self.RS = RSTrigger(state=0)

    def Step(self, VYVOD, OV, NaSign, IA, IB, IC, IAB, IBC, ICA):

        vvod = (not(OV or VYVOD)) and (self.SGF1==1) # ТО: Ввод
        oper_vyvod = (OV or VYVOD) and (self.SGF1==1) # ТО: Оперативный вывод

        # Переключение с фазных на линейные токи
        Ia = IA if (self.SGF1==0) else IAB
        Ib = IB if (self.SGF1==0) else IBC
        Ic = IC if (self.SGF1==0) else ICA

        I = max(Ia, Ib, Ic)
        io = (self.SGF1==1) and (self.RS.run((I>=self.Iset), (I<0.95*self.Iset)))
        pusk = vvod and io

        self.T1.IN = pusk
        srabsign, ET = self.T1.start()  # Запускаем таймер и получаем выход и прошедшее время   
        srab = srabsign and (not NaSign)     

        return vvod, oper_vyvod, pusk, io, srabsign, srab, ET
 
    # Геттеры и сеттеры
    def get_SGF1(self):
        return self.SGF1
    def set_SGF1(self, value):
        self.SGF1 = value
    def get_SGF2(self):
        return self.SGF2
    def set_SGF2(self, value):
        self.SGF2 = value

    def get_T1(self):
        return self.T1.PT  # Предустановленное время таймера
    # Сеттер для времени таймера
    def set_T1(self, T):
        self.T1.set_PT(T)  # Устанавливаем предустановленное время таймера

if __name__ == "__main__":
    ptoc1 = LVPTOC(SGF1=1, SGF2=0, T1=0, Iset=1)
    res = ptoc1.Step(0,0,0,0,0,0,0,0,0)
    print(res)