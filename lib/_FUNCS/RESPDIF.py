# ДТЗт (RESPDIF)

# SGF1 - Ввод_функции - Ввод функции в работу (Не предусмотрено/ Предусмотрено)
# SGF2 - Реж_блок - Режим блокировки (Без блокировки / Блокировка по 2 гармонике / Блокировка по 5 гармонике / Блокировка по 2 и 5 гармоникам)
#SGF3 - Контр_БВКЗ - Контроль от БВКЗ (Без контроля БВКЗ/ С контролем БВКЗ)

from lib._TIMERS.TIMERS import TON  
from lib._ADD.iodzt import ioDZT # импортирует ИО ДТЗ

class RESPDIF:
    def __init__(self, SGF1, SGF2, SGF3, T1, Isr, Isr_zagrub, It1, It2, Kt1, Kt2):
        self.SGF1 = SGF1
        self.SGF2 = SGF2
        self.SGF3 = SGF3
        self.Isr_zagrub = Isr_zagrub
        self.Iset = Isr
        self.T1a = TON()
        self.T1a.set_PT(T1)
        self.T1b = TON()
        self.T1b.set_PT(T1)
        self.T1c = TON()
        self.T1c.set_PT(T1)

        self.ioA = ioDZT(Isr, Isr_zagrub, It1, It2, Kt1, Kt2)
        self.ioB = ioDZT(Isr, Isr_zagrub, It1, It2, Kt1, Kt2)
        self.ioC = ioDZT(Isr, Isr_zagrub, It1, It2, Kt1, Kt2)

    def Step(self, VYVOD, OV, OVst, NaSign, IAdiff, IBdiff, ICdiff, IAbias, IBbias, ICbias, CurCirc, OpSelA, OpSelB, OpSelC, d2g_pusk_A, d2g_pusk_B, d2g_pusk_C, d5g_pusk_A, d5g_pusk_B, d5g_pusk_C):

        vvod = (not(OV or OVst or VYVOD)) and (self.SGF1==1) # ДТЗ: Ввод
        oper_vyvod = (OV or OVst or VYVOD) and (self.SGF1==1) # ДТЗ: Оперативный вывод

        io_A = (self.SGF1==1) and self.ioA.Step(IAdiff, IAbias, CurCirc, OpSelA, self.SGF3)
        io_B = (self.SGF1==1) and self.ioB.Step(IBdiff, IBbias, CurCirc, OpSelB, self.SGF3)
        io_C = (self.SGF1==1) and self.ioC.Step(ICdiff, ICbias, CurCirc, OpSelC, self.SGF3)

        if self.SGF2==2 or self.SGF2==4:
            _p0001 = 1
        else:
            _p0001 = 0
        _p001 = d2g_pusk_A and _p0001 
        _p002 = d2g_pusk_B and _p0001 
        _p003 = d2g_pusk_C and _p0001

        if self.SGF2==1:
            _p004 = 1
        else:
            _p004 = 0

        if self.SGF2==3 or self.SGF2==4:
            _p0002 = 1
        else:
            _p0002 = 0
        _p005 = d5g_pusk_A and _p0002
        _p006 = d5g_pusk_B and _p0002 
        _p007 = d5g_pusk_C and _p0002

        pusk_A = vvod and io_A and (_p004 or (not(_p001 or _p005)))
        pusk_B = vvod and io_B and (_p004 or (not(_p002 or _p006)))
        pusk_C = vvod and io_C and (_p004 or (not(_p003 or _p007)))

        self.T1a.IN = pusk_A
        srabsign_A, ET_A = self.T1a.start()
        self.T1b.IN = pusk_B
        srabsign_B, ET_B = self.T1b.start()
        self.T1c.IN = pusk_C
        srabsign_C, ET_C = self.T1c.start()

        srab_A = (not NaSign) and srabsign_A
        srab_B = (not NaSign) and srabsign_B
        srab_C = (not NaSign) and srabsign_C

        pusk = pusk_A or pusk_B or pusk_C
        srabsign = srabsign_A or srabsign_B or srabsign_C
        srab = srab_A or srab_B or srab_C

        return vvod, oper_vyvod, pusk_A, srab_A, srabsign_A, io_A, pusk_B, srab_B, srabsign_B, io_B, pusk_C, srab_C, srabsign_C, io_C, pusk, srabsign, srab 

    # Геттеры и сеттеры
    def get_SGF1(self):
        return self.SGF1
    def set_SGF1(self, value):
        self.SGF1 = value

    def get_SGF2(self):
        return self.SGF2
    def set_SGF2(self, value):
        self.SGF2 = value

    def get_SGF3(self):
        return self.SGF3
    def set_SGF3(self, value):
        self.SGF3 = value

    def get_T1(self):
        return self.T1.PT
    def set_T1(self, T):
        self.T1.set_PT(T)

    def get_Isr(self):
        return self.Isr
    def set_Isr(self, Isr):
        self.Isr=Isr

    def get_Isr_zagrub(self):
        return self.Isr_zagrub
    def set_Isr_zagrub(self, Isr_zagrub):
        self.Isr_zagrub=Isr_zagrub        

    def get_It1(self):
        return self.It1
    def set_It1(self, It1):
        self.It1=It1

    def get_It2(self):
        return self.It2
    def set_It2(self, It2):
        self.It2=It2

    def get_Kt1(self):
        return self.Kt1
    def set_Kt1(self, Kt1):
        self.Kt1=Kt1

    def get_Kt2(self):
        return self.Kt2
    def set_Kt2(self, Kt2):
        self.Kt2=Kt2

      