# Функция ТО блок РПН

# SGF1 - Ввод_функции - Ввод функции в работу (Не предусмотрено/ Предусмотрено)

from lib2.TRIGGERS.TRIGGERS import RSTrigger

class PHSTRPTOC_TORPN:
    def __init__(self, SGF1, Iset):
        self.SGF1 = SGF1
        self.Iset = Iset
        self.RS = RSTrigger(state=0)

    def Step(self, VYVOD, OV, IA, IB, IC):

        vvod = (not(OV or VYVOD)) and (self.SGF1==1) # ТО: Ввод
        oper_vyvod = (OV or VYVOD) and (self.SGF1==1) # ТО Оперативный вывод

        I = max(IA, IB, IC)
        io = (self.SGF1==1) and (self.RS.run((I>=self.Iset), (I<0.95*self.Iset)))
        pusk = vvod and io 

        return vvod, oper_vyvod, pusk, io
 
    # Геттеры и сеттеры
    def get_SGF1(self):
        return self.SGF1
    def set_SGF1(self, value):
        self.SGF1 = value


if __name__ == "__main__":
    f = PHSTRPTOC_TORPN(SGF1=1, T1=0, Iset=1)
    res = f.Step(0,0,0,0,0,0)
    print(res)