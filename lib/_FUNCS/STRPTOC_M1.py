# Функция контроля тока ЗДЗ

# SGF1 - Ввод_функции - Ввод функции в работу (Не предусмотрено/ Предусмотрено)

from lib._TIMERS.TIMERS import TON  
from lib._TRIGGERS.TRIGGERS import RSTrigger
from lib._ADD.threePhaseSys import ThreePhaseSystem # класс для расчета аналоговых значений 

class STRPTOC:
    def __init__(self, SGF1, SGF2, Iset, U0set, T1, T2):
        self.SGF1 = SGF1
        self.SGF2 = SGF2        
        self.Iset = Iset
        self.U0set = U0set
        self.T1 = TON()
        self.T1.set_PT(T1)
        self.T2 = TON()
        self.T2.set_PT(T2)
        self.RS_i = RSTrigger(state=0)
        self.RS_u = RSTrigger(state=0)

    def Step(self, OV, IA, IB, IC, UA1, dUA1, UB1, dUB1, UC1, dUC1, zdz1, zdz2):

        threeU1 = ThreePhaseSystem(UA1, dUA1, UB1, dUB1, UC1, dUC1)
        U1simm = threeU1.calculate_symmetric_components()
        U0_3u0 = U1simm['U0']['amplitude']

        vvod = not(OV) and (self.SGF1==1) # Ввод

        I = max(IA, IB, IC)
        io_i = self.RS_i.run((I>=self.Iset), (I<0.95*self.Iset))
        io_u = self.RS_u.run((U0_3u0>=self.U0set), (U0_3u0<0.95*self.U0set))

        obnaruzh_dugi = (zdz1 or zdz2) and vvod
        self.T2.IN = obnaruzh_dugi
        neisp, ET_n = self.T2.start()  

        _pusk =  vvod and (zdz1 or zdz2) and (io_i or io_u) and (not (neisp if self.SGF2==1 else 0))
        self.T1.IN = _pusk
        srab, ET_s = self.T1.start() 

        return vvod, obnaruzh_dugi, neisp, srab, U0_3u0
 
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
        return self.T1.PT
    def set_T1(self, T):
        self.T1.set_PT(T)

    def get_T2(self):
        return self.T2.PT
    def set_T2(self, T):
        self.T2.set_PT(T)