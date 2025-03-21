# ЧАСТЬ СХЕМЫ ФСУ ДЛЯ ПРОВЕРКИ ТОКОВЫХ ФУНКЦИЙ Т

# НЕ ДОДЕЛАНО!!!!!!

from lib._FBS.LVTOC import LVTOC # импорт ФБ ТО
from lib._FBS.TOVCTOC import TOVCTOC # импорт ФБ ЗП
from lib._FBS.LVARCTOC import LVARCTOC # импорт ФБ ТК ЗДЗ
from lib._FBS.STRPALC import STRPALC # импорт ФБ РТПО
from lib._FBS.LVNSTOC import LVNSTOC # импорт ФБ ЗОП
from lib._FBS.TTOCLGC import TTOCLGC # импорт ФБ ЛЗТ
from lib._FBS.TOFFLVLGC import TOFFLVLGC # импорт ЛО Т
from lib._FBS.T_LVALH import T_LVALH # импорт ПС Т
from lib._ADD.threePhaseSys import ThreePhaseSystem # класс для расчета аналоговых значений 

class partTOKZ:
    def __init__(self, SGF1_ptoc1_lvtoc, SGF2_ptoc1_lvtoc, T1_ptoc1_lvtoc, Iset_ptoc1_lvtoc,
                SGF1_hvptoc1_lovctoc, T1_hvptoc1_lovctoc, Iset_hvptoc1_lovctoc,
                SGF1_ptoc1_lvarctoc, SGF2_ptoc1_lvarctoc, Iset_ptoc1_lvarctoc,
                SGF1_hvptoc1_strpalc, Iset_hvptoc1_strpalc, SGF1_lvptoc1_strpalc, Iset_lvptoc1_strpalc, SGF1_lvptoc2_strpalc, Iset_lvptoc2_strpalc,
                SGF1_nsptoc1_lvnstoc, SGF2_nsptoc1_lvnstoc, T1_nsptoc1_lvnstoc, I2set_nsptoc1_lvnstoc, RatioSet_nsptoc1_lvnstoc, In_nsptoc1_lvnstoc,
                SGF1_ptrc1_ttoclgc, SGF2_ptrc1_ttoclgc, SGF3_ptrc1_ttoclgc, T1_ptrc1_ttoclgc,
                SGF1_ptrc1_tofflvlgc, SGF1_rbre1_tofflvlgc, SGF2_rbre1_tofflvlgc, SGF3_rbre1_tofflvlgc, SGF1_rblc1_tofflvlgc, SGF2_rblc1_tofflvlgc, SGF3_rblc1_tofflvlgc,

                ):

        self.lvtoc = LVTOC(SGF1_ptoc1_lvtoc, SGF2_ptoc1_lvtoc, T1_ptoc1_lvtoc, Iset_ptoc1_lvtoc)
        self.tovctoc = TOVCTOC(SGF1_hvptoc1_lovctoc, T1_hvptoc1_lovctoc, Iset_hvptoc1_lovctoc)
        self.lvarctoc = LVARCTOC(SGF1_ptoc1_lvarctoc, SGF2_ptoc1_lvarctoc, Iset_ptoc1_lvarctoc)
        self.strpalc = STRPALC(SGF1_hvptoc1_strpalc, Iset_hvptoc1_strpalc, SGF1_lvptoc1_strpalc, Iset_lvptoc1_strpalc, SGF1_lvptoc2_strpalc, Iset_lvptoc2_strpalc)
        self.lvnstoc = LVNSTOC(SGF1_nsptoc1_lvnstoc, SGF2_nsptoc1_lvnstoc, T1_nsptoc1_lvnstoc, I2set_nsptoc1_lvnstoc, RatioSet_nsptoc1_lvnstoc, In_nsptoc1_lvnstoc)
        self.ttoclgc = TTOCLGC(SGF1_ptrc1_ttoclgc, SGF2_ptrc1_ttoclgc, SGF3_ptrc1_ttoclgc, T1_ptrc1_ttoclgc)
        self.tofflvlgc = TOFFLVLGC(SGF1_ptrc1_tofflvlgc, SGF1_rbre1_tofflvlgc, SGF2_rbre1_tofflvlgc, SGF3_rbre1_tofflvlgc, SGF1_rblc1_tofflvlgc, SGF2_rblc1_tofflvlgc, SGF3_rblc1_tofflvlgc)
        self.lvalh = T_LVALH()    


