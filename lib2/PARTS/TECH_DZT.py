# ЧАСТЬ СХЕМЫ ФСУ ДЛЯ ПРОВЕРКИ ГАЗОВЫХ И ТЕХНОЛОГИЧЕСКИХ ЗАЩИТ
# ИСПОЛНЕНИЯ ДЗТ2

from lib2.FBS.APTTECHLGC import APTTECHLGC # импорт ТЗ
from lib2.FBS.ALMTECHLGC_UIRZ import ALMTECHLGC_UIRZ # импорт ТС
from lib2.FBS.TALMGASLGC import TALMGASLGC
from lib2.FBS.TTRGASLGC import TTRGASLGC
from lib2.FBS.TLTCGASLGC import TLTCGASLGC

from lib2.FBS.TPRMOFFLVLGC import TPRMOFFLVLGC # импорт ЛО Т для ДЗТ
from lib2.FBS.DZT2_LVALH import DZT2_LVALH # импорт ПС
from lib2.FBS.DZT2_SignAssembly import DZT2_SignAssembly

#from lib._FBS.TOFFLVLGC import TOFFLVLGC # импорт ЛО Т
#from lib._FBS.T_SignAssembly import T_SignAssembly
#from lib._FBS.T_LVALH import T_LVALH # импорт ПС

