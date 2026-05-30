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

    def Step(self, DI_ControllerDisable, DI_APTTECHLGC, DI_OILPTRC, DI_WINPTRC, DI_VLVPTRC, DI_OILPTRC_Sign, DI_WINPTRC_Sign, DI_VLVPTRC_Sign, OILTempEmerg, OILTempHigh, WINTempEmerg, WINTempHigh, VLVop, OILIsolOp, WINIsolOp, VLVIsolOp, Reset, DI_ALMTECHLGC, DI_PRVLVPTRC1, DI_SHVLVPTRC1, DI_LEVPTRC1, DI_PRVLVPTRC1_Sign, DI_SHVLVPTRC1_Sign, DI_LEVPTRC1_Sign, PRVLVOp, SHVLVOp, LowOILLevel, DI_TALMGASLGC, DI_TALMGASLGC_Sign, SignContact, GASSignIsolOp, DI_TTRGASLGC, DI_TTRGASLGC_Sign, TripContact, GASTripIsolOp, DI_TLTCGASLGC, DI_TLTCGASLGC_Sign, JetRelayContact, GASLTCIsolOp,

    DI_TPRMOFFLVLGC, DI_TJNTPTRC, DI_JNTRBRE,

    HighOILLevel, HighOILLevelLTC, LowOILLevelLTC, OILTempLowLTC, FailCoolSys, ProblemCoolSys, OpExtOfARC_NN1, OpExtOfARC_NN2, OpExtOfCBFP_NN1, OpExtOfCBFP_NN2, OpExtOfCoolSys
        ):
        # Вычисляем ТЗ
        vvod_oilptrc1_apttechlgc, oper_vyvod_oilptrc1_apttechlgc, srab_oilptrc1_apttechlgc, srabsign_oilptrc1_apttechlgc, zablok_oilptrc1_apttechlgc, ET_oilptrc1_apttechlgc, vvod_winptrc1_apttechlgc, oper_vyvod_winptrc1_apttechlgc, srab_winptrc1_apttechlgc, srabsign_winptrc1_apttechlgc, zablok_winptrc1_apttechlgc, ET_winptrc1_apttechlgc, vvod_vlvptrc1_apttechlgc, oper_vyvod_vlvptrc1_apttechlgc, srab_vlvptrc1_apttechlgc, srabsign_vlvptrc1_apttechlgc, zablok_vlvptrc1_apttechlgc, ET_vlvptrc1_apttechlgc = self.apttechlgc.Step(DI_ControllerDisable, DI_APTTECHLGC, DI_OILPTRC, DI_WINPTRC, DI_VLVPTRC, DI_OILPTRC_Sign, DI_WINPTRC_Sign, DI_VLVPTRC_Sign, OILTempEmerg, OILTempHigh, WINTempEmerg, WINTempHigh, VLVop, OILIsolOp, WINIsolOp, VLVIsolOp, Reset)
        # Вычисляем ТС
        vvod_prvlvptrc1_almtechlgc, oper_vyvod_prvlvptrc1_almtechlgc, srab_prvlvptrc1_almtechlgc, srabsign_prvlvptrc1_almtechlgc, vvod_shvlvptrc1_almtechlgc, oper_vyvod_shvlvptrc1_almtechlgc, srab_shvlvptrc1_almtechlgc, srabsign_shvlvptrc1_almtechlgc, vvod_levptrc1_almtechlgc, oper_vyvod_levptrc1_almtechlgc, srab_levptrc1_almtechlgc, srabsign_levptrc1_almtechlgc = self.almtechlgc.Step(DI_ControllerDisable, DI_ALMTECHLGC, DI_PRVLVPTRC1, DI_SHVLVPTRC1, DI_LEVPTRC1, DI_PRVLVPTRC1_Sign, DI_SHVLVPTRC1_Sign, DI_LEVPTRC1_Sign, PRVLVOp, SHVLVOp, LowOILLevel)
        # Вычисляем ГЗ сигн
        vvod_ptrc1_talmgaslgc, oper_vyvod_ptrc1_talmgaslgc, srab_ptrc1_talmgaslgc, srabsign_ptrc1_talmgaslgc, zablok_ptrc1_talmgaslgc, ET_ptrc1_talmgaslgc = self.talmgaslgc.Step(DI_ControllerDisable, DI_TALMGASLGC, DI_TALMGASLGC_Sign, SignContact, GASSignIsolOp, Reset)
        # Вычисляем ГЗ откл
        OV_f = 0
        vvod_ptrc1_ttrgaslgc, oper_vyvod_ptrc1_ttrgaslgc, srab_ptrc1_ttrgaslgc, srabsign_ptrc1_ttrgaslgc, zablok_ptrc1_ttrgaslgc, ET_ptrc1_ttrgaslgc = self.ttrgaslgc.Step(DI_ControllerDisable, DI_TTRGASLGC, OV_f, DI_TTRGASLGC_Sign, TripContact, GASTripIsolOp, Reset)
        # Вычисляем ГЗ РПН
        vvod_ptrc1_tltcgaslgc, oper_vyvod_ptrc1_tltcgaslgc, srab_ptrc1_tltcgaslgc, srabsign_ptrc1_tltcgaslgc, zablok_ptrc1_tltcgaslgc, ET_ptrc1_tltcgaslgc = self.tltcgaslgc.Step(DI_ControllerDisable, DI_TLTCGASLGC, OV_f, DI_TLTCGASLGC_Sign, JetRelayContact, GASLTCIsolOp, Reset)
        # Собираем кортеж срабатываний
        signals_tprmofflvlgc = (srab_oilptrc1_apttechlgc, srab_winptrc1_apttechlgc, srab_vlvptrc1_apttechlgc, srab_prvlvptrc1_almtechlgc, srab_shvlvptrc1_almtechlgc, srab_levptrc1_almtechlgc, srab_ptrc1_talmgaslgc, srab_ptrc1_ttrgaslgc, srab_ptrc1_tltcgaslgc) 

        # вычисляем ЛО Т
        vvod_ptrc1_tprmofflvlgc, oper_vyvod_ptrc1_tprmofflvlgc, pusk_ptrc1_tprmofflvlgc, srab_ptrc1_tprmofflvlgc, vvod_rbre1_tprmofflvlgc, oper_vyvod_rbre1_tprmofflvlgc, zapret_rbre1_tprmofflvlgc = self.tprmofflvlgc.Step(DI_ControllerDisable, DI_TPRMOFFLVLGC, DI_TJNTPTRC, signals_tprmofflvlgc, DI_JNTRBRE)
        # вычисляем СС
        SS_gz_sign, SS_gz_nizk_isol, SS_gz_zablok, SS_tz_sign, SS_tz_nizk_isol, SS_tz_zablok, SS_ts_sign, SS_vnesh_otkl, SS_vyh_zepi_razobr, SS_bi_vyved, SS_ot_sign, SS_neispr_ot_gz, SS_neispr_ot_tz, SS_ot_nn_sign, SS_obsh_vnesh_sign = self.tsa.Step(DI_ControllerDisable, gz_sign=(SignContact, TripContact, JetRelayContact), gz_ki=(GASSignIsolOp, GASTripIsolOp, GASLTCIsolOp), gz_zablok=(zablok_ptrc1_talmgaslgc, zablok_ptrc1_ttrgaslgc, zablok_ptrc1_tltcgaslgc), tz_sign=(OILTempEmerg, OILTempHigh, WINTempEmerg, WINTempHigh, VLVop), tz_ki=(OILIsolOp, WINIsolOp, VLVIsolOp), tz_zablok=(zablok_oilptrc1_apttechlgc, zablok_winptrc1_apttechlgc, zablok_vlvptrc1_apttechlgc), ts_sign=(PRVLVOp, SHVLVOp, LowOILLevel, HighOILLevel, HighOILLevelLTC, LowOILLevelLTC, OILTempLowLTC, FailCoolSys, ProblemCoolSys), vnesh_otkl=(OpExtOfARC_NN1, OpExtOfARC_NN2, OpExtOfCBFP_NN1, OpExtOfCBFP_NN2, OpExtOfCoolSys), Polozh_SA1=0, Polozh_SA2=0, Polozh_SA3=0, Polozh_SA4=0, Polozh_SG1=0, Polozh_SG2=0, Polozh_SG3=0, ot_gz=0, ot_tz=0, ot_zdz_nn1=0, ot_zdz_nn2=0, ot_urov_nn1=0, ot_urov_nn2=0, vnesh_sign=(0, 0, 0, 0))
        # вычисляем ПС
        pusk_lvalh = self.lvalh.Step(DI_ControllerDisable, (srab_ptrc1_tprmofflvlgc, srabsign_ptrc1_talmgaslgc, srabsign_ptrc1_ttrgaslgc, srabsign_ptrc1_tltcgaslgc, srabsign_oilptrc1_apttechlgc, srabsign_winptrc1_apttechlgc, srabsign_vlvptrc1_apttechlgc, srabsign_prvlvptrc1_almtechlgc, srabsign_shvlvptrc1_almtechlgc, srabsign_levptrc1_almtechlgc), sgf1_sign = SS_gz_sign, sgf2_sign = SS_gz_nizk_isol, sgf3_sign = SS_gz_zablok, sgf4_sign = SS_tz_sign, sgf5_sign = SS_tz_nizk_isol, sgf6_sign = SS_tz_zablok, sgf7_sign = SS_ts_sign, sgf8_sign = SS_ot_sign, sgf9_sign = SS_ot_nn_sign, sgf10_sign = SS_vnesh_otkl, sgf11_sign = SS_vyh_zepi_razobr, sgf12_sign = SS_bi_vyved, sgf13_sign = SS_obsh_vnesh_sign)

        return (vvod_oilptrc1_apttechlgc, oper_vyvod_oilptrc1_apttechlgc, srab_oilptrc1_apttechlgc, srabsign_oilptrc1_apttechlgc, zablok_oilptrc1_apttechlgc, vvod_winptrc1_apttechlgc, oper_vyvod_winptrc1_apttechlgc, srab_winptrc1_apttechlgc, srabsign_winptrc1_apttechlgc, zablok_winptrc1_apttechlgc, vvod_vlvptrc1_apttechlgc, oper_vyvod_vlvptrc1_apttechlgc, srab_vlvptrc1_apttechlgc, srabsign_vlvptrc1_apttechlgc, zablok_vlvptrc1_apttechlgc,  vvod_prvlvptrc1_almtechlgc, oper_vyvod_prvlvptrc1_almtechlgc, srab_prvlvptrc1_almtechlgc, srabsign_prvlvptrc1_almtechlgc, vvod_shvlvptrc1_almtechlgc, oper_vyvod_shvlvptrc1_almtechlgc, srab_shvlvptrc1_almtechlgc, srabsign_shvlvptrc1_almtechlgc, vvod_levptrc1_almtechlgc, oper_vyvod_levptrc1_almtechlgc, srab_levptrc1_almtechlgc, srabsign_levptrc1_almtechlgc, vvod_ptrc1_talmgaslgc, oper_vyvod_ptrc1_talmgaslgc, srab_ptrc1_talmgaslgc, srabsign_ptrc1_talmgaslgc, zablok_ptrc1_talmgaslgc, vvod_ptrc1_ttrgaslgc, oper_vyvod_ptrc1_ttrgaslgc, srab_ptrc1_ttrgaslgc, srabsign_ptrc1_ttrgaslgc, zablok_ptrc1_ttrgaslgc, vvod_ptrc1_tltcgaslgc, oper_vyvod_ptrc1_tltcgaslgc, srab_ptrc1_tltcgaslgc, srabsign_ptrc1_tltcgaslgc, zablok_ptrc1_tltcgaslgc, 

        vvod_ptrc1_tprmofflvlgc, oper_vyvod_ptrc1_tprmofflvlgc, pusk_ptrc1_tprmofflvlgc, srab_ptrc1_tprmofflvlgc, vvod_rbre1_tprmofflvlgc, oper_vyvod_rbre1_tprmofflvlgc, zapret_rbre1_tprmofflvlgc,

        SS_gz_sign, SS_gz_nizk_isol, SS_gz_zablok, SS_tz_sign, SS_tz_nizk_isol, SS_tz_zablok, SS_ts_sign, SS_vnesh_otkl, SS_vyh_zepi_razobr, SS_bi_vyved, SS_ot_sign, SS_neispr_ot_gz, SS_neispr_ot_tz, SS_ot_nn_sign, SS_obsh_vnesh_sign,

        pusk_lvalh)
       

if __name__ == "__main__":
    part = part_TECH(SGF1=1)
    res = part.Step(0, (0,0,0), 0,0,0,0,0,0,0,0,0,0,0,0,0)
    print(res)



            


