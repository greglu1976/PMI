# ДТЗт (RESPDIF)

# SGF1 - Ввод_функции - Ввод функции в работу (Не предусмотрено/ Предусмотрено)
# SGF2 - Реж_блок - Режим блокировки (Без блокировки / Блокировка по 2 гармонике / Блокировка по 5 гармонике / Блокировка по 2 и 5 гармоникам)
#SGF3 - Контр_БВКЗ - Контроль от БВКЗ (Без контроля БВКЗ/ С контролем БВКЗ)


from lib._TIMERS.TIMERS import TON  
from lib._TRIGGERS.TRIGGERS import RSTrigger
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
        self.RSa = RSTrigger(state=0)
        self.RSb = RSTrigger(state=0)
        self.RSc = RSTrigger(state=0)
        self.io = ioDZT(Isr, Isr_zagrub, It1, It2, Kt1, Kt2)


    def Step(self, VYVOD, OV, OVst, NaSign, IAdiff, IBdiff, ICdiff):

        vvod = (not(OV or OVst or VYVOD)) and (self.SGF1==1) # ДТО: Ввод
        oper_vyvod = (OV or OVst or VYVOD) and (self.SGF1==1) # ДТО: Оперативный вывод

        io_A = (self.SGF1==1) and (self.RSa.run((IAdiff>=self.Iset), (IAdiff<0.95*self.Iset)))
        io_B = (self.SGF1==1) and (self.RSb.run((IBdiff>=self.Iset), (IBdiff<0.95*self.Iset)))
        io_C = (self.SGF1==1) and (self.RSc.run((ICdiff>=self.Iset), (ICdiff<0.95*self.Iset)))

        pusk_A = vvod and io_A
        pusk_B = vvod and io_B
        pusk_C = vvod and io_C

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

    def get_T1(self):
        return self.T1.PT
    def set_T1(self, T):
        self.T1.set_PT(T)

    def get_Iset(self):
        return self.Iset
    def set_Iset(self, Iset):
        self.Iset=Iset