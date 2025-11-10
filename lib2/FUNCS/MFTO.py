# Функция МФТО 561.0171

#SGF1 - МФТО - Ввод функции в работу (Выведено/ Введено)

from lib._TIMERS.TIMERS import TON  
from lib._TRIGGERS.TRIGGERS import RSTrigger

class PolarComplex:
    def __init__(self, amplitude, angle_deg=0):
        self.amp = amplitude
        self.ang = angle_deg

class MFTO:
    def __init__(self, SGF1, SGF2, T, Iset):
        self.SGF1 = SGF1
        self.SGF2 = SGF2 # БСТО
        self.Iset = Iset
        self.T1 = TON(T)
        self.RS_Ia = RSTrigger(state=0)
        self.RS_Ib = RSTrigger(state=0)
        self.RS_Ic = RSTrigger(state=0)        

    def Step(self, VYVOD, BSTO, IA, IB, IC):

        ia = self.RS_Ia.run((IA.amp>=self.Iset), (IA.amp<0.95*self.Iset))
        ib = self.RS_Ib.run((IB.amp>=self.Iset), (IB.amp<0.95*self.Iset))
        ic = self.RS_Ic.run((IC.amp>=self.Iset), (IC.amp<0.95*self.Iset))

        _p01 = (ia and ib) or (ib and ic) or (ic and ia)
        _p02 = 0 if self.SGF2 == 0 else BSTO
        _p03 = VYVOD if self.SGF1 == 1 else 1

        pusk = _p01 and (not _p02) and (not _p03) 

        self.T1.IN = pusk
        srab, ET = self.T1.start()

        return pusk, srab


if __name__ == "__main__":
    mfto = MFTO(SGF1=1, SGF2=1, T=0, Iset=5)
    res = mfto.Step(VYVOD=0, BSTO=0, IA=1, IB=1, IC=1)
    print(res)