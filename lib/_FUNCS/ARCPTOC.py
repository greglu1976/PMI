# Функция ЗДЗ в составе ОЛ ARCPTOC

#SGF1 - Ввод_функции - Ввод функции в работу (Не предусмотрено/ Предусмотрено)

from lib._TIMERS.TIMERS import TON  
from lib._TRIGGERS.TRIGGERS import RSTrigger

class ARCPTOC:
    def __init__(self, SGF1, SGF2, SGF3, SGF4, T1, T2, Iset, U0set):
        self.SGF1 = SGF1
        self.SGF2 = SGF2
        self.SGF3 = SGF3
        self.SGF4 = SGF4        
        self.Iset = Iset*5 # Номиальный ток 5 А!!!!!
        self.U0set = U0set        
        self.T1 = TON()
        self.T1.set_PT(T1)
        self.T2 = TON()
        self.T2.set_PT(T2)
        self.RSi = RSTrigger(state=0)
        self.RSu = RSTrigger(state=0)

    def Step(self, VYVOD, NaSign, SrabZDZ, BNNshSrab, KtrTokZDZ, IA, IB, IC, U0):

        vvod = (not(VYVOD)) and (self.SGF1==1) # ЗДЗ: Ввод
        oper_vyvod = (VYVOD) and (self.SGF1==1) # ЗДЗ: Оперативный вывод

        I = max(IA, IB, IC)
        io_max = (self.SGF1==1) and (self.RSi.run((I>=self.Iset), (I<0.95*self.Iset)))
        uo = (self.SGF1==1) and (self.RSu.run((U0>=self.U0set), (U0<0.95*self.U0set)))

        _p001 = (not(0 if self.SGF4==0 else BNNshSrab)) and uo
        _p002 = _p001 or io_max

        if self.SGF3==1:
            _p003 = io_max
        elif self.SGF3==2:
            _p003 =_p002            
        elif self.SGF3==3:
            _p003 = KtrTokZDZ
        else:
            _p003=1

        _p004 = vvod and SrabZDZ

        self.T2.IN = _p004
        ZDZ_neispr, ET2 = self.T2.start()
        pusk = _p003 and _p004 and not(0 if self.SGF2==0 else ZDZ_neispr)

        self.T1.IN = pusk
        ZDZ_srabsign, ET1 = self.T1.start()
        ZDZ_srab = ZDZ_srabsign and (not NaSign)     

        return vvod, oper_vyvod, ZDZ_neispr, ZDZ_srab, ZDZ_srabsign, pusk, uo, io_max
 
