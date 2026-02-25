# ФБ Контроллер присоединения (КП) (SWCTRL)
# НЕ ПРОВЕРЕНО!!

### SGF ###
# SGF1_swctrl - Ввод ФБ КП

#SGF1 - Ввод_функции - Ввод функции в работу (Не предусмотрено/ Предусмотренно)
#SGF2 - Бл_вкл_от_авар_откл - Блокировка включения от аварийного 		отключения В	(Не предусмотрено/ Предусмотрено)

#Т1 - Тперекл (Допустимое время переключения)
#Т2 - Тблк (Выдержка времени подавления выдачи положения "Не определено")


from lib2.FUNCS.LWCBCSWI import LWCBCSWI # импортируем функцию УВ из состава КП

class SWCTRL:
    def __init__(self, SGF1_swctrl, SGF1_cbcswi1_swctrl, SGF2_cbcswi1_swctrl, T1_cbcswi1_swctrl, T2_cbcswi1_swctrl, T3_cbcswi1_swctrl, T4_cbcswi1_swctrl):
        self.SGF1_swctrl = SGF1_swctrl
        self.cbcswi1 = LWCBCSWI(SGF1_cbcswi1_swctrl, SGF2_cbcswi1_swctrl, T1_cbcswi1_swctrl, T2_cbcswi1_swctrl, T3_cbcswi1_swctrl, T4_cbcswi1_swctrl)

    def Step(self, VYVOD, OV_swctrl, KSV_blk_otkl, otkl_v_ot_pu, otkl_v_ichm, mestnoe, otkl_v_ot_tu, otkl_v_asu, kluch_md_priv, vkl_v_ot_pu, vkl_v_ichm, distanz, vkl_v_ot_tu, vkl_v_asu, ksv_blok_vkl, ksv_v_avar_otkl, v_otkl_bk, v_vkl_bk):

        vvod_swctrl = (not(OV_swctrl or VYVOD)) and (self.SGF1_swctrl==1) # ФБ КП: Ввод
        oper_vyvod_swctrl = (OV_swctrl or VYVOD) and (self.SGF1_swctrl==1) # ФБ КП: Оперативный вывод

        vvod_cbcswi1_swctrl, uv_otkluchit_cbcswi1_swctrl, uv_idet_per_cbcswi1_swctrl, uv_prev_vrem_per_cbcswi1_swctrl, uv_vkluchit_cbcswi1_swctrl, uv_ne_opredeleno_cbcswi1_swctrl, uv_otklucheno_cbcswi1_swctrl, uv_vklucheno_cbcswi1_swctrl, uv_neispr_neopred_cbcswi1_swctrl = self.cbcswi1.Step(vvod_swctrl, KSV_blk_otkl, otkl_v_ot_pu, otkl_v_ichm, mestnoe, otkl_v_ot_tu, otkl_v_asu, kluch_md_priv, vkl_v_ot_pu, vkl_v_ichm, distanz, vkl_v_ot_tu, vkl_v_asu, ksv_blok_vkl, ksv_v_avar_otkl, v_otkl_bk, v_vkl_bk)

        return vvod_swctrl, oper_vyvod_swctrl, vvod_cbcswi1_swctrl, uv_otkluchit_cbcswi1_swctrl, uv_idet_per_cbcswi1_swctrl, uv_prev_vrem_per_cbcswi1_swctrl, uv_vkluchit_cbcswi1_swctrl, uv_ne_opredeleno_cbcswi1_swctrl, uv_otklucheno_cbcswi1_swctrl, uv_vklucheno_cbcswi1_swctrl, uv_neispr_neopred_cbcswi1_swctrl

if __name__ == "__main__":
    fb = SWCTRL()
    res = fb.Step(0,0,0,0)
    print(res)