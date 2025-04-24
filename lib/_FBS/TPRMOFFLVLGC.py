# (TPRMOFFLVLGC) Функция ЛО Т - Логика отключения трансформатора 35 кВ для ДЗТ

from lib._FUNCS.T_TJNTPTRC import T_TJNTPTRC
from lib._FUNCS.JNTRBRE_2 import JNTRBRE

class TPRMOFFLVLGC:
    def __init__(self, SGF1_ptrc1, SGF1_rbre1):
        self.ptrc1 = T_TJNTPTRC(SGF1_ptrc1)
        self.rbre1 = JNTRBRE(SGF1_rbre1)

    def Step(self, VYVOD, OV_tprmofflvlgc, OV_ptrc1_tprmofflvlgc, signals, OV_rbre1_tprmofflvlgc):

        mtz2_srab=0
        mtz3_srab=0
        vvod_ptrc1_tprmofflvlgc, oper_vyvod_ptrc1_tprmofflvlgc, pusk_ptrc1_tprmofflvlgc, srab_ptrc1_tprmofflvlgc = self.ptrc1.Step(VYVOD, OV_tprmofflvlgc, OV_ptrc1_tprmofflvlgc, signals, mtz2_srab, mtz3_srab)

        vvod_rbre1_tprmofflvlgc, oper_vyvod_rbre1_tprmofflvlgc, zapret_rbre1_tprmofflvlgc = self.rbre1.Step(VYVOD, OV_tprmofflvlgc, OV_rbre1_tprmofflvlgc, pusk_ptrc1_tprmofflvlgc)

        return vvod_ptrc1_tprmofflvlgc, oper_vyvod_ptrc1_tprmofflvlgc, pusk_ptrc1_tprmofflvlgc, srab_ptrc1_tprmofflvlgc, vvod_rbre1_tprmofflvlgc, oper_vyvod_rbre1_tprmofflvlgc, zapret_rbre1_tprmofflvlgc

