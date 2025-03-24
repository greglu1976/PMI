# ФБ Токовая отсечка (ТО) (LVTOC)
# НЕ ПРОВЕРЕНО!!
from lib._FUNCS.LVPTOC import LVPTOC # импортируем функцию ТО

class LVTOC:
    def __init__(self, SGF1_ptoc1_lvtoc, SGF2_ptoc1_lvtoc, T1_ptoc1_lvtoc, Iset_ptoc1_lvtoc):
        self.ptoc1 = LVPTOC(SGF1_ptoc1_lvtoc, SGF2_ptoc1_lvtoc, T1_ptoc1_lvtoc, Iset_ptoc1_lvtoc)

    def Step(self, VYVOD, OV_ptoc1_lvtoc, NaSign_ptoc1_lvtoc, IA, IB, IC, IAB, IBC, ICA):
        vvod_ptoc1_lvtoc, oper_vyvod_ptoc1_lvtoc, pusk_ptoc1_lvtoc, io_ptoc1_lvtoc, srabsign_ptoc1_lvtoc, srab_ptoc1_lvtoc, ET_ptoc1_lvtoc = self.ptoc1.Step(VYVOD, OV_ptoc1_lvtoc, NaSign_ptoc1_lvtoc, IA, IB, IC, IAB, IBC, ICA)
        return vvod_ptoc1_lvtoc, oper_vyvod_ptoc1_lvtoc, pusk_ptoc1_lvtoc, io_ptoc1_lvtoc, srabsign_ptoc1_lvtoc, srab_ptoc1_lvtoc, ET_ptoc1_lvtoc

if __name__ == "__main__":
    fb = LVTOC(SGF1=1, SGF2=1, T1=0, Iset=1)
    res = fb.Step(0,0,0,0,0,0,0,0,0)
    print(res)