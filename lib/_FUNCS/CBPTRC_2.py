# для ЛО выключателя НН (с тремя (3) выводами функции)

from lib._TIMERS.TIMERS import TP

class CBPTRC:
    def __init__(self, SGF1=0, T1=0.5):
        self.SGF1 = SGF1
        self.T1 = TP()
        self.T1.set_PT(T1)

    def Step(self, VYVOD, OV, OV_st, LO_t_srab):
        vvod = (not(VYVOD or OV or OV_st)) and (self.SGF1==1)
        oper_vyvod = (VYVOD or OV or OV_st) and (self.SGF1==1)
        otkl = vvod and LO_t_srab
        self.T1.IN = otkl
        otkl_avar, ET_t1 = self.T1.start() 
        return vvod, oper_vyvod, otkl, otkl_avar

    def get_SGF1(self):
        return self.SGF1
    def set_SGF1(self, value):
        self.SGF1 = value

    def get_T1(self):
        return self.T1.PT  # Предустановленное время таймера
    def set_T1(self, T):
        self.T1.set_PT(T)  # Устанавливаем предустановленное время таймера        
 