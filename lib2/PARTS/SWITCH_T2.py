# ЧАСТЬ СХЕМЫ ФСУ ДЛЯ КСВ, КП, КА, УВ, УРОВ
# ИСПОЛНЕНИЯ Т2

from lib2.FBS.LVCBSUP import LVCBSUP # импорт ФБ КСВ
from lib2.FBS.SWCTRL import SWCTRL # импорт ФБ КП
from lib2.FBS.HVBCTRL import HVBCTRL # импорт ФБ УВ
from lib2.FBS.T_SwitchDevice import T_Switch_Device # импорт ФБ КА
from lib2.FBS.T2_SignAssembly import T2_SignAssembly # импорт ФБ СС T2
from lib2.FBS.T2_LVALH import T2_LVALH # импорт ФБ ПС
from lib2.FBS.TPBRF_T import TPBRF # импорт ФБ УРОВ
from lib2.FBS.HVTCBOFF import HVTCBOFF # импорт ФБ ЛО ВН

class SWITCH:
    def __init__(self, 
    SGF1_rcbf1_lvcbsup, SGF2_rcbf1_lvcbsup, SGF3_rcbf1_lvcbsup, SGF4_rcbf1_lvcbsup, SGF5_rcbf1_lvcbsup, SGF6_rcbf1_lvcbsup, SGF7_rcbf1_lvcbsup, SGF8_rcbf1_lvcbsup, T1_rcbf1_lvcbsup, T2_rcbf1_lvcbsup, T3_rcbf1_lvcbsup,
    SGF1_swctrl, SGF1_cbcswi1_swctrl, SGF2_cbcswi1_swctrl, T1_cbcswi1_swctrl, T2_cbcswi1_swctrl, T3_cbcswi1_swctrl, T4_cbcswi1_swctr,
    SGF1_cbcswi1_hvbctrl, T1_cbcswi1_hvbctrl,
    SGF1_tsd, SGF1_xcbr1_tsd, SGF2_xcbr1_tsd, SGF3_xcbr1_tsd, SGF4_xcbr1_tsd, SGF5_xcbr1_tsd,  T1_xcbr1_tsd, T2_xcbr1_tsd, T3_xcbr1_tsd, T4_xcbr1_tsd,
    SGF1_lvalh, SGF2_lvalh, SGF3_lvalh, SGF4_lvalh, SGF5_lvalh, SGF6_lvalh, SGF7_lvalh, SGF8_lvalh, SGF9_lvalh, SGF10_lvalh,
    SGF1_rbrf1_tpbrf, SGF2_rbrf1_tpbrf, SGF3_rbrf1_tpbrf, SGF4_rbrf1_tpbrf, SGF5_rbrf1_tpbrf, SGF6_rbrf1_tpbrf, T1_rbrf1_tpbrf, Iset_rbrf1_tpbrf,
    SGF1_hvcbptrc1_hvtcboff, T1_hvcbptrc1_hvtcboff
    ):

        # Инициализируем ФБ КСВ 
        self.lvcbsup = LVCBSUP(SGF1_rcbf1_lvcbsup, SGF2_rcbf1_lvcbsup, SGF3_rcbf1_lvcbsup, SGF4_rcbf1_lvcbsup, SGF5_rcbf1_lvcbsup, SGF6_rcbf1_lvcbsup, SGF7_rcbf1_lvcbsup, SGF8_rcbf1_lvcbsup, T1_rcbf1_lvcbsup, T2_rcbf1_lvcbsup, T3_rcbf1_lvcbsup)
    
        # Инициализируем ФБ КП
        self.swctrl = SWCTRL(SGF1_swctrl, SGF1_cbcswi1_swctrl, SGF2_cbcswi1_swctrl, T1_cbcswi1_swctrl, T2_cbcswi1_swctrl, T3_cbcswi1_swctrl, T4_cbcswi1_swctr)               

        # Инициализируем ФБ УВ
        self.hvbctrl = HVBCTRL(SGF1_cbcswi1_hvbctrl, T1_cbcswi1_hvbctrl)

        # Инициализируем ФБ КА
        self.tsd = T_Switch_Device(SGF1_tsd, SGF1_xcbr1_tsd, SGF2_xcbr1_tsd, SGF3_xcbr1_tsd, SGF4_xcbr1_tsd, SGF5_xcbr1_tsd, T1_xcbr1_tsd, T2_xcbr1_tsd, T3_xcbr1_tsd, T4_xcbr1_tsd)

        # Инициализируем ФБ СС
        self.tsa = T2_SignAssembly()

        # Инициализируем ФБ ПС
        self.t_lvalh = T2_LVALH( SGF1_lvalh, SGF2_lvalh, SGF3_lvalh, SGF4_lvalh, SGF5_lvalh, SGF6_lvalh, SGF7_lvalh, SGF8_lvalh, SGF9_lvalh, SGF10_lvalh)

        # Инициализируем ФБ УРОВ
        self.tpbrf = TPBRF(SGF1_rbrf1_tpbrf, SGF2_rbrf1_tpbrf, SGF3_rbrf1_tpbrf, SGF4_rbrf1_tpbrf, SGF5_rbrf1_tpbrf, SGF6_rbrf1_tpbrf, T1_rbrf1_tpbrf, Iset_rbrf1_tpbrf)

        # Инициализируем ФБ ЛО ВН
        self.hvtcboff = HVTCBOFF(SGF1_hvcbptrc1_hvtcboff, T1_hvcbptrc1_hvtcboff)      

        # Инициализация переменных, которые должны быть инициализированы для расчетов - но по логике так не получается (обратные связи)
        self.v_otkluchen_xcbr1_tsd = False
        self.v_vkluchen_xcbr1_tsd = False  
        self.v_neisp_pol_xcbr1_tsd = False
        self.uv_otkluchit_cbcswi1_swctrl = False
        self.srab_na_sebya_rbrf1_tpbrf = False  

    def Step(self, 
    DI_ControllerDisable, 
    DI_LVCBSUP, CBCS_CBOS1_OCControl, CBOS2_OCControl, InsTr, LowIns, EnBlk, Reset, OpnCBFrmKnob, OperOpnCB, T_LVCBSUP_1_ClsResourceExcess, ExternalBlkCB, CBCSCtrl, CBOS1Ctrl, CBOS2Ctrl, CBCSWorking, CBOS1Working, CBOS2Working,
    DI_SWCTRL, OpnCBFrmCtrlPanel, T_SWCTRL_1_OpnCBFrm_HMI, LocKey, OpnCBFrmRemoteCtrl, T_SWCTRL_1_OpnCBFrm_ACS, KeyLocDist, ClsCBFrmCtrlPanel, T_SWCTRL_1_ClsCBFrm_HMI, ClsCBFrmRemoteCtrl, T_SWCTRL_1_ClsCBFrm_ACS, CBPosOpn, CBPosCls,
    DI_HVBCTRL, OperClsCB, 
    DI_SD, 
    ExternalRBRFStart,
    OpExtOfARC_NN1, OpExtOfCBFP_NN1, OpExtOfARC_NN2, OpExtOfCBFP_NN2
    ):
        
        # === НАЧАЛО ИЗМЕНЕНИЙ ===
        # Жесткая логическая связь: Дистанционное = НЕ Местное
        # Если mestnoe=1, то Remote станет 0. Если mestnoe=0, то Remote станет 1.
        # Мы перезаписываем входящий аргумент Remote перед использованием.
        distanz = 1 - int(LocKey) 
        #mestnoe = 1 - int(Remote) 
        # === КОНЕЦ ИЗМЕНЕНИЙ ===


        vvod_hvcbptrc1_hvtcboff, oper_vyvod_hvcbptrc1_hvtcboff, otkl_hvcbptrc1_hvtcboff, otkl_avar_hvcbptrc1_hvtcboff = self.hvtcboff.Step(DI_ControllerDisable, OV_hvcbptrc1_hvtcboff=0, LO_t_srab=0, vnesh_otkl_zdz=OpExtOfARC_NN1 or OpExtOfARC_NN2, vnesh_otkl_urov=OpExtOfCBFP_NN1 or OpExtOfCBFP_NN2)

        vvod_rcbf1_lvcbsup, oper_vyvod_rcbf1_lvcbsup, v_samoproisv_otkl_rcbf1_lvcbsup, neispr_V_rcbf1_lvcbsup, v_avar_otkl_rcbf1_lvcbsup, rfk_rcbf1_lvcbsup, blok_vkl_rcbf1_lvcbsup, blok_otkl_rcbf1_lvcbsup, neisp_emu_rcbf1_lvcbsup, zashita_emv_rcbf1_lvcbsup, zashita_emo1_rcbf1_lvcbsup, zashita_emo2_rcbf1_lvcbsup = self.lvcbsup.Step(DI_ControllerDisable, DI_LVCBSUP, CBCS_CBOS1_OCControl, CBOS2_OCControl, otkl_hvcbptrc1_hvtcboff, self.srab_na_sebya_rbrf1_tpbrf, InsTr, LowIns, EnBlk, self.v_neisp_pol_xcbr1_tsd, self.v_otkluchen_xcbr1_tsd, self.v_vkluchen_xcbr1_tsd, Reset, self.uv_otkluchit_cbcswi1_swctrl, OpnCBFrmKnob, OperOpnCB, T_LVCBSUP_1_ClsResourceExcess, ExternalBlkCB, CBCSCtrl, CBOS1Ctrl, CBOS2Ctrl, CBCSWorking, CBOS1Working, CBOS2Working)

        vvod_swctrl, oper_vyvod_swctrl, vvod_cbcswi1_swctrl, self.uv_otkluchit_cbcswi1_swctrl, uv_idet_per_cbcswi1_swctrl, uv_prev_vrem_per_cbcswi1_swctrl, uv_vkluchit_cbcswi1_swctrl, uv_ne_opredeleno_cbcswi1_swctrl, uv_otklucheno_cbcswi1_swctrl, uv_vklucheno_cbcswi1_swctrl, uv_neispr_neopred_cbcswi1_swctrl = self.swctrl.Step(DI_ControllerDisable, DI_SWCTRL, blok_otkl_rcbf1_lvcbsup, OpnCBFrmCtrlPanel, T_SWCTRL_1_OpnCBFrm_HMI, LocKey, OpnCBFrmRemoteCtrl, T_SWCTRL_1_OpnCBFrm_ACS, KeyLocDist, ClsCBFrmCtrlPanel, T_SWCTRL_1_ClsCBFrm_HMI, distanz, ClsCBFrmRemoteCtrl, T_SWCTRL_1_ClsCBFrm_ACS, blok_vkl_rcbf1_lvcbsup, v_avar_otkl_rcbf1_lvcbsup, CBPosOpn, CBPosCls)

        vvod_cbcswi1_hvbctrl, oper_vyvod_cbcswi1_hvbctrl, uv_vkl_cbcswi1_hvbctrl = self.hvbctrl.Step(DI_ControllerDisable, DI_HVBCTRL, OperClsCB, blok_vkl_rcbf1_lvcbsup)

        vvod_tds, oper_vyvod_tds,  vvod_xcbr1_tsd, v_prom_pol_xcbr1_tsd, self.v_otkluchen_xcbr1_tsd, self.v_vkluchen_xcbr1_tsd, self.v_neisp_pol_xcbr1_tsd, v_otkluchit_rele_xcbr1_tsd, v_vkluchit_rele_xcbr1_tsd = self.tsd.Step(DI_ControllerDisable, DI_SD, CBPosOpn, CBPosCls, self.uv_otkluchit_cbcswi1_swctrl, otkl_avar_hvcbptrc1_hvtcboff, self.srab_na_sebya_rbrf1_tpbrf, OperOpnCB, blok_otkl_rcbf1_lvcbsup, CBOS1Working, CBOS2Working, Reset, uv_vkluchit_cbcswi1_swctrl, uv_vkl_cbcswi1_hvbctrl, CBCSWorking)

        vvod_rbrf1_tpbrf, oper_vyvod_rbrf1_tpbrf, uskorenie_rbrf1_tpbrf, srab_rbrf1_tpbrf, pusk_rbrf1_tpbrf, io_rbrf1_tpbrf, self.srab_na_sebya_rbrf1_tpbrf = self.tpbrf.Step(DI_ControllerDisable, OV_rbrf1_tpbrf=0, blok_otkl_rcbf1_lvcbsup=blok_otkl_rcbf1_lvcbsup, LO_VN_otkl=0, kontr_emo1=CBOS1Ctrl, kontr_emo2=CBOS2Ctrl, Puski=(0,0), pusk_urov_vnesh=ExternalRBRFStart, IA=0, IB=0, IC=0)

        ss_prev_vrem_per_ka = self.tsa.Step(VYVOD=DI_ControllerDisable, prev_vrem_ka=(uv_prev_vrem_per_cbcswi1_swctrl,))[10]

        pusk_t_lvalh = self.t_lvalh.Step(VYVOD=DI_ControllerDisable, COMM_SIGN=(v_samoproisv_otkl_rcbf1_lvcbsup, neispr_V_rcbf1_lvcbsup), sgf9_sign=ss_prev_vrem_per_ka)

        return (
            vvod_rcbf1_lvcbsup, oper_vyvod_rcbf1_lvcbsup, v_samoproisv_otkl_rcbf1_lvcbsup, neispr_V_rcbf1_lvcbsup, v_avar_otkl_rcbf1_lvcbsup, rfk_rcbf1_lvcbsup, blok_vkl_rcbf1_lvcbsup, blok_otkl_rcbf1_lvcbsup, neisp_emu_rcbf1_lvcbsup, zashita_emv_rcbf1_lvcbsup, zashita_emo1_rcbf1_lvcbsup, zashita_emo2_rcbf1_lvcbsup,
            vvod_swctrl, oper_vyvod_swctrl, vvod_cbcswi1_swctrl, self.uv_otkluchit_cbcswi1_swctrl, uv_idet_per_cbcswi1_swctrl, uv_prev_vrem_per_cbcswi1_swctrl, uv_vkluchit_cbcswi1_swctrl, uv_ne_opredeleno_cbcswi1_swctrl, uv_otklucheno_cbcswi1_swctrl, uv_vklucheno_cbcswi1_swctrl, uv_neispr_neopred_cbcswi1_swctrl,
            vvod_cbcswi1_hvbctrl, oper_vyvod_cbcswi1_hvbctrl, uv_vkl_cbcswi1_hvbctrl,
            vvod_tds, oper_vyvod_tds,  vvod_xcbr1_tsd, v_prom_pol_xcbr1_tsd, self.v_otkluchen_xcbr1_tsd, self.v_vkluchen_xcbr1_tsd, self.v_neisp_pol_xcbr1_tsd, v_otkluchit_rele_xcbr1_tsd, v_vkluchit_rele_xcbr1_tsd, ss_prev_vrem_per_ka, pusk_t_lvalh,
            self.srab_na_sebya_rbrf1_tpbrf,
            vvod_hvcbptrc1_hvtcboff, otkl_hvcbptrc1_hvtcboff, otkl_avar_hvcbptrc1_hvtcboff
        )

if __name__ == "__main__":
    part = SWITCH()
    res = part.Step(0, (0,0,0), 0,0,0,0,0,0,0,0,0,0,0,0,0)
    print(res)



            


