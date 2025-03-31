# Функция УРОВ для Т, Т2

# SGF1 - Ввод функции в работу (Не предусмотрено/ Предусмотрено)
# SGF2 - Ускорение при блокировке отключения В (Не предусмотрено/ Предусмотрено)
# SGF3 - УРОВ с подхватом по току (Не предусмотрено/ Предусмотрено)
# SGF4 - Контроль ЭМО (Не предусмотрено/ Предусмотрено по ЭМО1/ Предусмотрено по ЭМО1 и ЭМО2)
# SGF5 - Действие внешнего УРОВ на вышестоящий выключатель (Не предусмотрено/ Предусмотрено)
# SGF6 - Контроль по току при действии "на себя" (Не предусмотрено/ Предусмотрено по внутр. ПО/ Предусмотрено по внеш. ПО)

from lib._TIMERS.TIMERS import TON  
from lib._TRIGGERS.TRIGGERS import RSTrigger

class TPRBRF:
    def __init__(self, SGF1, SGF2, SGF3, SGF4, SGF5, SGF6, T1, Iset):
        self.SGF1 = SGF1
        self.SGF2 = SGF2
        self.SGF3 = SGF3
        self.SGF4 = SGF4
        self.SGF5 = SGF5
        self.SGF6 = SGF6        
        self.Iset = Iset
        self.T1 = TON()
        self.T1.set_PT(T1)
        self.RS = RSTrigger(state=0)
        self.RSgen = RSTrigger(state=0)

    def Step(self, VYVOD, OV, KSV_blok_otkl, LO_VN_otkl, kontr_emo1, kontr_emo2, Puski, pusk_urov_vnesh, IA, IB, IC):

        vvod = (not(OV or VYVOD)) and (self.SGF1==1) # УРОВ: Ввод
        oper_vyvod = (OV or VYVOD) and (self.SGF1==1) # УРОВ: Оперативный вывод

        I = max(IA, IB, IC)
        io = (self.SGF1==1) and (self.RS.run((I>=self.Iset), (I<0.95*self.Iset)))

        if self.SGF6==1:
            _p001 = io
        elif self.SGF6==2:
            _p001 = any(Puski)
        else:
            _p001 = 1       
        srab_na_sebya = pusk_urov_vnesh and (self.SGF1==1) and _p001

        if self.SGF4==1:
            _p002 = kontr_emo1
        elif self.SGF4==2:
            _p002 = kontr_emo1 and kontr_emo2
        else:
            _p002 = 0    

        _p003 = not(_p002) and (LO_VN_otkl or(srab_na_sebya if self.SGF5==1 else 0)) and vvod
        _p004 = not(vvod) or not(io) or (1 if self.SGF3==0 else 0)
        _p005 = self.RS.run((_p003 if self.SGF3==1 else 0), _p004)
        pusk = _p005 or (io and (_p003 if self.SGF3==0 else 0))
        uskorenie = pusk and (KSV_blok_otkl if self.SGF2==1 else 0)

        self.T1.IN = pusk
        _p006, ET = self.T1.start()  # Запускаем таймер и получаем выход и прошедшее время   
        srab = _p006 or uskorenie   

        return vvod, oper_vyvod, uskorenie, srab, pusk, io, srab_na_sebya, ET
 
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

    def get_T1(self):
        return self.T1.PT  # Предустановленное время таймера
    def set_T1(self, T):
        self.T1.set_PT(T)  # Устанавливаем предустановленное время таймера

if __name__ == "__main__":
    f = TPRBRF(SGF1=1, T1=0, Iset=1)
    res = f.Step(0,0,0,0,0,0)
    print(res)