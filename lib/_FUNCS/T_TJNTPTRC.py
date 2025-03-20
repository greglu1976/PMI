# (T_TJNTPTRC) ЛО - Логика отключения (в составе устройства ЮНИТ-М3-Т)
# SGF1 - Ввод_функции - Ввод функции в работу (Не предусмотрено/ Предусмотренно)

class T_TJNTPTRC:
    def __init__(self, SGF1=0):
        self.SGF1 = SGF1

    def Step(self, VYVOD, OV, OVlo, signals = (0,), mtz2_srab=0, mtz3_srab=0):
        vvod = (not(OV or OVlo or VYVOD)) and (self.SGF1==1) # Ввод
        oper_vyvod = (OV or OVlo or VYVOD) and (self.SGF1==1) # Оперативный вывод

        pusk = any(signals)
        srab = vvod and (pusk or mtz2_srab or mtz3_srab)
        return vvod, oper_vyvod, pusk, srab

    # Геттер для SGF1
    def get_SGF1(self):
        return self.SGF1
    # Сеттер для SGF1
    def set_SGF1(self, value):
        self.SGF1 = value


if __name__ == "__main__":
    lo = T_TJNTPTRC(SGF1=1)
    res = lo.Step(0,0,0, (0,0,0,0,), 0,1)
    print(res)