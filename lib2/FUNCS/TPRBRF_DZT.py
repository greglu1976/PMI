# Функция УРОВ для ДЗТ2

# SGF1 - Ввод функции в работу (Не предусмотрено/ Предусмотрено)
# SGF2 - УРОВ с подхватом по току (Не предусмотрено/ Предусмотрено)
# SGF3 - Действие внешнего УРОВ на вышестоящий выключатель (Не предусмотрено/ Предусмотрено)
# SGF4 - Контроль по току при действии "на себя" (Не предусмотрено/ Предусмотрено)

from lib._TIMERS.TIMERS import TON  
from lib._TRIGGERS.TRIGGERS import RSTrigger

class TPRBRF:
    def __init__(self, SGF1, SGF2, SGF3, SGF4, T1, Iset):
        self.SGF1 = SGF1
        self.SGF2 = SGF2
        self.SGF3 = SGF3
        self.SGF4 = SGF4
        self.Iset = Iset
        self.T1 = TON()
        self.T1.set_PT(T1)
        self.RS = RSTrigger(state=0)
        self.RSgen = RSTrigger(state=0)

    def Step(self, VYVOD, OV, LO_VN_otkl, pusk_urov_vnesh, IA, IB, IC):

        vvod = (not(OV or VYVOD)) and (self.SGF1==1) # УРОВ: Ввод
        oper_vyvod = (OV or VYVOD) and (self.SGF1==1) # УРОВ: Оперативный вывод
        I = max(IA, IB, IC)
        io = (self.SGF1==1) and (self.RS.run((I>=self.Iset), (I<0.95*self.Iset)))
        srab_na_sebya = pusk_urov_vnesh and (self.SGF1==1) and (io if self.SGF4==1 else 1)
        _p001 = LO_VN_otkl or (srab_na_sebya if self.SGF3==1 else 0)
        _p002 = not(vvod) or not(io) or (1 if self.SGF2==0 else 0)
        _p003 = (vvod and _p001) if self.SGF2==1 else 0
        _p004 = (vvod and _p001) if self.SGF2==0 else 0      
        _p005 = self.RSgen.run(_p003, _p002)
        pusk = _p005 or (io and _p004)
        #print("_p001", _p001, "_p002", _p002, "_p003", _p003, "_p004", _p004, "_p005", _p005,)

        self.T1.IN = pusk
        srab, ET = self.T1.start()  # Запускаем таймер и получаем выход и прошедшее время   

        return vvod, oper_vyvod, srab, pusk, io, srab_na_sebya, ET
 
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

    def get_T1(self):
        return self.T1.PT  # Предустановленное время таймера
    def set_T1(self, T):
        self.T1.set_PT(T)  # Устанавливаем предустановленное время таймера

if __name__ == "__main__":
    f = TPRBRF(SGF1=1, T1=0, Iset=1)
    res = f.Step(0,0,0,0,0,0)
    print(res)