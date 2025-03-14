# ФБ Защита от перегрузки (ЗП Т 35) (TOVCTOC)


from _FUNCS.PHPTOC_T import PHPTOC_T

class TOVCTOC:
    def __init__(self, SGF1_ptrc1_tltcgaslgc, SGF2_ptrc1_tltcgaslgc, T1_ptrc1_tltcgaslgc):

        self.ptrc1 = PHPTOC_T(SGF1_ptrc1_tltcgaslgc, SGF2_ptrc1_tltcgaslgc, T1_ptrc1_tltcgaslgc)

    OV_f=0
    def Step(self, VYVOD, OV_ptrc1_tltcgaslgc, OV_f,  NaSign_ptrc1_tltcgaslgc, srabKont_ptrc1_tltcgaslgc, srabKI_ptrc1_tltcgaslgc, Sbros):
        vvod_ptrc1_tltcgaslgc, oper_vyvod_ptrc1_tltcgaslgc, srab_ptrc1_tltcgaslgc, srabsign_ptrc1_tltcgaslgc, zablok_ptrc1_tltcgaslgc, ET_ptrc1_tltcgaslgc = self.ptrc1.Step(VYVOD, OV_ptrc1_tltcgaslgc, OV_f, NaSign_ptrc1_tltcgaslgc, srabKont_ptrc1_tltcgaslgc, srabKI_ptrc1_tltcgaslgc, Sbros)

        return (vvod_ptrc1_tltcgaslgc, oper_vyvod_ptrc1_tltcgaslgc, srab_ptrc1_tltcgaslgc, srabsign_ptrc1_tltcgaslgc, zablok_ptrc1_tltcgaslgc, ET_ptrc1_tltcgaslgc)



if __name__ == "__main__":
    tovctoc = TOVCTOC(SGF1=1, T1=0, Iset=1)
    res = tovctoc.Step(0,0,0,0,0,0)
    print(res)