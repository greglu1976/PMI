# ЧАСТЬ СХЕМЫ ФСУ ДЛЯ ПРОВЕРКИ КЦТ, ДЗТ, ПС, ЛО, 
# ИСПОЛНЕНИЯ ДЗТ2

from lib._FBS.CTR import CTR # импорт ФБ КЦТ
from lib._FBS.TDIF import TDIF # импорт ФБ ДЗТ
from lib._FBS.TPRMOFFLVLGC import TPRMOFFLVLGC # импорт ФБ ЛО Т (ДЗТ)
from lib._FBS.DZT2_LVALH import DZT2_LVALH # импорт ПС


class partDZT:
    def __init__(self, SGF1_rctr1_ctr, SGF2_rctr1_ctr, T1_rctr1_ctr, T2_rctr1_ctr, Inom_rctr1_ctr, Imin_rctr1_ctr, Ksym_rctr1_ctr, LIsym_rctr1_ctr,
            SGF1_rctr2_ctr, SGF2_rctr2_ctr, T1_rctr2_ctr, T2_rctr2_ctr, Inom_rctr2_ctr, Imin_rctr2_ctr, Ksym_rctr2_ctr, LIsym_rctr2_ctr,
            SGF1_rctr3_ctr, SGF2_rctr3_ctr, T1_rctr3_ctr, T2_rctr3_ctr, Inom_rctr3_ctr, Imin_rctr3_ctr, Ksym_rctr3_ctr, LIsym_rctr3_ctr,
            Sbaz, Ubaz_vn, Ubaz_nn, Iperv_vn, Iperv_nn, Inom_term_vn, Inom_term_nn, Ivtor_vn, Ivtor_nn, k_sch_vn, k_sch_nn, n_sch_vn, n_sch_nn, compens_3i0_vn, compens_3i0_nn, Ubaz_nn2, Iperv_nn2, Inom_term_nn2, Ivtor_nn2, k_sch_nn2, n_sch_nn2, compens_3i0_nn2,
            SGF1_pdif1_tdif, SGF2_pdif1_tdif, SGF3_pdif1_tdif, T1_pdif1_tdif, Isr_pdif1_tdif, Isr_zagrub_pdif1_tdif, It1_pdif1_tdif, It2_pdif1_tdif, Kt1_pdif1_tdif, Kt2_pdif1_tdif,
            SGF1_pdif2_tdif, T1_pdif2_tdif, Iset_pdif2_tdif,
            SGF1_hf2phar1_tdif, T1_hf2phar1_tdif, T2_hf2phar1_tdif, Ratio_hf2phar1_tdif,
            SGF1_hf5phar1_tdif, T1_hf5phar1_tdif, T2_hf5phar1_tdif, Ratio_hf5phar1_tdif,
            SGF1_rctr1_tdif, T1_rctr1_tdif, Iset_rctr1_tdif,
            SGF1_ptrc1_tprmofflvlgc, SGF1_rbre1_tprmofflvlgc, Side1, Side2, Side3
            ):
        # Инициализируем ФБ КЦТ
        self.ctr = CTR(SGF1_rctr1_ctr, SGF2_rctr1_ctr, T1_rctr1_ctr, T2_rctr1_ctr, Inom_rctr1_ctr, Imin_rctr1_ctr, Ksym_rctr1_ctr, LIsym_rctr1_ctr,
            SGF1_rctr2_ctr, SGF2_rctr2_ctr, T1_rctr2_ctr, T2_rctr2_ctr, Inom_rctr2_ctr, Imin_rctr2_ctr, Ksym_rctr2_ctr, LIsym_rctr2_ctr,
            SGF1_rctr3_ctr, SGF2_rctr3_ctr, T1_rctr3_ctr, T2_rctr3_ctr, Inom_rctr3_ctr, Imin_rctr3_ctr, Ksym_rctr3_ctr, LIsym_rctr3_ctr) 
        # Инициализируем ФБ ДЗТ
        self.tdif = TDIF(Sbaz, Ubaz_vn, Ubaz_nn, Iperv_vn, Iperv_nn, Inom_term_vn, Inom_term_nn, Ivtor_vn, Ivtor_nn, k_sch_vn, k_sch_nn, n_sch_vn, n_sch_nn, compens_3i0_vn, compens_3i0_nn, Ubaz_nn2, Iperv_nn2, Inom_term_nn2, Ivtor_nn2, k_sch_nn2, n_sch_nn2, compens_3i0_nn2, SGF1_pdif1_tdif, SGF2_pdif1_tdif, SGF3_pdif1_tdif, T1_pdif1_tdif, Isr_pdif1_tdif, Isr_zagrub_pdif1_tdif, It1_pdif1_tdif, It2_pdif1_tdif, Kt1_pdif1_tdif, Kt2_pdif1_tdif, SGF1_pdif2_tdif, T1_pdif2_tdif, Iset_pdif2_tdif, SGF1_hf2phar1_tdif, T1_hf2phar1_tdif, T2_hf2phar1_tdif, Ratio_hf2phar1_tdif, SGF1_hf5phar1_tdif, T1_hf5phar1_tdif, T2_hf5phar1_tdif, Ratio_hf5phar1_tdif, SGF1_rctr1_tdif, T1_rctr1_tdif, Iset_rctr1_tdif)
        # Инициализируем ФБ ЛО Т
        self.tprmofflvlgc = TPRMOFFLVLGC(SGF1_ptrc1_tprmofflvlgc, SGF1_rbre1_tprmofflvlgc)
        # Инициализируем ПС
        self.lvalh = DZT2_LVALH(SGF1=0, SGF2=0, SGF3=0, SGF4=0, SGF5=0, SGF6=0, SGF7=0, SGF8=0, SGF9=0, SGF10=0, SGF11=0, SGF12=0, SGF13=0)

        self.Side1 = Side1
        self.Side2 = Side2
        self.Side3 = Side3

    def Step(self, VYVOD, OV_ctr, OVst_rctr1, IA, dIA, IB, dIB, IC, dIC, OVst_rctr2, OVst_rctr3, IA1, dIA1, IB1, dIB1, IC1, dIC1, OV_tdif, OV_pdif1_tdif, NaSign_pdif1_tdif, OV_pdif2_tdif, NaSign_pdif2_tdif, IA2harm, IB2harm, IC2harm, IA5harm, IB5harm, IC5harm, OV_rctr1_tdif, OV_tprmofflvlgc, OV_ptrc1_tprmofflvlgc, OV_rbre1_tprmofflvlgc):

        IA_rctr3 = IA1
        IB_rctr3 = IB1
        IC_rctr3 = IC1   #0   исключим из расчета токи 3 стороны
        vvod_rctr1_ctr, oper_vyvod_rctr1_ctr, pusk_obryv_rctr1_ctr, srab_obryv_rctr1_ctr, pusk_assym_rctr1_ctr, srab_assym_rctr1_ctr, vvod_rctr2_ctr, oper_vyvod_rctr2_ctr, pusk_obryv_rctr2_ctr, srab_obryv_rctr2_ctr, pusk_assym_rctr2_ctr, srab_assym_rctr2_ctr, vvod_rctr3_ctr, oper_vyvod_rctr3_ctr, pusk_obryv_rctr3_ctr, srab_obryv_rctr3_ctr, pusk_assym_rctr3_ctr, srab_assym_rctr3_ctr, srab_ctr = self.ctr.Step(VYVOD, OV_ctr, OVst_rctr1, IA, IB, IC, OVst_rctr2, IA1, IB1, IC1, OVst_rctr3, IA_rctr3, IB_rctr3, IC_rctr3)

        # Выключаем стороны для ДЗТ не используемые
        IA = 0 if self.Side1==0 else IA
        IB = 0 if self.Side1==0 else IB
        IC = 0 if self.Side1==0 else IC
        IA1_nn = 0 if self.Side2==0 else IA1
        IB1_nn = 0 if self.Side2==0 else IB1
        IC1_nn = 0 if self.Side2==0 else IC1
        IA_nn2 = 0 if self.Side3==0 else IA1
        IB_nn2 = 0 if self.Side3==0 else IB1
        IC_nn2 = 0 if self.Side3==0 else IC1 
        dIA_nn2 = dIA1
        dIB_nn2 = dIB1
        dIC_nn2 = dIC1
        vvod_pdif2_tdif, oper_vyvod_pdif2_tdif, pusk_A_pdif2_tdif, srab_A_pdif2_tdif, srabsign_A_pdif2_tdif, io_A_pdif2_tdif, pusk_B_pdif2_tdif, srab_B_pdif2_tdif, srabsign_B_pdif2_tdif, io_B_pdif2_tdif, pusk_C_pdif2_tdif, srab_C_pdif2_tdif, srabsign_C_pdif2_tdif, io_C_pdif2_tdif, pusk_pdif2_tdif, srabsign_pdif2_tdif, srab_pdif2_tdif, vvod_pdif1_tdif, oper_vyvod_pdif1_tdif, pusk_A_pdif1_tdif, srab_A_pdif1_tdif, srabsign_A_pdif1_tdif, io_A_pdif1_tdif, pusk_B_pdif1_tdif, srab_B_pdif1_tdif, srabsign_B_pdif1_tdif, io_B_pdif1_tdif, pusk_C_pdif1_tdif, srab_C_pdif1_tdif, srabsign_C_pdif1_tdif, io_C_pdif1_tdif, pusk_pdif1_tdif, srabsign_pdif1_tdif, srab_pdif1_tdif, pusk_A_hf2phar1_tdif, pusk_B_hf2phar1_tdif, pusk_C_hf2phar1_tdif, pusk_hf2phar1_tdif, pusk_A_hf5phar1_tdif, pusk_B_hf5phar1_tdif, pusk_C_hf5phar1_tdif, pusk_hf5phar1_tdif, vvod_rctr1_tdif, oper_vyvod_rctr1_tdif, srab_A_rctr1_tdif, srab_B_rctr1_tdif, srab_C_rctr1_tdif, srab_rctr1_tdif, neispr_rctr1_tdif, diffA, restA, diffB, restB, diffC, restC = self.tdif.Step(VYVOD, IA, dIA, IB, dIB, IC, dIC, IA1_nn, dIA1, IB1_nn, dIB1, IC1_nn, dIC1, OV_tdif, OV_pdif2_tdif, NaSign_pdif2_tdif, OV_pdif1_tdif, NaSign_pdif1_tdif, srab_ctr, IA2harm, IB2harm, IC2harm, IA5harm, IB5harm, IC5harm, OV_rctr1_tdif, IA_nn2, dIA_nn2, IB_nn2, dIB_nn2, IC_nn2, dIC_nn2)

        vvod_ptrc1_tprmofflvlgc, oper_vyvod_ptrc1_tprmofflvlgc, pusk_ptrc1_tprmofflvlgc, srab_ptrc1_tprmofflvlgc, vvod_rbre1_tprmofflvlgc, oper_vyvod_rbre1_tprmofflvlgc, zapret_rbre1_tprmofflvlgc = self.tprmofflvlgc.Step(VYVOD, OV_tprmofflvlgc, OV_ptrc1_tprmofflvlgc, (srab_pdif2_tdif, srab_pdif1_tdif), OV_rbre1_tprmofflvlgc)

        pusk_lvalh = self.lvalh.Step(VYVOD, COMM_SIGN = (srab_pdif2_tdif, srab_pdif1_tdif, srab_ctr, srab_rctr1_tdif))

        return (vvod_rctr1_ctr, oper_vyvod_rctr1_ctr, pusk_obryv_rctr1_ctr, srab_obryv_rctr1_ctr, pusk_assym_rctr1_ctr, srab_assym_rctr1_ctr, vvod_rctr2_ctr, oper_vyvod_rctr2_ctr, pusk_obryv_rctr2_ctr, srab_obryv_rctr2_ctr, pusk_assym_rctr2_ctr, srab_assym_rctr2_ctr, vvod_rctr3_ctr, oper_vyvod_rctr3_ctr, pusk_obryv_rctr3_ctr, srab_obryv_rctr3_ctr, pusk_assym_rctr3_ctr, srab_assym_rctr3_ctr, srab_ctr, vvod_pdif2_tdif, oper_vyvod_pdif2_tdif, pusk_A_pdif2_tdif, srab_A_pdif2_tdif, srabsign_A_pdif2_tdif, io_A_pdif2_tdif, pusk_B_pdif2_tdif, srab_B_pdif2_tdif, srabsign_B_pdif2_tdif, io_B_pdif2_tdif, pusk_C_pdif2_tdif, srab_C_pdif2_tdif, srabsign_C_pdif2_tdif, io_C_pdif2_tdif, pusk_pdif2_tdif, srabsign_pdif2_tdif, srab_pdif2_tdif, vvod_pdif1_tdif, oper_vyvod_pdif1_tdif, pusk_A_pdif1_tdif, srab_A_pdif1_tdif, srabsign_A_pdif1_tdif, io_A_pdif1_tdif, pusk_B_pdif1_tdif, srab_B_pdif1_tdif, srabsign_B_pdif1_tdif, io_B_pdif1_tdif, pusk_C_pdif1_tdif, srab_C_pdif1_tdif, srabsign_C_pdif1_tdif, io_C_pdif1_tdif, pusk_pdif1_tdif, srabsign_pdif1_tdif, srab_pdif1_tdif, pusk_A_hf2phar1_tdif, pusk_B_hf2phar1_tdif, pusk_C_hf2phar1_tdif, pusk_hf2phar1_tdif, pusk_A_hf5phar1_tdif, pusk_B_hf5phar1_tdif, pusk_C_hf5phar1_tdif, pusk_hf5phar1_tdif, vvod_rctr1_tdif, oper_vyvod_rctr1_tdif, srab_A_rctr1_tdif, srab_B_rctr1_tdif, srab_C_rctr1_tdif, srab_rctr1_tdif, neispr_rctr1_tdif, vvod_ptrc1_tprmofflvlgc, oper_vyvod_ptrc1_tprmofflvlgc, pusk_ptrc1_tprmofflvlgc, srab_ptrc1_tprmofflvlgc, vvod_rbre1_tprmofflvlgc, oper_vyvod_rbre1_tprmofflvlgc, zapret_rbre1_tprmofflvlgc, pusk_lvalh, diffA, restA, diffB, restB, diffC, restC
        )


