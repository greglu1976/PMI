# ФБ ЗДЗ ОЛ (ARCTOC)

from lib._FUNCS.ARCPTOC import ARCPTOC
from lib._ADD.threePhaseSys import ThreePhaseSystem # класс для расчета аналоговых значений 

class ARCTOC:
    def __init__(self, SGF1_arcptoc1_arctoc, SGF2_arcptoc1_arctoc, SGF3_arcptoc1_arctoc, SGF4_arcptoc1_arctoc, T1_arcptoc1_arctoc, T2_arcptoc1_arctoc, Iset_arcptoc1_arctoc, U0set_arcptoc1_arctoc):
        self.arcptoc1 = ARCPTOC(SGF1_arcptoc1_arctoc, SGF2_arcptoc1_arctoc, SGF3_arcptoc1_arctoc, SGF4_arcptoc1_arctoc, T1_arcptoc1_arctoc, T2_arcptoc1_arctoc, Iset_arcptoc1_arctoc, U0set_arcptoc1_arctoc)

    def Step(self, VYVOD, OV_ZDZ, NaSign_ZDZ, SrabZDZ, BNNshSrab, KtrTokZDZ, IA, IB, IC, UA1, dUA1, UB1, dUB1, UC1, dUC1):

        threeU = ThreePhaseSystem(UA1, dUA1, UB1, dUB1, UC1, dUC1)
        Usimm = threeU.calculate_symmetric_components()
        U0 = 3*Usimm['U0']['amplitude']

        vvod, oper_vyvod, ZDZ_neispr, ZDZ_srab, ZDZ_srabsign, pusk, uo, io_max = self.arcptoc1.Step(VYVOD or OV_ZDZ, NaSign_ZDZ, SrabZDZ, BNNshSrab, KtrTokZDZ, IA, IB, IC, U0)

        return vvod, oper_vyvod, ZDZ_neispr, ZDZ_srab, ZDZ_srabsign, pusk, uo, io_max, U0

