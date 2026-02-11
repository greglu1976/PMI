# ФБ Логическая защит трансформатора (ЛЗТ) для Т (TTOCLGC)

from lib2.FUNCS.TLGCPTRC import PHSTRPTOC_T # импортируем функцию ЛЗТ

class TTOCLGC:
    def __init__(self, SGF1_ptrc1_ttoclgc, SGF2_ptrc1_ttoclgc, SGF3_ptrc1_ttoclgc, T1_ptrc1_ttoclgc):
        self.ptrc1 = PHSTRPTOC_T(SGF1_ptrc1_ttoclgc, SGF2_ptrc1_ttoclgc, SGF3_ptrc1_ttoclgc, T1_ptrc1_ttoclgc)

    def Step(self, VYVOD, OV_ptrc1_ttoclgc, vnesh_pusk_ptrc1_ttoclgc, mtz2_pusk_ptrc1_ttoclgc, mtz3_pusk_ptrc1_ttoclgc, blok_lzt_ptrc1_ttoclgc):

        vvod_ptrc1_ttoclgc, oper_vyvod_ptrc1_ttoclgc, pusk_ptrc1_ttoclgc, srab_ptrc1_ttoclgc, ET_ptrc1_ttoclgc = self.ptrc1.Step(VYVOD, OV_ptrc1_ttoclgc, vnesh_pusk_ptrc1_ttoclgc, mtz2_pusk_ptrc1_ttoclgc, mtz3_pusk_ptrc1_ttoclgc, blok_lzt_ptrc1_ttoclgc)

        return vvod_ptrc1_ttoclgc, oper_vyvod_ptrc1_ttoclgc, pusk_ptrc1_ttoclgc, srab_ptrc1_ttoclgc, ET_ptrc1_ttoclgc

if __name__ == "__main__":
    fb = TTOCLGC(SGF1=1, SGF2=1, T1=0, Iset=1)
    res = fb.Step(0,0,0,0,0,0,0,0,0)
    print(res)