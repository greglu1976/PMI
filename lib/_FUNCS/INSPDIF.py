# ДТО (INSPDIF)

#SGF1 - Ввод_функции - Ввод функции в работу (Не предусмотрено/ Предусмотрено)

from lib._TIMERS.TIMERS import TON  
from lib._TRIGGERS.TRIGGERS import RSTrigger

class INSPDIF:
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

    def Step(self, VYVOD, OV, OVst, NaSign, IAdiff, IBdiff, ICdiff):
        vvod = (not(OV or OVst or VYVOD)) and (self.SGF1==1) # ДТО: Ввод
        oper_vyvod = (OV or OVst or VYVOD) and (self.SGF1==1) # ДТО: Оперативный вывод
        io_A = (self.SGF1==1) and (self.RSa.run((IA>=settingI), (IA<0.95*settingI)))

        
        io_B = (self.SGF1==1) and (self.RSb.run((IB>=settingI), (IB<0.95*settingI)))
        io_C = (self.SGF1==1) and (self.RSc.run((IC>=settingI), (IC<0.95*settingI)))



        return vvod, oper_vyvod


    def AfterStep(self, NaSign, SV1vkl, SV2vkl, io_A, io_B, io_C, BNTpuskA, BNTpuskB, BNTpuskC, kpon_pusk, vvod):

        # Логика фазы А
        mtzA_pusk = vvod and ((kpon_pusk if (self.SGF2==1) else 1) and io_A) and not(0 if (self.SGF3==0) else BNTpuskA)
        # Логика фазы B
        mtzB_pusk = vvod and ((kpon_pusk if (self.SGF2==1) else 1) and io_B) and not(0 if (self.SGF3==0) else BNTpuskB)
        # Логика фазы C
        mtzC_pusk = vvod and ((kpon_pusk if (self.SGF2==1) else 1) and io_C) and not(0 if (self.SGF3==0) else BNTpuskC)

        sv_ctl = 0 if (self.SGF7==0) else (SV1vkl or SV2vkl) if (self.SGF7==1) else not(SV1vkl or SV2vkl) 
        gen_pusk = not(sv_ctl) and (mtzA_pusk or mtzB_pusk or mtzC_pusk)

        self.T1.IN = gen_pusk
        Q, ET = self.T1.start()  # Запускаем таймер и получаем выход и прошедшее время
        mtz_srabsign = Q
        mtz_srab = mtz_srabsign and not(NaSign)

        return mtzA_pusk, mtzB_pusk, mtzC_pusk, gen_pusk, mtz_srabsign, mtz_srab, ET

    def PreStep(self, IA, IB, IC, KZN1neipr, KPON1pusk, VNN1vkl, KZN2neipr, KPON2pusk, VNN2vkl): # Вспомогательный метод для предварительного вычисления значений для БНТ
        kpon_gen1 = 0 if (self.SGF5==0) else (VNN1vkl and (KZN1neipr if (self.SGF4==0) else 0) or (KPON1pusk and not(KZN1neipr if(self.SGF4==1) else 0)))
        kpon_gen2 = 0 if (self.SGF6==0) else (VNN2vkl and (KZN2neipr if (self.SGF4==0) else 0) or (KPON2pusk and not(KZN2neipr if(self.SGF4==1) else 0)))
        kpon_gen = ((1 if (self.SGF5==0) else 0) or not(VNN1vkl)) and ((1 if (self.SGF6==0) else 0) or not(VNN2vkl))

        #print('kpon_gen', self.SGF5, self.SGF6)
        kpon_pusk = kpon_gen1 or kpon_gen2 or kpon_gen
        set_changer = 0 if (self.SGF2==1) else not(kpon_pusk)
        settingI = self.Iset if (set_changer==0) else self.Icoarse
        io_A = (self.SGF1==1) and (self.RSa.run((IA>=settingI), (IA<0.95*settingI)))
        io_B = (self.SGF1==1) and (self.RSb.run((IB>=settingI), (IB<0.95*settingI)))
        io_C = (self.SGF1==1) and (self.RSc.run((IC>=settingI), (IC<0.95*settingI)))
        #print('set_changer', set_changer, kpon_gen1, kpon_gen2, kpon_gen)
        return io_A, io_B, io_C, kpon_pusk, set_changer

    def PrePreStep(self, VYVOD, OV, OVst):
        vvod = (not(OV or OVst or VYVOD)) and (self.SGF1==1) # МТЗ: Ввод
        oper_vyvod = (OV or OVst or VYVOD) and (self.SGF1==1) # МТЗ: Оперативный вывод
        return vvod, oper_vyvod       

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
    def get_SGF4(self):
        return self.SGF4
    def set_SGF4(self, value):
        self.SGF4 = value

    def get_SGF5(self):
        return self.SGF5
    def set_SGF5(self, value):
        self.SGF5 = value
    def get_SGF6(self):
        return self.SGF6
    def set_SGF6(self, value):
        self.SGF6 = value

    def get_SGF7(self):
        return self.SGF7
    def set_SGF7(self, value):
        self.SGF7 = value

    def get_T1(self):
        return self.T1.PT  # Предустановленное время таймера
    # Сеттер для времени таймера
    def set_T1(self, T):
        self.T1.set_PT(T)  # Устанавливаем предустановленное время таймера