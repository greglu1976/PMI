# ЧАСТЬ СХЕМЫ ФСУ ДЛЯ ПРОВЕРКИ ТОКОВЫХ ФУНКЦИЙ Т

from lib2.FBS.LVTOC import LVTOC # импорт ФБ ТО
from lib2.FBS.TOVCTOC import TOVCTOC # импорт ФБ ЗП
from lib2.FBS.LVARCTOC import LVARCTOC # импорт ФБ ТК ЗДЗ
from lib2.FBS.LTCBLKTOC import LTCBLKTOC # импорт ТО блок РПН
#from lib._FBS.STRPALC import STRPALC # импорт ФБ РТПО
from lib2.FBS.LVNSTOC import LVNSTOC # импорт ФБ ЗОП
from lib2.FBS.TTOCLGC import TTOCLGC # импорт ФБ ЛЗТ
from lib2.FBS.TOFFLVLGC import TOFFLVLGC # импорт ЛО Т
from lib2.FBS.T_LVALH import T_LVALH # импорт ПС Т
from lib2.ADD.threePhaseSys import ThreePhaseSystem # класс для расчета аналоговых значений 

class partTOKZ:
    def __init__(self, SGF1_ptoc1_lvtoc, SGF2_ptoc1_lvtoc, T1_ptoc1_lvtoc, Iset_ptoc1_lvtoc,
                SGF1_hvptoc1_lovctoc, T1_hvptoc1_lovctoc, Iset_hvptoc1_lovctoc,
                SGF1_ptoc1_lvarctoc, SGF2_ptoc1_lvarctoc, Iset_ptoc1_lvarctoc,
                SGF1_ptoc1_ltcblktoc, Iset_ptoc1_ltcblktoc,
                #SGF1_hvptoc1_strpalc, Iset_hvptoc1_strpalc, SGF1_lvptoc1_strpalc, Iset_lvptoc1_strpalc, SGF1_lvptoc2_strpalc, Iset_lvptoc2_strpalc,
                SGF1_nsptoc1_lvnstoc, SGF2_nsptoc1_lvnstoc, T1_nsptoc1_lvnstoc, I2set_nsptoc1_lvnstoc, RatioSet_nsptoc1_lvnstoc, 
                SGF1_ptrc1_ttoclgc, SGF2_ptrc1_ttoclgc, SGF3_ptrc1_ttoclgc, T1_ptrc1_ttoclgc,
                SGF1_ptrc1_tofflvlgc, SGF1_rbre1_tofflvlgc, SGF2_rbre1_tofflvlgc, SGF3_rbre1_tofflvlgc, SGF1_rblc1_tofflvlgc, SGF2_rblc1_tofflvlgc, SGF3_rblc1_tofflvlgc,
                Inom
                ):

        self.lvtoc = LVTOC(SGF1_ptoc1_lvtoc, SGF2_ptoc1_lvtoc, T1_ptoc1_lvtoc, Iset_ptoc1_lvtoc*Inom)
        self.tovctoc = TOVCTOC(SGF1_hvptoc1_lovctoc, T1_hvptoc1_lovctoc, Iset_hvptoc1_lovctoc*Inom)
        self.lvarctoc = LVARCTOC(SGF1_ptoc1_lvarctoc, SGF2_ptoc1_lvarctoc, Iset_ptoc1_lvarctoc*Inom)
        self.ltcblktoc = LTCBLKTOC(SGF1_ptoc1_ltcblktoc, Iset_ptoc1_ltcblktoc*Inom)
        #self.strpalc = STRPALC(SGF1_hvptoc1_strpalc, Iset_hvptoc1_strpalc, SGF1_lvptoc1_strpalc, Iset_lvptoc1_strpalc, SGF1_lvptoc2_strpalc, Iset_lvptoc2_strpalc)
        self.lvnstoc = LVNSTOC(SGF1_nsptoc1_lvnstoc, SGF2_nsptoc1_lvnstoc, T1_nsptoc1_lvnstoc, I2set_nsptoc1_lvnstoc*Inom, RatioSet_nsptoc1_lvnstoc, Inom)
        self.ttoclgc = TTOCLGC(SGF1_ptrc1_ttoclgc, SGF2_ptrc1_ttoclgc, SGF3_ptrc1_ttoclgc, T1_ptrc1_ttoclgc)
        self.tofflvlgc = TOFFLVLGC(SGF1_ptrc1_tofflvlgc, SGF1_rbre1_tofflvlgc, SGF2_rbre1_tofflvlgc, SGF3_rbre1_tofflvlgc, SGF1_rblc1_tofflvlgc, SGF2_rblc1_tofflvlgc, SGF3_rblc1_tofflvlgc)
        self.lvalh = T_LVALH()  
         

    def Step(self, DI_ControllerDisable, IA, dIA, IB, dIB, IC, dIC,
    DI_LVTOC, DI_LVTOC_Sign,
    DI_TOVCTOC, DI_TOVCTOC_Sign,
    DI_LVARCTOC, LVTTOC_1_PTOC1_Str, LVTTOC_1_PTOC2_Str, LVTTOC_1_PTOC3_Str,
    DI_LTCBLKTOC,
    #OV_strpalc, OV_hvptoc1_strpalc, OV_lvptoc1_strpalc, IA1, IB1, IC1,  OV_lvptoc2_strpalc, IA2, IB2, IC2,
    DI_LVNSTOC, DI_LVNSTOC_Sign,
    DI_TTOCLGC, ExtTLGCPTRCStr, BlkLPT1, BlkLPT2,
    DI_TRESOFFLVLGS, DI_PTRC1, DI_RBRE1, DI_LVCBRBLC1,
    ):

        # Расчитываем аналоги
        threeI = ThreePhaseSystem(IA, dIA, IB, dIB, IC, dIC)
        Is = threeI.calculate_line_voltages()
        IAB = Is['Uab']['amplitude']   #/(3**0.5) убрал приведение к базису, вроде в Сириусе-Т не приводится
        IBC = Is['Ubc']['amplitude']   #/(3**0.5)
        ICA = Is['Uca']['amplitude']   #/(3**0.5)
        Isimm = threeI.calculate_symmetric_components()
        I1 = Isimm['U1']['amplitude']
        I2 = Isimm['U2']['amplitude']
        I0 = 3*Isimm['U0']['amplitude']        

        # Рассчитываем ТО
        vvod_ptoc1_lvtoc, oper_vyvod_ptoc1_lvtoc, pusk_ptoc1_lvtoc, io_ptoc1_lvtoc, srabsign_ptoc1_lvtoc, srab_ptoc1_lvtoc, ET_ptoc1_lvtoc =  self.lvtoc.Step(DI_ControllerDisable, DI_LVTOC, DI_LVTOC_Sign, IA, IB, IC, IAB, IBC, ICA)
        # Рассчитываем ЗП
        vvod_hvptoc1_lovctoc, oper_vyvod_hvptoc1_lovctoc, pusk_hvptoc1_lovctoc, io_hvptoc1_lovctoc, srab_hvptoc1_lovctoc, srabotkl_hvptoc1_lovctoc, ET_hvptoc1_lovctoc = self.tovctoc.Step(DI_ControllerDisable, DI_TOVCTOC, DI_TOVCTOC_Sign, IA, IB, IC)
        # Рассчитываем ТК ЗДЗ
        vvod_ptoc1_lvarctoc, oper_vyvod_ptoc1_lvarctoc, pusk_ptoc1_lvarctoc, io_ptoc1_lvarctoc =  self.lvarctoc.Step(DI_ControllerDisable, DI_LVARCTOC, IA, IB, IC, LVTTOC_1_PTOC1_Str, LVTTOC_1_PTOC2_Str, LVTTOC_1_PTOC3_Str) 

        # Рассчитываем ТО РПН
        vvod_ptoc1_ltcblktoc, oper_vyvod_ptoc1_ltcblktoc, pusk_ptoc1_ltcblktoc, io_ptoc1_ltcblktoc = self.ltcblktoc.Step(DI_ControllerDisable, DI_LTCBLKTOC, IA, IB, IC)      

        # Рассчитываем РТПО
        #vvod_hvptoc1_strpalc, oper_vyvod_hvptoc1_strpalc, pusk_hvptoc1_strpalc, io_hvptoc1_strpalc, vvod_lvptoc1_strpalc, oper_vyvod_lvptoc1_strpalc, pusk_lvptoc1_strpalc, io_lvptoc1_strpalc, vvod_lvptoc2_strpalc, oper_vyvod_lvptoc2_strpalc, pusk_lvptoc2_strpalc, io_lvptoc2_strpalc, pusk_strpalc, vvod_strpalc = self.strpalc.Step(DI_ControllerDisable, OV_strpalc, OV_hvptoc1_strpalc, IA, IB, IC,  OV_lvptoc1_strpalc, IA1, IB1, IC1, OV_lvptoc2_strpalc, IA2, IB2, IC2)        
        # Рассчитываем ЗОП
        vvod_nsptoc1_lvnstoc, oper_vyvod_nsptoc1_lvnstoc, srab_nsptoc1_lvnstoc, srabsign_nsptoc1_lvnstoc, pusk_nsptoc1_lvnstoc, io_I2_nsptoc1_lvnstoc, io_rat_nsptoc1_lvnstoc, ET_nsptoc1_lvnstoc = self.lvnstoc.Step(DI_ControllerDisable, DI_LVNSTOC, DI_LVNSTOC_Sign, I2, I1)
        # Рассчитываем ЛЗТ
        vvod_ptrc1_ttoclgc, oper_vyvod_ptrc1_ttoclgc, pusk_ptrc1_ttoclgc, srab_ptrc1_ttoclgc, ET_ptrc1_ttoclgc =  self.ttoclgc.Step(DI_ControllerDisable, DI_TTOCLGC, ExtTLGCPTRCStr, LVTTOC_1_PTOC2_Str, LVTTOC_1_PTOC3_Str, BlkLPT1 or BlkLPT2)       
        # Рассчитываем ЛО Т
        vvod_ptrc1_tofflvlgc, oper_vyvod_ptrc1_tofflvlgc, pusk_ptrc1_tofflvlgc, srab_ptrc1_tofflvlgc, vvod_rblc1_tofflvlgc, oper_vyvod_rblc1_tofflvlgc, zapret_rblc1_tofflvlgc, vvod_rbre1_tofflvlgc, oper_vyvod_rbre1_tofflvlgc, zapret_rbre1_tofflvlgc = self.tofflvlgc.Step(DI_ControllerDisable, DI_TRESOFFLVLGS, DI_PTRC1, signals_tofflvlg=(srab_ptoc1_lvtoc, srabotkl_hvptoc1_lovctoc, srab_nsptoc1_lvnstoc, srab_ptrc1_ttoclgc), mtz2_srab_tofflvlg=0, mtz3_srab_tofflvlg=0, OVzapv_tofflvlg=DI_RBRE1, OVzavr_tofflvlg=DI_LVCBRBLC1)
        # вычисляем ПС
        pusk_lvalh = self.lvalh.Step(DI_ControllerDisable, sign_ps_tuple = (srab_hvptoc1_lovctoc, srabsign_nsptoc1_lvnstoc, srabsign_ptoc1_lvtoc, srab_ptrc1_tofflvlgc))
        return (
            vvod_ptoc1_lvtoc, oper_vyvod_ptoc1_lvtoc, pusk_ptoc1_lvtoc, io_ptoc1_lvtoc, srabsign_ptoc1_lvtoc, srab_ptoc1_lvtoc,
            vvod_hvptoc1_lovctoc, oper_vyvod_hvptoc1_lovctoc, pusk_hvptoc1_lovctoc, io_hvptoc1_lovctoc, srab_hvptoc1_lovctoc, srabotkl_hvptoc1_lovctoc,
            vvod_ptoc1_lvarctoc, oper_vyvod_ptoc1_lvarctoc, pusk_ptoc1_lvarctoc, io_ptoc1_lvarctoc,
            #vvod_hvptoc1_strpalc, oper_vyvod_hvptoc1_strpalc, pusk_hvptoc1_strpalc, io_hvptoc1_strpalc, vvod_lvptoc1_strpalc, oper_vyvod_lvptoc1_strpalc, pusk_lvptoc1_strpalc, io_lvptoc1_strpalc, vvod_lvptoc2_strpalc, oper_vyvod_lvptoc2_strpalc, pusk_lvptoc2_strpalc, io_lvptoc2_strpalc, pusk_strpalc, vvod_strpalc,
            vvod_nsptoc1_lvnstoc, oper_vyvod_nsptoc1_lvnstoc, srab_nsptoc1_lvnstoc, srabsign_nsptoc1_lvnstoc, pusk_nsptoc1_lvnstoc, io_I2_nsptoc1_lvnstoc, io_rat_nsptoc1_lvnstoc,
            vvod_ptrc1_ttoclgc, oper_vyvod_ptrc1_ttoclgc, pusk_ptrc1_ttoclgc, srab_ptrc1_ttoclgc,
            vvod_ptrc1_tofflvlgc, oper_vyvod_ptrc1_tofflvlgc, pusk_ptrc1_tofflvlgc, srab_ptrc1_tofflvlgc, vvod_rblc1_tofflvlgc, oper_vyvod_rblc1_tofflvlgc, zapret_rblc1_tofflvlgc, vvod_rbre1_tofflvlgc, oper_vyvod_rbre1_tofflvlgc, zapret_rbre1_tofflvlgc,
            pusk_lvalh,
            vvod_ptoc1_ltcblktoc, oper_vyvod_ptoc1_ltcblktoc, pusk_ptoc1_ltcblktoc, io_ptoc1_ltcblktoc,
            IAB, IBC, ICA, I1, I2, I0
        )    




            


