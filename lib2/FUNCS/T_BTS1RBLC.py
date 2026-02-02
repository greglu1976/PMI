# (T_BTS1RBLC) ЗАВР - Логика запрета АВР (в составе устройства ЮНИТ-М3-Т)
# SGF1 - Ввод_функции - Ввод функции в работу (Не предусмотрено/ Предусмотренно)
# SGF2 - ЗАВР_МТЗ2 - Запрет АВР при срабатывании МТЗ 2 ст.(Не предусмотрено/ Предусмотрено)
# SGF3 - ЗАВР_МТЗ3 - Запрет АВР при срабатывании МТЗ 3 ст. (Не предусмотрено/ Предусмотрено)



class T_BTS1RBLC:
    def __init__(self, SGF1=0, SGF2=0, SGF3=0):
        self.SGF1 = SGF1 # SGF1 - Ввод_функции - Ввод функции в работу (Не предусмотрено/ Предусмотренно)
        self.SGF2 = SGF2 # SGF2 - ЗАПВ_МТЗ2 - Запрет АПВ при срабатывании МТЗ 2 ст. (Не предусмотрено/ Предусмотрено)
        self.SGF3 = SGF3 # SGF3 - ЗАПВ_МТЗ3 - Запрет АПВ при срабатывании МТЗ 3 ст. (Не предусмотрено/ Предусмотрено)               
 
    def Step(self, VYVOD, OV, OVzavr, mtz2_srab, mtz3_srab):
        vvod = (not(OV or OVzavr or VYVOD)) and (self.SGF1==1) # МТЗ: Ввод
        oper_vyvod = (OV or OVzavr or VYVOD) and (self.SGF1==1) # МТЗ: Оперативный вывод
        mtz2_sr = 0 if (self.SGF2==0) else mtz2_srab
        mtz3_sr = 0 if (self.SGF3==0) else mtz3_srab        
        zapret = vvod and (mtz2_sr or mtz3_sr)
        return vvod, oper_vyvod, zapret

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

if __name__ == "__main__":
    ps = T_BTS1RBLC(SGF1=1, SGF2=1, SGF3=0)
    res = ps.Step(0,0,0,1,0)
    print(res)