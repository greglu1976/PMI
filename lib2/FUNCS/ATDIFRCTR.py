# КЦТнеб- контроль исправности токовых цепей по небалансу в дифцепях RCTR1:ATDIFRCTR

# SGF1 - Ввод_функции - Ввод функции в работу (Не предусмотрено/ Предусмотрено)

from lib2.TIMERS.TIMERS import TON  
from lib2.TRIGGERS.TRIGGERS import RSTrigger

class ATDIFRCTR:
    def __init__(self, SGF1, T1, Iset):
        self.SGF1 = SGF1
        self.Iset = Iset
        self.T1a = TON()
        self.T1a.set_PT(T1)
        self.T1b = TON()
        self.T1b.set_PT(T1)
        self.T1c = TON()
        self.T1c.set_PT(T1)
        self.RSa = RSTrigger(state=0)
        self.RSb = RSTrigger(state=0)
        self.RSc = RSTrigger(state=0)

    def Step(self, VYVOD, OV, OVst, kzt_srab, IAdiff, IBdiff, ICdiff):

        vvod = (not(OV or VYVOD or OVst)) and (self.SGF1==1) # КЦТнеб: Ввод
        oper_vyvod = (OV or VYVOD or OVst) and (self.SGF1==1) # КЦТнеб: Оперативный вывод

        io_A = self.RSa.run((IAdiff>=self.Iset), (IAdiff<0.95*self.Iset))
        io_B = self.RSb.run((IBdiff>=self.Iset), (IBdiff<0.95*self.Iset))
        io_C = self.RSc.run((ICdiff>=self.Iset), (ICdiff<0.95*self.Iset))

        self.T1a.IN = io_A
        pusk_A, ETa = self.T1a.start() 
        self.T1b.IN = io_B
        pusk_B, ETb = self.T1b.start()     
        self.T1c.IN = io_C
        pusk_C, ETc = self.T1c.start() 

        srab_A = vvod and pusk_A
        srab_B = vvod and pusk_B
        srab_C = vvod and pusk_C

        srab = srab_A or srab_B or srab_C
        neispr = srab or kzt_srab

        return vvod, oper_vyvod, srab_A, srab_B, srab_C, srab, neispr
 
    # Геттеры и сеттеры
    def get_SGF1(self):
        return self.SGF1
    def set_SGF1(self, value):
        self.SGF1 = value

    def get_T1(self):
        return self.T1.PT 
    def set_T1(self, T):
        self.T1.set_PT(T) 

    def get_Iset(self):
        return self.Iset 
    def set_Iset(self, Iset):
        self.Iset=Iset