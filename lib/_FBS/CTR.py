# ФБ КЦТ 

from lib._FUNCS.DIFRCTR import DIFRCTR

class CTR:
    def __init__(self, SGF1_rctr1, SGF2_rctr1, T1_rctr1, T2_rctr1, Inom_rctr1, Imin_rctr1, Ksym_rctr1, LIsym_rctr1,
            SGF1_rctr2, SGF2_rctr2, T1_rctr2, T2_rctr2, Inom_rctr2, Imin_rctr2, Ksym_rctr2, LIsym_rctr2,
            SGF1_rctr3, SGF2_rctr3, T1_rctr3, T2_rctr3, Inom_rctr3, Imin_rctr3, Ksym_rctr3, LIsym_rctr3):

        self.rctr1 = DIFRCTR(SGF1_rctr1, SGF2_rctr1, T1_rctr1, T2_rctr1, Inom_rctr1, Imin_rctr1, Ksym_rctr1, LIsym_rctr1)
        self.rctr2 = DIFRCTR(SGF1_rctr2, SGF2_rctr2, T1_rctr2, T2_rctr2, Inom_rctr2, Imin_rctr2, Ksym_rctr2, LIsym_rctr2)
        self.rctr3 = DIFRCTR(SGF1_rctr3, SGF2_rctr3, T1_rctr3, T2_rctr3, Inom_rctr3, Imin_rctr3, Ksym_rctr3, LIsym_rctr3)

    def Step(self, VYVOD, OV, OVst_rctr1, IA_rctr1, IB_rctr1, IC_rctr1, OVst_rctr2, IA_rctr2, IB_rctr2, IC_rctr2, OVst_rctr3, IA_rctr3, IB_rctr3, IC_rctr3):

        vvod_rctr1, oper_vyvod_rctr1, pusk_obryv_rctr1, srab_obryv_rctr1, pusk_assym_rctr1, srab_assym_rctr1 = self.rctr1.Step(VYVOD, OV, OVst_rctr1, IA_rctr1, IB_rctr1, IC_rctr1)
        vvod_rctr2, oper_vyvod_rctr2, pusk_obryv_rctr2, srab_obryv_rctr2, pusk_assym_rctr2, srab_assym_rctr2 = self.rctr2.Step(VYVOD, OV, OVst_rctr2, IA_rctr2, IB_rctr2, IC_rctr2)

        vvod_rctr3, oper_vyvod_rctr3, pusk_obryv_rctr3, srab_obryv_rctr3, pusk_assym_rctr3, srab_assym_rctr3 = self.rctr3.Step(VYVOD, OV, OVst_rctr3, IA_rctr3, IB_rctr3, IC_rctr3)
        # Общие цепи
        srab = srab_assym_rctr1 or srab_assym_rctr2 or srab_assym_rctr3

        return (vvod_rctr1, oper_vyvod_rctr1, pusk_obryv_rctr1, srab_obryv_rctr1, pusk_assym_rctr1, srab_assym_rctr1,
        vvod_rctr2, oper_vyvod_rctr2, pusk_obryv_rctr2, srab_obryv_rctr2, pusk_assym_rctr2, srab_assym_rctr2,
        vvod_rctr3, oper_vyvod_rctr3, pusk_obryv_rctr3, srab_obryv_rctr3, pusk_assym_rctr3, srab_assym_rctr3,
        srab)

