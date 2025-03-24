# ФБ Защита от обрыва провода (ЗОП) (LVNSTOC)

from lib._FUNCS.LVNSPTOC import LVNSPTOC # импортируем функцию ЗОП

class LVNSTOC:
    def __init__(self, SGF1_nsptoc1_lvnstoc, SGF2_nsptoc1_lvnstoc, T1_nsptoc1_lvnstoc, I2set_nsptoc1_lvnstoc, RatioSet_nsptoc1_lvnstoc, In_nsptoc1_lvnstoc):
        self.nsptoc1 = LVNSPTOC(SGF1_nsptoc1_lvnstoc, SGF2_nsptoc1_lvnstoc, T1_nsptoc1_lvnstoc, I2set_nsptoc1_lvnstoc, RatioSet_nsptoc1_lvnstoc, In_nsptoc1_lvnstoc)

    def Step(self, VYVOD, OV_nsptoc1_lvnstoc, NaSign_nsptoc1_lvnstoc, I2, I1):

        vvod_nsptoc1_lvnstoc, oper_vyvod_nsptoc1_lvnstoc, srab_nsptoc1_lvnstoc, srabsign_nsptoc1_lvnstoc, pusk_nsptoc1_lvnstoc, io_I2_nsptoc1_lvnstoc, io_rat_nsptoc1_lvnstoc, ET_nsptoc1_lvnstoc = self.nsptoc1.Step(VYVOD, OV_nsptoc1_lvnstoc, NaSign_nsptoc1_lvnstoc, I2, I1)

        return vvod_nsptoc1_lvnstoc, oper_vyvod_nsptoc1_lvnstoc, srab_nsptoc1_lvnstoc, srabsign_nsptoc1_lvnstoc, pusk_nsptoc1_lvnstoc, io_I2_nsptoc1_lvnstoc, io_rat_nsptoc1_lvnstoc, ET_nsptoc1_lvnstoc

if __name__ == "__main__":
    fb = LVNSTOC(SGF1=1, SGF2=1, T1=0, Iset=1)
    res = fb.Step(0,0,0,0,0,0,0,0,0)
    print(res)