class part_TECH:
    def __init__(self, SGF1_oilptrc1_apttechlgc, SGF2_oilptrc1_apttechlgc, SGF1_winptrc1_apttechlgc, SGF2_winptrc1_apttechlgc, SGF1_vlvptrc1_apttechlgc, SGF2_vlvptrc1_apttechlgc, T1_apttechlgc, SGF1_prvlvptrc1_almtechlgc, SGF1_shvlvptrc1_almtechlgc,SGF1_levptrc1_almtechlgc, SGF1_ptrc1_talmgaslgc, SGF2_ptrc1_talmgaslgc, T1_ptrc1_talmgaslgc, SGF1_ptrc1_ttrgaslgc, SGF2_ptrc1_ttrgaslgc, T1_ptrc1_ttrgaslgc, SGF1_ptrc1_tltcgaslgc, SGF2_ptrc1_tltcgaslgc, T1_ptrc1_tltcgaslgc,

    SGF1_ptrc1_tprmofflvlgc, SGF1_rbre1_tprmofflvlgc,

    SGF1_tsa, SGF2_tsa, SGF3_tsa, SGF4_tsa, SGF5_tsa, SGF6_tsa, SGF7_tsa, SGF8_tsa, SGF9_tsa, SGF10_tsa, SGF11_tsa, SGF12_tsa, SGF13_tsa,

    SGF1_lvalh, SGF2_lvalh, SGF3_lvalh, SGF4_lvalh, SGF5_lvalh, SGF6_lvalh, SGF7_lvalh, SGF8_lvalh, SGF9_lvalh, SGF10_lvalh, SGF11_lvalh, SGF12_lvalh, SGF13_lvalh
    ):
        # Инициализируем ФБ ТЗ       
        self.apttechlgc = APTTECHLGC(SGF1_oilptrc1_apttechlgc, SGF2_oilptrc1_apttechlgc, SGF1_winptrc1_apttechlgc, SGF2_winptrc1_apttechlgc, SGF1_vlvptrc1_apttechlgc, SGF2_vlvptrc1_apttechlgc, T1_apttechlgc)
        # Инициализируем ФБ ТС
        self.almtechlgc =  ALMTECHLGC_UIRZ(SGF1_prvlvptrc1_almtechlgc, SGF1_shvlvptrc1_almtechlgc,SGF1_levptrc1_almtechlgc)
        # Инициализируем ФБ ГЗ сигн
        self.talmgaslgc =  TALMGASLGC(SGF1_ptrc1_talmgaslgc, SGF2_ptrc1_talmgaslgc, T1_ptrc1_talmgaslgc)
        # Инициализируем ФБ ГЗ откл
        self.ttrgaslgc = TTRGASLGC(SGF1_ptrc1_ttrgaslgc, SGF2_ptrc1_ttrgaslgc, T1_ptrc1_ttrgaslgc)
        # Инициализируем ФБ ГЗ РПН
        self.tltcgaslgc = TLTCGASLGC(SGF1_ptrc1_tltcgaslgc, SGF2_ptrc1_tltcgaslgc, T1_ptrc1_tltcgaslgc)
        # Инициализируем ФБ ЛО Т  
        self.tprmofflvlgc = TPRMOFFLVLGC(SGF1_ptrc1_tprmofflvlgc, SGF1_rbre1_tprmofflvlgc)
        # Инициализируем СС
        self.tsa = DZT2_SignAssembly(SGF1_tsa, SGF2_tsa, SGF3_tsa, SGF4_tsa, SGF5_tsa, SGF6_tsa, SGF7_tsa, SGF8_tsa, SGF9_tsa, SGF10_tsa, SGF11_tsa, SGF12_tsa, SGF13_tsa)
        # ИНициализируем ПС
        self.lvalh = DZT2_LVALH(SGF1_lvalh, SGF2_lvalh, SGF3_lvalh, SGF4_lvalh, SGF5_lvalh, SGF6_lvalh, SGF7_lvalh, SGF8_lvalh, SGF9_lvalh, SGF10_lvalh, SGF11_lvalh, SGF12_lvalh, SGF13_lvalh)

    def Step(self, VYVOD, OV_tz, OV_dtm, OV_dto, OV_rd, NaSign_dtm, NaSign_dto, NaSign_rd, srabKontOtkl_m, srabKontSign_m, srabKontOtkl_o, srabKontSign_o, srabKontOtkl_rd, srabKI_m, srabKI_o, srabKI_rd, Sbros, OV_ts, OV_pk, OV_ok, OV_lev, NaSign_pk, NaSign_ok, NaSign_lev, srabKontOtkl_pk, srabKontOtkl_ok, srabKontOtkl_lev, OV_ptrc1_talmgaslgc, NaOtkl_ptrc1_talmgaslgc, srabKont_ptrc1_talmgaslgc, srabKI_ptrc1_talmgaslgc, OV_ptrc1_ttrgaslgc, NaSign_ptrc1_ttrgaslgc, srabKont_ptrc1_ttrgaslgc, srabKI_ptrc1_ttrgaslgc, OV_ptrc1_tltcgaslgc, NaSign_ptrc1_tltcgaslgc, srabKont_ptrc1_tltcgaslgc, srabKI_ptrc1_tltcgaslgc,

    OV_tprmofflvlgc, OV_ptrc1_tprmofflvlgc, OV_rbre1_tprmofflvlgc,

    oil_t_hi_level, oil_ltc_hi_level, oil_ltc_lo_level, oil_ltc_lo_temp, otkaz_so, neisp_so, vnesh_otk_zdz1, vnesh_otk_zdz2, vnesh_otk_urov1, vnesh_otk_urov2, vnesh_otkl_so
        ):
        # Вычисляем ТЗ
        vvod_oilptrc1_apttechlgc, oper_vyvod_oilptrc1_apttechlgc, srab_oilptrc1_apttechlgc, srabsign_oilptrc1_apttechlgc, zablok_oilptrc1_apttechlgc, ET_oilptrc1_apttechlgc, vvod_winptrc1_apttechlgc, oper_vyvod_winptrc1_apttechlgc, srab_winptrc1_apttechlgc, srabsign_winptrc1_apttechlgc, zablok_winptrc1_apttechlgc, ET_winptrc1_apttechlgc, vvod_vlvptrc1_apttechlgc, oper_vyvod_vlvptrc1_apttechlgc, srab_vlvptrc1_apttechlgc, srabsign_vlvptrc1_apttechlgc, zablok_vlvptrc1_apttechlgc, ET_vlvptrc1_apttechlgc = self.apttechlgc.Step(VYVOD, OV_tz, OV_dtm, OV_dto, OV_rd, NaSign_dtm, NaSign_dto, NaSign_rd, srabKontOtkl_m, srabKontSign_m, srabKontOtkl_o, srabKontSign_o, srabKontOtkl_rd, srabKI_m, srabKI_o, srabKI_rd, Sbros)
        # Вычисляем ТС
        vvod_prvlvptrc1_almtechlgc, oper_vyvod_prvlvptrc1_almtechlgc, srab_prvlvptrc1_almtechlgc, srabsign_prvlvptrc1_almtechlgc, vvod_shvlvptrc1_almtechlgc, oper_vyvod_shvlvptrc1_almtechlgc, srab_shvlvptrc1_almtechlgc, srabsign_shvlvptrc1_almtechlgc, vvod_levptrc1_almtechlgc, oper_vyvod_levptrc1_almtechlgc, srab_levptrc1_almtechlgc, srabsign_levptrc1_almtechlgc = self.almtechlgc.Step(VYVOD, OV_ts, OV_pk, OV_ok, OV_lev, NaSign_pk, NaSign_ok, NaSign_lev, srabKontOtkl_pk, srabKontOtkl_ok, srabKontOtkl_lev)
        # Вычисляем ГЗ сигн
        vvod_ptrc1_talmgaslgc, oper_vyvod_ptrc1_talmgaslgc, srab_ptrc1_talmgaslgc, srabsign_ptrc1_talmgaslgc, zablok_ptrc1_talmgaslgc, ET_ptrc1_talmgaslgc = self.talmgaslgc.Step(VYVOD, OV_ptrc1_talmgaslgc, NaOtkl_ptrc1_talmgaslgc, srabKont_ptrc1_talmgaslgc, srabKI_ptrc1_talmgaslgc, Sbros)
        # Вычисляем ГЗ откл
        OV_f = 0
        vvod_ptrc1_ttrgaslgc, oper_vyvod_ptrc1_ttrgaslgc, srab_ptrc1_ttrgaslgc, srabsign_ptrc1_ttrgaslgc, zablok_ptrc1_ttrgaslgc, ET_ptrc1_ttrgaslgc = self.ttrgaslgc.Step(VYVOD, OV_ptrc1_ttrgaslgc, OV_f, NaSign_ptrc1_ttrgaslgc, srabKont_ptrc1_ttrgaslgc, srabKI_ptrc1_ttrgaslgc, Sbros)
        # Вычисляем ГЗ РПН
        vvod_ptrc1_tltcgaslgc, oper_vyvod_ptrc1_tltcgaslgc, srab_ptrc1_tltcgaslgc, srabsign_ptrc1_tltcgaslgc, zablok_ptrc1_tltcgaslgc, ET_ptrc1_tltcgaslgc = self.tltcgaslgc.Step(VYVOD, OV_ptrc1_tltcgaslgc, OV_f, NaSign_ptrc1_tltcgaslgc, srabKont_ptrc1_tltcgaslgc, srabKI_ptrc1_tltcgaslgc, Sbros)
        # Собираем кортеж срабатываний
        signals_tprmofflvlgc = (srab_oilptrc1_apttechlgc, srab_winptrc1_apttechlgc, srab_vlvptrc1_apttechlgc, srab_prvlvptrc1_almtechlgc, srab_shvlvptrc1_almtechlgc, srab_levptrc1_almtechlgc, srab_ptrc1_talmgaslgc, srab_ptrc1_ttrgaslgc, srab_ptrc1_tltcgaslgc) 

        # вычисляем ЛО Т
        vvod_ptrc1_tprmofflvlgc, oper_vyvod_ptrc1_tprmofflvlgc, pusk_ptrc1_tprmofflvlgc, srab_ptrc1_tprmofflvlgc, vvod_rbre1_tprmofflvlgc, oper_vyvod_rbre1_tprmofflvlgc, zapret_rbre1_tprmofflvlgc = self.tprmofflvlgc.Step(VYVOD, OV_tprmofflvlgc, OV_ptrc1_tprmofflvlgc, signals_tprmofflvlgc, OV_rbre1_tprmofflvlgc)
        # вычисляем СС
        SS_gz_sign, SS_gz_nizk_isol, SS_gz_zablok, SS_tz_sign, SS_tz_nizk_isol, SS_tz_zablok, SS_ts_sign, SS_vnesh_otkl, SS_vyh_zepi_razobr, SS_bi_vyved, SS_ot_sign, SS_neispr_ot_gz, SS_neispr_ot_tz, SS_ot_nn_sign, SS_obsh_vnesh_sign = self.tsa.Step(VYVOD, gz_sign=(srabKont_ptrc1_talmgaslgc, srabKont_ptrc1_ttrgaslgc, srabKont_ptrc1_tltcgaslgc), gz_ki=(srabKI_ptrc1_talmgaslgc, srabKI_ptrc1_ttrgaslgc, srabKI_ptrc1_tltcgaslgc), gz_zablok=(zablok_ptrc1_talmgaslgc, zablok_ptrc1_ttrgaslgc, zablok_ptrc1_tltcgaslgc), tz_sign=(srabKontOtkl_m, srabKontSign_m, srabKontOtkl_o, srabKontSign_o, srabKontOtkl_rd), tz_ki=(srabKI_m, srabKI_o, srabKI_rd), tz_zablok=(zablok_oilptrc1_apttechlgc, zablok_winptrc1_apttechlgc, zablok_vlvptrc1_apttechlgc), ts_sign=(srabKontOtkl_pk, srabKontOtkl_ok, srabKontOtkl_lev, oil_t_hi_level, oil_ltc_hi_level, oil_ltc_lo_level, oil_ltc_lo_temp, otkaz_so, neisp_so), vnesh_otkl=(vnesh_otk_zdz1, vnesh_otk_zdz2, vnesh_otk_urov1, vnesh_otk_urov2, vnesh_otkl_so), Polozh_SA1=0, Polozh_SA2=0, Polozh_SA3=0, Polozh_SA4=0, Polozh_SG1=0, Polozh_SG2=0, Polozh_SG3=0, ot_gz=0, ot_tz=0, ot_zdz_nn1=0, ot_zdz_nn2=0, ot_urov_nn1=0, ot_urov_nn2=0, vnesh_sign=(0, 0, 0, 0))
        # вычисляем ПС
        pusk_lvalh = self.lvalh.Step(VYVOD, (srab_ptrc1_tprmofflvlgc, srabsign_ptrc1_talmgaslgc, srabsign_ptrc1_ttrgaslgc, srabsign_ptrc1_tltcgaslgc, srabsign_oilptrc1_apttechlgc, srabsign_winptrc1_apttechlgc, srabsign_vlvptrc1_apttechlgc, srabsign_prvlvptrc1_almtechlgc, srabsign_shvlvptrc1_almtechlgc, srabsign_levptrc1_almtechlgc), sgf1_sign = SS_gz_sign, sgf2_sign = SS_gz_nizk_isol, sgf3_sign = SS_gz_zablok, sgf4_sign = SS_tz_sign, sgf5_sign = SS_tz_nizk_isol, sgf6_sign = SS_tz_zablok, sgf7_sign = SS_ts_sign, sgf8_sign = SS_ot_sign, sgf9_sign = SS_ot_nn_sign, sgf10_sign = SS_vnesh_otkl, sgf11_sign = SS_vyh_zepi_razobr, sgf12_sign = SS_bi_vyved, sgf13_sign = SS_obsh_vnesh_sign)

        return (vvod_oilptrc1_apttechlgc, oper_vyvod_oilptrc1_apttechlgc, srab_oilptrc1_apttechlgc, srabsign_oilptrc1_apttechlgc, zablok_oilptrc1_apttechlgc, vvod_winptrc1_apttechlgc, oper_vyvod_winptrc1_apttechlgc, srab_winptrc1_apttechlgc, srabsign_winptrc1_apttechlgc, zablok_winptrc1_apttechlgc, vvod_vlvptrc1_apttechlgc, oper_vyvod_vlvptrc1_apttechlgc, srab_vlvptrc1_apttechlgc, srabsign_vlvptrc1_apttechlgc, zablok_vlvptrc1_apttechlgc,  vvod_prvlvptrc1_almtechlgc, oper_vyvod_prvlvptrc1_almtechlgc, srab_prvlvptrc1_almtechlgc, srabsign_prvlvptrc1_almtechlgc, vvod_shvlvptrc1_almtechlgc, oper_vyvod_shvlvptrc1_almtechlgc, srab_shvlvptrc1_almtechlgc, srabsign_shvlvptrc1_almtechlgc, vvod_levptrc1_almtechlgc, oper_vyvod_levptrc1_almtechlgc, srab_levptrc1_almtechlgc, srabsign_levptrc1_almtechlgc, vvod_ptrc1_talmgaslgc, oper_vyvod_ptrc1_talmgaslgc, srab_ptrc1_talmgaslgc, srabsign_ptrc1_talmgaslgc, zablok_ptrc1_talmgaslgc, vvod_ptrc1_ttrgaslgc, oper_vyvod_ptrc1_ttrgaslgc, srab_ptrc1_ttrgaslgc, srabsign_ptrc1_ttrgaslgc, zablok_ptrc1_ttrgaslgc, vvod_ptrc1_tltcgaslgc, oper_vyvod_ptrc1_tltcgaslgc, srab_ptrc1_tltcgaslgc, srabsign_ptrc1_tltcgaslgc, zablok_ptrc1_tltcgaslgc, 

        vvod_ptrc1_tprmofflvlgc, oper_vyvod_ptrc1_tprmofflvlgc, pusk_ptrc1_tprmofflvlgc, srab_ptrc1_tprmofflvlgc, vvod_rbre1_tprmofflvlgc, oper_vyvod_rbre1_tprmofflvlgc, zapret_rbre1_tprmofflvlgc,

        SS_gz_sign, SS_gz_nizk_isol, SS_gz_zablok, SS_tz_sign, SS_tz_nizk_isol, SS_tz_zablok, SS_ts_sign, SS_vnesh_otkl, SS_vyh_zepi_razobr, SS_bi_vyved, SS_ot_sign, SS_neispr_ot_gz, SS_neispr_ot_tz, SS_ot_nn_sign, SS_obsh_vnesh_sign,

        pusk_lvalh)
       

if __name__ == "__main__":
    part = part_TECH(SGF1=1)
    res = part.Step(0, (0,0,0), 0,0,0,0,0,0,0,0,0,0,0,0,0)
    print(res)



            


