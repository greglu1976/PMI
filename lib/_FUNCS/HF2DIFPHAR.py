# ИО Д2Г - детектор второй гармоники (Д2Г) (HF2DIFPHAR)
# SGF1 - Перекрест_блок - Перекрестная блокировка (Не предусмотрено/ Предусмотрено)

from lib._TRIGGERS.TRIGGERS import RSTrigger
from lib._TIMERS.TIMERS import TP, TOF  

class HF2DIFPHAR:
    def __init__(self, SGF1, T1, T2, Ratio):
        self.SGF1 = SGF1
        self.Ratio = Ratio             
        self.T1a = TOF()
        self.T1a.set_PT(T1)
        self.T1b = TOF()
        self.T1b.set_PT(T1)
        self.T1c = TOF()
        self.T1c.set_PT(T1)
        self.T2a = TP()
        self.T2a.set_PT(T2)
        self.T2b = TP()
        self.T2b.set_PT(T2)
        self.T2c = TP()
        self.T2c.set_PT(T2)
        self.RSa = RSTrigger(state=0)
        self.RSb = RSTrigger(state=0)
        self.RSc = RSTrigger(state=0)        

    def Step(self, VVOD, IAdiff, IAdiff2h, IBdiff, IBdiff2h, ICdiff, ICdiff2h):

        a_ratio = 0 if (IAdiff==0) else IAdiff2h/IAdiff
        a_rat_start = self.RSa.run((a_ratio>=self.Ratio), (a_ratio<0.95*self.Ratio))
        self.T1a.IN = a_rat_start
        Qa, ETa = self.T1a.start() 

        b_ratio = 0 if (IBdiff==0) else IBdiff2h/IBdiff
        b_rat_start = self.RSb.run((b_ratio>=self.Ratio), (b_ratio<0.95*self.Ratio))
        self.T1b.IN = b_rat_start
        Qb, ETb = self.T1b.start() 

        c_ratio = 0 if (ICdiff==0) else ICdiff2h/ICdiff
        c_rat_start = self.RSc.run((c_ratio>=self.Ratio), (c_ratio<0.95*self.Ratio))
        self.T1c.IN = c_rat_start
        Qc, ETc = self.T1c.start() 

        _p001 = (Qb or  Qc) and (self.SGF1==1)
        _p002 = (Qa or  Qc) and (self.SGF1==1)
        _p003 = (Qb or  Qa) and (self.SGF1==1)

        self.T2a.IN = _p001
        _p004, ET2a = self.T2a.start() 
        self.T2b.IN = _p002
        _p005, ET2b = self.T2b.start() 
        self.T2c.IN = _p003
        _p006, ET2c = self.T2c.start() 

        #print(_p004, _p005, _p006, _p001, _p002, _p003, ET2a, ET2b, ET2c)

        pusk_A = VVOD and (Qa or (_p001 and _p004))
        pusk_B = VVOD and (Qb or (_p002 and _p005))
        pusk_C = VVOD and (Qc or (_p003 and _p006))

        pusk = pusk_A or pusk_B or pusk_C
     
        return pusk_A, pusk_B, pusk_C, pusk

    # Геттеры и сеттеры
    def get_SGF1(self):
        return self.SGF1
    def set_SGF1(self, value):
        self.SGF1 = value
 