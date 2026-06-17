# ЧАСТЬ СХЕМЫ ФСУ ДЛЯ ПРОВЕРКИ ТОКОВЫХ ФУНКЦИЙ ДЗТ

from lib2.FBS.TOVCTOC_DZT import TOVCTOC # импорт ФБ ЗП

from lib2.FBS.LVARCTOC import LVARCTOC # импорт ФБ ТК ЗДЗ
from lib2.FBS.LTCBLKTOC import LTCBLKTOC # импорт ТО блок РПН
from lib2.FBS.STRPALC import STRPALC # импорт ФБ РТПО

from lib2.FBS.TPALC import TPALC # импорт ФБ ТО ЗПО
from lib2.FBS.EQPALC import EQPALC # импорт ФБ ЗПО

from lib2.FBS.TPRMOFFLVLGC import TPRMOFFLVLGC # импорт ЛО Т для ДЗТ
from lib2.FBS.DZT2_LVALH import DZT2_LVALH # импорт ПС


class partTOKZ:
    def __init__(self, 
                SGF1_hvptoc1_tovctoc, T1_hvptoc1_tovctoc, Iset_hvptoc1_tovctoc, SGF1_ptoc1_tovctoc, T1_ptoc1_tovctoc, Iset_ptoc1_tovctoc, SGF1_ptoc2_tovctoc, T1_ptoc2_tovctoc, Iset_ptoc2_tovctoc,
                SGF1_ptoc1_lvarctoc, Iset_ptoc1_lvarctoc,
                SGF1_ptoc1_ltcblktoc, Iset_ptoc1_ltcblktoc,
                SGF1_hvptoc1_strpalc, Iset_hvptoc1_strpalc, SGF1_lvptoc1_strpalc, Iset_lvptoc1_strpalc, SGF1_lvptoc2_strpalc, Iset_lvptoc2_strpalc,
                SGF1_hvptoc1_tpalc, Iset_hvptoc1_tpalc, SGF1_lvptoc1_tpalc, Iset_lvptoc1_tpalc, SGF1_lvptoc2_tpalc, Iset_lvptoc2_tpalc,
                SGF1_lvoileqpalc_eqpalc, SGF2_lvoileqpalc_eqpalc, SGF3_lvoileqpalc_eqpalc,T1_lvoileqpalc_eqpalc,
                SGF1_ptrc1_tprmofflvlgc, SGF1_rbre1_tprmofflvlgc,
                Inom, Inom2, Inom3
                ):

        # инициализируем ЗП
        self.tovctoc = TOVCTOC(SGF1_hvptoc1_tovctoc, T1_hvptoc1_tovctoc, Iset_hvptoc1_tovctoc*Inom, SGF1_ptoc1_tovctoc, T1_ptoc1_tovctoc, Iset_ptoc1_tovctoc*Inom2, SGF1_ptoc2_tovctoc, T1_ptoc2_tovctoc, Iset_ptoc2_tovctoc*Inom3)
        # инициализируем ТК ЗДЗ, ТО РПН, РТПО
        SGF2_ptoc1_lvarctoc = 0 
        self.lvarctoc = LVARCTOC(SGF1_ptoc1_lvarctoc, SGF2_ptoc1_lvarctoc, Iset_ptoc1_lvarctoc*Inom)
        self.ltcblktoc = LTCBLKTOC(SGF1_ptoc1_ltcblktoc, Iset_ptoc1_ltcblktoc*Inom)
        self.strpalc = STRPALC(SGF1_hvptoc1_strpalc, Iset_hvptoc1_strpalc*Inom, SGF1_lvptoc1_strpalc, Iset_lvptoc1_strpalc*Inom2, SGF1_lvptoc2_strpalc, Iset_lvptoc2_strpalc*Inom3)
        # инициализируем ТО ЗПО, ЗПО
        self.tpalc = TPALC(SGF1_hvptoc1_tpalc, Iset_hvptoc1_tpalc*Inom, SGF1_lvptoc1_tpalc, Iset_lvptoc1_tpalc*Inom2, SGF1_lvptoc2_tpalc, Iset_lvptoc2_tpalc*Inom3)
        self.eqpalc = EQPALC(SGF1_lvoileqpalc_eqpalc, SGF2_lvoileqpalc_eqpalc, SGF3_lvoileqpalc_eqpalc,T1_lvoileqpalc_eqpalc)
        # инициализируем ЛО Т, ПС
        self.tprmofflvlgc = TPRMOFFLVLGC(SGF1_ptrc1_tprmofflvlgc, SGF1_rbre1_tprmofflvlgc)
        self.lvalh = DZT2_LVALH()  
         

    def Step(self, DI_ControllerDisable, 
    DI_TOVCTOC, DI_TOVCTOC_HVPTOC1, DI_TOVCTOC_Sign, IA, IB, IC, DI_TOVCTOC_LVPTOC1, IA1, IB1, IC1,  DI_TOVCTOC_LVPTOC2, 
    DI_LVARCTOC,
    DI_LTCBLKTOC,
    DI_STRTPALC, DI_STRTPALC_HVPTOC1, DI_STRTPALC_LVPTOC1, DI_STRTPALC_LVPTOC2,
    DI_TPALC, DI_TPALC_HVPTOC1, DI_TPALC_LVPTOC1, DI_TPALC_LVPTOC2,
    DI_EQPALC, DI_EQPALC_Sign, FailCoolSys, AlcOilTmp,
    DI_TPRMOFFLVLGC, DI_TJNTPTRC, DI_JNTRBRE,
    ):

        IA2=IA1
        IB2=IB1
        IC2=IC1
        NaOtkl_hvptoc1_tovctoc = DI_TOVCTOC_Sign
        NaOtkl_ptoc1_tovctoc = DI_TOVCTOC_Sign
        NaOtkl_ptoc2_tovctoc = DI_TOVCTOC_Sign
        # Рассчитываем ЗП
        vvod_hvptoc1_tovctoc, oper_vyvod_hvptoc1_tovctoc, pusk_hvptoc1_tovctoc, io_hvptoc1_tovctoc, srab_hvptoc1_tovctoc, srabotkl_hvptoc1_tovctoc, vvod_ptoc1_tovctoc, oper_vyvod_ptoc1_tovctoc, pusk_ptoc1_tovctoc, io_ptoc1_tovctoc, srab_ptoc1_tovctoc, srabotkl_ptoc1_tovctoc, vvod_ptoc2_tovctoc, oper_vyvod_ptoc2_tovctoc, pusk_ptoc2_tovctoc, io_ptoc2_tovctoc, srab_ptoc2_tovctoc, srabotkl_ptoc2_tovctoc, srab_tovctoc = self.tovctoc.Step(DI_ControllerDisable, DI_TOVCTOC, DI_TOVCTOC_HVPTOC1, NaOtkl_hvptoc1_tovctoc, IA, IB, IC, DI_TOVCTOC_LVPTOC1, NaOtkl_ptoc1_tovctoc, IA1, IB1, IC1, DI_TOVCTOC_LVPTOC2, NaOtkl_ptoc2_tovctoc, IA2, IB2, IC2)
        # Рассчитываем ТК ЗДЗ
        mtz1_pusk=mtz2_pusk=mtz3_pusk=0
        vvod_ptoc1_lvarctoc, oper_vyvod_ptoc1_lvarctoc, pusk_ptoc1_lvarctoc, io_ptoc1_lvarctoc =  self.lvarctoc.Step(DI_ControllerDisable, DI_LVARCTOC, IA, IB, IC, mtz1_pusk, mtz2_pusk, mtz3_pusk) 
        # Рассчитываем ТО РПН
        vvod_ptoc1_ltcblktoc, oper_vyvod_ptoc1_ltcblktoc, pusk_ptoc1_ltcblktoc, io_ptoc1_ltcblktoc = self.ltcblktoc.Step(DI_ControllerDisable, DI_LTCBLKTOC, IA, IB, IC)      
        # Рассчитываем РТПО
        vvod_hvptoc1_strpalc, oper_vyvod_hvptoc1_strpalc, pusk_hvptoc1_strpalc, io_hvptoc1_strpalc, vvod_lvptoc1_strpalc, oper_vyvod_lvptoc1_strpalc, pusk_lvptoc1_strpalc, io_lvptoc1_strpalc, vvod_lvptoc2_strpalc, oper_vyvod_lvptoc2_strpalc, pusk_lvptoc2_strpalc, io_lvptoc2_strpalc, pusk_strpalc, vvod_strpalc = self.strpalc.Step(DI_ControllerDisable, DI_STRTPALC, DI_STRTPALC_HVPTOC1, IA, IB, IC,  DI_STRTPALC_LVPTOC1, IA1, IB1, IC1,  DI_STRTPALC_LVPTOC2, IA2, IB2, IC2)        
        # Рассчитываем ТО ЗПО
        vvod_hvptoc1_tpalc, oper_vyvod_hvptoc1_tpalc, pusk_hvptoc1_tpalc, io_hvptoc1_tpalc, vvod_lvptoc1_tpalc, oper_vyvod_lvptoc1_tpalc, pusk_lvptoc1_tpalc, io_lvptoc1_tpalc, vvod_lvptoc2_tpalc, oper_vyvod_lvptoc2_tpalc, pusk_lvptoc2_tpalc, io_lvptoc2_tpalc, pusk_tpalc, vvod_tpalc = self.tpalc.Step(DI_ControllerDisable, DI_TPALC, DI_TPALC_HVPTOC1, IA, IB, IC,  DI_TPALC_LVPTOC1, IA1, IB1, IC1,  DI_TPALC_LVPTOC2, IA2, IB2, IC2)
        # Рассчитываем ЗПО
        vvod_lvoileqpalc_eqpalc, oper_vyvod_lvoileqpalc_eqpalc, pusk_lvoileqpalc_eqpalc, srabsign_lvoileqpalc_eqpalc, srab_lvoileqpalc_eqpalc = self.eqpalc.Step(DI_ControllerDisable, DI_EQPALC, DI_EQPALC_Sign, FailCoolSys, pusk_tpalc, AlcOilTmp)      
        # Рассчитываем ЛО Т
        signals = (srab_lvoileqpalc_eqpalc, srabotkl_hvptoc1_tovctoc, srabotkl_ptoc1_tovctoc, srabotkl_ptoc2_tovctoc)
        vvod_ptrc1_tprmofflvlgc, oper_vyvod_ptrc1_tprmofflvlgc, pusk_ptrc1_tprmofflvlgc, srab_ptrc1_tprmofflvlgc, vvod_rbre1_tprmofflvlgc, oper_vyvod_rbre1_tprmofflvlgc, zapret_rbre1_tprmofflvlgc = self.tprmofflvlgc.Step(DI_ControllerDisable, DI_TPRMOFFLVLGC, DI_TJNTPTRC, signals, DI_JNTRBRE)
        # вычисляем ПС
        pusk_lvalh = self.lvalh.Step(DI_ControllerDisable, COMM_SIGN=(pusk_lvoileqpalc_eqpalc, srab_hvptoc1_tovctoc, srab_ptoc1_tovctoc, srab_ptoc2_tovctoc, srab_ptrc1_tprmofflvlgc))

        return  (
            vvod_hvptoc1_tovctoc, oper_vyvod_hvptoc1_tovctoc, pusk_hvptoc1_tovctoc, io_hvptoc1_tovctoc, srab_hvptoc1_tovctoc, srabotkl_hvptoc1_tovctoc, vvod_ptoc1_tovctoc, oper_vyvod_ptoc1_tovctoc, pusk_ptoc1_tovctoc, io_ptoc1_tovctoc, srab_ptoc1_tovctoc, srabotkl_ptoc1_tovctoc, vvod_ptoc2_tovctoc, oper_vyvod_ptoc2_tovctoc, pusk_ptoc2_tovctoc, io_ptoc2_tovctoc, srab_ptoc2_tovctoc, srabotkl_ptoc2_tovctoc, srab_tovctoc,

            vvod_ptoc1_lvarctoc, oper_vyvod_ptoc1_lvarctoc, pusk_ptoc1_lvarctoc, io_ptoc1_lvarctoc,

            vvod_ptoc1_ltcblktoc, oper_vyvod_ptoc1_ltcblktoc, pusk_ptoc1_ltcblktoc, io_ptoc1_ltcblktoc,

            vvod_hvptoc1_strpalc, oper_vyvod_hvptoc1_strpalc, pusk_hvptoc1_strpalc, io_hvptoc1_strpalc, vvod_lvptoc1_strpalc, oper_vyvod_lvptoc1_strpalc, pusk_lvptoc1_strpalc, io_lvptoc1_strpalc, vvod_lvptoc2_strpalc, oper_vyvod_lvptoc2_strpalc, pusk_lvptoc2_strpalc, io_lvptoc2_strpalc, pusk_strpalc, vvod_strpalc,

            vvod_hvptoc1_tpalc, oper_vyvod_hvptoc1_tpalc, pusk_hvptoc1_tpalc, io_hvptoc1_tpalc, vvod_lvptoc1_tpalc, oper_vyvod_lvptoc1_tpalc, pusk_lvptoc1_tpalc, io_lvptoc1_tpalc, vvod_lvptoc2_tpalc, oper_vyvod_lvptoc2_tpalc, pusk_lvptoc2_tpalc, io_lvptoc2_tpalc, pusk_tpalc, vvod_tpalc,

            vvod_lvoileqpalc_eqpalc, oper_vyvod_lvoileqpalc_eqpalc, pusk_lvoileqpalc_eqpalc, srabsign_lvoileqpalc_eqpalc, srab_lvoileqpalc_eqpalc,

            vvod_ptrc1_tprmofflvlgc, oper_vyvod_ptrc1_tprmofflvlgc, pusk_ptrc1_tprmofflvlgc, srab_ptrc1_tprmofflvlgc, vvod_rbre1_tprmofflvlgc, oper_vyvod_rbre1_tprmofflvlgc, zapret_rbre1_tprmofflvlgc,

            pusk_lvalh
        )  




            


