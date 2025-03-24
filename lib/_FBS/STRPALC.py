# ФБ Токовые органы пуска охлаждения (РТПО) (STRPALC)

from lib._FUNCS.STRPTOC import STRPTOC # импортируем функцию РТПО

class STRPALC:
    def __init__(self, SGF1_hvptoc1_strpalc, Iset_hvptoc1_strpalc, SGF1_lvptoc1_strpalc, Iset_lvptoc1_strpalc, SGF1_lvptoc2_strpalc, Iset_lvptoc2_strpalc):
        self.hvptoc1 = STRPTOC(SGF1_hvptoc1_strpalc, Iset_hvptoc1_strpalc)
        self.lvptoc1 = STRPTOC(SGF1_lvptoc1_strpalc, Iset_lvptoc1_strpalc)
        self.lvptoc2 = STRPTOC(SGF1_lvptoc2_strpalc, Iset_lvptoc2_strpalc)        

    def Step(self, VYVOD, OV_strpalc, OV_hvptoc1_strpalc, IA, IB, IC,  OV_lvptoc1_strpalc, IA1, IB1, IC1,  OV_lvptoc2_strpalc, IA2, IB2, IC2):

        vvod_hvptoc1_strpalc, oper_vyvod_hvptoc1_strpalc, pusk_hvptoc1_strpalc, io_hvptoc1_strpalc = self.hvptoc1.Step(VYVOD, OV_strpalc, OV_hvptoc1_strpalc, IA, IB, IC)
        vvod_lvptoc1_strpalc, oper_vyvod_lvptoc1_strpalc, pusk_lvptoc1_strpalc, io_lvptoc1_strpalc = self.lvptoc1.Step(VYVOD, OV_strpalc, OV_lvptoc1_strpalc, IA1, IB1, IC1)
        vvod_lvptoc2_strpalc, oper_vyvod_lvptoc2_strpalc, pusk_lvptoc2_strpalc, io_lvptoc2_strpalc = self.lvptoc2.Step(VYVOD, OV_strpalc, OV_lvptoc2_strpalc, IA2, IB2, IC2)

        pusk_strpalc = pusk_hvptoc1_strpalc or pusk_lvptoc1_strpalc or pusk_lvptoc2_strpalc
        vvod_strpalc = vvod_hvptoc1_strpalc or vvod_lvptoc1_strpalc or vvod_lvptoc2_strpalc

        return vvod_hvptoc1_strpalc, oper_vyvod_hvptoc1_strpalc, pusk_hvptoc1_strpalc, io_hvptoc1_strpalc, vvod_lvptoc1_strpalc, oper_vyvod_lvptoc1_strpalc, pusk_lvptoc1_strpalc, io_lvptoc1_strpalc, vvod_lvptoc2_strpalc, oper_vyvod_lvptoc2_strpalc, pusk_lvptoc2_strpalc, io_lvptoc2_strpalc, pusk_strpalc, vvod_strpalc

if __name__ == "__main__":
    fb = STRPALC(SGF1=1, T1=0, Iset=1)
    res = fb.Step(0,0,0,0,0,0)
    print(res)