# для отключающей ступени ГЗ с префиксом f_

from lib._TIMERS.TIMERS import TON  
from lib._TRIGGERS.TRIGGERS import SRTrigger

class TECHPTRC:
    def __init__(self, SGF1=0, SGF2=0, T=0):
        self.SGF1 = SGF1
        self.SGF2 = SGF2
        self.T1 = TON()
        self.T1.set_PT(T)
        self.SR = SRTrigger(state=0)

    def Step(self, OV, VYVOD, NaSign, srabKont, srabKI, Sbros):
        self.T1.IN = srabKI
        Q, ET = self.T1.start()  # Запускаем таймер и получаем выход и прошедшее время
        vvod = (not(OV or VYVOD)) and (self.SGF1==1)
        oper_vyvod = (OV or VYVOD) and (self.SGF1==1)
        zablok = 0 if (self.SGF2==0) else self.SR.run(Q and vvod, not(vvod) or Sbros)
        srabsign = vvod and srabKont and not(zablok)
        srab = not(NaSign) and srabsign
        return vvod, oper_vyvod, srab, srabsign, zablok, ET

        # Геттер для SGF1
    def get_SGF1(self):
        return self.SGF1
    # Сеттер для SGF1
    def set_SGF1(self, value):
        self.SGF1 = value
    # Геттер для SGF2
    def get_SGF2(self):
        return self.SGF2
    # Сеттер для SGF2
    def set_SGF2(self, value):
        self.SGF2 = value
        # Геттер для времени таймера
    def get_T1(self):
        return self.T1.PT  # Предустановленное время таймера
    # Сеттер для времени таймера
    def set_T1(self, T):
        self.T1.set_PT(T)  # Устанавливаем предустановленное время таймера