#######################################
#######################################
#######################################


    def Step(self, VYVOD, OV_lvttoc, SV1vkl, SV2vkl, IA, dIA, IB, dIB, IC, dIC, VNN1vkl, VNN2vkl, 
        OVst_ptoc1, NaSign_ptoc1,
        OVst_ptoc2, NaSign_ptoc2,
        OVst_ptoc3, NaSign_ptoc3,
        KPONvnesh_ptuv1, UA1, dUA1, UB1, dUB1, UC1, dUC1,  
        KPONvnesh_ptuv2, UA2, dUA2, UB2, dUB2, UC2, dUC2, 
        IA2harm, IB2harm, IC2harm,
        OV_lvrbvtr1, vnesh_bnn_srab_lvrbvtr1,
        OV_lvrbvtr2, vnesh_bnn_srab_lvrbvtr2,
        OVlot, OVlo, OVzapv, OVzavr,
        ):

        # Расчитываем аналоги
        threeI = ThreePhaseSystem(IA, dIA, IB, dIB, IC, dIC)
        Is = threeI.calculate_line_voltages()
        IAB = Is['Uab']['amplitude']/(3**0.5)
        IBC = Is['Ubc']['amplitude']/(3**0.5)
        ICA = Is['Uca']['amplitude']/(3**0.5)
        threeU1 = ThreePhaseSystem(UA1, dUA1, UB1, dUB1, UC1, dUC1)
        U1s = threeU1.calculate_line_voltages()
        UAB_ptuv1 = U1s['Uab']['amplitude']
        UBC_ptuv1 = U1s['Ubc']['amplitude']
        UCA_ptuv1= U1s['Uca']['amplitude']
        U1simm = threeU1.calculate_symmetric_components()
        U2_ptuv1 = U1simm['U2']['amplitude']
        threeU2 = ThreePhaseSystem(UA2, dUA2, UB2, dUB2, UC2, dUC2)
        U2s = threeU2.calculate_line_voltages()
        UAB_ptuv2 = U2s['Uab']['amplitude']
        UBC_ptuv2 = U2s['Ubc']['amplitude']
        UCA_ptuv2= U2s['Uca']['amplitude']
        U2simm = threeU2.calculate_symmetric_components()
        U2_ptuv2 = U2simm['U2']['amplitude']

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

        U0_ptuv2 = 3*U2simm['U0']['amplitude']
        U1_ptuv2 = U2simm['U1']['amplitude']
        # вычисляем КЦН НН
        vvod_lvrbvtr1, oper_vyvod_lvrbvtr1, u_lin_pusk_lvrbvtr1, u2_pusk_lvrbvtr1, pusk_lvrbvtr1, neispr_zn_lvrbvtr1 = self.lvrbvtr1.Step(VYVOD, OV_lvrbvtr1, vnesh_bnn_srab_lvrbvtr1, UAB_ptuv1, UBC_ptuv1, UCA_ptuv1, U2_ptuv1)
        vvod_lvrbvtr2, oper_vyvod_lvrbvtr2, u_lin_pusk_lvrbvtr2, u2_pusk_lvrbvtr2, pusk_lvrbvtr2, neispr_zn_lvrbvtr2 = self.lvrbvtr2.Step(VYVOD, OV_lvrbvtr2, vnesh_bnn_srab_lvrbvtr2, UAB_ptuv2, UBC_ptuv2, UCA_ptuv2, U2_ptuv2)
        # вычисляем МТЗ
        vvod_ptoc1_lvttoc, oper_vyvod_ptoc1_lvttoc, mtzA_pusk_ptoc1_lvttoc, mtzB_pusk_ptoc1_lvttoc, mtzC_pusk_ptoc1_lvttoc, gen_pusk_ptoc1_lvttoc, mtz_srabsign_ptoc1_lvttoc, mtz_srab_ptoc1_lvttoc, io_A_ptoc1_lvttoc, io_B_ptoc1_lvttoc, io_C_ptoc1_lvttoc, vvod_ptoc2_lvttoc, oper_vyvod_ptoc2_lvttoc, mtzA_pusk_ptoc2_lvttoc, mtzB_pusk_ptoc2_lvttoc, mtzC_pusk_ptoc2_lvttoc, gen_pusk_ptoc2_lvttoc, mtz_srabsign_ptoc2_lvttoc, mtz_srab_ptoc2_lvttoc, io_A_ptoc2_lvttoc, io_B_ptoc2_lvttoc, io_C_ptoc2_lvttoc, vvod_ptoc3_lvttoc, oper_vyvod_ptoc3_lvttoc, mtzA_pusk_ptoc3_lvttoc, mtzB_pusk_ptoc3_lvttoc, mtzC_pusk_ptoc3_lvttoc, gen_pusk_ptoc3_lvttoc, mtz_srabsign_ptoc3_lvttoc, mtz_srab_ptoc3_lvttoc, io_A_ptoc3_lvttoc, io_B_ptoc3_lvttoc, io_C_ptoc3_lvttoc, kpon_pusk_ptuv1_lvttoc, kpon_pusk_ptuv2_lvttoc, ia_start_out_phar1_lvttoc, ib_start_out_phar1_lvttoc, ic_start_out_phar1_lvttoc, start_phar1_lvttoc, blok_rblc1_lvttoc, mtz_pusk_lvttoc = self.lvttoc.Step(VYVOD, OV_lvttoc, SV1vkl, SV2vkl, IA, IAB, IB, IBC, IC, ICA, neispr_zn_lvrbvtr1, VNN1vkl, neispr_zn_lvrbvtr2, VNN2vkl, OVst_ptoc1, NaSign_ptoc1, OVst_ptoc2, NaSign_ptoc2, OVst_ptoc3, NaSign_ptoc3, KPONvnesh_ptuv1, UAB_ptuv1, UBC_ptuv1, UCA_ptuv1, U2_ptuv1, KPONvnesh_ptuv2, UAB_ptuv2, UBC_ptuv2, UCA_ptuv2, U2_ptuv2, IA2harm, IB2harm, IC2harm)
        # вычисляем ЛО Т
        vvod_ptrc1, oper_vyvod_ptrc1, pusk_ptrc1, srab_ptrc1, vvod_rblc1, oper_vyvod_rblc1, zapret_rblc1, vvod_rbre1, oper_vyvod_rbre1, zapret_rbre1 = self.tofflvlgc.Step(VYVOD, OVlot, OVlo, (mtz_srab_ptoc1_lvttoc,), mtz_srab_ptoc2_lvttoc, mtz_srab_ptoc3_lvttoc, OVzapv, OVzavr)
        # вычисляем ПС
        pusk_lvalv = self.lvalv.Step(VYVOD, COMM_SIGN = (mtz_srabsign_ptoc1_lvttoc, mtz_srabsign_ptoc2_lvttoc, mtz_srabsign_ptoc3_lvttoc, srab_ptrc1, neispr_zn_lvrbvtr1, neispr_zn_lvrbvtr2))

        return (vvod_lvrbvtr1, oper_vyvod_lvrbvtr1, u_lin_pusk_lvrbvtr1, u2_pusk_lvrbvtr1, pusk_lvrbvtr1, neispr_zn_lvrbvtr1, 
        vvod_lvrbvtr2, oper_vyvod_lvrbvtr2, u_lin_pusk_lvrbvtr2, u2_pusk_lvrbvtr2, pusk_lvrbvtr2, neispr_zn_lvrbvtr2,
        vvod_ptoc1_lvttoc, oper_vyvod_ptoc1_lvttoc, mtzA_pusk_ptoc1_lvttoc, mtzB_pusk_ptoc1_lvttoc, mtzC_pusk_ptoc1_lvttoc, gen_pusk_ptoc1_lvttoc, mtz_srabsign_ptoc1_lvttoc, mtz_srab_ptoc1_lvttoc, io_A_ptoc1_lvttoc, io_B_ptoc1_lvttoc, io_C_ptoc1_lvttoc, vvod_ptoc2_lvttoc, oper_vyvod_ptoc2_lvttoc, mtzA_pusk_ptoc2_lvttoc, mtzB_pusk_ptoc2_lvttoc, mtzC_pusk_ptoc2_lvttoc, gen_pusk_ptoc2_lvttoc, mtz_srabsign_ptoc2_lvttoc, mtz_srab_ptoc2_lvttoc, io_A_ptoc2_lvttoc, io_B_ptoc2_lvttoc, io_C_ptoc2_lvttoc, vvod_ptoc3_lvttoc, oper_vyvod_ptoc3_lvttoc, mtzA_pusk_ptoc3_lvttoc, mtzB_pusk_ptoc3_lvttoc, mtzC_pusk_ptoc3_lvttoc, gen_pusk_ptoc3_lvttoc, mtz_srabsign_ptoc3_lvttoc, mtz_srab_ptoc3_lvttoc, io_A_ptoc3_lvttoc, io_B_ptoc3_lvttoc, io_C_ptoc3_lvttoc, kpon_pusk_ptuv1_lvttoc, kpon_pusk_ptuv2_lvttoc, ia_start_out_phar1_lvttoc, ib_start_out_phar1_lvttoc, ic_start_out_phar1_lvttoc, start_phar1_lvttoc, blok_rblc1_lvttoc, mtz_pusk_lvttoc, vvod_ptrc1, oper_vyvod_ptrc1, pusk_ptrc1, srab_ptrc1, vvod_rblc1, oper_vyvod_rblc1, zapret_rblc1, vvod_rbre1, oper_vyvod_rbre1, zapret_rbre1, pusk_lvalv, IAB, dIAB, IBC, dIBC, ICA, dICA, I2, I0, I1, UAB_ptuv1, UBC_ptuv1, UCA_ptuv1, U2_ptuv1, U0_ptuv1, U1_ptuv1, UAB_ptuv2, UBC_ptuv2, UCA_ptuv2, U2_ptuv2, U0_ptuv2, U1_ptuv2
        )
       

if __name__ == "__main__":
    part = partOfFsuInTOC(SGF1=1)
    res = part.Step(0, (0,0,0), 0,0,0,0,0,0,0,0,0,0,0,0,0)
    print(res)



            


