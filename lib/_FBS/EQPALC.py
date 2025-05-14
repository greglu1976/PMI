# Защита от потери охлаждения (ЗПО) (EQPALC)
# НЕ ПРОВЕРЕНО!!
from lib._FUNCS.LVOILEQPALC import LVOILEQPALC # импортируем функцию ЗПО

class EQPALC:
    def __init__(self, SGF1_lvoileqpalc_eqpalc, SGF2_lvoileqpalc_eqpalc, SGF3_lvoileqpalc_eqpalc,T1_lvoileqpalc_eqpalc):
        self.palc1 = LVOILEQPALC(SGF1_lvoileqpalc_eqpalc, SGF2_lvoileqpalc_eqpalc, SGF3_lvoileqpalc_eqpalc,T1_lvoileqpalc_eqpalc)

    def Step(self, VYVOD, OV, NaSign, otkaz_so, ToZpoPusk, t_masla_zpo):

        vvod_lvoileqpalc_eqpalc, oper_vyvod_lvoileqpalc_eqpalc, pusk_lvoileqpalc_eqpalc, srabsign_lvoileqpalc_eqpalc, srab_lvoileqpalc_eqpalc, ET = self.palc1.Step(VYVOD, OV, NaSign, otkaz_so, ToZpoPusk, t_masla_zpo)

        return vvod_lvoileqpalc_eqpalc, oper_vyvod_lvoileqpalc_eqpalc, pusk_lvoileqpalc_eqpalc, srabsign_lvoileqpalc_eqpalc, srab_lvoileqpalc_eqpalc

if __name__ == "__main__":
    fb = EQPALC(SGF1=1, SGF2=1, SGF3=1, T1=0)
    res = fb.Step(0,0,0,0,0,0,0,0,0)
    print(res)