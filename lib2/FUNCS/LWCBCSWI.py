# Функция УВ в составе КП

#SGF1 - Ввод_функции - Ввод функции в работу (Не предусмотрено/ Предусмотренно)
#SGF2 - Бл_вкл_от_авар_откл - Блокировка включения от аварийного 		отключения В	(Не предусмотрено/ Предусмотрено)

#Т1 - Тперекл (Допустимое время переключения)
#Т2 - Тблк (Выдержка времени подавления выдачи положения "Не определено")

from lib2.TIMERS.TIMERS import TON, TP 
from lib2.TRIGGERS.TRIGGERS import RSTrigger

class LWCBCSWI:
    def __init__(self, SGF1, SGF2, T1, T2, T3, T4):
        self.SGF1 = SGF1
        self.SGF2 = SGF2
        self.T1 = TON()
        self.T1.set_PT(T1)
        self.T21 = TON()
        self.T21.set_PT(T2)
        self.T22 = TON()
        self.T22.set_PT(T2)
        self.T3 = TP()
        self.T3.set_PT(T3)
        self.T4 = TP()
        self.T4.set_PT(T4)
                             
        self.RS1 = RSTrigger(state=0)        
        self.RS2 = RSTrigger(state=0)
        self.RS3 = RSTrigger(state=0)        
        self.RS4 = RSTrigger(state=0)

        # Инициализация переменных
        self.uv_prev_vrem_per = False

    def Step(self, VVOD, KSV_blk_otkl, otkl_v_ot_pu, otkl_v_ichm, mestnoe, otkl_v_ot_tu, otkl_v_asu, kluch_md_priv, vkl_v_ot_pu, vkl_v_ichm, distanz, vkl_v_ot_tu, vkl_v_asu, ksv_blok_vkl, ksv_v_avar_otkl, v_otkl_bk, v_vkl_bk):

        vvod = VVOD and (self.SGF1==1) # УВ: Ввод

        self.T21.IN = not(v_otkl_bk) and not(v_vkl_bk)
        _p001, ET_t21 = self.T21.start()   
        self.T22.IN = v_otkl_bk and v_vkl_bk
        _p002, ET_t22 = self.T22.start()   

        _p003 = v_otkl_bk and not(v_vkl_bk) 
        _p004 = not(v_otkl_bk) and v_vkl_bk

        uv_otklucheno = self.RS3.run(_p003, (_p001 or _p002 or _p004 or not(vvod)))
        uv_vklucheno = self.RS4.run(_p004, (_p001 or _p002 or _p003 or not(vvod)))
        uv_neispr_neopred = _p002 and vvod
        uv_ne_opredeleno = _p001 and vvod

        self.T3.IN = (mestnoe and otkl_v_ot_pu) or (mestnoe and otkl_v_ichm) or (distanz and otkl_v_ot_tu) or (distanz and otkl_v_asu)
        _p006, ET_t3 = self.T3.start() 
        self.T4.IN = (mestnoe and vkl_v_ot_pu) or (mestnoe and vkl_v_ichm) or (distanz and vkl_v_ot_tu) or (distanz and vkl_v_asu)
        _p005, ET_t4 = self.T4.start()   

        uv_otkluchit = self.RS1.run(_p006, (not(vvod) or KSV_blk_otkl or kluch_md_priv or _p003 or self.uv_prev_vrem_per))
        uv_vkluchit = self.RS2.run(_p005, (not(vvod) or kluch_md_priv or ksv_blok_vkl or (0 if self.SGF2==0 else ksv_v_avar_otkl) or _p004 or self.uv_prev_vrem_per))

        uv_idet_per = uv_otkluchit or uv_vkluchit

        self.T1.IN = uv_idet_per
        self.uv_prev_vrem_per, ET_t1 = self.T1.start()  
   
        return vvod, uv_otkluchit, uv_idet_per, self.uv_prev_vrem_per, uv_vkluchit, uv_ne_opredeleno, uv_otklucheno, uv_vklucheno, uv_neispr_neopred #, ET_t1, ET_t21, ET_t22, ET_t3, ET_t4, _p001, _p002, _p003, _p004, _p005, _p006  

    # Геттеры и сеттеры
    def get_SGF1(self):
        return self.SGF1
    def set_SGF1(self, value):
        self.SGF1 = value
    def get_SGF2(self):
        return self.SGF2
    def set_SGF2(self, value):
        self.SGF2 = value

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
