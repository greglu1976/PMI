# для технологической сигнализации

class TECHPTRC_4:
    def __init__(self, SGF1=0):
        self.SGF1 = SGF1

    def Step(self, VYVOD, OV_fb, OV_func, NaSign, srabKont):
        vvod = (not(VYVOD or OV_fb or OV_func)) and (self.SGF1==1)
        oper_vyvod = (VYVOD or OV_fb or OV_func) and (self.SGF1==1)
        srabsign = vvod and srabKont
        srab = not(NaSign) and srabsign
        return vvod, oper_vyvod, srab, srabsign

        # Геттер для SGF1
    def get_SGF1(self):
        return self.SGF1
    # Сеттер для SGF1
    def set_SGF1(self, value):
        self.SGF1 = value
 