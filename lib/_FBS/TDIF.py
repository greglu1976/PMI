# ФБ ДЗТ
# 

from lib._FUNCS.HF2DIFPHAR import HF2DIFPHAR
from lib._FUNCS.ATDIFRCTR import ATDIFRCTR
from lib._FUNCS.INSPDIF import INSPDIF
from lib._FUNCS.RESPDIF import RESPDIF
from lib._FUNCS.BLKRCTR import BLKRCTR # заглушка вместо БВКЗ
from lib._ADD.calc_diff_bias import CalcDiffBias # модуль задания исходных параметров сторон и выравнивания токов сторон

class TDIF:
    def __init__(self, 
        Sbaz, Ubaz_vn, Ubaz_nn, Iperv_vn, Iperv_nn, Inom_term_vn, Inom_term_nn, Ivtor_vn, Ivtor_nn, k_sch_vn, k_sch_nn, n_sch_vn, n_sch_nn, compens_3i0_vn, compens_3i0_nn, Ubaz_nn2, Iperv_nn2, Inom_term_nn2, Ivtor_nn2, k_sch_nn2, n_sch_nn2, compens_3i0_nn2,
        SGF1_pdif1_tdif, SGF2_pdif1_tdif, SGF3_pdif1_tdif, T1_pdif1_tdif, Isr_pdif1_tdif, Isr_zagrub_pdif1_tdif, It1_pdif1_tdif, It2_pdif1_tdif, Kt1_pdif1_tdif, Kt2_pdif1_tdif,
        SGF1_pdif2_tdif, T1_pdif2_tdif, Iset_pdif2_tdif,
        SGF1_hf2phar1_tdif, T1_hf2phar1_tdif, T2_hf2phar1_tdif, Ratio_hf2phar1_tdif,
        SGF1_hf5phar1_tdif, T1_hf5phar1_tdif, T2_hf5phar1_tdif, Ratio_hf5phar1_tdif,
        SGF1_rctr1_tdif, T1_rctr1_tdif, Iset_rctr1_tdif
        ):
        self.calc = CalcDiffBias(Sbaz, Ubaz_vn, Ubaz_nn, Iperv_vn, Iperv_nn, Inom_term_vn, Inom_term_nn, Ivtor_vn, Ivtor_nn, k_sch_vn, k_sch_nn, n_sch_vn, n_sch_nn, compens_3i0_vn, compens_3i0_nn, Ubaz_nn2, Iperv_nn2, Inom_term_nn2, Ivtor_nn2, k_sch_nn2, n_sch_nn2, compens_3i0_nn2)

        self.calc2h = CalcDiffBias(Sbaz, Ubaz_vn, Ubaz_nn, Iperv_vn, Iperv_nn, Inom_term_vn, Inom_term_nn, Ivtor_vn, Ivtor_nn, k_sch_vn, k_sch_nn, n_sch_vn, n_sch_nn, compens_3i0_vn, compens_3i0_nn, Ubaz_nn2, Iperv_nn2, Inom_term_nn2, Ivtor_nn2, k_sch_nn2, n_sch_nn2, compens_3i0_nn2)

        self.calc5h = CalcDiffBias(Sbaz, Ubaz_vn, Ubaz_nn, Iperv_vn, Iperv_nn, Inom_term_vn, Inom_term_nn, Ivtor_vn, Ivtor_nn, k_sch_vn, k_sch_nn, n_sch_vn, n_sch_nn, compens_3i0_vn, compens_3i0_nn, Ubaz_nn2, Iperv_nn2, Inom_term_nn2, Ivtor_nn2, k_sch_nn2, n_sch_nn2, compens_3i0_nn2)

        self.pdif1 = RESPDIF(SGF1_pdif1_tdif, SGF2_pdif1_tdif, SGF3_pdif1_tdif, T1_pdif1_tdif, Isr_pdif1_tdif, Isr_zagrub_pdif1_tdif, It1_pdif1_tdif, It2_pdif1_tdif, Kt1_pdif1_tdif, Kt2_pdif1_tdif)
        self.pdif2 = INSPDIF(SGF1_pdif2_tdif, T1_pdif2_tdif, Iset_pdif2_tdif)
        self.hf2phar1 = HF2DIFPHAR(SGF1_hf2phar1_tdif, T1_hf2phar1_tdif, T2_hf2phar1_tdif, Ratio_hf2phar1_tdif)
        self.hf5phar1 = HF2DIFPHAR(SGF1_hf5phar1_tdif, T1_hf5phar1_tdif, T2_hf5phar1_tdif, Ratio_hf5phar1_tdif)
        self.rctr1 = ATDIFRCTR(SGF1_rctr1_tdif, T1_rctr1_tdif, Iset_rctr1_tdif)
        self.blkrctr1 = BLKRCTR()


    def Step(self, VYVOD, IA_vn, dIA_vn, IB_vn, dIB_vn, IC_vn, dIC_vn, IA_nn, dIA_nn, IB_nn, dIB_nn, IC_nn, dIC_nn, OV_tdif, OV_pdif2_tdif, NaSign_pdif2_tdif, OV_pdif1_tdif, NaSign_pdif1_tdif, CurCirc, IAdiff2h, IBdiff2h, ICdiff2h, IAdiff5h, IBdiff5h, ICdiff5h, OV_rctr1_tdif, IA_nn2, dIA_nn2, IB_nn2, dIB_nn2, IC_nn2, dIC_nn2):

        # вычисляем тормозные и диф токи
        diff_currs, bias_currs  = self.calc.Step(IA_vn, dIA_vn, IB_vn, dIB_vn, IC_vn, dIC_vn, IA_nn, dIA_nn, IB_nn, dIB_nn, IC_nn, dIC_nn, IA_nn2, dIA_nn2, IB_nn2, dIB_nn2, IC_nn2, dIC_nn2)
        #print('IdiffA=', diff_currs[0][0], 'IrestA=', bias_currs[0][0])
        #print('IdiffB=', diff_currs[1][0], 'IrestB=',bias_currs[1][0])
        #print('IdiffC=', diff_currs[2][0], 'IrestC=', bias_currs[2][0])

        # вычисляем дифотсечку        
        vvod_pdif2_tdif, oper_vyvod_pdif2_tdif, pusk_A_pdif2_tdif, srab_A_pdif2_tdif, srabsign_A_pdif2_tdif, io_A_pdif2_tdif, pusk_B_pdif2_tdif, srab_B_pdif2_tdif, srabsign_B_pdif2_tdif, io_B_pdif2_tdif, pusk_C_pdif2_tdif, srab_C_pdif2_tdif, srabsign_C_pdif2_tdif, io_C_pdif2_tdif, pusk_pdif2_tdif, srabsign_pdif2_tdif, srab_pdif2_tdif  = self.pdif2.Step(VYVOD, OV_tdif, OV_pdif2_tdif, NaSign_pdif2_tdif, diff_currs[0][0], diff_currs[1][0], diff_currs[2][0])

        # вычисляем ДТЗт - первый шаг
        vvod_pdif1_tdif, oper_vyvod_pdif1_tdif, sgf3_pdif1_tdif = self.pdif1.PreStep(VYVOD, OV_tdif, OV_pdif1_tdif)

        # вычисляем БВКЗ это заглушка , в статике ее не проверить
        OpSelA_blkrctr1_tdif, OpSelB_blkrctr1_tdif, OpSelC_blkrctr1_tdif, OpSel_blkrctr1_tdif = self.blkrctr1.Step(vvod_pdif1_tdif, sgf3_pdif1_tdif)

        # вычисляем 2 гармонику в диф токе
        diff_currs2h, bias_currs2h  = self.calc2h.Step(IAdiff2h, dIA_vn, IBdiff2h, dIB_vn, ICdiff2h, dIC_vn, IA_nn=0, dIA_nn=0, IB_nn=0, dIB_nn=0, IC_nn=0, dIC_nn=0, IA_nn2=0, dIA_nn2=0, IB_nn2=0, dIB_nn2=0, IC_nn2=0, dIC_nn2=0)
        pusk_A_hf2phar1_tdif, pusk_B_hf2phar1_tdif, pusk_C_hf2phar1_tdif, pusk_hf2phar1_tdif = self.hf2phar1.Step(vvod_pdif1_tdif, diff_currs[0][0], diff_currs2h[0][0], diff_currs[1][0], diff_currs2h[1][0], diff_currs[2][0], diff_currs2h[2][0])
        
        # вычисляем 5 гармонику в диф токе
        diff_currs5h, bias_currs5h  = self.calc5h.Step(IAdiff5h, dIA_vn, IBdiff5h, dIB_vn, ICdiff5h, dIC_vn, IA_nn=0, dIA_nn=0, IB_nn=0, dIB_nn=0, IC_nn=0, dIC_nn=0, IA_nn2=0, dIA_nn2=0, IB_nn2=0, dIB_nn2=0, IC_nn2=0, dIC_nn2=0)
        pusk_A_hf5phar1_tdif, pusk_B_hf5phar1_tdif, pusk_C_hf5phar1_tdif, pusk_hf5phar1_tdif = self.hf5phar1.Step(vvod_pdif1_tdif, diff_currs[0][0], diff_currs5h[0][0], diff_currs[1][0], diff_currs5h[1][0], diff_currs[2][0], diff_currs5h[2][0])

        # вычисляем ДТЗт - второй шаг
        pusk_A_pdif1_tdif, srab_A_pdif1_tdif, srabsign_A_pdif1_tdif, io_A_pdif1_tdif, pusk_B_pdif1_tdif, srab_B_pdif1_tdif, srabsign_B_pdif1_tdif, io_B_pdif1_tdif, pusk_C_pdif1_tdif, srab_C_pdif1_tdif, srabsign_C_pdif1_tdif, io_C_pdif1_tdif, pusk_pdif1_tdif, srabsign_pdif1_tdif, srab_pdif1_tdif = self.pdif1.AfterStep(vvod_pdif1_tdif, NaSign_pdif1_tdif, diff_currs[0][0], diff_currs[1][0], diff_currs[2][0], bias_currs[0][0], bias_currs[1][0], bias_currs[2][0], CurCirc, OpSelA_blkrctr1_tdif, OpSelB_blkrctr1_tdif, OpSelC_blkrctr1_tdif, pusk_A_hf2phar1_tdif, pusk_B_hf2phar1_tdif, pusk_C_hf2phar1_tdif, pusk_A_hf5phar1_tdif, pusk_B_hf5phar1_tdif, pusk_C_hf5phar1_tdif)

        # вычисляем КЦТнеб
        vvod_rctr1_tdif, oper_vyvod_rctr1_tdif, srab_A_rctr1_tdif, srab_B_rctr1_tdif, srab_C_rctr1_tdif, srab_rctr1_tdif, neispr_rctr1_tdif = self.rctr1.Step(VYVOD, OV_tdif, OV_rctr1_tdif, CurCirc, diff_currs[0][0], diff_currs[1][0], diff_currs[2][0])

        return (
            vvod_pdif2_tdif, oper_vyvod_pdif2_tdif, pusk_A_pdif2_tdif, srab_A_pdif2_tdif, srabsign_A_pdif2_tdif, io_A_pdif2_tdif, pusk_B_pdif2_tdif, srab_B_pdif2_tdif, srabsign_B_pdif2_tdif, io_B_pdif2_tdif, pusk_C_pdif2_tdif, srab_C_pdif2_tdif, srabsign_C_pdif2_tdif, io_C_pdif2_tdif, pusk_pdif2_tdif, srabsign_pdif2_tdif, srab_pdif2_tdif,
            vvod_pdif1_tdif, oper_vyvod_pdif1_tdif, pusk_A_pdif1_tdif, srab_A_pdif1_tdif, srabsign_A_pdif1_tdif, io_A_pdif1_tdif, pusk_B_pdif1_tdif, srab_B_pdif1_tdif, srabsign_B_pdif1_tdif, io_B_pdif1_tdif, pusk_C_pdif1_tdif, srab_C_pdif1_tdif, srabsign_C_pdif1_tdif, io_C_pdif1_tdif, pusk_pdif1_tdif, srabsign_pdif1_tdif, srab_pdif1_tdif,
            pusk_A_hf2phar1_tdif, pusk_B_hf2phar1_tdif, pusk_C_hf2phar1_tdif, pusk_hf2phar1_tdif,
            pusk_A_hf5phar1_tdif, pusk_B_hf5phar1_tdif, pusk_C_hf5phar1_tdif, pusk_hf5phar1_tdif,
            vvod_rctr1_tdif, oper_vyvod_rctr1_tdif, srab_A_rctr1_tdif, srab_B_rctr1_tdif, srab_C_rctr1_tdif, srab_rctr1_tdif, neispr_rctr1_tdif, diff_currs[0][0], bias_currs[0][0], diff_currs[1][0], bias_currs[1][0], diff_currs[2][0], bias_currs[2][0])


