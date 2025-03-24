# ФБ ТО блокировки РПН (ТО РПН) (LTCBLKTOC)

from lib._FUNCS.PHSTRPTOC_TORPN import PHSTRPTOC_TORPN # импортируем функцию ТО РПН

class LTCBLKTOC:
    def __init__(self, SGF1_ptoc1_ltcblktoc, Iset_ptoc1_ltcblktoc):
        self.ptoc1 = PHSTRPTOC_TORPN(SGF1_ptoc1_ltcblktoc, Iset_ptoc1_ltcblktoc)

    def Step(self, VYVOD, OV_ptoc1_ltcblktoc, IA, IB, IC):
        vvod_ptoc1_ltcblktoc, oper_vyvod_ptoc1_ltcblktoc, pusk_ptoc1_ltcblktoc, io_ptoc1_ltcblktoc = self.ptoc1.Step(VYVOD, OV_ptoc1_ltcblktoc, IA, IB, IC)
        return vvod_ptoc1_ltcblktoc, oper_vyvod_ptoc1_ltcblktoc, pusk_ptoc1_ltcblktoc, io_ptoc1_ltcblktoc

if __name__ == "__main__":
    fb = LTCBLKTOC(SGF1=1, Iset=1)
    res = fb.Step(0,0,0,0,0,0)
    print(res)