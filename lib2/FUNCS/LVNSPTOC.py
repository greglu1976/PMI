# Функция защиты от обрыва провода ЗОП
 
# SGF1 - Ввод_функции - Ввод функции в работу (Не предусмотрено/ Предусмотрено)
# SGF2 - Реж_ЗОП - Режим работы ЗОП (По току I2/ По отношению I2/I1/ По току I2 или отношению I2/I1)

from lib2.TIMERS.TIMERS import TON
from lib2.TRIGGERS.TRIGGERS import RSTrigger

class LVNSPTOC:
    def __init__(self, SGF1, SGF2, T1, I2set, RatioSet, In):
        self.SGF1 = SGF1
        self.SGF2 = SGF2        
        self.I2set = I2set
        self.RatioSet = RatioSet
        self.In = In
        self.T1 = TON()
        self.T1.set_PT(T1)
        self.RS1 = RSTrigger(state=0)
        self.RS2 = RSTrigger(state=0)
        self.RS3 = RSTrigger(state=0)                

    def Step(self, VYVOD, OV, NaSign, I2, I1):

        vvod = (not(OV or VYVOD)) and (self.SGF1==1) # ЗОП: Ввод
        oper_vyvod = (OV or VYVOD) and (self.SGF1==1) # ЗОП: Оперативный вывод

        io_I2 = (self.SGF1==1) and (self.RS1.run((I2>=self.I2set), (I2<0.95*self.I2set)))

        if I1!=0:
            _tr1 = self.RS2.run(((I2/I1)>=self.RatioSet), ((I2/I1)<0.95*self.RatioSet))
            _tr2 = self.RS3.run((I1>=0.04*self.In), (I1<0.95*0.04*self.In))
            io_rat = (self.SGF1==1) and _tr1 and _tr2
        else:
            io_rat=0
        pusk = vvod and ((io_I2 if self.SGF2==0 else 0) or (io_rat if self.SGF2==1 else 0) or ((io_I2 or io_rat) if self.SGF2==2 else 0))  
        self.T1.IN = pusk
        srabsign, ET = self.T1.start()  # Запускаем таймер и получаем выход и прошедшее время   
        srab = srabsign and not NaSign     

        return vvod, oper_vyvod, srab, srabsign, pusk, io_I2, io_rat, ET
 
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

if __name__ == "__main__":
    f = LVNSPTOC(SGF1=1, T1=0, Iset=1)
    res = f.Step(0,0,0,0,0,0)
    print(res)