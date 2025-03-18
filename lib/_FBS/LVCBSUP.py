# ФБ Контроль силового выключателя (КСВ) (LVCBSUP)
# НЕ ПРОВЕРЕНО!!

#SGF1_rcbf1_lvcbsup - Ввод_функции - Ввод функции в работу (Не предусмотрено/ Предусмотрено)
#SGF2_rcbf1_lvcbsup - Бл_вкл_от_низ.ур.КИ - Блокировка включения низкого уровня контроля изоляции	(Не предусмотрено/ Предусмотрено)
#SGF3_rcbf1_lvcbsup - Бл_вкл_от_неисп_пол - Блокировка включения от неисправности положения В (Не предусмотрено/ Предусмотрено)
#SGF4_rcbf1_lvcbsup - Бл_вкл_от_прев_рес - Блокировка включения от превышения ресурса В (Не предусмотрено/ Предусмотрено)
#SGF5_rcbf1_lvcbsup - Контроль_ОТ_ЭМ - Контроль ОТ цепей ЭМВ, ЭМО1 и ЭМО2 (Не предусмотрено/ ЭМВ и ЭМО1/ ЭМВ, ЭМО1 и ЭМО2)
#SGF6_rcbf1_lvcbsup - Контроль_ЭМ - Контроль ЭМВ, ЭМО1 и ЭМО2 при формировании	неисправности цепей ЭМУ 	(Не предусмотрено/ ЭМВ и ЭМО1/ ЭМВ, ЭМО1 и ЭМО2)
#SGF7_rcbf1_lvcbsup - Контроль_сигн_ст - Контроль низкого уровня изоляции для работы аварийного уровня изоляции (Не предусмотрено/ Предусмотрено)
#SGF8_rcbf1_lvcbsup - Контроль_кнопки - Разрешение сброса "РФК" от кнопки (Не предусмотрено/ Предусмотрено)
#SGF9_rcbf1_lvcbsup - Бл_упр_от_ав.ур.КИ - Блокировка управления от аварийного уровня контроля изоляции	(Не предусмотрено/ Предусмотрено)


from lib._FUNCS.LVTRRCBF import LVTRRCBF # импортируем функцию КСВ

class LVCBSUP:
    def __init__(self, SGF1_rcbf1_lvcbsup, SGF2_rcbf1_lvcbsup, SGF3_rcbf1_lvcbsup, SGF4_rcbf1_lvcbsup, SGF5_rcbf1_lvcbsup, SGF6_rcbf1_lvcbsup, SGF7_rcbf1_lvcbsup, SGF8_rcbf1_lvcbsup, SGF9_rcbf1_lvcbsup, T1_rcbf1_lvcbsup, T2_rcbf1_lvcbsup, T3_rcbf1_lvcbsup):

        self.rcbf1 = LVTRRCBF(SGF1_rcbf1_lvcbsup, SGF2_rcbf1_lvcbsup, SGF3_rcbf1_lvcbsup, SGF4_rcbf1_lvcbsup, SGF5_rcbf1_lvcbsup, SGF6_rcbf1_lvcbsup, SGF7_rcbf1_lvcbsup, SGF8_rcbf1_lvcbsup, SGF9_rcbf1_lvcbsup, T1_rcbf1_lvcbsup, T2_rcbf1_lvcbsup, T3_rcbf1_lvcbsup)

    def Step(self, VYVOD, OV_rcbf1_lvcbsup, ot_emo1emv, ot_emo2, lovn_otkl, urov_nasebya, avar_isol_V, niz_isol_V, pruzh_ne_zaved, V_neispr_pol, V_otkl, V_vkl, Sbros, UV_otkl, otkl_ot_knopk, oper_otkl_V, KRV_resurs_V, vnesh_blok_upr_V, kontr_emv, kontr_emo1, kontr_emo2, rabota_emv, rabota_emo1, rabota_emo2):

        vvod_rcbf1_lvcbsup, oper_vyvod_rcbf1_lvcbsup, v_samoproisv_otkl_rcbf1_lvcbsup, neispr_V_rcbf1_lvcbsup, v_avar_otkl_rcbf1_lvcbsup, rfk_rcbf1_lvcbsup, blok_vkl_rcbf1_lvcbsup, blok_otkl_rcbf1_lvcbsup, neisp_emu_rcbf1_lvcbsup, zashita_emv_rcbf1_lvcbsup, zashita_emo1_rcbf1_lvcbsup, zashita_emo2_rcbf1_lvcbsup = self.rcbf1.Step(VYVOD, OV_rcbf1_lvcbsup, ot_emo1emv, ot_emo2, lovn_otkl, urov_nasebya, avar_isol_V, niz_isol_V, pruzh_ne_zaved, V_neispr_pol, V_otkl, V_vkl, Sbros, UV_otkl, otkl_ot_knopk, oper_otkl_V, KRV_resurs_V, vnesh_blok_upr_V, kontr_emv, kontr_emo1, kontr_emo2, rabota_emv, rabota_emo1, rabota_emo2)
        return vvod_rcbf1_lvcbsup, oper_vyvod_rcbf1_lvcbsup, v_samoproisv_otkl_rcbf1_lvcbsup, neispr_V_rcbf1_lvcbsup, v_avar_otkl_rcbf1_lvcbsup, rfk_rcbf1_lvcbsup, blok_vkl_rcbf1_lvcbsup, blok_otkl_rcbf1_lvcbsup, neisp_emu_rcbf1_lvcbsup, zashita_emv_rcbf1_lvcbsup, zashita_emo1_rcbf1_lvcbsup, zashita_emo2_rcbf1_lvcbsup

