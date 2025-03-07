# Функц блок ТС 

# НЕ ТЕСТИРОВАЛСЯ!

from f_TECHPTRC_4 import TECHPTRC_4

class ALMTECHLGC_UIRZ:
    def __init__(self, SGF1_prvlvptrc1_almtechlgc, SGF1_shvlvptrc1_almtechlgc,SGF1_levptrc1_almtechlgc):
        self.prvlvptrc1 = TECHPTRC_4(SGF1_prvlvptrc1_almtechlgc)
        self.shvlvptrc1 = TECHPTRC_4(SGF1_shvlvptrc1_almtechlgc)
        self.levptrc1 = TECHPTRC_4(SGF1_levptrc1_almtechlgc)

    def Step(self, VYVOD, OV_ts, OV_pk, OV_ok, OV_lev, NaSign_pk, NaSign_ok, NaSign_lev, srabKontOtkl_pk, srabKontOtkl_ok, srabKontOtkl_lev):
        vvod_prvlvptrc1_almtechlgc, oper_vyvod_prvlvptrc1_almtechlgc, srab_prvlvptrc1_almtechlgc, srabsign_prvlvptrc1_almtechlgc = self.prvlvptrc1.Step( VYVOD, OV_ts, OV_pk, NaSign_pk, srabKontOtkl_pk)
        vvod_shvlvptrc1_almtechlgc, oper_vyvod_shvlvptrc1_almtechlgc, srab_shvlvptrc1_almtechlgc, srabsign_shvlvptrc1_almtechlgc = self.shvlvptrc1.Step( VYVOD, OV_ts, OV_ok, NaSign_ok, srabKontOtkl_ok)
        vvod_levptrc1_almtechlgc, oper_vyvod_levptrc1_almtechlgc, srab_levptrc1_almtechlgc, srabsign_levptrc1_almtechlgc = self.levptrc1.Step( VYVOD, OV_ts, OV_lev, NaSign_lev, srabKontOtkl_lev)

        return (vvod_prvlvptrc1_almtechlgc, oper_vyvod_prvlvptrc1_almtechlgc, srab_prvlvptrc1_almtechlgc, srabsign_prvlvptrc1_almtechlgc, vvod_shvlvptrc1_almtechlgc, oper_vyvod_shvlvptrc1_almtechlgc, srab_shvlvptrc1_almtechlgc, srabsign_shvlvptrc1_almtechlgc, vvod_levptrc1_almtechlgc, oper_vyvod_levptrc1_almtechlgc, srab_levptrc1_almtechlgc, srabsign_levptrc1_almtechlgc)

