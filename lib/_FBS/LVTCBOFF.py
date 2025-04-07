# LVTCBOFF Функциональный блок Логика отключения В НН Т 35 (ЛО НН) (LVTCBOFF) (в составе устройства ЮНИТ-М3-Т)

from lib._FUNCS.CBPTRC_2 import CBPTRC
from lib._FUNCS.JNTRBRE_2 import JNTRBRE
from lib._FUNCS.BTS1RBLC_2 import BTS1RBLC

class LVTCBOFF:
    def __init__(self,
    SGF1_lvcbptrc1_lvtcboff, T1_lvcbptrc1_lvtcboff,
    SGF1_lvcbrecrbre1_lvtcboff,
    SGF1_lvbtsrblc1_lvtcboff 
    ):
        self.lvcbptrc1 = CBPTRC(SGF1_lvcbptrc1_lvtcboff, T1_lvcbptrc1_lvtcboff)
        self.lvcbrecrbre1 = JNTRBRE(SGF1_lvcbrecrbre1_lvtcboff)
        self.lvbtsrblc1 = BTS1RBLC(SGF1_lvbtsrblc1_lvtcboff)

    def Step(self, VYVOD, OV_lvtcboff, OV_lvcbptrc1_lvtcboff, OV_lvcbrecrbre1_lvtcboff, OV_lvbtsrblc1_lvtcboff, lot_srab, lot_zapret_apv, lot_zapret_avr):

        vvod_lvcbptrc1_lvtcboff, oper_vyvod_lvcbptrc1_lvtcboff, otkl_lvcbptrc1_lvtcboff, otkl_avar_lvcbptrc1_lvtcboff = self.lvcbptrc1.Step(VYVOD, OV_lvtcboff, OV_lvcbptrc1_lvtcboff, lot_srab)
        vvod_lvcbrecrbre1_lvtcboff, oper_vyvod_lvcbrecrbre1_lvtcboff, zapret_lvcbrecrbre1_lvtcboff = self.lvcbrecrbre1.Step(VYVOD, OV_lvtcboff, OV_lvcbrecrbre1_lvtcboff, lot_zapret_apv)
        vvod_lvbtsrblc1_lvtcboff, oper_vyvod_lvbtsrblc1_lvtcboff, zapret_lvbtsrblc1_lvtcboff = self.lvbtsrblc1.Step(VYVOD, OV_lvtcboff, OV_lvbtsrblc1_lvtcboff, lot_zapret_avr)

        return vvod_lvcbptrc1_lvtcboff, oper_vyvod_lvcbptrc1_lvtcboff, otkl_lvcbptrc1_lvtcboff, otkl_avar_lvcbptrc1_lvtcboff, vvod_lvcbrecrbre1_lvtcboff, oper_vyvod_lvcbrecrbre1_lvtcboff, zapret_lvcbrecrbre1_lvtcboff, vvod_lvbtsrblc1_lvtcboff, oper_vyvod_lvbtsrblc1_lvtcboff, zapret_lvbtsrblc1_lvtcboff

if __name__ == "__main__":
    fb = LVTCBOFF()
    res = fb.Step(0,0,0,0,0,0,0)
    print(res)