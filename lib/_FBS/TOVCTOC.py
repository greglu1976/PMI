# ФБ Защита от перегрузки (ЗП Т 35) (TOVCTOC)
# проверено 14.03.25

from lib._FUNCS.PHPTOC_T import PHPTOC_T # импортируем функцию ЗП

class TOVCTOC:
    def __init__(self, SGF1_hvptoc1_lovctoc, T1_hvptoc1_lovctoc, Iset_hvptoc1_lovctoc):
        self.hvptoc1 = PHPTOC_T(SGF1_hvptoc1_lovctoc, T1_hvptoc1_lovctoc, Iset_hvptoc1_lovctoc)

    def Step(self, VYVOD, OV_hvptoc1_lovctoc, NaOtkl_hvptoc1_lovctoc, IA, IB, IC):
        vvod_hvptoc1_lovctoc, oper_vyvod_hvptoc1_lovctoc, pusk_hvptoc1_lovctoc, io_hvptoc1_lovctoc, srab_hvptoc1_lovctoc, srabotkl_hvptoc1_lovctoc, ET_hvptoc1_lovctoc = self.hvptoc1.Step(VYVOD, OV_hvptoc1_lovctoc, NaOtkl_hvptoc1_lovctoc, IA, IB, IC)
        return vvod_hvptoc1_lovctoc, oper_vyvod_hvptoc1_lovctoc, pusk_hvptoc1_lovctoc, io_hvptoc1_lovctoc, srab_hvptoc1_lovctoc, srabotkl_hvptoc1_lovctoc, ET_hvptoc1_lovctoc


if __name__ == "__main__":
    tovctoc = TOVCTOC(SGF1=1, T1=0, Iset=1)
    res = tovctoc.Step(0,0,0,0,0,0)
    print(res)