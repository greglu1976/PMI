# ФБ Токовые органы пуска защиты от потери охлаждения (ТО ЗПО) (TPALC)

from lib2.FUNCS.PHSTRPTOC import PHSTRPTOC # импортируем функцию ТО

class TPALC:
    def __init__(self, SGF1_hvptoc1_tpalc, Iset_hvptoc1_tpalc, SGF1_lvptoc1_tpalc, Iset_lvptoc1_tpalc, SGF1_lvptoc2_tpalc, Iset_lvptoc2_tpalc):
        self.hvptoc1 = PHSTRPTOC(SGF1_hvptoc1_tpalc, Iset_hvptoc1_tpalc)
        self.lvptoc1 = PHSTRPTOC(SGF1_lvptoc1_tpalc, Iset_lvptoc1_tpalc)
        self.lvptoc2 = PHSTRPTOC(SGF1_lvptoc2_tpalc, Iset_lvptoc2_tpalc)        

    def Step(self, VYVOD, OV_tpalc, OV_hvptoc1_tpalc, IA, IB, IC,  OV_lvptoc1_tpalc, IA1, IB1, IC1,  OV_lvptoc2_tpalc, IA2, IB2, IC2):

        vvod_hvptoc1_tpalc, oper_vyvod_hvptoc1_tpalc, pusk_hvptoc1_tpalc, io_hvptoc1_tpalc = self.hvptoc1.Step(VYVOD, OV_tpalc, OV_hvptoc1_tpalc, IA, IB, IC)
        vvod_lvptoc1_tpalc, oper_vyvod_lvptoc1_tpalc, pusk_lvptoc1_tpalc, io_lvptoc1_tpalc = self.lvptoc1.Step(VYVOD, OV_tpalc, OV_lvptoc1_tpalc, IA1, IB1, IC1)
        vvod_lvptoc2_tpalc, oper_vyvod_lvptoc2_tpalc, pusk_lvptoc2_tpalc, io_lvptoc2_tpalc = self.lvptoc2.Step(VYVOD, OV_tpalc, OV_lvptoc2_tpalc, IA2, IB2, IC2)

        pusk_tpalc = pusk_hvptoc1_tpalc or pusk_lvptoc1_tpalc or pusk_lvptoc2_tpalc
        vvod_tpalc = vvod_hvptoc1_tpalc or vvod_lvptoc1_tpalc or vvod_lvptoc2_tpalc

        return vvod_hvptoc1_tpalc, oper_vyvod_hvptoc1_tpalc, pusk_hvptoc1_tpalc, io_hvptoc1_tpalc, vvod_lvptoc1_tpalc, oper_vyvod_lvptoc1_tpalc, pusk_lvptoc1_tpalc, io_lvptoc1_tpalc, vvod_lvptoc2_tpalc, oper_vyvod_lvptoc2_tpalc, pusk_lvptoc2_tpalc, io_lvptoc2_tpalc, pusk_tpalc, vvod_tpalc

if __name__ == "__main__":
    fb = TPALC(SGF1=1, T1=0, Iset=1)
    res = fb.Step(0,0,0,0,0,0)
    print(res)