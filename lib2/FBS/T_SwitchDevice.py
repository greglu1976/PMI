# ФБ (T_SwitchDevice) КА - Коммутационные аппараты (в составе устройства ЮНИТ-М3-Т)
# НЕ ПРОВЕРЕНО!!

### SGF ###
# SGF1_tsd - Ввод ФБ КА
# SGF1_xcbr1_tsd - Ввод_функции - Ввод функции в работу	(Не предусмотрено/ Предусмотрено)
# SGF2_xcbr1_tsd - Режим_откл - Режим отключения выключателя (Длительный/ Импульсный)
# SGF3_xcbr1_tsd - Контр_раб_ЭМО - Контроль работы ЭМО 	(Не предусмотрено/ Предусмотрено)
# SGF4_xcbr1_tsd - Режим_вкл - Режим включения выключателя 	(Длительный/ Импульсный)
# SGF5_xcbr1_tsd - Контр_раб_ЭМВ - Контроль работы ЭМВ 	(Не предусмотрено/ Предусмотрено)
# SGF6_xcbr1_tsd - Блок_откл_от_КСВ - Блокировка отключения от КСВ	(Не предусмотрено/ Предусмотрено)

from lib2.FUNCS.LVCBXCBR import LVCBXCBR # импортируем функцию В

class T_Switch_Device:
    def __init__(self, SGF1_tsd, SGF1_xcbr1_tsd, SGF2_xcbr1_tsd, SGF3_xcbr1_tsd, SGF4_xcbr1_tsd, SGF5_xcbr1_tsd, T1_xcbr1_tsd, T2_xcbr1_tsd, T3_xcbr1_tsd, T4_xcbr1_tsd):
        self.SGF1_tsd = SGF1_tsd
        self.xcbr1 = LVCBXCBR(SGF1_xcbr1_tsd, SGF2_xcbr1_tsd, SGF3_xcbr1_tsd, SGF4_xcbr1_tsd, SGF5_xcbr1_tsd, T1_xcbr1_tsd, T2_xcbr1_tsd, T3_xcbr1_tsd, T4_xcbr1_tsd)

    def Step(self, VYVOD, OV_tsd, v_otkl_bk, v_vkl_bk, kp_uv_otkluchit, lovn_lo_otkl_avar, urov_nasebya, oper_otkl_v, ksv_blok_otkl, rabota_emo1, rabota_emo2, sbros, kp_uv_vkluchit, uv_uv_vkluchit, rabota_emv):

        vvod_tds = (not(OV_tsd or VYVOD)) and (self.SGF1_tsd==1) # ФБ КА: Ввод
        oper_vyvod_tds = (OV_tsd or VYVOD) and (self.SGF1_tsd==1) # ФБ КА: Оперативный вывод

        vvod_xcbr1_tsd, v_prom_pol_xcbr1_tsd, v_otkluchen_xcbr1_tsd, v_vkluchen_xcbr1_tsd, v_neisp_pol_xcbr1_tsd, v_otkluchit_rele_xcbr1_tsd, v_vkluchit_rele_xcbr1_tsd = self.xcbr1.Step(vvod_tds, v_otkl_bk, v_vkl_bk, kp_uv_otkluchit, lovn_lo_otkl_avar, urov_nasebya, oper_otkl_v, ksv_blok_otkl, rabota_emo1, rabota_emo2, sbros, kp_uv_vkluchit, uv_uv_vkluchit, rabota_emv)

        return vvod_tds, oper_vyvod_tds,  vvod_xcbr1_tsd, v_prom_pol_xcbr1_tsd, v_otkluchen_xcbr1_tsd, v_vkluchen_xcbr1_tsd, v_neisp_pol_xcbr1_tsd, v_otkluchit_rele_xcbr1_tsd, v_vkluchit_rele_xcbr1_tsd

if __name__ == "__main__":
    fb = T_Switch_Device(SGF1=1, T1=0)
    res = fb.Step(0,0,0,0)
    print(res)