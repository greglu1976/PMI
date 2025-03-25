# ЧАСТЬ СХЕМЫ ФСУ ДЛЯ КСВ, КП, КА, УВ
# ЭТА версия с СС, ПС (Изм. по срав с part_SWITCH - убран второй sbros!)
# ИСПОЛНЕНИЯ Т

from lib._FBS.LVCBSUP import LVCBSUP # импорт ФБ КСВ
from lib._FBS.SWCTRL import SWCTRL # импорт ФБ КП
from lib._FBS.HVBCTRL import HVBCTRL # импорт ФБ УВ
from lib._FBS.T_SwitchDevice import T_Switch_Device # импорт ФБ КА
from lib._FBS.T_SignAssembly import T_SignAssembly # импорт ФБ СС
from lib._FBS.T_LVALH import T_LVALH # импорт ФБ ПС

class SWITCH:
    def __init__(self, 
    SGF1_rcbf1_lvcbsup, SGF2_rcbf1_lvcbsup, SGF3_rcbf1_lvcbsup, SGF4_rcbf1_lvcbsup, SGF5_rcbf1_lvcbsup, SGF6_rcbf1_lvcbsup, SGF7_rcbf1_lvcbsup, SGF8_rcbf1_lvcbsup, T1_rcbf1_lvcbsup, T2_rcbf1_lvcbsup, T3_rcbf1_lvcbsup,
    SGF1_swctrl, SGF1_cbcswi1_swctrl, SGF2_cbcswi1_swctrl, T1_cbcswi1_swctrl, T2_cbcswi1_swctrl, T3_cbcswi1_swctrl, T4_cbcswi1_swctr,
    SGF1_cbcswi1_hvbctrl, T1_cbcswi1_hvbctrl,
    SGF1_tsd, SGF1_xcbr1_tsd, SGF2_xcbr1_tsd, SGF3_xcbr1_tsd, SGF4_xcbr1_tsd, SGF5_xcbr1_tsd, SGF6_xcbr1_tsd, T1_xcbr1_tsd, T2_xcbr1_tsd, T3_xcbr1_tsd, T4_xcbr1_tsd,
    SGF13_tsa
    ):

        # Инициализируем ФБ КСВ 
        self.lvcbsup = LVCBSUP(SGF1_rcbf1_lvcbsup, SGF2_rcbf1_lvcbsup, SGF3_rcbf1_lvcbsup, SGF4_rcbf1_lvcbsup, SGF5_rcbf1_lvcbsup, SGF6_rcbf1_lvcbsup, SGF7_rcbf1_lvcbsup, SGF8_rcbf1_lvcbsup, T1_rcbf1_lvcbsup, T2_rcbf1_lvcbsup, T3_rcbf1_lvcbsup)
    
        # Инициализируем ФБ КП
        self.swctrl = SWCTRL(SGF1_swctrl, SGF1_cbcswi1_swctrl, SGF2_cbcswi1_swctrl, T1_cbcswi1_swctrl, T2_cbcswi1_swctrl, T3_cbcswi1_swctrl, T4_cbcswi1_swctr)               

        # Инициализируем ФБ УВ
        self.hvbctrl = HVBCTRL(SGF1_cbcswi1_hvbctrl, T1_cbcswi1_hvbctrl)

        # Инициализируем ФБ КА
        self.tsd = T_Switch_Device(SGF1_tsd, SGF1_xcbr1_tsd, SGF2_xcbr1_tsd, SGF3_xcbr1_tsd, SGF4_xcbr1_tsd, SGF5_xcbr1_tsd, SGF6_xcbr1_tsd, T1_xcbr1_tsd, T2_xcbr1_tsd, T3_xcbr1_tsd, T4_xcbr1_tsd)

        # Инициализируем ФБ СС
        self.tsa = T_SignAssembly(SGF13_tsa)

        # Инициализируем ФБ ПС
        self.t_lvalh = T_LVALH()

        # Инициализация переменных, которые должны быть инициализированы для расчетов - но по логике так не получается (обратные связи)
        self.v_otkluchen_xcbr1_tsd = False
        self.v_vkluchen_xcbr1_tsd = False  
        self.v_neisp_pol_xcbr1_tsd = False
        self.uv_otkluchit_cbcswi1_swctrl = False    

    def Step(self, 
    VYVOD, 
    OV_rcbf1_lvcbsup, ot_emo1emv, ot_emo2, lovn_otkl, urov_nasebya, avar_isol_V, niz_isol_V, pruzh_ne_zaved, Sbros, otkl_ot_knopk, oper_otkl_V, KRV_resurs_V, vnesh_blok_upr_V, kontr_emv, kontr_emo1, kontr_emo2, rabota_emv, rabota_emo1, rabota_emo2,
    OV_swctrl, otkl_v_ot_pu, otkl_v_ichm, mestnoe, otkl_v_ot_tu, otkl_v_asu, kluch_md_priv, vkl_v_ot_pu, vkl_v_ichm, distanz, vkl_v_ot_tu, vkl_v_asu, v_otkl_bk, v_vkl_bk,
    OV_cbcswi1_hvbctrl, oper_vkl_v, 
    OV_tsd, lovn_lo_otkl_avar, oper_otkl_v
    ):
        vvod_rcbf1_lvcbsup, oper_vyvod_rcbf1_lvcbsup, v_samoproisv_otkl_rcbf1_lvcbsup, neispr_V_rcbf1_lvcbsup, v_avar_otkl_rcbf1_lvcbsup, rfk_rcbf1_lvcbsup, blok_vkl_rcbf1_lvcbsup, blok_otkl_rcbf1_lvcbsup, neisp_emu_rcbf1_lvcbsup, zashita_emv_rcbf1_lvcbsup, zashita_emo1_rcbf1_lvcbsup, zashita_emo2_rcbf1_lvcbsup = self.lvcbsup.Step(VYVOD, OV_rcbf1_lvcbsup, ot_emo1emv, ot_emo2, lovn_otkl, urov_nasebya, avar_isol_V, niz_isol_V, pruzh_ne_zaved, self.v_neisp_pol_xcbr1_tsd, self.v_otkluchen_xcbr1_tsd, self.v_vkluchen_xcbr1_tsd, Sbros, self.uv_otkluchit_cbcswi1_swctrl, otkl_ot_knopk, oper_otkl_V, KRV_resurs_V, vnesh_blok_upr_V, kontr_emv, kontr_emo1, kontr_emo2, rabota_emv, rabota_emo1, rabota_emo2)

        vvod_swctrl, oper_vyvod_swctrl, vvod_cbcswi1_swctrl, self.uv_otkluchit_cbcswi1_swctrl, uv_idet_per_cbcswi1_swctrl, uv_prev_vrem_per_cbcswi1_swctrl, uv_vkluchit_cbcswi1_swctrl, uv_ne_opredeleno_cbcswi1_swctrl, uv_otklucheno_cbcswi1_swctrl, uv_vklucheno_cbcswi1_swctrl, uv_neispr_neopred_cbcswi1_swctrl = self.swctrl.Step(VYVOD, OV_swctrl, blok_otkl_rcbf1_lvcbsup, otkl_v_ot_pu, otkl_v_ichm, mestnoe, otkl_v_ot_tu, otkl_v_asu, kluch_md_priv, vkl_v_ot_pu, vkl_v_ichm, distanz, vkl_v_ot_tu, vkl_v_asu, blok_vkl_rcbf1_lvcbsup, v_avar_otkl_rcbf1_lvcbsup, v_otkl_bk, v_vkl_bk)

        vvod_cbcswi1_hvbctrl, oper_vyvod_cbcswi1_hvbctrl, uv_vkl_cbcswi1_hvbctrl = self.hvbctrl.Step(VYVOD, OV_cbcswi1_hvbctrl, oper_vkl_v, blok_vkl_rcbf1_lvcbsup)

        vvod_tds, oper_vyvod_tds,  vvod_xcbr1_tsd, v_prom_pol_xcbr1_tsd, self.v_otkluchen_xcbr1_tsd, self.v_vkluchen_xcbr1_tsd, self.v_neisp_pol_xcbr1_tsd, v_otkluchit_rele_xcbr1_tsd, v_vkluchit_rele_xcbr1_tsd = self.tsd.Step(VYVOD, OV_tsd, v_otkl_bk, v_vkl_bk, self.uv_otkluchit_cbcswi1_swctrl, lovn_lo_otkl_avar, urov_nasebya, oper_otkl_v, blok_otkl_rcbf1_lvcbsup, rabota_emo1, rabota_emo2, Sbros, uv_vkluchit_cbcswi1_swctrl, uv_vkl_cbcswi1_hvbctrl, rabota_emv)

        ss_prev_vrem_per_ka = self.tsa.Step(VYVOD=VYVOD, prev_vrem_ka=(uv_prev_vrem_per_cbcswi1_swctrl,))[15]

        pusk_t_lvalh = self.t_lvalh.Step(VYVOD=VYVOD, sign_ps_tuple=(v_samoproisv_otkl_rcbf1_lvcbsup, neispr_V_rcbf1_lvcbsup), sgf13_sign=ss_prev_vrem_per_ka)

        return (
            vvod_rcbf1_lvcbsup, oper_vyvod_rcbf1_lvcbsup, v_samoproisv_otkl_rcbf1_lvcbsup, neispr_V_rcbf1_lvcbsup, v_avar_otkl_rcbf1_lvcbsup, rfk_rcbf1_lvcbsup, blok_vkl_rcbf1_lvcbsup, blok_otkl_rcbf1_lvcbsup, neisp_emu_rcbf1_lvcbsup, zashita_emv_rcbf1_lvcbsup, zashita_emo1_rcbf1_lvcbsup, zashita_emo2_rcbf1_lvcbsup,
            vvod_swctrl, oper_vyvod_swctrl, vvod_cbcswi1_swctrl, self.uv_otkluchit_cbcswi1_swctrl, uv_idet_per_cbcswi1_swctrl, uv_prev_vrem_per_cbcswi1_swctrl, uv_vkluchit_cbcswi1_swctrl, uv_ne_opredeleno_cbcswi1_swctrl, uv_otklucheno_cbcswi1_swctrl, uv_vklucheno_cbcswi1_swctrl, uv_neispr_neopred_cbcswi1_swctrl,
            vvod_cbcswi1_hvbctrl, oper_vyvod_cbcswi1_hvbctrl, uv_vkl_cbcswi1_hvbctrl,
            vvod_tds, oper_vyvod_tds,  vvod_xcbr1_tsd, v_prom_pol_xcbr1_tsd, self.v_otkluchen_xcbr1_tsd, self.v_vkluchen_xcbr1_tsd, self.v_neisp_pol_xcbr1_tsd, v_otkluchit_rele_xcbr1_tsd, v_vkluchit_rele_xcbr1_tsd, ss_prev_vrem_per_ka, pusk_t_lvalh
        )

if __name__ == "__main__":
    part = SWITCH()
    res = part.Step(0, (0,0,0), 0,0,0,0,0,0,0,0,0,0,0,0,0)
    print(res)



            


