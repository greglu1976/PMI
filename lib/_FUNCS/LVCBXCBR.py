# Функция В выключатель в составе КА

#SGF1 - Ввод_функции - Ввод функции в работу	(Не предусмотрено/ Предусмотрено)
#SGF2 - Режим_откл - Режим отключения выключателя (Длительный/ Импульсный)
#SGF3 - Контр_раб_ЭМО - Контроль работы ЭМО 	(Не предусмотрено/ Предусмотрено)
#SGF4 - Режим_вкл - Режим включения выключателя 	(Длительный/ Импульсный)
#SGF5 - Контр_раб_ЭМВ - Контроль работы ЭМВ 	(Не предусмотрено/ Предусмотрено)
#SGF6 - Блок_откл_от_КСВ - Блокировка отключения от КСВ	(Не предусмотрено/ Предусмотрено)
#Т4 - 	Для исключения ситуации «опрокидывания» выключателя при раннем съёме команды «В:Включить (реле)» что характерно для некоторых видов масляных выключателей, предусмотрена дополнительная задержка на снятие команды задаваемая уставкой.

from lib._TIMERS.TIMERS import TON, TP_with_R 
from lib._TRIGGERS.TRIGGERS import RSTrigger

class LVCBXCBR:
    def __init__(self, SGF1, SGF2, SGF3, SGF4, SGF5, SGF6, T1, T2, T3, T4):
        self.SGF1 = SGF1
        self.SGF2 = SGF2
        self.SGF3 = SGF3
        self.SGF4 = SGF4
        self.SGF5 = SGF5
        self.SGF6 = SGF6
        self.T1 = TON()
        self.T1.set_PT(T1)
        self.T2 =  TP_with_R()
        self.T2.set_PT(T2)
        self.T3 =  TP_with_R()
        self.T3.set_PT(T3)
        self.T4 = TON()
        self.T4.set_PT(T4)
        self.RS1 = RSTrigger(state=0)        
        self.RS2 = RSTrigger(state=0)

        # Инициализация переменных
        self._p008 = False

    def Step(self, VVOD, v_otkl_bk, v_vkl_bk, kp_uv_otkluchit, lovn_lo_otkl_avar, urov_nasebya, oper_otkl_v, ksv_blok_otkl, rabota_emo1, rabota_emo2, sbros, kp_uv_vkluchit, uv_uv_vkluchit, rabota_emv):

        vvod = VVOD and (self.SGF1==1) # В: Ввод

        v_otkluchen = vvod and v_otkl_bk and not(v_vkl_bk)       
        v_vkluchen = vvod and v_vkl_bk and not(v_otkl_bk)  

        _p001 = vvod and (not(v_otkl_bk^v_vkl_bk))

        self.T1.IN = _p001
        v_neisp_pol, ET_t1 = self.T1.start()   
        v_prom_pol = _p001 and not(v_neisp_pol)

        _p002 = kp_uv_otkluchit or lovn_lo_otkl_avar or urov_nasebya or oper_otkl_v
        _p003 = _p002 and not(ksv_blok_otkl)
        _p004 = not(vvod) or sbros or (v_otkluchen and not(0 if self.SGF3==0 else (rabota_emo1 or rabota_emo2)))

        self.T2.IN = _p003 if self.SGF2==1 else 0
        self.T2.R = _p004
        _p005, ET_t2 = self.T2.start()

        v_otkluchit_rele = (self.RS1.run(0 if self.SGF2==1 else _p003, _p004)) or _p005

        _p006 = kp_uv_vkluchit or uv_uv_vkluchit
        self.T4.IN = v_vkluchen and (not(0 if self.SGF5==0 else rabota_emv))
        _p007, ET_t4 = self.T4.start()
        self._p008 = (_p002 or self._p008) and _p006
        _p009 = sbros or _p002 or self._p008 or not(vvod) or _p007

        self.T3.IN = _p006 if self.SGF4==1 else 0
        self.T3.R = _p009
        _p010, ET_t3 = self.T3.start()

        v_vkluchit_rele = (self.RS2.run(0 if self.SGF4==1 else _p006, _p009)) or _p010

        return vvod, v_prom_pol, v_otkluchen, v_vkluchen, v_neisp_pol, v_otkluchit_rele, v_vkluchit_rele, ET_t1, ET_t2, ET_t3, ET_t4, _p001, _p002, _p003, _p004, _p005, _p006, _p007, self._p008, _p009, _p010 

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

    def get_T4(self):
        return self.T4.PT  # Предустановленное время таймера
    # Сеттер для времени таймера
    def set_T4(self, T):
        self.T4.set_PT(T)  # Устанавливаем предустановленное время таймера
