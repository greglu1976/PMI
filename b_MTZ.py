# ЧАСТЬ СХЕМЫ ФСУ ДЛЯ ПРОВЕРКИ МТЗ Т2
# 
# Максимальная токовая защита с пуском по напряжению (МТЗ/U) (LVTTOC)
# SGF1 - Сборка_ток_цепей - Сборка токовых цепей (Звезда/ Треугольник)

from LVTTOC_FB_MTZ import LVTTOC # импорт ФБ МТЗ
from T_LVRVTR import T_LVRVTR # импорт Ф КЦН НН
from TOFFLVLGC_FB_LO_T import TOFFLVLGC # импорт ЛО Т
from DZT2_LVALH import DZT2_LVALH # импорт ПС
from threePhaseSys import ThreePhaseSystem # клас для расчета аналоговых значений 

class partOfFsuInTOC:
    def __init__(self, SGF1, SGF1_ptoc1, SGF2_ptoc1, SGF3_ptoc1, SGF4_ptoc1, SGF5_ptoc1, SGF6_ptoc1, SGF7_ptoc1, T1_ptoc1, Iset_ptoc1, Icoarse_ptoc1,
                SGF1_ptoc2, SGF2_ptoc2, SGF3_ptoc2, SGF4_ptoc2, SGF5_ptoc2, SGF6_ptoc2, SGF7_ptoc2, T1_ptoc2, Iset_ptoc2, Icoarse_ptoc2,
                SGF1_ptoc3, SGF2_ptoc3, SGF3_ptoc3, SGF4_ptoc3, SGF5_ptoc3, SGF6_ptoc3, SGF7_ptoc3, T1_ptoc3, Iset_ptoc3, Icoarse_ptoc3,
                SGF1_ptuv1, Uop_ptuv1, U2op_ptuv1,
                SGF1_ptuv2, Uop_ptuv2, U2op_ptuv2,
                SGF1_phar1, Imax_phar1, Ratio_phar1,
                SGF1_rblc1,
                SGF1_lvrbvtr1, SGF2_lvrbvtr1, u_min_lvrbvtr1, u2_max_lvrbvtr1, t1_lvrbvtr1,
                SGF1_lvrbvtr2, SGF2_lvrbvtr2, u_min_lvrbvtr2, u2_max_lvrbvtr2, t1_lvrbvtr2,
                SGF1_ptrc1_tofflvlgc, SGF1_rbre1_tofflvlgc, SGF2_rbre1_tofflvlgc, SGF3_rbre1_tofflvlgc, SGF1_rblc1_tofflvlgc, SGF2_rblc1_tofflvlgc, SGF3_rblc1_tofflvlgc,
                ):
        # Инициализируем ФБ МТЗ Т2        
        self.lvttoc = LVTTOC(SGF1, SGF1_ptoc1, SGF2_ptoc1, SGF3_ptoc1, SGF4_ptoc1, SGF5_ptoc1, SGF6_ptoc1, SGF7_ptoc1, T1_ptoc1, Iset_ptoc1, Icoarse_ptoc1,
                SGF1_ptoc2, SGF2_ptoc2, SGF3_ptoc2, SGF4_ptoc2, SGF5_ptoc2, SGF6_ptoc2, SGF7_ptoc2, T1_ptoc2, Iset_ptoc2, Icoarse_ptoc2,
                SGF1_ptoc3, SGF2_ptoc3, SGF3_ptoc3, SGF4_ptoc3, SGF5_ptoc3, SGF6_ptoc3, SGF7_ptoc3, T1_ptoc3, Iset_ptoc3, Icoarse_ptoc3,
                SGF1_ptuv1, Uop_ptuv1, U2op_ptuv1,
                SGF1_ptuv2, Uop_ptuv2, U2op_ptuv2,
                SGF1_phar1, Imax_phar1, Ratio_phar1,
                SGF1_rblc1)
        # Инициализируем ФБ КЦН НН1 и КЦН НН2        
        self.lvrbvtr1 = T_LVRVTR(SGF1_lvrbvtr1, SGF2_lvrbvtr1, u_min_lvrbvtr1, u2_max_lvrbvtr1, t1_lvrbvtr1)
        self.lvrbvtr2 = T_LVRVTR(SGF1_lvrbvtr2, SGF2_lvrbvtr2, u_min_lvrbvtr2, u2_max_lvrbvtr2, t1_lvrbvtr2)
        # Инициализируем ФБ ЛО Т       
        self.tofflvlgc = TOFFLVLGC(SGF1_ptrc1_tofflvlgc, SGF1_rbre1_tofflvlgc, SGF2_rbre1_tofflvlgc, SGF3_rbre1_tofflvlgc, SGF1_rblc1_tofflvlgc, SGF2_rblc1_tofflvlgc, SGF3_rblc1_tofflvlgc)
        # ИНициализируем ПС
        self.lvalv = DZT2_LVALH(SGF1=0, SGF2=0, SGF3=0, SGF4=0, SGF5=0, SGF6=0, SGF7=0, SGF8=0, SGF9=0, SGF10=0, SGF11=0, SGF12=0, SGF13=0)

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



            


