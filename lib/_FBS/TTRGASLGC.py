# Функц блок ГЗ откл

from lib._FUNCS.TECHPTRC import TECHPTRC

class TTRGASLGC:
    def __init__(self, SGF1_ptrc1_ttrgaslgc, SGF2_ptrc1_ttrgaslgc, T1_ptrc1_ttrgaslgc):

        self.ptrc1 = TECHPTRC(SGF1_ptrc1_ttrgaslgc, SGF2_ptrc1_ttrgaslgc, T1_ptrc1_ttrgaslgc)

    OV_f = 0

    def Step(self, VYVOD, OV_ptrc1_ttrgaslgc, OV_f, NaSign_ptrc1_ttrgaslgc, srabKont_ptrc1_ttrgaslgc, srabKI_ptrc1_ttrgaslgc, Sbros):
        vvod_ptrc1_ttrgaslgc, oper_vyvod_ptrc1_ttrgaslgc, srab_ptrc1_ttrgaslgc, srabsign_ptrc1_ttrgaslgc, zablok_ptrc1_ttrgaslgc, ET_ptrc1_ttrgaslgc = self.ptrc1.Step(VYVOD, OV_ptrc1_ttrgaslgc, OV_f, NaSign_ptrc1_ttrgaslgc, srabKont_ptrc1_ttrgaslgc, srabKI_ptrc1_ttrgaslgc, Sbros)

        return (vvod_ptrc1_ttrgaslgc, oper_vyvod_ptrc1_ttrgaslgc, srab_ptrc1_ttrgaslgc, srabsign_ptrc1_ttrgaslgc, zablok_ptrc1_ttrgaslgc, ET_ptrc1_ttrgaslgc)


