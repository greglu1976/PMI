# Орган блокировки ЛЗШ (БЛЗШ) (LBPRBLC) RBLC1
# SGF1 - БлокЛЗШ_выбор_ст - Выбор ступени блокировки (Не предусмотрено/ 1 ступень/ 2 ступень/ 3 ступень)


class LBPRBLC:
    def __init__(self, SGF1=0):
        self.SGF1 = SGF1
 
    def Step(self, mtz1_pusk, mtz2_pusk, mtz3_pusk):

        blok = 0 if (self.SGF1==1) else mtz1_pusk if (self.SGF1==2) else mtz2_pusk if (self.SGF1==3) else mtz3_pusk

        return blok

    # Геттеры и сеттеры
    def get_SGF1(self):
        return self.SGF1
    def set_SGF1(self, value):
        self.SGF1 = value
 