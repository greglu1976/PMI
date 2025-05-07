# ЧАСТЬ СХЕМЫ ФСУ ДЛЯ ПРОВЕРКИ ЛО, УРОВ, ПС, СС
# ИСПОЛНЕНИЯ ДЗТ2

# Проверяемые функции
from lib._FBS.HVTCBOFF import HVTCBOFF # импорт ФБ ЛО ВН
from lib._FBS.LVTCBOFF_DZT import LVTCBOFF # импорт ЛО НН
from lib._FBS.TPBRF_DZT import TPBRF # импорт ФБ УРОВ

# Вспомогательные функции
from lib._FBS.TPRMOFFLVLGC import TPRMOFFLVLGC # импорт ЛО Т для ДЗТ
from lib._FBS.DZT2_LVALH import DZT2_LVALH # импорт ПС
from lib._FBS.DZT2_SignAssembly import DZT2_SignAssembly

class part_LO:
    def __init__(self,
        # УРОВ   
        SGF1_rbrf1_tpbrf, SGF2_rbrf1_tpbrf, SGF3_rbrf1_tpbrf, SGF4_rbrf1_tpbrf, T1_rbrf1_tpbrf, Iset_rbrf1_tpbrf,
        # ЛО Т 
        SGF1_ptrc1_tprmofflvlgc, SGF1_rbre1_tprmofflvlgc, 
        # ЛО ВН
        SGF1_hvcbptrc1_hvtcboff, T1_hvcbptrc1_hvtcboff,
        # ЛО НН1
        SGF1_lvcbptrc1_lvtcboff1, T1_lvcbptrc1_lvtcboff1, SGF1_lvcbrecrbre1_lvtcboff1,
        # ЛО НН2
        SGF1_lvcbptrc1_lvtcboff2, T1_lvcbptrc1_lvtcboff2, SGF1_lvcbrecrbre1_lvtcboff2,      
        # СС
        SGF1_tsa, SGF2_tsa, SGF3_tsa, SGF4_tsa, SGF5_tsa, SGF6_tsa, SGF7_tsa, SGF8_tsa, SGF9_tsa, SGF10_tsa, SGF11_tsa, SGF12_tsa, SGF13_tsa,
        # ПС
        SGF1_lvalh, SGF2_lvalh, SGF3_lvalh, SGF4_lvalh, SGF5_lvalh, SGF6_lvalh, SGF7_lvalh, SGF8_lvalh, SGF9_lvalh, SGF10_lvalh, SGF11_lvalh, SGF12_lvalh, SGF13_lvalh
        ):

        Inom = 5    
        # Инициализируем ФБ УРОВ
        self.tpbrf = TPBRF(SGF1_rbrf1_tpbrf, SGF2_rbrf1_tpbrf, SGF3_rbrf1_tpbrf, SGF4_rbrf1_tpbrf, T1_rbrf1_tpbrf, Iset_rbrf1_tpbrf*Inom)

        # Инициализируем ФБ ЛО Т       
        self.tprmofflvlgc = TPRMOFFLVLGC(SGF1_ptrc1_tprmofflvlgc, SGF1_rbre1_tprmofflvlgc)

        # Инициализируем ФБ ЛО ВН
        self.hvtcboff = HVTCBOFF(SGF1_hvcbptrc1_hvtcboff, T1_hvcbptrc1_hvtcboff)

        # Инициализируем ФБ ЛО НН1   
        self.lvtcboff1 = LVTCBOFF(SGF1_lvcbptrc1_lvtcboff1, T1_lvcbptrc1_lvtcboff1, SGF1_lvcbrecrbre1_lvtcboff1)

        # Инициализируем ФБ ЛО НН2
        self.lvtcboff2 = LVTCBOFF(SGF1_lvcbptrc1_lvtcboff2, T1_lvcbptrc1_lvtcboff2, SGF1_lvcbrecrbre1_lvtcboff2)

        # Инициализируем СС
        self.tsa = DZT2_SignAssembly(SGF1_tsa, SGF2_tsa, SGF3_tsa, SGF4_tsa, SGF5_tsa, SGF6_tsa, SGF7_tsa, SGF8_tsa, SGF9_tsa, SGF10_tsa, SGF11_tsa, SGF12_tsa, SGF13_tsa)

        # ИНициализируем ПС
        self.lvalh = DZT2_LVALH(SGF1_lvalh, SGF2_lvalh, SGF3_lvalh, SGF4_lvalh, SGF5_lvalh, SGF6_lvalh, SGF7_lvalh, SGF8_lvalh, SGF9_lvalh, SGF10_lvalh, SGF11_lvalh, SGF12_lvalh, SGF13_lvalh)

    def Step(self, VYVOD,
        # для ЛО Т
        vnesh_otkl_ot_so,
        OV_tprmofflvlgc, OV_ptrc1_tprmofflvlgc, OV_rbre1_tprmofflvlgc,
        # для ЛО ВН
        OV_hvcbptrc1_hvtcboff, vnesh_otkl_zdz1, vnesh_otkl_zdz2, vnesh_otkl_urov1, vnesh_otkl_urov2, 
        # для ЛО НН1
        OV_lvtcboff1, OV_lvcbptrc1_lvtcboff1, OV_lvcbrecrbre1_lvtcboff1,
        # для ЛО НН2
        OV_lvtcboff2, OV_lvcbptrc1_lvtcboff2, OV_lvcbrecrbre1_lvtcboff2,
        # для УРОВ
        OV_rbrf1_tpbrf, pusk_urov_vnesh, IA, IB, IC,
        # для CC
        Polozh_SA1, Polozh_SA2, Polozh_SA3, Polozh_SA4, Polozh_SG1, Polozh_SG2, Polozh_SG3, ot_gz, ot_tz, ot_zdz_nn1, ot_zdz_nn2, ot_urov_nn1, ot_urov_nn2, vnesh_sign1, vnesh_sign2,vnesh_sign3, vnesh_sign4 
        ):

        # кортеж срабатываний, здесь только одно - внешнее откл. от СО   
        signals_tprmofflvlgc = (vnesh_otkl_ot_so, 0)
        # вычисляем ЛО Т
        vvod_ptrc1_tprmofflvlgc, oper_vyvod_ptrc1_tprmofflvlgc, pusk_ptrc1_tprmofflvlgc, srab_ptrc1_tprmofflvlgc, vvod_rbre1_tprmofflvlgc, oper_vyvod_rbre1_tprmofflvlgc, zapret_rbre1_tprmofflvlgc = self.tprmofflvlgc.Step(VYVOD, OV_tprmofflvlgc, OV_ptrc1_tprmofflvlgc, signals_tprmofflvlgc, OV_rbre1_tprmofflvlgc)

        # вычисляем ЛО ВН 
        vnesh_otkl_zdz = vnesh_otkl_zdz1 or vnesh_otkl_zdz2
        vnesh_otkl_urov = vnesh_otkl_urov1 or vnesh_otkl_urov2
        vvod_hvcbptrc1_hvtcboff, oper_vyvod_hvcbptrc1_hvtcboff, otkl_hvcbptrc1_hvtcboff, otkl_avar_hvcbptrc1_hvtcboff = self.hvtcboff.Step(VYVOD, OV_hvcbptrc1_hvtcboff, srab_ptrc1_tprmofflvlgc, vnesh_otkl_zdz, vnesh_otkl_urov)

        # вычисляем ЛО НН1  
        vvod_lvcbptrc1_lvtcboff1, oper_vyvod_lvcbptrc1_lvtcboff1, otkl_lvcbptrc1_lvtcboff1, otkl_avar_lvcbptrc1_lvtcboff1, vvod_lvcbrecrbre1_lvtcboff1, oper_vyvod_lvcbrecrbre1_lvtcboff1, zapret_lvcbrecrbre1_lvtcboff1 = self.lvtcboff1.Step(VYVOD, OV_lvtcboff1, OV_lvcbptrc1_lvtcboff1, OV_lvcbrecrbre1_lvtcboff1, srab_ptrc1_tprmofflvlgc, zapret_rbre1_tprmofflvlgc)

        # вычисляем ЛО НН2  
        vvod_lvcbptrc1_lvtcboff2, oper_vyvod_lvcbptrc1_lvtcboff2, otkl_lvcbptrc1_lvtcboff2, otkl_avar_lvcbptrc1_lvtcboff2, vvod_lvcbrecrbre1_lvtcboff2, oper_vyvod_lvcbrecrbre1_lvtcboff2, zapret_lvcbrecrbre1_lvtcboff2 = self.lvtcboff2.Step(VYVOD, OV_lvtcboff2, OV_lvcbptrc1_lvtcboff2, OV_lvcbrecrbre1_lvtcboff2, srab_ptrc1_tprmofflvlgc, zapret_rbre1_tprmofflvlgc)

        # вычисляем УРОВ
        vvod_rbrf1_tpbrf, oper_vyvod_rbrf1_tpbrf, srab_rbrf1_tpbrf, pusk_rbrf1_tpbrf, io_rbrf1_tpbrf, srab_na_sebya_rbrf1_tpbrf = self.tpbrf.Step(VYVOD, OV_rbrf1_tpbrf, otkl_hvcbptrc1_hvtcboff, pusk_urov_vnesh, IA, IB, IC)

        # вычисляем СС
        SS_gz_sign, SS_gz_nizk_isol, SS_gz_zablok, SS_tz_sign, SS_tz_nizk_isol, SS_tz_zablok, SS_ts_sign, SS_vnesh_otkl, SS_vyh_zepi_razobr, SS_bi_vyved, SS_ot_sign, SS_neispr_ot_gz, SS_neispr_ot_tz, SS_ot_nn_sign, SS_obsh_vnesh_sign = self.tsa.Step(VYVOD, gz_sign=(0,), gz_ki=(0,), gz_zablok=(0,), tz_sign=(0,), tz_ki=(0,), tz_zablok=(0,), ts_sign=(0,), vnesh_otkl=(0,), Polozh_SA1=Polozh_SA1, Polozh_SA2=Polozh_SA2, Polozh_SA3=Polozh_SA3, Polozh_SA4=Polozh_SA4, Polozh_SG1=Polozh_SG1, Polozh_SG2=Polozh_SG2, Polozh_SG3=Polozh_SG3, ot_gz=ot_gz, ot_tz=ot_tz, ot_zdz_nn1=ot_zdz_nn1, ot_zdz_nn2=ot_zdz_nn2, ot_urov_nn1=ot_urov_nn1, ot_urov_nn2=ot_urov_nn2, vnesh_sign=(vnesh_sign1, vnesh_sign2,vnesh_sign3,vnesh_sign4))

        # вычисляем ПС
        pusk_lvalh = self.lvalh.Step(VYVOD, (srab_ptrc1_tprmofflvlgc, srab_rbrf1_tpbrf, srab_na_sebya_rbrf1_tpbrf), sgf1_sign = SS_gz_sign, sgf2_sign = SS_gz_nizk_isol, sgf3_sign = SS_gz_zablok, sgf4_sign = SS_tz_sign, sgf5_sign = SS_tz_nizk_isol, sgf6_sign = SS_tz_zablok, sgf7_sign = SS_ts_sign, sgf8_sign = SS_ot_sign, sgf9_sign = SS_ot_nn_sign, sgf10_sign = SS_vnesh_otkl, sgf11_sign = SS_vyh_zepi_razobr, sgf12_sign = SS_bi_vyved, sgf13_sign = SS_obsh_vnesh_sign)

        return (vvod_ptrc1_tprmofflvlgc, oper_vyvod_ptrc1_tprmofflvlgc, pusk_ptrc1_tprmofflvlgc, srab_ptrc1_tprmofflvlgc, vvod_rbre1_tprmofflvlgc, oper_vyvod_rbre1_tprmofflvlgc, zapret_rbre1_tprmofflvlgc,
        vvod_hvcbptrc1_hvtcboff, oper_vyvod_hvcbptrc1_hvtcboff, otkl_hvcbptrc1_hvtcboff, otkl_avar_hvcbptrc1_hvtcboff,
        vvod_lvcbptrc1_lvtcboff1, oper_vyvod_lvcbptrc1_lvtcboff1, otkl_lvcbptrc1_lvtcboff1, otkl_avar_lvcbptrc1_lvtcboff1, vvod_lvcbrecrbre1_lvtcboff1, oper_vyvod_lvcbrecrbre1_lvtcboff1, zapret_lvcbrecrbre1_lvtcboff1,
        vvod_lvcbptrc1_lvtcboff2, oper_vyvod_lvcbptrc1_lvtcboff2, otkl_lvcbptrc1_lvtcboff2, otkl_avar_lvcbptrc1_lvtcboff2, vvod_lvcbrecrbre1_lvtcboff2, oper_vyvod_lvcbrecrbre1_lvtcboff2, zapret_lvcbrecrbre1_lvtcboff2,
        vvod_rbrf1_tpbrf, oper_vyvod_rbrf1_tpbrf, srab_rbrf1_tpbrf, pusk_rbrf1_tpbrf, io_rbrf1_tpbrf, srab_na_sebya_rbrf1_tpbrf,
        SS_gz_sign, SS_gz_nizk_isol, SS_gz_zablok, SS_tz_sign, SS_tz_nizk_isol, SS_tz_zablok, SS_ts_sign, SS_vnesh_otkl, SS_vyh_zepi_razobr, SS_bi_vyved, SS_ot_sign, SS_neispr_ot_gz, SS_neispr_ot_tz, SS_ot_nn_sign, SS_obsh_vnesh_sign,
        pusk_lvalh
        )
       

if __name__ == "__main__":
    part = part_LO(SGF1=1)
    res = part.Step()
    print(res)



            


