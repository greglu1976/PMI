# Функц блок ГЗ откл



#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ВНИЗУ НЕ ПРАВЛЕНО !!!!!!!!!!!!!!!!!!!!!!!!!!!

from f_TECHPTRC import TECHPTRC

class TTRGASLGC:
    def __init__(self, SGF1_ptrc1_talmgaslgc, SGF2_ptrc1_talmgaslgc, T1_ptrc1_talmgaslgc):

        self.ptrc1 = TECHPTRC(SGF1_ptrc1_talmgaslgc, SGF2_ptrc1_talmgaslgc, T1_ptrc1_talmgaslgc)


    def Step(self, VYVOD, OV, NaOtkl, srabKont, srabKI, Sbros):
        vvod_ptrc1_talmgaslgc, oper_vyvod_ptrc1_talmgaslgc, srab_ptrc1_talmgaslgc, srabsign_ptrc1_talmgaslgc, zablok_ptrc1_talmgaslgc, ET_ptrc1_talmgaslgc = self.ptrc1.Step( OV, VYVOD, NaOtkl, srabKont, srabKI, Sbros)

        return (vvod_ptrc1_talmgaslgc, oper_vyvod_ptrc1_talmgaslgc, srab_ptrc1_talmgaslgc, srabsign_ptrc1_talmgaslgc, zablok_ptrc1_talmgaslgc, ET_ptrc1_talmgaslgc)


