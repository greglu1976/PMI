# Функция АПВ

#SGF1 - Ввод _функции - Ввод функции в работу (Не предусмотрено/ Предусмотрено)
#SGF2 - Реж_конт_U - Режим контроля напряжения (Не предусмотрено/ Оперативный/ КННш+КОНп/ КОНш+КННп/ КННш+КОНп-КОНш+КННп)
#SGF3 - Контр_синхр - Контроль синхронизма и напряжений (Не предусмотрено/ Предусмотрено)
#SGF4 - Число_циклов - Количество циклов АПВ (1/ 2)
#SGF5 - Блок_2ц_ОЗЗ - Режим блокировки второго цикла при ОЗЗ (Не предусмотрено/ Предусмотрено)
#Т1 - Тгот_1ц - Готовность для однократного АПВ
#Т6 - Тгот_2ц - Готовность для двухкратного АПВ


from lib._TIMERS.TIMERS import TON, TP 
from lib._TRIGGERS.TRIGGERS import RSTrigger


class LVLINRREC:
    def __init__(self, SGF1, SGF2, SGF3, SGF4, SGF5, T1, T2, T3, T4=0.1, T5=3, T6=1.5):
        self.SGF1 = SGF1
        self.SGF2 = SGF2
        self.SGF3 = SGF3
        self.SGF4 = SGF4
        self.SGF5 = SGF5
        self.T1 = TON()
        self.T1.set_PT(T1)
        self.T2 = TON()
        self.T2.set_PT(T2)
        self.T3 = TON()
        self.T3.set_PT(T3)
        self.T4 = TP()
        self.T4.set_PT(T4)
        self.T5 = TON()
        self.T5.set_PT(T5)
        self.T6 = TP()
        self.T6.set_PT(T6)                                
        self.RS1 = RSTrigger(state=0)        
        self.RS2 = RSTrigger(state=0)
        self.RS3 = RSTrigger(state=0)        
        self.RS4 = RSTrigger(state=0)

        # Инициализация переменных
        self.apv_gotov_1 = False
        self.apv_gotov_2 = False
        self.apv_zaderzh_vkl = False
        self.apv_2_cycl = False
        self.apv_tek_2_cycl = False


    def Step(self, VYVOD, OV, KSV_blk, Vvkl, KSV_rfk, ZAPV_zapv, Vnesh_zaprAPV, APV_blk2cycl, GSOZZ, KSV_avarotkl, KS_razrAvtVklV, APV_bezKontr, APV_KNNSH, APV_KONsh, KNNsh_pusk, KONp_pusk, KONsh_pusk, KNNp_pusk):

        vvod = (not(OV or VYVOD)) and (self.SGF1==1) # АПВ: Ввод
        oper_vyvod = (OV or VYVOD) and (self.SGF1==1) # АПВ: Оперативный вывод

        _p002 = not(KSV_rfk) or ZAPV_zapv or Vnesh_zaprAPV
        self.T1.IN = not(KSV_blk) and Vvkl and not(_p002)
        _p001, ET_t1 = self.T1.start()   

        _p003 = KNNsh_pusk and KONp_pusk
        _p004 = KONsh_pusk and KNNp_pusk
        _p005 = (APV_KNNSH and _p003) or (APV_KONsh and _p004)
        _p006 = _p004 or _p003

        if self.SGF2 == 1:
                _p007 = _p005
        elif self.SGF2 == 2:
                _p007 = _p003
        elif self.SGF2 == 3:
                _p007 = _p004
        elif self.SGF2 == 4:
                _p007 = _p006
        else:
                _p007 = 0 

        _p008 = 1 if self.SGF3==0 else (KS_razrAvtVklV or APV_bezKontr or _p007)
        self.T4.IN = KSV_avarotkl
        _p009, ET_t4 = self.T4.start() 
        apv_tekush_cycl = self.RS3.run(_p009, not(self.apv_gotov_1))
        self.T2.IN = apv_tekush_cycl
        _p010, ET_t2 = self.T2.start() 

        apv_1_cycl = _p010 and _p008

        self.T6.IN = self.apv_2_cycl
        _t6, ET_t6 = self.T6.start() 
        _p011 = (not(_t6)) and _p001

        self.apv_gotov_1 = self.RS1.run(_p011, (not vvod or _p002 or apv_1_cycl or self.apv_zaderzh_vkl))
        sgf4_out = 1 if self.SGF4==0 else 0
        sgf5_out = (0 if self.SGF5==0 else GSOZZ) and self.apv_tek_2_cycl
        self.apv_gotov_2 = self.RS2.run(_p011, (not vvod or sgf4_out or _p002 or APV_blk2cycl or self.apv_2_cycl or self.apv_zaderzh_vkl or sgf5_out))

        _p012 = not(self.apv_gotov_1) or self.apv_gotov_2
        self.apv_tek_2_cycl = self.RS4.run(_p009, _p012)

        self.T5.IN = self.apv_tek_2_cycl
        _p013, ET_t5 = self.T5.start()

        self.apv_2_cycl = _p008 and _p013
        _p014 = _p010 or _p013

        self.T3.IN = _p014
        self.apv_zaderzh_vkl, ET_t3 = self.T3.start()

        apv_vkl_ks = 0 if self.SGF3==0 else (_p008 and KNNsh_pusk and KNNp_pusk)
        apv_vkl = not KSV_blk and (self.apv_2_cycl or apv_1_cycl)        
 
        return vvod, oper_vyvod, self.apv_gotov_1, self.apv_gotov_2, apv_tekush_cycl, apv_1_cycl, apv_vkl, self.apv_2_cycl, self.apv_tek_2_cycl, self.apv_zaderzh_vkl, apv_vkl_ks, ET_t1, ET_t2, ET_t3, ET_t4, ET_t5, ET_t6, _p001, _p002, _p003, _p004, _p005, _p006, _p007, _p008, _p009, _p010, _p011, _p012, _p013, _p014


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

    def get_T5(self):            
        return self.T5.PT  # Предустановленное время таймера    
    # Сеттер для времени таймера
    def set_T5(self, T):  
        self.T5.set_PT(T)  # Устанавливаем предустановленное время таймера

    def get_T6(self):            
        return self.T6.PT  # Предустановленное время таймера    
    # Сеттер для времени таймера
    def set_T6(self, T):  
        self.T6.set_PT(T)  # Устанавливаем предустановленное время таймера  

if __name__ == "__main__":
    ptoc1 = LVLINRREC(SGF1=1, SGF2=0, T1=0, Iset=1)
    res = ptoc1.Step(0,0,0,0,0,0,0,0,0)
    print(res)