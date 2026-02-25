# Функция контроля тока ЗДЗ для Т и Т2

# SGF1 - Ввод_функции - Ввод функции в работу (Не предусмотрено/ Предусмотрено)
# SGF2 - Выбор_пуск - Выбор пускового органа (Внутренний/  МТЗ 1 ст/ МТЗ 2 ст/ МТЗ 3 ст)

from lib2.TRIGGERS.TRIGGERS import RSTrigger

class PHSTRPTOC_T:
    def __init__(self, SGF1, SGF2, Iset):
        self.SGF1 = SGF1
        self.SGF2 = SGF2       
        self.Iset = Iset
        self.RS = RSTrigger(state=0)

    def Step(self, VYVOD, OV, IA, IB, IC, mtz1_pusk, mtz2_pusk, mtz3_pusk):

        vvod = (not(OV or VYVOD)) and (self.SGF1==1) # ТК ЗДЗ: Ввод
        oper_vyvod = (OV or VYVOD) and (self.SGF1==1) # ТК ЗДЗ: Оперативный вывод

        I = max(IA, IB, IC)
        io = (self.SGF1==1) and (self.RS.run((I>=self.Iset), (I<0.95*self.Iset))) and (1 if self.SGF2==0 else 0)
        pusk = vvod and (io or (mtz1_pusk if self.SGF2==1 else 0) or (mtz2_pusk if self.SGF2==2 else 0) or (mtz3_pusk if self.SGF2==3 else 0))

        return vvod, oper_vyvod, pusk, io
 
    # Геттеры и сеттеры
    def get_SGF1(self):
        return self.SGF1
    def set_SGF1(self, value):
        self.SGF1 = value
    def get_SGF2(self):
        return self.SGF2
    def set_SGF2(self, value):
        self.SGF2 = value

if __name__ == "__main__":
    f = PHSTRPTOC_T(SGF1=1, T1=0, Iset=1)
    res = f.Step(0,0,0,0,0,0)
    print(res)