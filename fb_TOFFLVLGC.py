# (TOFFLVLGC) Функция ЛО Т - Логика отключения трансформатора 35 кВ (в составе устройства ЮНИТ-М3-Т)

from T_TJNTPTRC import T_TJNTPTRC
from T_JNTRBRE import T_JNTRBRE
from T_BTS1RBLC import T_BTS1RBLC

class TOFFLVLGC:
    def __init__(self, SGF1_ptrc1_tofflvlgc, SGF1_rbre1_tofflvlgc, SGF2_rbre1_tofflvlgc, SGF3_rbre1_tofflvlgc, SGF1_rblc1_tofflvlgc, SGF2_rblc1_tofflvlgc, SGF3_rblc1_tofflvlgc):
        self.ptrc1 = T_TJNTPTRC(SGF1_ptrc1_tofflvlgc)
        self.rbre1 = T_JNTRBRE(SGF1_rbre1_tofflvlgc, SGF2_rbre1_tofflvlgc, SGF3_rbre1_tofflvlgc)
        self.rblc1 = T_BTS1RBLC(SGF1_rblc1_tofflvlgc, SGF2_rblc1_tofflvlgc, SGF3_rblc1_tofflvlgc)

    def Step(self, VYVOD, OV_tofflvlg, OVlo_tofflvlg, signals_tofflvlg, mtz2_srab_tofflvlg, mtz3_srab_tofflvlg, OVzapv_tofflvlg, OVzavr_tofflvlg):

        vvod_ptrc1_tofflvlgc, oper_vyvod_ptrc1_tofflvlgc, pusk_ptrc1_tofflvlgc, srab_ptrc1_tofflvlgc = self.ptrc1.Step(VYVOD, OV_tofflvlg, OVlo_tofflvlg, signals_tofflvlg, mtz2_srab_tofflvlg, mtz3_srab_tofflvlg)
        vvod_rbre1_tofflvlgc, oper_vyvod_rbre1_tofflvlgc, zapret_rbre1_tofflvlgc = self.rbre1.Step(VYVOD, OV_tofflvlg, OVzapv_tofflvlg, pusk_ptrc1_tofflvlgc, mtz2_srab_tofflvlg, mtz3_srab_tofflvlg)
        vvod_rblc1_tofflvlgc, oper_vyvod_rblc1_tofflvlgc, zapret_rblc1_tofflvlgc = self.rblc1.Step(VYVOD, OV_tofflvlg, OVzavr_tofflvlg, mtz2_srab_tofflvlg, mtz3_srab_tofflvlg)

        return vvod_ptrc1_tofflvlgc, oper_vyvod_ptrc1_tofflvlgc, pusk_ptrc1_tofflvlgc, srab_ptrc1_tofflvlgc, vvod_rblc1_tofflvlgc, oper_vyvod_rblc1_tofflvlgc, zapret_rblc1_tofflvlgc, vvod_rbre1_tofflvlgc, oper_vyvod_rbre1_tofflvlgc, zapret_rbre1_tofflvlgc

if __name__ == "__main__":
    lot = TOFFLVLGC(SGF1_ptrc1=0, SGF1_rbre1=0, SGF2_rbre1=0, SGF3_rbre1=0, SGF1_rblc1=0, SGF2_rblc1=0, SGF3_rblc=0)
    res = lot.Step(0,0,0,(0,0),0,0,0,0)
    print(res)