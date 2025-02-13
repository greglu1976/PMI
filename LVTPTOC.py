# Ступень МТЗ трансформатора с НН1, НН2

#SGF1 - Ввод_функции - Ввод функции в работу (Не предусмотрено/ Предусмотрено)
#SGF2 - Тип_КПОН - Тип пуска по напряжению (Управляющее напряжение / Вольтметровая блокировка)
#SGF3 - Реж_БНТ - Режим контроля от БНТ (Не предусмотрено/ Предусмотрено)
#SGF4 - Реж_БНН_КПОН - Режим КПОН при неисправности ЦН  (Деблокировка (Чувств. уставка)/ Блокировка (Грубая уставка))
#SGF5 - Реж_КПОН1 - Режим контроля от КПОН1 (Не предусмотрено/ Предусмотрено)
#SGF6 - Реж_КПОН2 - Режим контроля от КПОН2 (Не предусмотрено/ Предусмотрено)
#SGF7 - Контр_СВ - Режим контроля СВ НН (Не предусмотрено/ Блокировка ступени при включенном СВ/ 	Блокировка ступени при отключенном СВ)

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

    def Step(self, VYVOD, OV, OVst, NaSign, SV1vkl, SV2vkl, IA, IB, IC, BNTpuskA, BNTpuskB, BNTpuskC, KZN1neipr, KPON1pusk, VNN1vkl, KZN2neipr, KPON2pusk, VNN2vkl):
        vvod, oper_vyvod = self.PrePreStep(VYVOD, OV, OVst)
        io_A, io_B, io_C, kpon_pusk, set_changer = self.PreStep(IA, IB, IC, KZN1neipr, KPON1pusk, VNN1vkl, KZN2neipr, KPON2pusk, VNN2vkl)
        mtzA_pusk, mtzB_pusk, mtzC_pusk, gen_pusk, mtz_srabsign, mtz_srab, ET = self.AfterStep(NaSign, SV1vkl, SV2vkl, io_A, io_B, io_C, BNTpuskA, BNTpuskB, BNTpuskC, kpon_pusk, vvod)
        return vvod, oper_vyvod, mtzA_pusk, io_A, mtzB_pusk, io_B, mtzC_pusk, io_C, gen_pusk, mtz_srabsign, mtz_srab, ET, kpon_pusk, set_changer


    def AfterStep(self, NaSign, SV1vkl, SV2vkl, io_A, io_B, io_C, BNTpuskA, BNTpuskB, BNTpuskC, kpon_pusk, vvod):

        #vvod = (not(OV or OVst or VYVOD)) and (self.SGF1==1) # МТЗ: Ввод
        #oper_vyvod = (OV or OVst or VYVOD) and (self.SGF1==1) # МТЗ: Оперативный вывод

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
        kpon_pusk = kpon_gen1 or kpon_gen2 or kpon_gen
        set_changer = 0 if (self.SGF2==1) else not(kpon_pusk)
        settingI = self.Iset if (set_changer==0) else self.Icoarse
        io_A = (self.SGF1==1) and (self.RSa.run((IA>=settingI), (IA<0.95*settingI)))
        io_B = (self.SGF1==1) and (self.RSb.run((IB>=settingI), (IB<0.95*settingI)))
        io_C = (self.SGF1==1) and (self.RSc.run((IC>=settingI), (IC<0.95*settingI)))
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