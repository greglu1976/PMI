# КЦН - Сигнализация неисправности цепей напряжения стороны трансформатора 35 кВ (в составе устройства ЮНИТ-М3-Т)
# SGF1 - Ввод _функции - Ввод функции в работу (Не предусмотрено/ Предусмотрено)
# SGF2 - Реж_пуска - Режим пуска (Внутренний / Внешний)

from lib2.TRIGGERS.TRIGGERS import RSTrigger
from lib2.TIMERS.TIMERS import TON  

class T_LVRVTR:
    def __init__(self, SGF1=0, SGF2=0, u_min=40, u2_max=10, t1=0):
        self.SGF1 = SGF1
        self.SGF2 = SGF2        
        self.u_min = u_min
        self.u2_max = u2_max            
        self.t1 = TON()
        self.t1.set_PT(t1)
        self.rs_u = RSTrigger(state=0)
        self.rs_u2 = RSTrigger(state=0)
     

    def Step(self, VYVOD = 0, OV = 0, vnesh_bnn_srab=0, u_ab=0, u_bc=0, u_ca=0, u2=0):

        vvod = (not(OV or VYVOD)) and (self.SGF1==1) # Ввод
        oper_vyvod = (OV or VYVOD) and (self.SGF1==1) # Оперативный вывод

        u_max = max(u_ab, u_bc, u_ca)
        #print(u_ab, u_bc, u_ca)
        io_u = self.rs_u.run((u_max<=self.u_min), (u_max>1.05*self.u_min))
        io_u2 = self.rs_u2.run((u2>=self.u2_max), (u2<0.95*self.u2_max))

        u_lin_pusk = (self.SGF1==1) and (0 if (self.SGF2==1) else io_u)
        u2_pusk = (self.SGF1==1) and (0 if (self.SGF2==1) else io_u2)

        pusk = vvod and (u_lin_pusk or u2_pusk)

        self.t1.IN = pusk
        Q, ET = self.t1.start()  # Запускаем таймер и получаем выход и прошедшее время

        neispr_zn = Q or (vvod and (0 if (self.SGF2==0) else vnesh_bnn_srab))

        return vvod, oper_vyvod, u_lin_pusk, u2_pusk, pusk, neispr_zn

    # Геттеры и сеттеры
    def get_SGF1(self):
        return self.SGF1
    def set_SGF1(self, value):
        self.SGF1 = value

    def get_T1(self):
        return self.t1.PT  # Предустановленное время таймера
    # Сеттер для времени таймера
    def set_T1(self, T):
        self.t1.set_PT(T)  # Устанавливаем предустановленное время таймера

    def get_u_min(self):
        return self.u_min
    def set_u_min(self, u_min):
        self.u_min = u_min

    def get_u2_max(self):
        return self.u2_max
    def set_u2_max(self, u2_max):
        self.u_min = u2_max

if __name__ == "__main__":
    kzn = T_LVRVTR(SGF1=1, SGF2=0, u_min=40, u2_max=10, t1=0)
    res = kzn.Step(VYVOD = 0, OV = 0, vnesh_bnn_srab=1, u_ab=30, u_bc=30, u_ca=30, u2=20)
    print(res)