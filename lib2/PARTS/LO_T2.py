# ЧАСТЬ СХЕМЫ ФСУ ДЛЯ ПРОВЕРКИ ЛО, УРОВ, ПС, СС
# ИСПОЛНЕНИЯ Т2

# Проверяемые функции
from lib2.FBS.TPBRF_T import TPBRF # импорт ФБ УРОВ
from lib2.FBS.HVTCBOFF import HVTCBOFF # импорт ФБ ЛО ВН
from lib2.FBS.LVTCBOFF import LVTCBOFF # импорт ЛО НН

# Вспомогательные функции
from lib2.FBS.LVTTOC_T2 import T2_LVTTOC # импорт ФБ МТЗ Т2
from lib2.FBS.LVTOC import LVTOC # импорт ФБ ТО
from lib2.FBS.LVCBSUP import LVCBSUP # импорт ФБ КСВ
from lib2.FBS.TOFFLVLGC import TOFFLVLGC # импорт ЛО Т
from lib2.FBS.T2_SignAssembly import T2_SignAssembly
from lib2.FBS.T2_LVALH import T2_LVALH # импорт ПС

class part_LO:
    def __init__(self, 
        SGF1, SGF1_ptoc1, SGF2_ptoc1, SGF3_ptoc1, SGF4_ptoc1, SGF5_ptoc1, SGF6_ptoc1, SGF7_ptoc1, T1_ptoc1, Iset_ptoc1, Icoarse_ptoc1,
        SGF1_ptoc2, SGF2_ptoc2, SGF3_ptoc2, SGF4_ptoc2, SGF5_ptoc2, SGF6_ptoc2, SGF7_ptoc2, T1_ptoc2, Iset_ptoc2, Icoarse_ptoc2,
        SGF1_ptoc3, SGF2_ptoc3, SGF3_ptoc3, SGF4_ptoc3, SGF5_ptoc3, SGF6_ptoc3, SGF7_ptoc3, T1_ptoc3, Iset_ptoc3, Icoarse_ptoc3,
        SGF1_ptuv1, Uop_ptuv1, U2op_ptuv1,
        SGF1_ptuv2, Uop_ptuv2, U2op_ptuv2,
        SGF1_phar1, Imax_phar1, Ratio_phar1,
        SGF1_rblc1,
        # ТО
        SGF1_ptoc1_lvtoc, SGF2_ptoc1_lvtoc, T1_ptoc1_lvtoc, Iset_ptoc1_lvtoc,
        # КСВ
        SGF1_rcbf1_lvcbsup, SGF2_rcbf1_lvcbsup, SGF3_rcbf1_lvcbsup, SGF4_rcbf1_lvcbsup, SGF5_rcbf1_lvcbsup, SGF6_rcbf1_lvcbsup, SGF7_rcbf1_lvcbsup, SGF8_rcbf1_lvcbsup, T1_rcbf1_lvcbsup, T2_rcbf1_lvcbsup, T3_rcbf1_lvcbsup,
        # УРОВ   
        SGF1_rbrf1_tpbrf, SGF2_rbrf1_tpbrf, SGF3_rbrf1_tpbrf, SGF4_rbrf1_tpbrf, SGF5_rbrf1_tpbrf, SGF6_rbrf1_tpbrf, T1_rbrf1_tpbrf, Iset_rbrf1_tpbrf,
        # ЛО Т 
        SGF1_ptrc1_tofflvlgc, SGF1_rbre1_tofflvlgc, SGF2_rbre1_tofflvlgc, SGF3_rbre1_tofflvlgc, SGF1_rblc1_tofflvlgc, SGF2_rblc1_tofflvlgc, SGF3_rblc1_tofflvlgc,
        # ЛО ВН
        SGF1_hvcbptrc1_hvtcboff, T1_hvcbptrc1_hvtcboff,
        # ЛО НН1
        SGF1_lvcbptrc1_lvtcboff1, T1_lvcbptrc1_lvtcboff1, SGF1_lvcbrecrbre1_lvtcboff1, SGF1_lvbtsrblc1_lvtcboff1,
        # ЛО НН12
        SGF1_lvcbptrc1_lvtcboff2, T1_lvcbptrc1_lvtcboff2, SGF1_lvcbrecrbre1_lvtcboff2, SGF1_lvbtsrblc1_lvtcboff2,
        # СС
        SGF1_tsa, SGF2_tsa, SGF3_tsa, SGF4_tsa, SGF5_tsa, SGF6_tsa, SGF7_tsa, SGF8_tsa, SGF9_tsa, SGF10_tsa, SGF11_tsa, SGF12_tsa, SGF13_tsa, SGF14_tsa, SGF15_tsa, SGF16_tsa, SGF17_tsa,
        # ПС
        SGF1_lvalh, SGF2_lvalh, SGF3_lvalh, SGF4_lvalh, SGF5_lvalh, SGF6_lvalh, SGF7_lvalh, SGF8_lvalh, SGF9_lvalh, SGF10_lvalh
        ):

        Inom = 1
        # Инициализируем ФБ МТЗ Т2        
        self.lvttoc = T2_LVTTOC(SGF1, SGF1_ptoc1, SGF2_ptoc1, SGF3_ptoc1, SGF4_ptoc1, SGF5_ptoc1, SGF6_ptoc1, SGF7_ptoc1, T1_ptoc1, Iset_ptoc1*Inom, Icoarse_ptoc1*Inom,
                SGF1_ptoc2, SGF2_ptoc2, SGF3_ptoc2, SGF4_ptoc2, SGF5_ptoc2, SGF6_ptoc2, SGF7_ptoc2, T1_ptoc2, Iset_ptoc2*Inom, Icoarse_ptoc2*Inom,
                SGF1_ptoc3, SGF2_ptoc3, SGF3_ptoc3, SGF4_ptoc3, SGF5_ptoc3, SGF6_ptoc3, SGF7_ptoc3, T1_ptoc3, Iset_ptoc3*Inom, Icoarse_ptoc3*Inom,
                SGF1_ptuv1, Uop_ptuv1, U2op_ptuv1,
                SGF1_ptuv2, Uop_ptuv2, U2op_ptuv2,
                SGF1_phar1, Imax_phar1*Inom, Ratio_phar1,
                SGF1_rblc1)
        # Инициализируем ФБ ТО
        self.lvtoc = LVTOC(SGF1_ptoc1_lvtoc, SGF2_ptoc1_lvtoc, T1_ptoc1_lvtoc, Iset_ptoc1_lvtoc*Inom)
        # Инициализируем ФБ КСВ 
        self.lvcbsup = LVCBSUP(SGF1_rcbf1_lvcbsup, SGF2_rcbf1_lvcbsup, SGF3_rcbf1_lvcbsup, SGF4_rcbf1_lvcbsup, SGF5_rcbf1_lvcbsup, SGF6_rcbf1_lvcbsup, SGF7_rcbf1_lvcbsup,
                SGF8_rcbf1_lvcbsup, T1_rcbf1_lvcbsup, T2_rcbf1_lvcbsup, T3_rcbf1_lvcbsup)
        # Инициализируем ФБ УРОВ
        self.tpbrf = TPBRF(SGF1_rbrf1_tpbrf, SGF2_rbrf1_tpbrf, SGF3_rbrf1_tpbrf, SGF4_rbrf1_tpbrf, SGF5_rbrf1_tpbrf, SGF6_rbrf1_tpbrf, T1_rbrf1_tpbrf, Iset_rbrf1_tpbrf*Inom)
        # Инициализируем ФБ ЛО Т       
        self.tofflvlgc = TOFFLVLGC(SGF1_ptrc1_tofflvlgc, SGF1_rbre1_tofflvlgc, SGF2_rbre1_tofflvlgc, SGF3_rbre1_tofflvlgc, SGF1_rblc1_tofflvlgc, SGF2_rblc1_tofflvlgc,
                SGF3_rblc1_tofflvlgc)
        # Инициализируем ФБ ЛО ВН
        self.hvtcboff = HVTCBOFF(SGF1_hvcbptrc1_hvtcboff, T1_hvcbptrc1_hvtcboff)  
        # Инициализируем ФБ ЛО НН1
        self.lvtcboff1 = LVTCBOFF(SGF1_lvcbptrc1_lvtcboff1, T1_lvcbptrc1_lvtcboff1, SGF1_lvcbrecrbre1_lvtcboff1, SGF1_lvbtsrblc1_lvtcboff1)
        # Инициализируем ФБ ЛО НН2
        self.lvtcboff2 = LVTCBOFF(SGF1_lvcbptrc1_lvtcboff2, T1_lvcbptrc1_lvtcboff2, SGF1_lvcbrecrbre1_lvtcboff2, SGF1_lvbtsrblc1_lvtcboff2)        
        # Инициализируем СС
        self.t_signassembly = T2_SignAssembly(SGF1_tsa, SGF2_tsa, SGF3_tsa, SGF4_tsa, SGF5_tsa, SGF6_tsa, SGF7_tsa, SGF8_tsa, SGF9_tsa, SGF10_tsa, SGF11_tsa, SGF12_tsa, SGF13_tsa, SGF14_tsa, SGF15_tsa, SGF16_tsa, SGF17_tsa)
        # ИНициализируем ПС
        self.lvalh = T2_LVALH(SGF1_lvalh, SGF2_lvalh, SGF3_lvalh, SGF4_lvalh, SGF5_lvalh, SGF6_lvalh, SGF7_lvalh, SGF8_lvalh, SGF9_lvalh, SGF10_lvalh)

    def Step(self, DI_ControllerDisable, 
        DI_LVTTOC, IA, IB, IC,
        DI_LVTOC,
        DI_TRESOFFLVLGS, DI_PTRC1, DI_RBRE1, DI_LVCBRBLC1,
        DI_HVTCBOFF, OpExtOfARC_NN1, OpExtOfCBFP_NN1, OpExtOfARC_NN2, OpExtOfCBFP_NN2, 
        DI_LVTRESCBOFF1, DI_LVCBPTRC1, DI_LVCBRECRBRE1, DI_LVBTSRBLC1,
        DI_LVTRESCBOFF2, DI_LVCBPTRC2, DI_LVCBRECRBRE2, DI_LVBTSRBLC2,
        DI_LVCBSUP, ExternalBlkCB,
        DI_TPBRF, ExternalRBRFStart, T_TPBRF_1_CBOS1Supervision, T_TPBRF_1_CBOS2Supervision,
        T2_PNL_1_CtlCirSwPos1, T2_PNL_1_CtlCirSwPos2, T2_PNL_1_CtlCirSwPos3, T2_PNL_1_CtlCirSwPos4, T2_PNL_1_CtlCirSwPos5, T2_PNL_1_CtlCirSwPos6, T2_PNL_1_TestBlockPos1, T2_PNL_1_TestBlockPos2, T2_PNL_1_TestBlockPos3, GAS_OCControl, OCcir_CB, 
        ARCnn1_OCControl, CBFPnn1_OCControl, ARCnn2_OCControl, CBFPnn2_OCControl, IEDvt_OCControl1, IEDvt_OCControl2, 
        ExtSignal1, ExtSignal2,ExtSignal3, ExtSignal4 
        ):


        # вычисляем МТЗ
        SV1vkl = SV2vkl = 0
        IAB = IBC = ICA = UAB_ptuv1 = UBC_ptuv1 = UCA_ptuv1 = U2_ptuv1 = 0
        UAB_ptuv2 = UBC_ptuv2 = UCA_ptuv2 = U2_ptuv2 = 0
        IA2harm = IB2harm = IC2harm = 0
        neispr_zn_lvrbvtr1 = VNN1vkl = OVst_ptoc1 = NaSign_ptoc1 = OVst_ptoc2 = NaSign_ptoc2 = OVst_ptoc3 = NaSign_ptoc3 = KPONvnesh_ptuv1 = 0
        neispr_zn_lvrbvtr2 = VNN2vkl = KPONvnesh_ptuv2 = 0

        vvod_ptoc1_lvttoc, oper_vyvod_ptoc1_lvttoc, mtzA_pusk_ptoc1_lvttoc, mtzB_pusk_ptoc1_lvttoc, mtzC_pusk_ptoc1_lvttoc, gen_pusk_ptoc1_lvttoc, mtz_srabsign_ptoc1_lvttoc, mtz_srab_ptoc1_lvttoc, io_A_ptoc1_lvttoc, io_B_ptoc1_lvttoc, io_C_ptoc1_lvttoc, vvod_ptoc2_lvttoc, oper_vyvod_ptoc2_lvttoc, mtzA_pusk_ptoc2_lvttoc, mtzB_pusk_ptoc2_lvttoc, mtzC_pusk_ptoc2_lvttoc, gen_pusk_ptoc2_lvttoc, mtz_srabsign_ptoc2_lvttoc, mtz_srab_ptoc2_lvttoc, io_A_ptoc2_lvttoc, io_B_ptoc2_lvttoc, io_C_ptoc2_lvttoc, vvod_ptoc3_lvttoc, oper_vyvod_ptoc3_lvttoc, mtzA_pusk_ptoc3_lvttoc, mtzB_pusk_ptoc3_lvttoc, mtzC_pusk_ptoc3_lvttoc, gen_pusk_ptoc3_lvttoc, mtz_srabsign_ptoc3_lvttoc, mtz_srab_ptoc3_lvttoc, io_A_ptoc3_lvttoc, io_B_ptoc3_lvttoc, io_C_ptoc3_lvttoc, kpon_pusk_ptuv1_lvttoc, kpon_pusk_ptuv2_lvttoc, ia_start_out_phar1_lvttoc, ib_start_out_phar1_lvttoc, ic_start_out_phar1_lvttoc, start_phar1_lvttoc, blok_rblc1_lvttoc, mtz_pusk_lvttoc = self.lvttoc.Step(DI_ControllerDisable, DI_LVTTOC, SV1vkl, SV2vkl, IA, IAB, IB, IBC, IC, ICA, neispr_zn_lvrbvtr1, VNN1vkl, neispr_zn_lvrbvtr2, VNN2vkl, OVst_ptoc1, NaSign_ptoc1, OVst_ptoc2, NaSign_ptoc2, OVst_ptoc3, NaSign_ptoc3, KPONvnesh_ptuv1, UAB_ptuv1, UBC_ptuv1, UCA_ptuv1, U2_ptuv1, KPONvnesh_ptuv2, UAB_ptuv2, UBC_ptuv2, UCA_ptuv2, U2_ptuv2, IA2harm, IB2harm, IC2harm)

        # Рассчитываем ТО
        NaSign_ptoc1_lvtoc = 0
        vvod_ptoc1_lvtoc, oper_vyvod_ptoc1_lvtoc, pusk_ptoc1_lvtoc, io_ptoc1_lvtoc, srabsign_ptoc1_lvtoc, srab_ptoc1_lvtoc, ET_ptoc1_lvtoc =  self.lvtoc.Step(DI_ControllerDisable, DI_LVTOC, NaSign_ptoc1_lvtoc, IA, IB, IC, IAB, IBC, ICA)

        # Собираем кортеж срабатываний
        signals_tofflvlg = (mtz_srab_ptoc1_lvttoc, srab_ptoc1_lvtoc) 

        # вычисляем ЛО Т
        vvod_ptrc1_tofflvlgc, oper_vyvod_ptrc1_tofflvlgc, pusk_ptrc1_tofflvlgc, srab_ptrc1_tofflvlgc, vvod_rblc1_tofflvlgc, oper_vyvod_rblc1_tofflvlgc, zapret_rblc1_tofflvlgc, vvod_rbre1_tofflvlgc, oper_vyvod_rbre1_tofflvlgc, zapret_rbre1_tofflvlgc = self.tofflvlgc.Step(DI_ControllerDisable, DI_TRESOFFLVLGS, DI_PTRC1, signals_tofflvlg, mtz_srab_ptoc2_lvttoc, mtz_srab_ptoc3_lvttoc, DI_RBRE1, DI_LVCBRBLC1)

        # вычисляем ЛО ВН
        vvod_hvcbptrc1_hvtcboff, oper_vyvod_hvcbptrc1_hvtcboff, otkl_hvcbptrc1_hvtcboff, otkl_avar_hvcbptrc1_hvtcboff = self.hvtcboff.Step(DI_ControllerDisable, DI_HVTCBOFF, srab_ptrc1_tofflvlgc, OpExtOfARC_NN1 or OpExtOfARC_NN2, OpExtOfCBFP_NN1 or OpExtOfCBFP_NN2)

        # вычисляем ЛО НН1
        vvod_lvcbptrc1_lvtcboff1, oper_vyvod_lvcbptrc1_lvtcboff1, otkl_lvcbptrc1_lvtcboff1, otkl_avar_lvcbptrc1_lvtcboff1, vvod_lvcbrecrbre1_lvtcboff1, oper_vyvod_lvcbrecrbre1_lvtcboff1, zapret_lvcbrecrbre1_lvtcboff1, vvod_lvbtsrblc1_lvtcboff1, oper_vyvod_lvbtsrblc1_lvtcboff1, zapret_lvbtsrblc1_lvtcboff1 = self.lvtcboff1.Step(DI_ControllerDisable, DI_LVTRESCBOFF1, DI_LVCBPTRC1, DI_LVCBRECRBRE1, DI_LVBTSRBLC1, srab_ptrc1_tofflvlgc, zapret_rbre1_tofflvlgc, zapret_rblc1_tofflvlgc)

        # вычисляем ЛО НН2
        vvod_lvcbptrc1_lvtcboff2, oper_vyvod_lvcbptrc1_lvtcboff2, otkl_lvcbptrc1_lvtcboff2, otkl_avar_lvcbptrc1_lvtcboff2, vvod_lvcbrecrbre1_lvtcboff2, oper_vyvod_lvcbrecrbre1_lvtcboff2, zapret_lvcbrecrbre1_lvtcboff2, vvod_lvbtsrblc1_lvtcboff2, oper_vyvod_lvbtsrblc1_lvtcboff2, zapret_lvbtsrblc1_lvtcboff2 = self.lvtcboff2.Step(DI_ControllerDisable, DI_LVTRESCBOFF2, DI_LVCBPTRC2, DI_LVCBRECRBRE2, DI_LVBTSRBLC2, srab_ptrc1_tofflvlgc, zapret_rbre1_tofflvlgc, zapret_rblc1_tofflvlgc)

        # вычисляем КСВ
        ot_emo1emv = ot_emo2 = 0
        srab_na_sebya_rbrf1_tpbrf = 0
        avar_isol_V = niz_isol_V = pruzh_ne_zaved =  v_neisp_pol_xcbr1_tsd = 0
        v_otkluchen_xcbr1_tsd = v_vkluchen_xcbr1_tsd = Sbros = 0
        otkl_ot_knopk = oper_otkl_V = KRV_resurs_V = uv_otkluchit_cbcswi1_swctrl = 0
        #kontr_emv = T_TPBRF_1_CBOS1Supervision = T_TPBRF_1_CBOS2Supervision = rabota_emv = rabota_emo1 = rabota_emo2 = 0
        kontr_emv = rabota_emv = rabota_emo1 = rabota_emo2 = 0
        vvod_rcbf1_lvcbsup, oper_vyvod_rcbf1_lvcbsup, v_samoproisv_otkl_rcbf1_lvcbsup, neispr_V_rcbf1_lvcbsup, v_avar_otkl_rcbf1_lvcbsup, rfk_rcbf1_lvcbsup, blok_vkl_rcbf1_lvcbsup, blok_otkl_rcbf1_lvcbsup, neisp_emu_rcbf1_lvcbsup, zashita_emv_rcbf1_lvcbsup, zashita_emo1_rcbf1_lvcbsup, zashita_emo2_rcbf1_lvcbsup = self.lvcbsup.Step(DI_ControllerDisable, DI_LVCBSUP, ot_emo1emv, ot_emo2, otkl_hvcbptrc1_hvtcboff, srab_na_sebya_rbrf1_tpbrf, avar_isol_V, niz_isol_V, pruzh_ne_zaved, v_neisp_pol_xcbr1_tsd, v_otkluchen_xcbr1_tsd, v_vkluchen_xcbr1_tsd, Sbros, uv_otkluchit_cbcswi1_swctrl, otkl_ot_knopk, oper_otkl_V, KRV_resurs_V, ExternalBlkCB, kontr_emv, T_TPBRF_1_CBOS1Supervision, T_TPBRF_1_CBOS2Supervision, rabota_emv, rabota_emo1, rabota_emo2)

        # вычисляем УРОВ
        vvod_rbrf1_tpbrf, oper_vyvod_rbrf1_tpbrf, uskorenie_rbrf1_tpbrf, srab_rbrf1_tpbrf, pusk_rbrf1_tpbrf, io_rbrf1_tpbrf, srab_na_sebya_rbrf1_tpbrf = self.tpbrf.Step(DI_ControllerDisable, DI_TPBRF, blok_otkl_rcbf1_lvcbsup, otkl_hvcbptrc1_hvtcboff, T_TPBRF_1_CBOS1Supervision, T_TPBRF_1_CBOS2Supervision, (mtz_pusk_lvttoc, pusk_ptoc1_lvtoc), ExternalRBRFStart, IA, IB, IC)

        # вычисляем СС
        srabKont_ptrc1_talmgaslgc = srabKont_ptrc1_ttrgaslgc = srabKont_ptrc1_tltcgaslgc = 0
        zablok_ptrc1_talmgaslgc = zablok_ptrc1_ttrgaslgc = zablok_ptrc1_tltcgaslgc = 0 
        srabKI_ptrc1_talmgaslgc = srabKI_ptrc1_ttrgaslgc = srabKI_ptrc1_tltcgaslgc = 0

        SS_gz_sign, SS_gz_zablok, SS_gz_nizk_isol, SS_vnesh_otkl, SS_vyh_zepi_razobr, SS_bi_vyved, SS_ot_sign, SS_neispr_ot_gz, SS_neispr_ot_v, SS_ot_nn_sign, SS_prev_vrem_per_ka, SS_obsh_vnesh_sign = self.t_signassembly.Step(DI_ControllerDisable, gz_sign=(srabKont_ptrc1_talmgaslgc, srabKont_ptrc1_ttrgaslgc, srabKont_ptrc1_tltcgaslgc), gz_zablok=(zablok_ptrc1_talmgaslgc, zablok_ptrc1_ttrgaslgc, zablok_ptrc1_tltcgaslgc), gz_ki=(srabKI_ptrc1_talmgaslgc, srabKI_ptrc1_ttrgaslgc, srabKI_ptrc1_tltcgaslgc), vnesh_otkl=(OpExtOfARC_NN1, OpExtOfARC_NN2, OpExtOfCBFP_NN1, OpExtOfCBFP_NN2), Polozh_SA1=T2_PNL_1_CtlCirSwPos1, Polozh_SA2=T2_PNL_1_CtlCirSwPos2, Polozh_SA3=T2_PNL_1_CtlCirSwPos3, Polozh_SA4=T2_PNL_1_CtlCirSwPos4, Polozh_SA5=T2_PNL_1_CtlCirSwPos5, Polozh_SA6=T2_PNL_1_CtlCirSwPos6, Polozh_SG1=T2_PNL_1_TestBlockPos1, Polozh_SG2=T2_PNL_1_TestBlockPos2, Polozh_SG3=T2_PNL_1_TestBlockPos3, ot_gz=GAS_OCControl, ot_v=OCcir_CB, ot_zdz_nn1=ARCnn1_OCControl, ot_zdz_nn2=ARCnn2_OCControl, ot_urov_nn1=CBFPnn1_OCControl, ot_urov_nn2=CBFPnn2_OCControl, ot_ieu_tn1=IEDvt_OCControl1, ot_ieu_tn2=IEDvt_OCControl2, prev_vrem_ka=(0,), vnesh_sign=(ExtSignal1, ExtSignal2, ExtSignal3, ExtSignal4))

        # вычисляем ПС

        pusk_lvalh = self.lvalh.Step(DI_ControllerDisable, COMM_SIGN=(mtz_srabsign_ptoc1_lvttoc, mtz_srabsign_ptoc2_lvttoc, mtz_srabsign_ptoc3_lvttoc, srab_ptrc1_tofflvlgc, srab_rbrf1_tpbrf, srab_na_sebya_rbrf1_tpbrf, neispr_V_rcbf1_lvcbsup, v_samoproisv_otkl_rcbf1_lvcbsup, srab_ptrc1_tofflvlgc), sgf1_sign=SS_gz_sign, sgf2_sign=SS_gz_nizk_isol, sgf3_sign=SS_gz_zablok, sgf4_sign=SS_ot_sign, sgf5_sign=SS_ot_nn_sign, sgf6_sign=SS_vnesh_otkl, sgf7_sign=SS_vyh_zepi_razobr, sgf8_sign=SS_bi_vyved, sgf9_sign=SS_prev_vrem_per_ka, sgf10_sign=SS_obsh_vnesh_sign)


        return (mtz_pusk_lvttoc, mtz_srab_ptoc1_lvttoc, mtz_srab_ptoc2_lvttoc, mtz_srab_ptoc3_lvttoc, pusk_ptoc1_lvtoc, srab_ptoc1_lvtoc,
        vvod_ptrc1_tofflvlgc, oper_vyvod_ptrc1_tofflvlgc, srab_ptrc1_tofflvlgc, vvod_rblc1_tofflvlgc, oper_vyvod_rblc1_tofflvlgc, zapret_rblc1_tofflvlgc, vvod_rbre1_tofflvlgc, oper_vyvod_rbre1_tofflvlgc, zapret_rbre1_tofflvlgc,
        vvod_hvcbptrc1_hvtcboff, oper_vyvod_hvcbptrc1_hvtcboff, otkl_hvcbptrc1_hvtcboff, otkl_avar_hvcbptrc1_hvtcboff,
        vvod_lvcbptrc1_lvtcboff1, oper_vyvod_lvcbptrc1_lvtcboff1, otkl_lvcbptrc1_lvtcboff1, otkl_avar_lvcbptrc1_lvtcboff1, vvod_lvcbrecrbre1_lvtcboff1, oper_vyvod_lvcbrecrbre1_lvtcboff1, zapret_lvcbrecrbre1_lvtcboff1, vvod_lvbtsrblc1_lvtcboff1, oper_vyvod_lvbtsrblc1_lvtcboff1, zapret_lvbtsrblc1_lvtcboff1,
        vvod_lvcbptrc1_lvtcboff2, oper_vyvod_lvcbptrc1_lvtcboff2, otkl_lvcbptrc1_lvtcboff2, otkl_avar_lvcbptrc1_lvtcboff2, vvod_lvcbrecrbre1_lvtcboff2, oper_vyvod_lvcbrecrbre1_lvtcboff2, zapret_lvcbrecrbre1_lvtcboff2, vvod_lvbtsrblc1_lvtcboff2, oper_vyvod_lvbtsrblc1_lvtcboff2, zapret_lvbtsrblc1_lvtcboff2,
        blok_otkl_rcbf1_lvcbsup,
        vvod_rbrf1_tpbrf, oper_vyvod_rbrf1_tpbrf, uskorenie_rbrf1_tpbrf, srab_rbrf1_tpbrf, pusk_rbrf1_tpbrf, io_rbrf1_tpbrf, srab_na_sebya_rbrf1_tpbrf,
        SS_gz_sign, SS_gz_zablok, SS_gz_nizk_isol, SS_vnesh_otkl, SS_vyh_zepi_razobr, SS_bi_vyved, SS_ot_sign, SS_neispr_ot_gz, SS_neispr_ot_v, SS_ot_nn_sign, SS_prev_vrem_per_ka, SS_obsh_vnesh_sign,
        pusk_lvalh)
       

if __name__ == "__main__":
    part = part_LO(SGF1=1)
    res = part.Step()
    print(res)



            


