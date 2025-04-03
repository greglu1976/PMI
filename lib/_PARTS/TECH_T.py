# ЧАСТЬ СХЕМЫ ФСУ ДЛЯ ПРОВЕРКИ ГАЗОВЫХ И ТЕХНОЛОГИЧЕСКИХ ЗАЩИТ
# ИСПОЛНЕНИЯ Т

from lib._FBS.APTTECHLGC import APTTECHLGC # импорт ТЗ
from lib._FBS.ALMTECHLGC_UIRZ import ALMTECHLGC_UIRZ # импорт ТС
from lib._FBS.TALMGASLGC import TALMGASLGC
from lib._FBS.TTRGASLGC import TTRGASLGC
from lib._FBS.TLTCGASLGC import TLTCGASLGC
from lib._FBS.TOFFLVLGC import TOFFLVLGC # импорт ЛО Т
from lib._FBS.T_SignAssembly import T_SignAssembly
from lib._FBS.T_LVALH import T_LVALH # импорт ПС

class part_TECH_T:
    def __init__(self, SGF1_oilptrc1_apttechlgc, SGF2_oilptrc1_apttechlgc, SGF1_winptrc1_apttechlgc, SGF2_winptrc1_apttechlgc, SGF1_vlvptrc1_apttechlgc, SGF2_vlvptrc1_apttechlgc, T1_apttechlgc, SGF1_prvlvptrc1_almtechlgc, SGF1_shvlvptrc1_almtechlgc,SGF1_levptrc1_almtechlgc, SGF1_ptrc1_talmgaslgc, SGF2_ptrc1_talmgaslgc, T1_ptrc1_talmgaslgc, SGF1_ptrc1_ttrgaslgc, SGF2_ptrc1_ttrgaslgc, T1_ptrc1_ttrgaslgc, SGF1_ptrc1_tltcgaslgc, SGF2_ptrc1_tltcgaslgc, T1_ptrc1_tltcgaslgc, SGF1_ptrc1_tofflvlgc, SGF1_rbre1_tofflvlgc, SGF2_rbre1_tofflvlgc, SGF3_rbre1_tofflvlgc, SGF1_rblc1_tofflvlgc, SGF2_rblc1_tofflvlgc, SGF3_rblc1_tofflvlgc, SGF1_t_lvalh, SGF2_t_lvalh, SGF3_t_lvalh, SGF4_t_lvalh, SGF5_t_lvalh, SGF6_t_lvalh, SGF7_t_lvalh, SGF8_t_lvalh, SGF9_t_lvalh, SGF10_t_lvalh, SGF11_t_lvalh, SGF12_t_lvalh, SGF13_t_lvalh, SGF14_t_lvalh, SGF1_t_signassembly, SGF2_t_signassembly, SGF3_t_signassembly, SGF4_t_signassembly, SGF5_t_signassembly, SGF6_t_signassembly, SGF7_t_signassembly, SGF8_t_signassembly, SGF9_t_signassembly, SGF10_t_signassembly, SGF11_t_signassembly, SGF12_t_signassembly, SGF13_t_signassembly):
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
        self.tofflvlgc = TOFFLVLGC(SGF1_ptrc1_tofflvlgc, SGF1_rbre1_tofflvlgc, SGF2_rbre1_tofflvlgc, SGF3_rbre1_tofflvlgc, SGF1_rblc1_tofflvlgc, SGF2_rblc1_tofflvlgc, SGF3_rblc1_tofflvlgc)
        # Инициализируем СС
        self.t_signassembly = T_SignAssembly(SGF1_t_signassembly, SGF2_t_signassembly, SGF3_t_signassembly, SGF4_t_signassembly, SGF5_t_signassembly, SGF6_t_signassembly, SGF7_t_signassembly, SGF8_t_signassembly, SGF9_t_signassembly, SGF10_t_signassembly, SGF11_t_signassembly, SGF12_t_signassembly, SGF13_t_signassembly)
        # ИНициализируем ПС
        self.lvalv = T_LVALH(SGF1_t_lvalh, SGF2_t_lvalh, SGF3_t_lvalh, SGF4_t_lvalh, SGF5_t_lvalh, SGF6_t_lvalh, SGF7_t_lvalh, SGF8_t_lvalh, SGF9_t_lvalh, SGF10_t_lvalh, SGF11_t_lvalh, SGF12_t_lvalh, SGF13_t_lvalh, SGF14_t_lvalh)

    def Step(self, VYVOD, OV_tz, OV_dtm, OV_dto, OV_rd, NaSign_dtm, NaSign_dto, NaSign_rd, srabKontOtkl_m, srabKontSign_m, srabKontOtkl_o, srabKontSign_o, srabKontOtkl_rd, srabKI_m, srabKI_o, srabKI_rd, Sbros, OV_ts, OV_pk, OV_ok, OV_lev, NaSign_pk, NaSign_ok, NaSign_lev, srabKontOtkl_pk, srabKontOtkl_ok, srabKontOtkl_lev, OV_ptrc1_talmgaslgc, NaOtkl_ptrc1_talmgaslgc, srabKont_ptrc1_talmgaslgc, srabKI_ptrc1_talmgaslgc, OV_ptrc1_ttrgaslgc, NaSign_ptrc1_ttrgaslgc, srabKont_ptrc1_ttrgaslgc, srabKI_ptrc1_ttrgaslgc, OV_ptrc1_tltcgaslgc, NaSign_ptrc1_tltcgaslgc, srabKont_ptrc1_tltcgaslgc, srabKI_ptrc1_tltcgaslgc, OV_tofflvlg, OVlo_tofflvlg, OVzapv_tofflvlg, OVzavr_tofflvlg, oil_t_hi_level, oil_ltc_hi_level, oil_ltc_lo_level, oil_ltc_lo_temp
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
        signals_tofflvlg = (srab_oilptrc1_apttechlgc, srab_winptrc1_apttechlgc, srab_vlvptrc1_apttechlgc, srab_prvlvptrc1_almtechlgc, srab_shvlvptrc1_almtechlgc, srab_levptrc1_almtechlgc, srab_ptrc1_talmgaslgc, srab_ptrc1_ttrgaslgc, srab_ptrc1_tltcgaslgc) 
        # Зануляем сраб МТЗ, здесь не требуется - а передать значения нужно
        mtz2_srab_tofflvlg=0
        mtz3_srab_tofflvlg=0
        # вычисляем ЛО Т
        vvod_ptrc1_tofflvlgc, oper_vyvod_ptrc1_tofflvlgc, pusk_ptrc1_tofflvlgc, srab_ptrc1_tofflvlgc, vvod_rblc1_tofflvlgc, oper_vyvod_rblc1_tofflvlgc, zapret_rblc1_tofflvlgc, vvod_rbre1_tofflvlgc, oper_vyvod_rbre1_tofflvlgc, zapret_rbre1_tofflvlgc = self.tofflvlgc.Step(VYVOD, OV_tofflvlg, OVlo_tofflvlg, signals_tofflvlg, mtz2_srab_tofflvlg, mtz3_srab_tofflvlg, OVzapv_tofflvlg, OVzavr_tofflvlg)
        # вычисляем СС       
        SS_gz_sign, SS_gz_zablok, SS_gz_nizk_isol, SS_tz_sign, SS_tz_nizk_isol, SS_tz_zablok, SS_ts_sign, SS_vnesh_otkl, SS_vyh_zepi_razobr, SS_bi_vyved, SS_ot_sign, SS_neispr_ot_gz,  SS_neispr_ot_tz, SS_neispr_ot_v, SS_ot_nn_sign, SS_prev_vrem_per_ka, SS_obsh_vnesh_sign = self.t_signassembly.Step(VYVOD, (srabKont_ptrc1_talmgaslgc, srabKont_ptrc1_ttrgaslgc, srabKont_ptrc1_tltcgaslgc), (zablok_ptrc1_talmgaslgc, zablok_ptrc1_ttrgaslgc, zablok_ptrc1_tltcgaslgc), (srabKI_ptrc1_talmgaslgc, srabKI_ptrc1_ttrgaslgc, srabKI_ptrc1_tltcgaslgc), (srabKontOtkl_m, srabKontSign_m, srabKontOtkl_o, srabKontSign_o, srabKontOtkl_rd), (srabKI_m, srabKI_o, srabKI_rd), (zablok_oilptrc1_apttechlgc, zablok_winptrc1_apttechlgc, zablok_vlvptrc1_apttechlgc), (srabKontOtkl_pk, srabKontOtkl_ok, srabKontOtkl_lev, oil_t_hi_level, oil_ltc_hi_level, oil_ltc_lo_level, oil_ltc_lo_temp), (0, 0), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, (0,), (0,)) # Обнулили контроль SA SG и пр. Здесь не проверяются эти цепи
        # вычисляем ПС
        pusk_lvalv = self.lvalv.Step(VYVOD, (srabsign_ptrc1_talmgaslgc, srabsign_ptrc1_ttrgaslgc, srabsign_ptrc1_tltcgaslgc, srabsign_oilptrc1_apttechlgc, srabsign_winptrc1_apttechlgc, srabsign_vlvptrc1_apttechlgc, srabsign_prvlvptrc1_almtechlgc, srabsign_shvlvptrc1_almtechlgc, srabsign_levptrc1_almtechlgc), SS_gz_sign, SS_gz_nizk_isol, SS_gz_zablok, SS_tz_sign, SS_tz_nizk_isol, SS_tz_zablok, SS_ts_sign, SS_ot_sign, SS_ot_nn_sign, SS_vnesh_otkl, SS_vyh_zepi_razobr, SS_bi_vyved, SS_prev_vrem_per_ka, SS_obsh_vnesh_sign)

        return (vvod_oilptrc1_apttechlgc, oper_vyvod_oilptrc1_apttechlgc, srab_oilptrc1_apttechlgc, srabsign_oilptrc1_apttechlgc, zablok_oilptrc1_apttechlgc, ET_oilptrc1_apttechlgc, vvod_winptrc1_apttechlgc, oper_vyvod_winptrc1_apttechlgc, srab_winptrc1_apttechlgc, srabsign_winptrc1_apttechlgc, zablok_winptrc1_apttechlgc, ET_winptrc1_apttechlgc, vvod_vlvptrc1_apttechlgc, oper_vyvod_vlvptrc1_apttechlgc, srab_vlvptrc1_apttechlgc, srabsign_vlvptrc1_apttechlgc, zablok_vlvptrc1_apttechlgc, ET_vlvptrc1_apttechlgc, vvod_prvlvptrc1_almtechlgc, oper_vyvod_prvlvptrc1_almtechlgc, srab_prvlvptrc1_almtechlgc, srabsign_prvlvptrc1_almtechlgc, vvod_shvlvptrc1_almtechlgc, oper_vyvod_shvlvptrc1_almtechlgc, srab_shvlvptrc1_almtechlgc, srabsign_shvlvptrc1_almtechlgc, vvod_levptrc1_almtechlgc, oper_vyvod_levptrc1_almtechlgc, srab_levptrc1_almtechlgc, srabsign_levptrc1_almtechlgc, vvod_ptrc1_talmgaslgc, oper_vyvod_ptrc1_talmgaslgc, srab_ptrc1_talmgaslgc, srabsign_ptrc1_talmgaslgc, zablok_ptrc1_talmgaslgc, ET_ptrc1_talmgaslgc, vvod_ptrc1_ttrgaslgc, oper_vyvod_ptrc1_ttrgaslgc, srab_ptrc1_ttrgaslgc, srabsign_ptrc1_ttrgaslgc, zablok_ptrc1_ttrgaslgc, ET_ptrc1_ttrgaslgc, vvod_ptrc1_tltcgaslgc, oper_vyvod_ptrc1_tltcgaslgc, srab_ptrc1_tltcgaslgc, srabsign_ptrc1_tltcgaslgc, zablok_ptrc1_tltcgaslgc, ET_ptrc1_tltcgaslgc, vvod_ptrc1_tofflvlgc, oper_vyvod_ptrc1_tofflvlgc, pusk_ptrc1_tofflvlgc, srab_ptrc1_tofflvlgc, vvod_rblc1_tofflvlgc, oper_vyvod_rblc1_tofflvlgc, zapret_rblc1_tofflvlgc, vvod_rbre1_tofflvlgc, oper_vyvod_rbre1_tofflvlgc, zapret_rbre1_tofflvlgc, SS_gz_sign, SS_gz_zablok, SS_gz_nizk_isol, SS_tz_sign, SS_tz_nizk_isol, SS_tz_zablok, SS_ts_sign, SS_vnesh_otkl, SS_vyh_zepi_razobr, SS_bi_vyved, SS_ot_sign, SS_neispr_ot_gz,  SS_neispr_ot_tz, SS_neispr_ot_v, SS_ot_nn_sign, SS_prev_vrem_per_ka, SS_obsh_vnesh_sign, pusk_lvalv)
       

if __name__ == "__main__":
    part = part_TECH_T(SGF1=1)
    res = part.Step(0, (0,0,0), 0,0,0,0,0,0,0,0,0,0,0,0,0)
    print(res)



            


