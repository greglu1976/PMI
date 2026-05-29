# ФБ Защита от перегрузки (ЗП Т 35) (TOVCTOC)

from lib2.FUNCS.PHPTOC_DZT import PHPTOC # импортируем функцию ЗП стороны

class TOVCTOC:
    def __init__(self, SGF1_hvptoc1_tovctoc, T1_hvptoc1_tovctoc, Iset_hvptoc1_tovctoc, SGF1_ptoc1_tovctoc, T1_ptoc1_tovctoc, Iset_ptoc1_tovctoc, SGF1_ptoc2_tovctoc, T1_ptoc2_tovctoc, Iset_ptoc2_tovctoc):
        self.hvptoc1 = PHPTOC(SGF1_hvptoc1_tovctoc, T1_hvptoc1_tovctoc, Iset_hvptoc1_tovctoc)
        self.ptoc1 = PHPTOC(SGF1_ptoc1_tovctoc, T1_ptoc1_tovctoc, Iset_ptoc1_tovctoc)
        self.ptoc2 = PHPTOC(SGF1_ptoc2_tovctoc, T1_ptoc2_tovctoc, Iset_ptoc2_tovctoc)        

    def Step(self, VYVOD, OV_tovctoc, OV_hvptoc1_tovctoc, NaOtkl_hvptoc1_tovctoc, IA, IB, IC,  OV_ptoc1_tovctoc, NaOtkl_ptoc1_tovctoc,  IA1, IB1, IC1,  OV_ptoc2_tovctoc, NaOtkl_ptoc2_tovctoc, IA2, IB2, IC2):

        vvod_hvptoc1_tovctoc, oper_vyvod_hvptoc1_tovctoc, pusk_hvptoc1_tovctoc, io_hvptoc1_tovctoc, srab_hvptoc1_tovctoc, srabotkl_hvptoc1_tovctoc, ET_hvptoc1_tovctoc = self.hvptoc1.Step(VYVOD, OV_tovctoc, OV_hvptoc1_tovctoc, NaOtkl_hvptoc1_tovctoc, IA, IB, IC)

        vvod_ptoc1_tovctoc, oper_vyvod_ptoc1_tovctoc, pusk_ptoc1_tovctoc, io_ptoc1_tovctoc, srab_ptoc1_tovctoc, srabotkl_ptoc1_tovctoc, ET_ptoc1_tovctoc = self.ptoc1.Step(VYVOD, OV_tovctoc, OV_ptoc1_tovctoc, NaOtkl_ptoc1_tovctoc, IA1, IB1, IC1)

        vvod_ptoc2_tovctoc, oper_vyvod_ptoc2_tovctoc, pusk_ptoc2_tovctoc, io_ptoc2_tovctoc, srab_ptoc2_tovctoc, srabotkl_ptoc2_tovctoc, ET_ptoc2_tovctoc = self.ptoc2.Step(VYVOD, OV_tovctoc, OV_ptoc2_tovctoc, NaOtkl_ptoc2_tovctoc, IA2, IB2, IC2)

        srab_tovctoc = srab_hvptoc1_tovctoc or srab_ptoc1_tovctoc or srab_ptoc2_tovctoc

        return vvod_hvptoc1_tovctoc, oper_vyvod_hvptoc1_tovctoc, pusk_hvptoc1_tovctoc, io_hvptoc1_tovctoc, srab_hvptoc1_tovctoc, srabotkl_hvptoc1_tovctoc, vvod_ptoc1_tovctoc, oper_vyvod_ptoc1_tovctoc, pusk_ptoc1_tovctoc, io_ptoc1_tovctoc, srab_ptoc1_tovctoc, srabotkl_ptoc1_tovctoc, vvod_ptoc2_tovctoc, oper_vyvod_ptoc2_tovctoc, pusk_ptoc2_tovctoc, io_ptoc2_tovctoc, srab_ptoc2_tovctoc, srabotkl_ptoc2_tovctoc, srab_tovctoc

if __name__ == "__main__":
    fb = TOVCTOC(SGF1=1, T1=0, Iset=1)
    res = fb.Step(0,0,0,0,0,0)
    print(res)