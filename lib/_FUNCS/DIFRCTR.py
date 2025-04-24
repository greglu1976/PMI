# Функция КЦТст1-3 - контроль исправности токовых цепей стороны 1 (2,3) RCTR2-6:DIFRCTR_UIRZ

# SGF1 - Ввод_функции - Ввод функции в работу (Не предусмотрено/ Предусмотрено)
# SGF2 - Контр_обр_пров - Режим контроля обрыва провода (Не предусмотрено/ Предусмотрено)


from lib._TIMERS.TIMERS import TON  
from lib._TRIGGERS.TRIGGERS import RSTrigger

class DIFRCTR:
    def __init__(self, SGF1, SGF2, T1, T2, Inom, Imin, Ksym, LIsym):
        self.SGF1 = SGF1
        self.SGF2 = SGF2
        self.Inom = Inom
        self.Imin = Imin
        self.Ksym = Ksym
        self.LIsym = LIsym
        self.T1 = TON()
        self.T1.set_PT(T1)
        self.T2 = TON()
        self.T2.set_PT(T2)
        self.RSmin = RSTrigger(state=0)
        self.RSminmax = RSTrigger(state=0)
        self.RSmax = RSTrigger(state=0)

    def Step(self, VYVOD, OV, OVst, IA, IB, IC):

        vvod = (not(OV or VYVOD or OVst)) and (self.SGF1==1) # КЦТст: Ввод
        oper_vyvod = (OV or VYVOD or OVst) and (self.SGF1==1) # КЦТст: Оперативный вывод

        Imax = max(IA, IB, IC)
        Imin = min(IA, IB, IC)
        _rat = Imin/Imax

        io_max = self.RSmax.run((Imax>=self.LIsym), (Imax<0.95*self.LIsym))
        io_min = self.RSmin.run((Imin<=self.Imin), (Imin>1.05*self.Imin))
        io_minmax = self.RSminmax.run((_rat<=self.Ksym), (_rat>1.05*self.Ksym))

        pusk_assym = vvod and io_max and io_minmax
        self.T2.IN = pusk_assym
        srab_assym, ETa = self.T2.start()  

        pusk_obryv = self.SGF2==1 and io_min and pusk_assym
        self.T1.IN = pusk_obryv
        srab_obryv, ETo = self.T1.start() 

        return vvod, oper_vyvod, pusk_obryv, srab_obryv, pusk_assym, srab_assym

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
    def set_T1(self, T):
        self.T1.set_PT(T)  # Устанавливаем предустановленное время таймера
    def get_T2(self):
        return self.T2.PT  # Предустановленное время таймера
    def set_T2(self, T):
        self.T2.set_PT(T)  # Устанавливаем предустановленное время таймера


if __name__ == "__main__":
    rtcr1 = DIFRCTR(SGF1=1, SGF2=0, T1=0, T2=0, Inom=1, Imin=0.5, Ksym=0.5, LIsym=1)
    res = rtcr1.Step(VYVOD=0, OV=0, OVst=0, IA=1, IB=1, IC=1)
    print(res)