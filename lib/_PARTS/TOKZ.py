# ЧАСТЬ СХЕМЫ ФСУ ДЛЯ ПРОВЕРКИ ТОКОВЫХ ФУНКЦИЙ Т

from lib._FBS.LVTOC import LVTOC # импорт ФБ ТО
from lib._FBS.TOVCTOC import TOVCTOC # импорт ФБ ЗП
from lib._FBS.LVARCTOC import LVARCTOC # импорт ФБ ТК ЗДЗ
from lib._FBS.LTCBLKTOC import LTCBLKTOC # импорт ТО блок РПН
#from lib._FBS.STRPALC import STRPALC # импорт ФБ РТПО
from lib._FBS.LVNSTOC import LVNSTOC # импорт ФБ ЗОП
from lib._FBS.TTOCLGC import TTOCLGC # импорт ФБ ЛЗТ
from lib._FBS.TOFFLVLGC import TOFFLVLGC # импорт ЛО Т
from lib._FBS.T_LVALH import T_LVALH # импорт ПС Т
from lib._ADD.threePhaseSys import ThreePhaseSystem # класс для расчета аналоговых значений 

class partTOKZ:
    def __init__(self, SGF1_ptoc1_lvtoc, SGF2_ptoc1_lvtoc, T1_ptoc1_lvtoc, Iset_ptoc1_lvtoc,
                SGF1_hvptoc1_lovctoc, T1_hvptoc1_lovctoc, Iset_hvptoc1_lovctoc,
                SGF1_ptoc1_lvarctoc, SGF2_ptoc1_lvarctoc, Iset_ptoc1_lvarctoc,
                SGF1_ptoc1_ltcblktoc, Iset_ptoc1_ltcblktoc,
                #SGF1_hvptoc1_strpalc, Iset_hvptoc1_strpalc, SGF1_lvptoc1_strpalc, Iset_lvptoc1_strpalc, SGF1_lvptoc2_strpalc, Iset_lvptoc2_strpalc,
                SGF1_nsptoc1_lvnstoc, SGF2_nsptoc1_lvnstoc, T1_nsptoc1_lvnstoc, I2set_nsptoc1_lvnstoc, RatioSet_nsptoc1_lvnstoc, In_nsptoc1_lvnstoc,
                SGF1_ptrc1_ttoclgc, SGF2_ptrc1_ttoclgc, SGF3_ptrc1_ttoclgc, T1_ptrc1_ttoclgc,
                SGF1_ptrc1_tofflvlgc, SGF1_rbre1_tofflvlgc, SGF2_rbre1_tofflvlgc, SGF3_rbre1_tofflvlgc, SGF1_rblc1_tofflvlgc, SGF2_rblc1_tofflvlgc, SGF3_rblc1_tofflvlgc,
                ):

        self.lvtoc = LVTOC(SGF1_ptoc1_lvtoc, SGF2_ptoc1_lvtoc, T1_ptoc1_lvtoc, Iset_ptoc1_lvtoc)
        self.tovctoc = TOVCTOC(SGF1_hvptoc1_lovctoc, T1_hvptoc1_lovctoc, Iset_hvptoc1_lovctoc)
        self.lvarctoc = LVARCTOC(SGF1_ptoc1_lvarctoc, SGF2_ptoc1_lvarctoc, Iset_ptoc1_lvarctoc)
        self.ltcblktoc = LTCBLKTOC(SGF1_ptoc1_ltcblktoc, Iset_ptoc1_ltcblktoc)
        #self.strpalc = STRPALC(SGF1_hvptoc1_strpalc, Iset_hvptoc1_strpalc, SGF1_lvptoc1_strpalc, Iset_lvptoc1_strpalc, SGF1_lvptoc2_strpalc, Iset_lvptoc2_strpalc)
        self.lvnstoc = LVNSTOC(SGF1_nsptoc1_lvnstoc, SGF2_nsptoc1_lvnstoc, T1_nsptoc1_lvnstoc, I2set_nsptoc1_lvnstoc, RatioSet_nsptoc1_lvnstoc, In_nsptoc1_lvnstoc)
        self.ttoclgc = TTOCLGC(SGF1_ptrc1_ttoclgc, SGF2_ptrc1_ttoclgc, SGF3_ptrc1_ttoclgc, T1_ptrc1_ttoclgc)
        self.tofflvlgc = TOFFLVLGC(SGF1_ptrc1_tofflvlgc, SGF1_rbre1_tofflvlgc, SGF2_rbre1_tofflvlgc, SGF3_rbre1_tofflvlgc, SGF1_rblc1_tofflvlgc, SGF2_rblc1_tofflvlgc, SGF3_rblc1_tofflvlgc)
        self.lvalh = T_LVALH()    

    def Step(self, VYVOD, IA, dIA, IB, dIB, IC, dIC,
    OV_ptoc1_lvtoc, NaSign_ptoc1_lvtoc,
    OV_hvptoc1_lovctoc, NaOtkl_hvptoc1_lovctoc,
    OV_ptoc1_lvarctoc, mtz1_pusk, mtz2_pusk, mtz3_pusk,
    OV_ptoc1_ltcblktoc,
    #OV_strpalc, OV_hvptoc1_strpalc, OV_lvptoc1_strpalc, IA1, IB1, IC1,  OV_lvptoc2_strpalc, IA2, IB2, IC2,
    OV_nsptoc1_lvnstoc, NaSign_nsptoc1_lvnstoc,
    OV_ptrc1_ttoclgc, vnesh_pusk_ptrc1_ttoclgc, blok_lzt_ptrc1_ttoclgc,
    OV_tofflvlg, OVlo_tofflvlg, OVzapv_tofflvlg, OVzavr_tofflvlg,
    ):

        # Расчитываем аналоги
        threeI = ThreePhaseSystem(IA, dIA, IB, dIB, IC, dIC)
        Is = threeI.calculate_line_voltages()
        IAB = Is['Uab']['amplitude']/(3**0.5)
        IBC = Is['Ubc']['amplitude']/(3**0.5)
        ICA = Is['Uca']['amplitude']/(3**0.5)
        Isimm = threeI.calculate_symmetric_components()
        I1 = Isimm['U1']['amplitude']
        I2 = Isimm['U2']['amplitude']
        I0 = 3*Isimm['U2']['amplitude']        

        # Рассчитываем ТО
        vvod_ptoc1_lvtoc, oper_vyvod_ptoc1_lvtoc, pusk_ptoc1_lvtoc, io_ptoc1_lvtoc, srabsign_ptoc1_lvtoc, srab_ptoc1_lvtoc, ET_ptoc1_lvtoc =  self.lvtoc.Step(VYVOD, OV_ptoc1_lvtoc, NaSign_ptoc1_lvtoc, IA, IB, IC, IAB, IBC, ICA)
        # Рассчитываем ЗП
        vvod_hvptoc1_lovctoc, oper_vyvod_hvptoc1_lovctoc, pusk_hvptoc1_lovctoc, io_hvptoc1_lovctoc, srab_hvptoc1_lovctoc, srabotkl_hvptoc1_lovctoc, ET_hvptoc1_lovctoc = self.tovctoc.Step(VYVOD, OV_hvptoc1_lovctoc, NaOtkl_hvptoc1_lovctoc, IA, IB, IC)
        # Рассчитываем ТК ЗДЗ
        vvod_ptoc1_lvarctoc, oper_vyvod_ptoc1_lvarctoc, pusk_ptoc1_lvarctoc, io_ptoc1_lvarctoc =  self.lvarctoc.Step(VYVOD, OV_ptoc1_lvarctoc, IA, IB, IC, mtz1_pusk, mtz2_pusk, mtz3_pusk) 

        # Рассчитываем ТО РПН
        vvod_ptoc1_ltcblktoc, oper_vyvod_ptoc1_ltcblktoc, pusk_ptoc1_ltcblktoc, io_ptoc1_ltcblktoc = self.ltcblktoc.Step(VYVOD, OV_ptoc1_ltcblktoc, IA, IB, IC)      

        # Рассчитываем РТПО
        #vvod_hvptoc1_strpalc, oper_vyvod_hvptoc1_strpalc, pusk_hvptoc1_strpalc, io_hvptoc1_strpalc, vvod_lvptoc1_strpalc, oper_vyvod_lvptoc1_strpalc, pusk_lvptoc1_strpalc, io_lvptoc1_strpalc, vvod_lvptoc2_strpalc, oper_vyvod_lvptoc2_strpalc, pusk_lvptoc2_strpalc, io_lvptoc2_strpalc, pusk_strpalc, vvod_strpalc = self.strpalc.Step(VYVOD, OV_strpalc, OV_hvptoc1_strpalc, IA, IB, IC,  OV_lvptoc1_strpalc, IA1, IB1, IC1, OV_lvptoc2_strpalc, IA2, IB2, IC2)        
        # Рассчитываем ЗОП
        vvod_nsptoc1_lvnstoc, oper_vyvod_nsptoc1_lvnstoc, srab_nsptoc1_lvnstoc, srabsign_nsptoc1_lvnstoc, pusk_nsptoc1_lvnstoc, io_I2_nsptoc1_lvnstoc, io_rat_nsptoc1_lvnstoc, ET_nsptoc1_lvnstoc = self.lvnstoc.Step(VYVOD, OV_nsptoc1_lvnstoc, NaSign_nsptoc1_lvnstoc, I2, I1)
        # Рассчитываем ЛЗТ
        vvod_ptrc1_ttoclgc, oper_vyvod_ptrc1_ttoclgc, pusk_ptrc1_ttoclgc, srab_ptrc1_ttoclgc, ET_ptrc1_ttoclgc =  self.ttoclgc.Step(VYVOD, OV_ptrc1_ttoclgc, vnesh_pusk_ptrc1_ttoclgc, mtz2_pusk, mtz3_pusk, blok_lzt_ptrc1_ttoclgc)       
        # Рассчитываем ЛО Т
        vvod_ptrc1_tofflvlgc, oper_vyvod_ptrc1_tofflvlgc, pusk_ptrc1_tofflvlgc, srab_ptrc1_tofflvlgc, vvod_rblc1_tofflvlgc, oper_vyvod_rblc1_tofflvlgc, zapret_rblc1_tofflvlgc, vvod_rbre1_tofflvlgc, oper_vyvod_rbre1_tofflvlgc, zapret_rbre1_tofflvlgc = self.tofflvlgc.Step(VYVOD, OV_tofflvlg, OVlo_tofflvlg, signals_tofflvlg=(srab_ptoc1_lvtoc, srabotkl_hvptoc1_lovctoc, srab_nsptoc1_lvnstoc, srab_ptrc1_ttoclgc), mtz2_srab_tofflvlg=0, mtz3_srab_tofflvlg=0, OVzapv_tofflvlg=OVzapv_tofflvlg, OVzavr_tofflvlg=OVzavr_tofflvlg)
        # вычисляем ПС
        pusk_lvalh = self.lvalh.Step(VYVOD, sign_ps_tuple = (srab_hvptoc1_lovctoc, srabsign_nsptoc1_lvnstoc, srab_ptrc1_tofflvlgc))
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




            


