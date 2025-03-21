# ФБ Токовый контроль ЗДЗ (ТК ЗДЗ) (LVARCTOC) для Т Т2

from lib._FUNCS.PHSTRPTOC_T import PHSTRPTOC_T # импортируем функцию ТК ЗДЗ

class LVARCTOC:
    def __init__(self, SGF1_ptoc1_lvarctoc, SGF2_ptoc1_lvarctoc, Iset_ptoc1_lvarctoc):
        self.ptoc1 = PHSTRPTOC_T(SGF1_ptoc1_lvarctoc, SGF2_ptoc1_lvarctoc, Iset_ptoc1_lvarctoc)

    def Step(self, VYVOD, OV_ptoc1_lvarctoc, IA, IB, IC, mtz1_pusk, mtz2_pusk, mtz3_pusk):
        vvod_ptoc1_lvarctoc, oper_vyvod_ptoc1_lvarctoc, pusk_ptoc1_lvarctoc, io_ptoc1_lvarctoc = self.ptoc1.Step(VYVOD, OV_ptoc1_lvarctoc, IA, IB, IC, mtz1_pusk, mtz2_pusk, mtz3_pusk)
        return vvod_ptoc1_lvarctoc, oper_vyvod_ptoc1_lvarctoc, pusk_ptoc1_lvarctoc, io_ptoc1_lvarctoc

if __name__ == "__main__":
    fb = LVARCTOC(SGF1=1, T1=0, Iset=1)
    res = fb.Step(0,0,0,0,0,0)
    print(res)