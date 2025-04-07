# (JNTRBRE) ЗАПВ - Логика запрета АПВ (в составе устройства ЮНИТ-М3-Т) ЗАПВ ЛО НН
# SGF1 - Ввод_функции - Ввод функции в работу (Не предусмотрено/ Предусмотренно)

class JNTRBRE:
    def __init__(self, SGF1=0):
        self.SGF1 = SGF1 # SGF1 - Ввод_функции - Ввод функции в работу (Не предусмотрено/ Предусмотренно)
 
    def Step(self, VYVOD, OV, OVzapv, lot_zapret_apv):
        vvod = (not(OV or OVzapv or VYVOD)) and (self.SGF1==1) # ЗАПВ: Ввод
        oper_vyvod = (OV or OVzapv or VYVOD) and (self.SGF1==1) # ЗАПВ: Оперативный вывод
        zapret = vvod and lot_zapret_apv
        return vvod, oper_vyvod, zapret

    # Геттеры и сеттеры
    def get_SGF1(self):
        return self.SGF1
    def set_SGF1(self, value):
        self.SGF1 = value


if __name__ == "__main__":
    f = JNTRBRE(SGF1=1)
    res = f.Step(0,0,0,0,0,1)
    print(res)