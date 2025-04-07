# (BTS1RBLC) ЗАВР - Логика запрета АВР (в составе устройства ЮНИТ-М3-Т) ЗАВР ЛО НН
# SGF1 - Ввод_функции - Ввод функции в работу (Не предусмотрено/ Предусмотренно)

class BTS1RBLC:
    def __init__(self, SGF1=0):
        self.SGF1 = SGF1 # SGF1 - Ввод_функции - Ввод функции в работу (Не предусмотрено/ Предусмотренно)
 
    def Step(self, VYVOD, OV, OVzavr, lot_zapret_avr):
        vvod = (not(OV or OVzavr or VYVOD)) and (self.SGF1==1) # ЗАВР: Ввод
        oper_vyvod = (OV or OVzavr or VYVOD) and (self.SGF1==1) # ЗАВР: Оперативный вывод
        zapret = vvod and lot_zapret_avr
        return vvod, oper_vyvod, zapret

    # Геттеры и сеттеры
    def get_SGF1(self):
        return self.SGF1
    def set_SGF1(self, value):
        self.SGF1 = value

if __name__ == "__main__":
    f = BTS1RBLC(SGF1=1)
    res = f.Step(0,0,0,1,0)
    print(res)