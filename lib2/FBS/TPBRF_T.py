# ФБ Устройство резервирования при отказе выключателя стороны ВН (УРОВ ВН) (TPBRF) для Т, Т2
# НЕ ПРОВЕРЕНО!!

from lib2.FUNCS.TPRBRF_T import TPRBRF # импортируем функцию УРОВ

class TPBRF:
    def __init__(self, SGF1_rbrf1_tpbrf, SGF2_rbrf1_tpbrf, SGF3_rbrf1_tpbrf, SGF4_rbrf1_tpbrf, SGF5_rbrf1_tpbrf, SGF6_rbrf1_tpbrf, T1_rbrf1_tpbrf, Iset_rbrf1_tpbrf):
        self.rbrf1 = TPRBRF(SGF1_rbrf1_tpbrf, SGF2_rbrf1_tpbrf, SGF3_rbrf1_tpbrf, SGF4_rbrf1_tpbrf, SGF5_rbrf1_tpbrf, SGF6_rbrf1_tpbrf, T1_rbrf1_tpbrf, Iset_rbrf1_tpbrf)

    def Step(self, VYVOD, OV_rbrf1_tpbrf, blok_otkl_rcbf1_lvcbsup, LO_VN_otkl, kontr_emo1, kontr_emo2, Puski, pusk_urov_vnesh, IA, IB, IC):
        vvod_rbrf1_tpbrf, oper_vyvod_rbrf1_tpbrf, uskorenie_rbrf1_tpbrf, srab_rbrf1_tpbrf, pusk_rbrf1_tpbrf, io_rbrf1_tpbrf, srab_na_sebya_rbrf1_tpbrf, ET_rbrf1_tpbrf = self.rbrf1.Step(VYVOD, OV_rbrf1_tpbrf, blok_otkl_rcbf1_lvcbsup, LO_VN_otkl, kontr_emo1, kontr_emo2, Puski, pusk_urov_vnesh, IA, IB, IC)
        return vvod_rbrf1_tpbrf, oper_vyvod_rbrf1_tpbrf, uskorenie_rbrf1_tpbrf, srab_rbrf1_tpbrf, pusk_rbrf1_tpbrf, io_rbrf1_tpbrf, srab_na_sebya_rbrf1_tpbrf

if __name__ == "__main__":
    fb = TPBRF()
    res = fb.Step(0,0,0,0,0,0,0,0,0)
    print(res)