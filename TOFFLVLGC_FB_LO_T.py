# (TOFFLVLGC) Функция ЛО Т - Логика отключения трансформатора 35 кВ (в составе устройства ЮНИТ-М3-Т)

from T_TJNTPTRC import T_TJNTPTRC
from T_JNTRBRE import T_JNTRBRE
from T_BTS1RBLC import T_BTS1RBLC

class TOFFLVLGC:
    def __init__(self, SGF1_ptrc1, SGF1_rbre1, SGF2_rbre1, SGF3_rbre1, SGF1_rblc1, SGF2_rblc1, SGF3_rblc1):
        self.ptrc1 = T_TJNTPTRC(SGF1_ptrc1)
        self.rbre1 = T_JNTRBRE(SGF1_rbre1, SGF2_rbre1, SGF3_rbre1)
        self.rblc1 = T_BTS1RBLC(SGF1_rblc1, SGF2_rblc1, SGF3_rblc1)

    def Step(self, VYVOD, OV, OVlo, signals, mtz2_srab, mtz3_srab, OVzapv, OVzavr):

        vvod_ptrc1, oper_vyvod_ptrc1, pusk_ptrc1, srab_ptrc1 = self.ptrc1.Step(VYVOD, OV, OVlo, signals, mtz2_srab, mtz3_srab)
        vvod_rbre1, oper_vyvod_rbre1, zapret_rbre1 = self.rbre1.Step(VYVOD, OV, OVzapv, pusk_ptrc1, mtz2_srab, mtz3_srab)
        vvod_rblc1, oper_vyvod_rblc1, zapret_rblc1 = self.rblc1.Step(VYVOD, OV, OVzavr, mtz2_srab, mtz3_srab)

        return vvod_ptrc1, oper_vyvod_ptrc1, pusk_ptrc1, srab_ptrc1, vvod_rblc1, oper_vyvod_rblc1, zapret_rblc1, vvod_rbre1, oper_vyvod_rbre1, zapret_rbre1

if __name__ == "__main__":
    lot = TOFFLVLGC(SGF1_ptrc1=0, SGF1_rbre1=0, SGF2_rbre1=0, SGF3_rbre1=0, SGF1_rblc1=0, SGF2_rblc1=0, SGF3_rblc=0)
    res = lot.Step(0,0,0,(0,0),0,0,0,0)
    print(res)