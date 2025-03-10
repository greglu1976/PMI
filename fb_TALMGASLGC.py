# Функц блок ГЗ сигн

from f_TECHPTRC_2 import TECHPTRC_2

class TALMGASLGC:
    def __init__(self, SGF1_ptrc1_talmgaslgc, SGF2_ptrc1_talmgaslgc, T1_ptrc1_talmgaslgc):

        self.ptrc1 = TECHPTRC_2(SGF1_ptrc1_talmgaslgc, SGF2_ptrc1_talmgaslgc, T1_ptrc1_talmgaslgc)


    def Step(self, VYVOD, OV_ptrc1_talmgaslgc, NaOtkl_ptrc1_talmgaslgc, srabKont_ptrc1_talmgaslgc, srabKI_ptrc1_talmgaslgc, Sbros):
        vvod_ptrc1_talmgaslgc, oper_vyvod_ptrc1_talmgaslgc, srab_ptrc1_talmgaslgc, srabsign_ptrc1_talmgaslgc, zablok_ptrc1_talmgaslgc, ET_ptrc1_talmgaslgc = self.ptrc1.Step(OV_ptrc1_talmgaslgc, VYVOD, NaOtkl_ptrc1_talmgaslgc, srabKont_ptrc1_talmgaslgc, srabKI_ptrc1_talmgaslgc, Sbros)

        return (vvod_ptrc1_talmgaslgc, oper_vyvod_ptrc1_talmgaslgc, srab_ptrc1_talmgaslgc, srabsign_ptrc1_talmgaslgc, zablok_ptrc1_talmgaslgc, ET_ptrc1_talmgaslgc)


