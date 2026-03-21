# ЧАСТЬ СХЕМЫ ФСУ ДЛЯ ПРОВЕРКИ МТЗ Т с учетом ТК ЗДЗ и ЛЗТ 
# 
# Максимальная токовая защита с пуском по напряжению (МТЗ/U) (LVTTOC)
# SGF1 - Сборка_ток_цепей - Сборка токовых цепей (Звезда/ Треугольник)

from lib2.FBS.LVTTOC_T import LVTTOC # импорт ФБ МТЗ Т
from lib2.FBS.T_LVRVTR import T_LVRVTR # импорт Ф КЦН НН
from lib2.FBS.TOFFLVLGC import TOFFLVLGC # импорт ЛО Т
from lib2.FBS.DZT2_LVALH import DZT2_LVALH # импорт ПС
from lib2.ADD.threePhaseSys import ThreePhaseSystem # класс для расчета аналоговых значений 

###########################################################
from lib2.FBS.LVARCTOC import LVARCTOC # импорт ФБ ТК ЗДЗ
from lib2.FBS.TTOCLGC import TTOCLGC # импорт ФБ ЛЗТ
###########################################################

class partOfFsuInTOC:
    def __init__(self, SGF1, SGF1_ptoc1, SGF2_ptoc1, SGF3_ptoc1, SGF4_ptoc1, SGF5_ptoc1, SGF6_ptoc1, T1_ptoc1, Iset_ptoc1, Icoarse_ptoc1,
                SGF1_ptoc2, SGF2_ptoc2, SGF3_ptoc2, SGF4_ptoc2, SGF5_ptoc2, SGF6_ptoc2, T1_ptoc2, Iset_ptoc2, Icoarse_ptoc2,
                SGF1_ptoc3, SGF2_ptoc3, SGF3_ptoc3, SGF4_ptoc3, SGF5_ptoc3, SGF6_ptoc3, T1_ptoc3, Iset_ptoc3, Icoarse_ptoc3,
                SGF1_ptuv1, Uop_ptuv1, U2op_ptuv1,
                #SGF1_ptuv2, Uop_ptuv2, U2op_ptuv2,
                SGF1_phar1, Imax_phar1, Ratio_phar1,
                SGF1_rblc1,
                SGF1_lvrbvtr1, SGF2_lvrbvtr1, u_min_lvrbvtr1, u2_max_lvrbvtr1, t1_lvrbvtr1,
                SGF1_ptrc1_tofflvlgc, SGF1_rbre1_tofflvlgc, SGF2_rbre1_tofflvlgc, SGF3_rbre1_tofflvlgc, SGF1_rblc1_tofflvlgc, SGF2_rblc1_tofflvlgc, SGF3_rblc1_tofflvlgc,
                SGF1_ptoc1_lvarctoc, SGF2_ptoc1_lvarctoc, Iset_ptoc1_lvarctoc,
                SGF1_ptrc1_ttoclgc, SGF2_ptrc1_ttoclgc, SGF3_ptrc1_ttoclgc, T1_ptrc1_ttoclgc,
                Inom
                ):
        # Инициализируем ФБ МТЗ Т       
        self.lvttoc = LVTTOC(SGF1, SGF1_ptoc1, SGF2_ptoc1, SGF3_ptoc1, SGF4_ptoc1, SGF5_ptoc1, SGF6_ptoc1, T1_ptoc1, Iset_ptoc1*Inom, Icoarse_ptoc1*Inom,
                SGF1_ptoc2, SGF2_ptoc2, SGF3_ptoc2, SGF4_ptoc2, SGF5_ptoc2, SGF6_ptoc2, T1_ptoc2, Iset_ptoc2*Inom, Icoarse_ptoc2*Inom,
                SGF1_ptoc3, SGF2_ptoc3, SGF3_ptoc3, SGF4_ptoc3, SGF5_ptoc3, SGF6_ptoc3, T1_ptoc3, Iset_ptoc3*Inom, Icoarse_ptoc3*Inom,
                SGF1_ptuv1, Uop_ptuv1, U2op_ptuv1,
                #SGF1_ptuv2, Uop_ptuv2, U2op_ptuv2,
                SGF1_phar1, Imax_phar1*Inom, Ratio_phar1,
                SGF1_rblc1)
        # Инициализируем ФБ КЦН НН    
        self.lvrbvtr1 = T_LVRVTR(SGF1_lvrbvtr1, SGF2_lvrbvtr1, u_min_lvrbvtr1, u2_max_lvrbvtr1, t1_lvrbvtr1)
        #self.lvrbvtr2 = T_LVRVTR(SGF1_lvrbvtr2, SGF2_lvrbvtr2, u_min_lvrbvtr2, u2_max_lvrbvtr2, t1_lvrbvtr2)
        # Инициализируем ФБ ЛО Т       
        self.tofflvlgc = TOFFLVLGC(SGF1_ptrc1_tofflvlgc, SGF1_rbre1_tofflvlgc, SGF2_rbre1_tofflvlgc, SGF3_rbre1_tofflvlgc, SGF1_rblc1_tofflvlgc, SGF2_rblc1_tofflvlgc, SGF3_rblc1_tofflvlgc)
        # ИНициализируем ПС
        self.lvalv = DZT2_LVALH(SGF1=0, SGF2=0, SGF3=0, SGF4=0, SGF5=0, SGF6=0, SGF7=0, SGF8=0, SGF9=0, SGF10=0, SGF11=0, SGF12=0, SGF13=0)

        ################################################################################################
        self.lvarctoc = LVARCTOC(SGF1_ptoc1_lvarctoc, SGF2_ptoc1_lvarctoc, Iset_ptoc1_lvarctoc*Inom)
        self.ttoclgc = TTOCLGC(SGF1_ptrc1_ttoclgc, SGF2_ptrc1_ttoclgc, SGF3_ptrc1_ttoclgc, T1_ptrc1_ttoclgc)
        ##################################################################################################

    def Step(self, DI_ControllerDisable, DI_LVTTOC, SBnnPosCls, IA, dIA, IB, dIB, IC, dIC, CBnnPosCls, 
        DI_PTOC1, DI_PTOC1_Sign,
        DI_PTOC2, DI_PTOC2_Sign,
        DI_PTOC3, DI_PTOC3_Sign,
        OutVoltStr, UA1, dUA1, UB1, dUB1, UC1, dUC1,  
        IA2harm, IB2harm, IC2harm,
        DI_LVRBVTR, OutBlkV,
        DI_TOFFLVLGC, DI_PTRC1, DI_RBRE1, DI_LVCBRBLC1,
        ):

        # Расчитываем аналоги
        threeI = ThreePhaseSystem(IA, dIA, IB, dIB, IC, dIC)
        Is = threeI.calculate_line_voltages()
        IAB = Is['Uab']['amplitude'] #/(3**0.5)
        IBC = Is['Ubc']['amplitude'] #/(3**0.5)
        ICA = Is['Uca']['amplitude'] #/(3**0.5)

        
        threeU1 = ThreePhaseSystem(UA1, dUA1, UB1, dUB1, UC1, dUC1)
        U1s = threeU1.calculate_line_voltages()
        UAB_ptuv1 = U1s['Uab']['amplitude']
        UBC_ptuv1 = U1s['Ubc']['amplitude']
        UCA_ptuv1= U1s['Uca']['amplitude']
        U1simm = threeU1.calculate_symmetric_components()
        U2_ptuv1 = U1simm['U2']['amplitude']

        # Нижерассчитанные значения используются ТОЛЬКО для индикации - в логике МТЗ не используются!!!
        Isimm = threeI.calculate_symmetric_components()
        dIAB = (Is['Uab']['angle'])
        dIBC = (Is['Ubc']['angle'])
        dICA = (Is['Uca']['angle'])
        I2 = Isimm['U2']['amplitude']
        I0 = 3*Isimm['U0']['amplitude']
        I1 = Isimm['U1']['amplitude'] 

        U0_ptuv1 = 3*U1simm['U0']['amplitude']
        U1_ptuv1 = U1simm['U1']['amplitude']

        # вычисляем КЦН НН
        vvod_lvrbvtr1, oper_vyvod_lvrbvtr1, u_lin_pusk_lvrbvtr1, u2_pusk_lvrbvtr1, pusk_lvrbvtr1, neispr_zn_lvrbvtr1 = self.lvrbvtr1.Step(DI_ControllerDisable, DI_LVRBVTR, OutBlkV, UAB_ptuv1, UBC_ptuv1, UCA_ptuv1, U2_ptuv1)
        #vvod_lvrbvtr2, oper_vyvod_lvrbvtr2, u_lin_pusk_lvrbvtr2, u2_pusk_lvrbvtr2, pusk_lvrbvtr2, neispr_zn_lvrbvtr2 = self.lvrbvtr2.Step(DI_ControllerDisable, OV_lvrbvtr2, vnesh_bnn_srab_lvrbvtr2, UAB_ptuv2, UBC_ptuv2, UCA_ptuv2, U2_ptuv2)
        # вычисляем МТЗ
        vvod_ptoc1_lvttoc, oper_vyvod_ptoc1_lvttoc, mtzA_pusk_ptoc1_lvttoc, mtzB_pusk_ptoc1_lvttoc, mtzC_pusk_ptoc1_lvttoc, gen_pusk_ptoc1_lvttoc, mtz_srabsign_ptoc1_lvttoc, mtz_srab_ptoc1_lvttoc, io_A_ptoc1_lvttoc, io_B_ptoc1_lvttoc, io_C_ptoc1_lvttoc, vvod_ptoc2_lvttoc, oper_vyvod_ptoc2_lvttoc, mtzA_pusk_ptoc2_lvttoc, mtzB_pusk_ptoc2_lvttoc, mtzC_pusk_ptoc2_lvttoc, gen_pusk_ptoc2_lvttoc, mtz_srabsign_ptoc2_lvttoc, mtz_srab_ptoc2_lvttoc, io_A_ptoc2_lvttoc, io_B_ptoc2_lvttoc, io_C_ptoc2_lvttoc, vvod_ptoc3_lvttoc, oper_vyvod_ptoc3_lvttoc, mtzA_pusk_ptoc3_lvttoc, mtzB_pusk_ptoc3_lvttoc, mtzC_pusk_ptoc3_lvttoc, gen_pusk_ptoc3_lvttoc, mtz_srabsign_ptoc3_lvttoc, mtz_srab_ptoc3_lvttoc, io_A_ptoc3_lvttoc, io_B_ptoc3_lvttoc, io_C_ptoc3_lvttoc, kpon_pusk_ptuv1_lvttoc, ia_start_out_phar1_lvttoc, ib_start_out_phar1_lvttoc, ic_start_out_phar1_lvttoc, start_phar1_lvttoc, blok_rblc1_lvttoc, mtz_pusk_lvttoc = self.lvttoc.Step(DI_ControllerDisable, DI_LVTTOC, SBnnPosCls, IA, IAB, IB, IBC, IC, ICA, neispr_zn_lvrbvtr1, CBnnPosCls, DI_PTOC1, DI_PTOC1_Sign, DI_PTOC2, DI_PTOC2_Sign, DI_PTOC3, DI_PTOC3_Sign, OutVoltStr, UAB_ptuv1, UBC_ptuv1, UCA_ptuv1, U2_ptuv1, IA2harm, IB2harm, IC2harm)

        # Рассчитываем ТК ЗДЗ
        OV_ptoc1_lvarctoc=0
        vvod_ptoc1_lvarctoc, oper_vyvod_ptoc1_lvarctoc, pusk_ptoc1_lvarctoc, io_ptoc1_lvarctoc =  self.lvarctoc.Step(DI_ControllerDisable, OV_ptoc1_lvarctoc, IA, IB, IC, gen_pusk_ptoc1_lvttoc, gen_pusk_ptoc2_lvttoc, gen_pusk_ptoc3_lvttoc) 
        # Рассчитываем ЛЗТ , переменные жестко задаем, т.к. они не отслеживаются в этой схеме
        OV_ptrc1_ttoclgc =0
        vnesh_pusk_ptrc1_ttoclgc = 0
        blok_lzt_ptrc1_ttoclgc = 0
        vvod_ptrc1_ttoclgc, oper_vyvod_ptrc1_ttoclgc, pusk_ptrc1_ttoclgc, srab_ptrc1_ttoclgc, ET_ptrc1_ttoclgc =  self.ttoclgc.Step(DI_ControllerDisable, OV_ptrc1_ttoclgc, vnesh_pusk_ptrc1_ttoclgc, gen_pusk_ptoc2_lvttoc, gen_pusk_ptoc3_lvttoc, blok_lzt_ptrc1_ttoclgc) 

        # вычисляем ЛО Т
        vvod_ptrc1, oper_vyvod_ptrc1, pusk_ptrc1, srab_ptrc1, vvod_rblc1, oper_vyvod_rblc1, zapret_rblc1, vvod_rbre1, oper_vyvod_rbre1, zapret_rbre1 = self.tofflvlgc.Step(DI_ControllerDisable, DI_TOFFLVLGC, DI_PTRC1, (mtz_srab_ptoc1_lvttoc,), mtz_srab_ptoc2_lvttoc, mtz_srab_ptoc3_lvttoc, DI_RBRE1, DI_LVCBRBLC1)
        # вычисляем ПС
        pusk_lvalv = self.lvalv.Step(DI_ControllerDisable, COMM_SIGN = (mtz_srabsign_ptoc1_lvttoc, mtz_srabsign_ptoc2_lvttoc, mtz_srabsign_ptoc3_lvttoc, srab_ptrc1, neispr_zn_lvrbvtr1))


        return (vvod_lvrbvtr1, oper_vyvod_lvrbvtr1, u_lin_pusk_lvrbvtr1, u2_pusk_lvrbvtr1, pusk_lvrbvtr1, neispr_zn_lvrbvtr1, 
                vvod_ptoc1_lvttoc, oper_vyvod_ptoc1_lvttoc, mtzA_pusk_ptoc1_lvttoc, mtzB_pusk_ptoc1_lvttoc, mtzC_pusk_ptoc1_lvttoc, gen_pusk_ptoc1_lvttoc, mtz_srabsign_ptoc1_lvttoc, mtz_srab_ptoc1_lvttoc, io_A_ptoc1_lvttoc, io_B_ptoc1_lvttoc, io_C_ptoc1_lvttoc, vvod_ptoc2_lvttoc, oper_vyvod_ptoc2_lvttoc, mtzA_pusk_ptoc2_lvttoc, mtzB_pusk_ptoc2_lvttoc, mtzC_pusk_ptoc2_lvttoc, gen_pusk_ptoc2_lvttoc, mtz_srabsign_ptoc2_lvttoc, mtz_srab_ptoc2_lvttoc, io_A_ptoc2_lvttoc, io_B_ptoc2_lvttoc, io_C_ptoc2_lvttoc, vvod_ptoc3_lvttoc, oper_vyvod_ptoc3_lvttoc, mtzA_pusk_ptoc3_lvttoc, mtzB_pusk_ptoc3_lvttoc, mtzC_pusk_ptoc3_lvttoc, gen_pusk_ptoc3_lvttoc, mtz_srabsign_ptoc3_lvttoc, mtz_srab_ptoc3_lvttoc, io_A_ptoc3_lvttoc, io_B_ptoc3_lvttoc, io_C_ptoc3_lvttoc, kpon_pusk_ptuv1_lvttoc, ia_start_out_phar1_lvttoc, ib_start_out_phar1_lvttoc, ic_start_out_phar1_lvttoc, start_phar1_lvttoc, blok_rblc1_lvttoc, mtz_pusk_lvttoc, vvod_ptrc1, oper_vyvod_ptrc1, pusk_ptrc1, srab_ptrc1, vvod_rblc1, oper_vyvod_rblc1, zapret_rblc1, vvod_rbre1, oper_vyvod_rbre1, zapret_rbre1, pusk_lvalv, pusk_ptoc1_lvarctoc, pusk_ptrc1_ttoclgc, IAB, dIAB, IBC, dIBC, ICA, dICA, I2, I0, I1, UAB_ptuv1, UBC_ptuv1, UCA_ptuv1, U2_ptuv1, U0_ptuv1, U1_ptuv1)
       
if __name__ == "__main__":
    part = partOfFsuInTOC(SGF1=1)
    res = part.Step(0, (0,0,0), 0,0,0,0,0,0,0,0,0,0,0,0,0)
    print(res)



            


