

from lib2.FBS.T_SwitchDevice import T_Switch_Device # импорт ФБ КА
from lib2.FUNCS.CLS import CLS
from lib2.FBS.T2_LVALH import T2_LVALH # импорт ФБ ПС
from lib2.FBS.LVCBSUP import LVCBSUP # импорт ФБ КСВ


class partKRV:
        
    def __init__(self, SGF1, Inom_V_pasp, Inom_otl_V_pasp, KRVpasp_Inom, KRVpasp_Inom_otkl,
            MRVpasp, Nach_znach_KRV, KRVsrab, Nach_znach_MRV, SGF2, T1, 
            SGF1_tsd, SGF1_xcbr1_tsd, SGF2_xcbr1_tsd, SGF3_xcbr1_tsd, SGF4_xcbr1_tsd, SGF5_xcbr1_tsd, T1_xcbr1_tsd, T2_xcbr1_tsd, T3_xcbr1_tsd, T4_xcbr1_tsd, SGF1_rcbf1_lvcbsup, SGF2_rcbf1_lvcbsup, SGF3_rcbf1_lvcbsup, SGF4_rcbf1_lvcbsup, SGF5_rcbf1_lvcbsup, SGF6_rcbf1_lvcbsup, SGF7_rcbf1_lvcbsup, SGF8_rcbf1_lvcbsup, T1_rcbf1_lvcbsup, T2_rcbf1_lvcbsup, T3_rcbf1_lvcbsup, 
            SGF1_lvalh, SGF2_lvalh, SGF3_lvalh, SGF4_lvalh, SGF5_lvalh, SGF6_lvalh, SGF7_lvalh, SGF8_lvalh, SGF9_lvalh, SGF10_lvalh):
        
        # Инициализируем КРВ
        self.krv = CLS(SGF1, Inom_V_pasp, Inom_otl_V_pasp, KRVpasp_Inom, KRVpasp_Inom_otkl, MRVpasp, Nach_znach_KRV, KRVsrab, Nach_znach_MRV, SGF2, T1)

        # Инициализируем ФБ КА
        self.tsd = T_Switch_Device(SGF1_tsd, SGF1_xcbr1_tsd, SGF2_xcbr1_tsd, SGF3_xcbr1_tsd, SGF4_xcbr1_tsd, SGF5_xcbr1_tsd, T1_xcbr1_tsd/1000, T2_xcbr1_tsd/1000, T3_xcbr1_tsd/1000, T4_xcbr1_tsd/1000)

        # Инициализируем ФБ КСВ 
        self.lvcbsup = LVCBSUP(SGF1_rcbf1_lvcbsup, SGF2_rcbf1_lvcbsup, SGF3_rcbf1_lvcbsup, SGF4_rcbf1_lvcbsup, SGF5_rcbf1_lvcbsup, SGF6_rcbf1_lvcbsup, SGF7_rcbf1_lvcbsup, SGF8_rcbf1_lvcbsup, T1_rcbf1_lvcbsup/1000, T2_rcbf1_lvcbsup/1000, T3_rcbf1_lvcbsup/1000)

        # Инициализируем ФБ ПС
        self.t_lvalh = T2_LVALH(SGF1_lvalh, SGF2_lvalh, SGF3_lvalh, SGF4_lvalh, SGF5_lvalh, SGF6_lvalh, SGF7_lvalh, SGF8_lvalh, SGF9_lvalh, SGF10_lvalh)

        # Инициализация переменных, которые должны быть инициализированы для расчетов - но по логике так не получается (обратные связи)
        self.v_otkluchen_xcbr1_tsd = 0
        self.v_vkluchen_xcbr1_tsd = 0  
        self.v_neisp_pol_xcbr1_tsd = 0
        self.v_otkluchit_rele_xcbr1_tsd = 0


    def Step(self, DI_ControllerDisable, CBPosOpn, CBPosCls, CLS_1_ResetCounter, LocKey, IA, IB, IC, Reset, OperOpnCB):

        # ================================== КРВ =========================================================

        CLS_1_CLS_FuncEnabled, CLS_1_CLS_MDResourceExcess, CLS_1_CLS_CBLifeExcess, CLS_1_CLS_COMMResourceExcess, CLS_1_CLS_MDCurrentResource, CLS_1_CLS_COMMCurrResourcePhsA, CLS_1_CLS_COMMCurrResourcePhsB, CLS_1_CLS_COMMCurrResourcePhsC = self.krv.Step(DI_ControllerDisable, self.v_vkluchen_xcbr1_tsd, self.v_otkluchen_xcbr1_tsd, CLS_1_ResetCounter, self.v_otkluchit_rele_xcbr1_tsd, LocKey, IA, IB, IC)
        ###############################################################################################################


        # ================================================== КСВ ===========================================================
        DI_LVCBSUP = 0
        CBCS_CBOS1_OCControl = 0
        CBOS2_OCControl = 0 
        otkl_hvcbptrc1_hvtcboff = 0
        srab_na_sebya_rbrf1_tpbrf = 0
        InsTr = 0 
        LowIns = 0
        EnBlk = 0
        uv_otkluchit_cbcswi1_swctrl = 0
        OpnCBFrmKnob = 0
        ExternalBlkCB = 0
        CBCSCtrl = 0
        CBOS1Ctrl = 0
        CBOS2Ctrl = 0 
        CBCSWorking = 0
        CBOS1Working = 0
        CBOS2Working = 0

        vvod_rcbf1_lvcbsup, oper_vyvod_rcbf1_lvcbsup, v_samoproisv_otkl_rcbf1_lvcbsup, neispr_V_rcbf1_lvcbsup, v_avar_otkl_rcbf1_lvcbsup, rfk_rcbf1_lvcbsup, blok_vkl_rcbf1_lvcbsup, blok_otkl_rcbf1_lvcbsup, neisp_emu_rcbf1_lvcbsup, zashita_emv_rcbf1_lvcbsup, zashita_emo1_rcbf1_lvcbsup, zashita_emo2_rcbf1_lvcbsup = self.lvcbsup.Step(DI_ControllerDisable, DI_LVCBSUP, CBCS_CBOS1_OCControl, CBOS2_OCControl, otkl_hvcbptrc1_hvtcboff, srab_na_sebya_rbrf1_tpbrf, InsTr, LowIns, EnBlk, self.v_neisp_pol_xcbr1_tsd, self.v_otkluchen_xcbr1_tsd, self.v_vkluchen_xcbr1_tsd, Reset, uv_otkluchit_cbcswi1_swctrl, OpnCBFrmKnob, OperOpnCB, CLS_1_CLS_CBLifeExcess, ExternalBlkCB, CBCSCtrl, CBOS1Ctrl, CBOS2Ctrl, CBCSWorking, CBOS1Working, CBOS2Working)

        ###############################################################################################################


        # ================================================== КА ===========================================================

        DI_SD = 0 
        otkl_avar_hvcbptrc1_hvtcboff = 0
        uv_vkluchit_cbcswi1_swctrl = 0
        uv_vkl_cbcswi1_hvbctrl = 0

        vvod_tds, oper_vyvod_tds, vvod_xcbr1_tsd, v_prom_pol_xcbr1_tsd, self.v_otkluchen_xcbr1_tsd, self.v_vkluchen_xcbr1_tsd, self.v_neisp_pol_xcbr1_tsd, self.v_otkluchit_rele_xcbr1_tsd, v_vkluchit_rele_xcbr1_tsd = self.tsd.Step(DI_ControllerDisable, DI_SD, CBPosOpn, CBPosCls, uv_otkluchit_cbcswi1_swctrl, otkl_avar_hvcbptrc1_hvtcboff, srab_na_sebya_rbrf1_tpbrf, OperOpnCB, blok_otkl_rcbf1_lvcbsup, CBOS1Working, CBOS2Working, Reset, uv_vkluchit_cbcswi1_swctrl, uv_vkl_cbcswi1_hvbctrl, CBCSWorking)

        # ================================================== ПС ===========================================================

        pusk_t_lvalh = self.t_lvalh.Step(VYVOD=DI_ControllerDisable, COMM_SIGN=(CLS_1_CLS_CBLifeExcess, v_samoproisv_otkl_rcbf1_lvcbsup, neispr_V_rcbf1_lvcbsup, v_avar_otkl_rcbf1_lvcbsup))

        return (
            v_samoproisv_otkl_rcbf1_lvcbsup, neispr_V_rcbf1_lvcbsup, v_avar_otkl_rcbf1_lvcbsup, blok_vkl_rcbf1_lvcbsup, blok_otkl_rcbf1_lvcbsup,  
                
            int(v_prom_pol_xcbr1_tsd), int(self.v_otkluchen_xcbr1_tsd), int(self.v_vkluchen_xcbr1_tsd), int(self.v_otkluchit_rele_xcbr1_tsd), int(v_vkluchit_rele_xcbr1_tsd),

            int(pusk_t_lvalh),

            CLS_1_CLS_FuncEnabled, CLS_1_CLS_MDResourceExcess, CLS_1_CLS_CBLifeExcess, CLS_1_CLS_COMMResourceExcess, CLS_1_CLS_MDCurrentResource, CLS_1_CLS_COMMCurrResourcePhsA, CLS_1_CLS_COMMCurrResourcePhsB, CLS_1_CLS_COMMCurrResourcePhsC
                )






