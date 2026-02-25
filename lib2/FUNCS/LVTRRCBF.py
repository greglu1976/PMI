# Функция КСВ

# SGF1 - Ввод_функции - Ввод функции в работу (Не предусмотрено/ Предусмотрено)
# SGF2 - Блок_вкл_низ_изол_В - Блокировка включения при низком уровне изоляции В (Не предусмотрено/ Предусмотрено)
# SGF3 - Блок_вкл_полож_В - Блокировка включения при неисправности положения В (Не предусмотрено/ Предусмотрено)
# SGF4 - Блок_вкл_ресурса_В - Блокировка включения при превышении ресурса В (Не предусмотрено/ Предусмотрено)
# SGF5 - Контроль_ОТ_ЭМ - Контроль ОТ цепей ЭМВ, ЭМО1 и ЭМО2 (Не предусмотрено/ ЭМВ и ЭМО1/ ЭМВ, ЭМО1 и ЭМО2)
# SGF6 - Контроль_ЭМ - Контроль ЭМВ, ЭМО1 и ЭМО2 при формировании	неисправности цепей ЭМУ (Не предусмотрено/ ЭМВ и ЭМО1/ ЭМВ, ЭМО1 и ЭМО2)
# SGF7 - Контроль_кнопки - Разрешение сброса "РФК" от кнопки (Не предусмотрено/ Предусмотрено)
# SGF8 - Блок_упр_КИ_В - Блокировка управления при снижениии уровня изоляции В (Не предусмотрено/ От аварийного/ От аврийного и низкого

from lib2.TIMERS.TIMERS import TON
from lib2.TRIGGERS.TRIGGERS import SRTrigger

class LVTRRCBF:
    def __init__(self, SGF1, SGF2, SGF3, SGF4, SGF5, SGF6, SGF7, SGF8, T1, T2, T3):
        self.SGF1 = SGF1
        self.SGF2 = SGF2
        self.SGF3 = SGF3
        self.SGF4 = SGF4
        self.SGF5 = SGF5
        self.SGF6 = SGF6
        self.SGF7 = SGF7
        self.SGF8 = SGF8
        self.T1 = TON()
        self.T1.set_PT(T1)
        self.T2 = TON()
        self.T2.set_PT(T2)
        self.T31 = TON()
        self.T31.set_PT(T3)
        self.T32 = TON()
        self.T32.set_PT(T3)
        self.T33 = TON()
        self.T33.set_PT(T3)
        self.SR1 = SRTrigger(state=0)        
        self.SR2 = SRTrigger(state=0)

    def Step(self, VYVOD, OV, ot_emo1emv, ot_emo2, lovn_otkl, urov_nasebya, avar_isol_V, niz_isol_V, pruzh_ne_zaved, V_neispr_pol, V_otkl, V_vkl, Sbros, UV_otkl, otkl_ot_knopk, oper_otkl_V, KRV_resurs_V, vnesh_blok_upr_V, kontr_emv, kontr_emo1, kontr_emo2, rabota_emv, rabota_emo1, rabota_emo2):

        vvod = (not(OV or VYVOD)) and (self.SGF1==1) # КСВ: Ввод
        oper_vyvod = (OV or VYVOD) and (self.SGF1==1) # КСВ: Оперативный вывод

        self.T31.IN = rabota_emv
        _p001, ET_t31 = self.T31.start()  
        self.T32.IN = rabota_emo1
        _p002, ET_t32 = self.T32.start() 
        self.T33.IN = rabota_emo2
        _p003, ET_t33 = self.T33.start() 

        ksv_zashita_emv = vvod and _p001
        ksv_zashita_emo1 = vvod and _p002
        ksv_zashita_emo2 = vvod and _p003        

        if self.SGF6 == 1:
            _p004 = not(kontr_emv ^ kontr_emo1)
        elif self.SGF6 == 2:
            _p004 = (not(kontr_emv ^ kontr_emo1)) or (not(kontr_emv ^ kontr_emo2))
        else:
            _p004 = 0

        self.T2.IN = _p004
        _p005, ET_t2 = self.T2.start() 

        ksv_neisp_emu = _p005 and vvod

        ######################## ИЗМ 25-03-25
        if self.SGF8==1:
            _p006 = avar_isol_V
        elif self.SGF8==2:
            _p006 = avar_isol_V and niz_isol_V
        else:
            _p006 = 0

        #_p006 = 0 if self.SGF9==0 else (avar_isol_V and (1 if self.SGF7==0 else niz_isol_V)) старая версия
        ksv_blok_otkl = vvod and (vnesh_blok_upr_V or _p006)

        if self.SGF5 == 1:
            _p007 = ot_emo1emv
        elif self.SGF5 == 2:
            _p007 = ot_emo1emv and ot_emo2
        else:
            _p007 = 1        

        self.T1.IN = pruzh_ne_zaved
        _p008, ET_t1 = self.T1.start() 

        ksv_neispr_V = (niz_isol_V or avar_isol_V or not(_p007) or _p008 or V_neispr_pol or _p005 or (_p001 or _p002 or _p003) or vnesh_blok_upr_V) and vvod
        _p009 = UV_otkl or (0 if self.SGF7==0 else otkl_ot_knopk) or oper_otkl_V # SGF8 поправлен на SGF7
        ksv_blok_vkl = (pruzh_ne_zaved or _p006 or not(_p007) or (0 if self.SGF2==0 else niz_isol_V) or _p005 or (0 if self.SGF3==0 else V_neispr_pol) or _p009 or (0 if self.SGF4==0 else KRV_resurs_V) or (lovn_otkl or urov_nasebya) or (rabota_emo1 or rabota_emo2) or vnesh_blok_upr_V) and vvod

        _p010 = not vvod or (V_otkl and Sbros) or _p009
        ksv_rfk = self.SR2.run((vvod and V_vkl), _p010)
        ksv_v_avar_otkl = ksv_rfk and V_otkl

        ksv_v_samoproisv_otkl = not (self.SR1.run((vvod and (lovn_otkl or urov_nasebya)), _p010)) and ksv_v_avar_otkl
 
        return vvod, oper_vyvod, ksv_v_samoproisv_otkl, ksv_neispr_V, ksv_v_avar_otkl, ksv_rfk, ksv_blok_vkl, ksv_blok_otkl, ksv_neisp_emu, ksv_zashita_emv, ksv_zashita_emo1, ksv_zashita_emo2 #, ET_t1, ET_t2, ET_t31, ET_t32, ET_t33, _p001, _p002, _p003, _p004, _p005, _p006, _p007, _p008, _p009, _p010


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
        self.SGF3= value
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
    def set_SG7(self, value):
        self.SGF7= value
    def get_SGF8(self):
        return self.SGF8
    def set_SGF8(self, value):
        self.SGF8 = value

    def get_T1(self):
        return self.T1.PT  # Предустановленное время таймера
    # Сеттер для времени таймера
    def set_T1(self, T):
        self.T1.set_PT(T)  # Устанавливаем предустановленное время таймера

    def get_T2(self):
        return self.T2.PT  # Предустановленное время таймера
    # Сеттер для времени таймера
    def set_T2(self, T):
        self.T2.set_PT(T)  # Устанавливаем предустановленное время таймера

    def get_T3(self):
        return self.T3.PT  # Предустановленное время таймера
    # Сеттер для времени таймера
    def set_T3(self, T):
        self.T3.set_PT(T)  # Устанавливаем предустановленное время таймера

