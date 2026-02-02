# Функц блок ТЗ

# НЕ ТЕСТИРОВАЛСЯ!

from lib2.FUNCS.TECHPTRC_3 import TECHPTRC_3
from lib2.FUNCS.TECHPTRC import TECHPTRC

class APTTECHLGC:
    def __init__(self, SGF1_oilptrc1_apttechlgc, SGF2_oilptrc1_apttechlgc,
                    SGF1_winptrc1_apttechlgc, SGF2_winptrc1_apttechlgc, 
                    SGF1_vlvptrc1_apttechlgc, SGF2_vlvptrc1_apttechlgc, T1_apttechlgc,
    ):
        self.oilptrc1 = TECHPTRC_3(SGF1_oilptrc1_apttechlgc, SGF2_oilptrc1_apttechlgc, T=T1_apttechlgc)
        self.winptrc1 = TECHPTRC_3(SGF1_winptrc1_apttechlgc, SGF2_winptrc1_apttechlgc, T=T1_apttechlgc)
        self.vlvptrc1 = TECHPTRC(SGF1_vlvptrc1_apttechlgc, SGF2_vlvptrc1_apttechlgc, T=T1_apttechlgc)

    def Step(self, VYVOD, OV_tz, OV_dtm, OV_dto, OV_rd, NaSign_dtm, NaSign_dto, NaSign_rd, srabKontOtkl_m, srabKontSign_m, srabKontOtkl_o, srabKontSign_o, srabKontOtkl_rd, srabKI_m, srabKI_o, srabKI_rd, Sbros):
        vvod_oilptrc1_apttechlgc, oper_vyvod_oilptrc1_apttechlgc, srab_oilptrc1_apttechlgc, srabsign_oilptrc1_apttechlgc, zablok_oilptrc1_apttechlgc, ET_oilptrc1_apttechlgc = self.oilptrc1.Step( VYVOD, OV_tz, OV_dtm, NaSign_dtm, srabKontOtkl_m, srabKontSign_m, srabKI_m, Sbros)
        vvod_winptrc1_apttechlgc, oper_vyvod_winptrc1_apttechlgc, srab_winptrc1_apttechlgc, srabsign_winptrc1_apttechlgc, zablok_winptrc1_apttechlgc, ET_winptrc1_apttechlgc = self.winptrc1.Step( VYVOD, OV_tz, OV_dto, NaSign_dto, srabKontOtkl_o, srabKontSign_o, srabKI_o, Sbros)

        vvod_vlvptrc1_apttechlgc, oper_vyvod_vlvptrc1_apttechlgc, srab_vlvptrc1_apttechlgc, srabsign_vlvptrc1_apttechlgc, zablok_vlvptrc1_apttechlgc, ET_vlvptrc1_apttechlgc = self.vlvptrc1.Step( VYVOD, OV_tz, OV_rd, NaSign_rd, srabKontOtkl_rd, srabKI_rd, Sbros)

        return (vvod_oilptrc1_apttechlgc, oper_vyvod_oilptrc1_apttechlgc, srab_oilptrc1_apttechlgc, srabsign_oilptrc1_apttechlgc, zablok_oilptrc1_apttechlgc, ET_oilptrc1_apttechlgc, vvod_winptrc1_apttechlgc, oper_vyvod_winptrc1_apttechlgc, srab_winptrc1_apttechlgc, srabsign_winptrc1_apttechlgc, zablok_winptrc1_apttechlgc, ET_winptrc1_apttechlgc, vvod_vlvptrc1_apttechlgc, oper_vyvod_vlvptrc1_apttechlgc, srab_vlvptrc1_apttechlgc, srabsign_vlvptrc1_apttechlgc, zablok_vlvptrc1_apttechlgc, ET_vlvptrc1_apttechlgc)
