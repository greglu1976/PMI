# Ступень МТЗ трансформатора с НН1, НН2

from lib._TIMERS.TIMERS import TON  
from lib._TRIGGERS.TRIGGERS import RSTrigger

class LVTPTOC:
    def __init__(self, SGF1=0, SGF2=0, SGF3=0, SGF4=0, SGF5=0, SGF6=0,SGF7=0, T1=0, Iset=1, Icoarse=2):
        self.SGF1 = SGF1
        self.SGF2 = SGF2
        self.SGF3 = SGF3
        self.SGF4 = SGF4
        self.SGF5 = SGF5
        self.SGF6 = SGF6  
        self.SGF7 = SGF7
        self.Iset = Iset
        self.Icoarse = Icoarse               
        self.T1 = TON()
        self.T1.set_PT(T1)
        self.RSa = RSTrigger(state=0)
        self.RSb = RSTrigger(state=0)
        self.RSc = RSTrigger(state=0)

    def Step(self, VYVOD, OV, OVst , NaSign, SV1vkl, SV2vkl, SGF1, IA, IAB, IB, IBC, IC, ICA, BNTpuskA, BNTpuskB, BNTpuskC, KZN1neipr, KPON1pusk, VNN1vkl, KZN2neipr, KPON2pusk, VNN2vkl):
        vvod = (not(OV or OVst or VYVOD)) and (self.SGF1==1) # МТЗ: Ввод
        oper_vyvod = (OV or OVst or VYVOD) and (self.SGF1==1) # МТЗ: Оперативный вывод

        # Реализация блока КПОН в составе ступени МТЗ
        #kpon_gen1 = 0 if (self.SGF5==0) else ((KZN1neipr if (self.SGF4==0) else (not(KZN1neipr) and KPON1pusk)) and VNN1vkl)
        kpon_gen1 = 0 if (self.SGF5==0) else (VNN1vkl and (KZN1neipr if (self.SGF4==0) else 0) or (KPON1pusk and not(KZN1neipr if(self.SGF4==1) else 0)))
        #kpon_gen2 = 0 if (self.SGF6==0) else ((KZN2neipr if (self.SGF4==0) else (not(KZN2neipr) and KPON2pusk)) and VNN2vkl)
        kpon_gen2 = 0 if (self.SGF6==0) else (VNN2vkl and (KZN2neipr if (self.SGF4==0) else 0) or (KPON2pusk and not(KZN2neipr if(self.SGF4==1) else 0)))
   
        kpon_gen = ((1 if (self.SGF5==0) else 0) or not(VNN1vkl)) and ((1 if (self.SGF6==0) else 0) or not(VNN2vkl))
        print(kpon_gen)
        kpon_pusk = kpon_gen1 or kpon_gen2 or kpon_gen
        # Проверка перевода на грубую уставку и подмена уставок
        set_changer = 0 if (self.SGF2==1) else not(kpon_pusk)
        settingI = self.Iset if (set_changer==0) else self.Icoarse

        # Логика фазы А
        Ia = IA if (SGF1==0) else IAB
        io_A = (self.SGF1==1) and (self.RSa.run((Ia>=settingI), (Ia<0.95*settingI)))
        mtzA_pusk = vvod and ((kpon_pusk if (self.SGF2==1) else 1) and io_A) and not(0 if (self.SGF3==0) else BNTpuskA)

        # Логика фазы B
        Ib = IB if (SGF1==0) else IBC
        io_B = (self.SGF1==1) and (self.RSb.run((Ib>=settingI), (Ib<0.95*settingI)))
        mtzB_pusk = vvod and ((kpon_pusk if (self.SGF2==1) else 1) and io_B) and not(0 if (self.SGF3==0) else BNTpuskB)

        # Логика фазы C
        Ic = IC if (SGF1==0) else ICA
        io_C = (self.SGF1==1) and (self.RSc.run((Ic>=settingI), (Ic<0.95*settingI)))
        mtzC_pusk = vvod and ((kpon_pusk if (self.SGF2==1) else 1) and io_C) and not(0 if (self.SGF3==0) else BNTpuskC)

        sv_ctl = 0 if (self.SGF7==0) else (SV1vkl or SV2vkl) if (self.SGF7==1) else not(SV1vkl or SV2vkl) 
        gen_pusk = not(sv_ctl) and (mtzA_pusk or mtzB_pusk or mtzC_pusk)

        self.T1.IN = gen_pusk
        Q, ET = self.T1.start()  # Запускаем таймер и получаем выход и прошедшее время
        mtz_srabsign = Q
        mtz_srab = mtz_srabsign and not(NaSign)

        return vvod, oper_vyvod, mtzA_pusk, io_A, mtzB_pusk, io_B, mtzC_pusk, io_C, gen_pusk, mtz_srabsign, mtz_srab, ET, kpon_pusk, set_changer

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