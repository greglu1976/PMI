# ЧАСТЬ СХЕМЫ ФСУ ДЛЯ ПРОВЕРКИ ЛО, УРОВ, ПС, СС
# ИСПОЛНЕНИЯ ДЗТ2

# Проверяемые функции
from lib2.FBS.HVTCBOFF import HVTCBOFF # импорт ФБ ЛО ВН
from lib2.FBS.LVTCBOFF_DZT import LVTCBOFF # импорт ЛО НН
from lib2.FBS.TPBRF_DZT import TPBRF # импорт ФБ УРОВ

# Вспомогательные функции
from lib2.FBS.TPRMOFFLVLGC import TPRMOFFLVLGC # импорт ЛО Т для ДЗТ
from lib2.FBS.DZT2_LVALH import DZT2_LVALH # импорт ПС
from lib2.FBS.DZT2_SignAssembly import DZT2_SignAssembly

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

    def Step(self, DI_ControllerDisable,
        # для ЛО Т
        OpExtOfCoolSys,
        DI_TPRMOFFLVLGC, DI_TJNTPTRC, DI_JNTRBRE,
        # для ЛО ВН
        DI_HVTCBOFF, OpExtOfARC_NN1, OpExtOfARC_NN2, OpExtOfCBFP_NN1, OpExtOfCBFP_NN2, 
        # для ЛО НН1
        DI_LVTPRMCBOFF1, DI_LVCBPTRC1, DI_LVCBRECRBRE1,
        # для ЛО НН2
        DI_LVTPRMCBOFF2, DI_LVCBPTRC2, DI_LVCBRECRBRE2,
        # для УРОВ
        DI_TPBRF, ExternalRBRFStart, IA, IB, IC,
        # для CC
        CtlCirSwPos1, CtlCirSwPos2, CtlCirSwPos3, CtlCirSwPos4, TestBlockPos1, TestBlockPos2, TestBlockPos3, GAS_OCControl, DZT2_SignAssembly_1_TECH_OCControlSignAssem, ARCnn1_OCControl, ARCnn2_OCControl, CBFPnn1_OCControl, CBFPnn2_OCControl, ExtSignal1, ExtSignal2,ExtSignal3, ExtSignal4 
        ):

        # кортеж срабатываний, здесь только одно - внешнее откл. от СО   
        signals_tprmofflvlgc = (OpExtOfCoolSys, 0)
        # вычисляем ЛО Т
        vvod_ptrc1_tprmofflvlgc, oper_vyvod_ptrc1_tprmofflvlgc, pusk_ptrc1_tprmofflvlgc, srab_ptrc1_tprmofflvlgc, vvod_rbre1_tprmofflvlgc, oper_vyvod_rbre1_tprmofflvlgc, zapret_rbre1_tprmofflvlgc = self.tprmofflvlgc.Step(DI_ControllerDisable, DI_TPRMOFFLVLGC, DI_TJNTPTRC, signals_tprmofflvlgc, DI_JNTRBRE)

        # вычисляем ЛО ВН 
        vnesh_otkl_zdz = OpExtOfARC_NN1 or OpExtOfARC_NN2
        vnesh_otkl_urov = OpExtOfCBFP_NN1 or OpExtOfCBFP_NN2
        vvod_hvcbptrc1_hvtcboff, oper_vyvod_hvcbptrc1_hvtcboff, otkl_hvcbptrc1_hvtcboff, otkl_avar_hvcbptrc1_hvtcboff = self.hvtcboff.Step(DI_ControllerDisable, DI_HVTCBOFF, srab_ptrc1_tprmofflvlgc, vnesh_otkl_zdz, vnesh_otkl_urov)

        # вычисляем ЛО НН1  
        vvod_lvcbptrc1_lvtcboff1, oper_vyvod_lvcbptrc1_lvtcboff1, otkl_lvcbptrc1_lvtcboff1, otkl_avar_lvcbptrc1_lvtcboff1, vvod_lvcbrecrbre1_lvtcboff1, oper_vyvod_lvcbrecrbre1_lvtcboff1, zapret_lvcbrecrbre1_lvtcboff1 = self.lvtcboff1.Step(DI_ControllerDisable, DI_LVTPRMCBOFF1, DI_LVCBPTRC1, DI_LVCBRECRBRE1, srab_ptrc1_tprmofflvlgc, zapret_rbre1_tprmofflvlgc)

        # вычисляем ЛО НН2  
        vvod_lvcbptrc1_lvtcboff2, oper_vyvod_lvcbptrc1_lvtcboff2, otkl_lvcbptrc1_lvtcboff2, otkl_avar_lvcbptrc1_lvtcboff2, vvod_lvcbrecrbre1_lvtcboff2, oper_vyvod_lvcbrecrbre1_lvtcboff2, zapret_lvcbrecrbre1_lvtcboff2 = self.lvtcboff2.Step(DI_ControllerDisable, DI_LVTPRMCBOFF2, DI_LVCBPTRC2, DI_LVCBRECRBRE2, srab_ptrc1_tprmofflvlgc, zapret_rbre1_tprmofflvlgc)

        # вычисляем УРОВ
        vvod_rbrf1_tpbrf, oper_vyvod_rbrf1_tpbrf, srab_rbrf1_tpbrf, pusk_rbrf1_tpbrf, io_rbrf1_tpbrf, srab_na_sebya_rbrf1_tpbrf = self.tpbrf.Step(DI_ControllerDisable, DI_TPBRF, otkl_hvcbptrc1_hvtcboff, ExternalRBRFStart, IA, IB, IC)

        # вычисляем СС
        SS_gz_sign, SS_gz_nizk_isol, SS_gz_zablok, SS_tz_sign, SS_tz_nizk_isol, SS_tz_zablok, SS_ts_sign, SS_vnesh_otkl, SS_vyh_zepi_razobr, SS_bi_vyved, SS_ot_sign, SS_neispr_ot_gz, SS_neispr_ot_tz, SS_ot_nn_sign, SS_obsh_vnesh_sign = self.tsa.Step(DI_ControllerDisable, gz_sign=(0,), gz_ki=(0,), gz_zablok=(0,), tz_sign=(0,), tz_ki=(0,), tz_zablok=(0,), ts_sign=(0,), vnesh_otkl=(OpExtOfCoolSys, OpExtOfARC_NN1, OpExtOfARC_NN2, OpExtOfCBFP_NN1, OpExtOfCBFP_NN2), Polozh_SA1=CtlCirSwPos1, Polozh_SA2=CtlCirSwPos2, Polozh_SA3=CtlCirSwPos3, Polozh_SA4=CtlCirSwPos4, Polozh_SG1=TestBlockPos1, Polozh_SG2=TestBlockPos2, Polozh_SG3=TestBlockPos3, ot_gz=GAS_OCControl, ot_tz=DZT2_SignAssembly_1_TECH_OCControlSignAssem, ot_zdz_nn1=ARCnn1_OCControl, ot_zdz_nn2=ARCnn2_OCControl, ot_urov_nn1=CBFPnn1_OCControl, ot_urov_nn2=CBFPnn2_OCControl, vnesh_sign=(ExtSignal1, ExtSignal2, ExtSignal3, ExtSignal4))

        # вычисляем ПС
        pusk_lvalh = self.lvalh.Step(DI_ControllerDisable, (srab_ptrc1_tprmofflvlgc, srab_rbrf1_tpbrf, srab_na_sebya_rbrf1_tpbrf), sgf1_sign = SS_gz_sign, sgf2_sign = SS_gz_nizk_isol, sgf3_sign = SS_gz_zablok, sgf4_sign = SS_tz_sign, sgf5_sign = SS_tz_nizk_isol, sgf6_sign = SS_tz_zablok, sgf7_sign = SS_ts_sign, sgf8_sign = SS_ot_sign, sgf9_sign = SS_ot_nn_sign, sgf10_sign = SS_vnesh_otkl, sgf11_sign = SS_vyh_zepi_razobr, sgf12_sign = SS_bi_vyved, sgf13_sign = SS_obsh_vnesh_sign)

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



            


