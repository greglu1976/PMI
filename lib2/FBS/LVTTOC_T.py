# Функциональный блок LVTTOC для Т
# Максимальная токовая защита с пуском по напряжению (МТЗ/U) (LVTTOC)
# SGF1 - Сборка_ток_цепей - Сборка токовых цепей (Звезда/ Треугольник)

from lib2.FUNCS.LVTPTOC_T import LVTPTOC
from lib2.FUNCS.VCPTUV import VCPTUV
from lib2.FUNCS.TOCPHAR import TOCPHAR
from lib2.FUNCS.LBPRBLC import LBPRBLC

class LVTTOC:
    def __init__(self, SGF1, SGF1_ptoc1, SGF2_ptoc1, SGF3_ptoc1, SGF4_ptoc1, SGF5_ptoc1, SGF6_ptoc1, T1_ptoc1, Iset_ptoc1, Icoarse_ptoc1,
                    SGF1_ptoc2, SGF2_ptoc2, SGF3_ptoc2, SGF4_ptoc2, SGF5_ptoc2, SGF6_ptoc2, T1_ptoc2, Iset_ptoc2, Icoarse_ptoc2,
                    SGF1_ptoc3, SGF2_ptoc3, SGF3_ptoc3, SGF4_ptoc3, SGF5_ptoc3, SGF6_ptoc3, T1_ptoc3, Iset_ptoc3, Icoarse_ptoc3,
                    SGF1_ptuv1, Uop_ptuv1, U2op_ptuv1,
                    SGF1_phar1, Imax_phar1, Ratio_phar1,
                    SGF1_rblc1
    ):
        self.ptoc1 = LVTPTOC(SGF1_ptoc1, SGF2_ptoc1, SGF3_ptoc1, SGF4_ptoc1, SGF5_ptoc1, SGF6_ptoc1, T1_ptoc1, Iset_ptoc1, Icoarse_ptoc1)
        self.ptoc2 = LVTPTOC(SGF1_ptoc2, SGF2_ptoc2, SGF3_ptoc2, SGF4_ptoc2, SGF5_ptoc2, SGF6_ptoc2, T1_ptoc2, Iset_ptoc2, Icoarse_ptoc2)
        self.ptoc3 = LVTPTOC(SGF1_ptoc3, SGF2_ptoc3, SGF3_ptoc3, SGF4_ptoc3, SGF5_ptoc3, SGF6_ptoc3, T1_ptoc3, Iset_ptoc3, Icoarse_ptoc3)
        self.ptuv1 = VCPTUV(SGF1_ptuv1, Uop_ptuv1, U2op_ptuv1)
        self.phar1 = TOCPHAR(SGF1_phar1, Imax_phar1, Ratio_phar1)
        self.rblc1 = LBPRBLC(SGF1_rblc1)
        self.SGF1 = SGF1


    def Step(self, VYVOD, OV, SV1vkl, IA, IAB, IB, IBC, IC, ICA, KZN1neipr, VNN1vkl, 
        OVst_ptoc1, NaSign_ptoc1,
        OVst_ptoc2, NaSign_ptoc2,
        OVst_ptoc3, NaSign_ptoc3,
        KPONvnesh_ptuv1, UAB_ptuv1, UBC_ptuv1, UCA_ptuv1, U2_ptuv1, 
        IA2harm, IB2harm, IC2harm):

        # Переключение с фазных на линейные токи
        Ia = IA if (self.SGF1==0) else IAB
        Ib = IB if (self.SGF1==0) else IBC
        Ic = IC if (self.SGF1==0) else ICA

        # Предпредварительный обсчет ступеней МТЗ
        vvod_ptoc1, oper_vyvod_ptoc1 = self.ptoc1.PrePreStep(VYVOD, OV, OVst_ptoc1)
        vvod_ptoc2, oper_vyvod_ptoc2 = self.ptoc2.PrePreStep(VYVOD, OV, OVst_ptoc2)
        vvod_ptoc3, oper_vyvod_ptoc3 = self.ptoc3.PrePreStep(VYVOD, OV, OVst_ptoc3)

        # Обсчет КПОН
        # Собираем условия ввода
        vvod_kpon1 = (vvod_ptoc1 and (self.ptoc1.get_SGF5()==1)) or (vvod_ptoc2 and (self.ptoc2.get_SGF5()==1)) or (vvod_ptoc3 and (self.ptoc3.get_SGF5()==1))      
        kpon_pusk_ptuv1 = self.ptuv1.Step(vvod_kpon1, KPONvnesh_ptuv1, UAB_ptuv1, UBC_ptuv1, UCA_ptuv1, U2_ptuv1)
        #vvod_kpon2 = (vvod_ptoc1 and (self.ptoc1.get_SGF6()==1)) or (vvod_ptoc2 and (self.ptoc2.get_SGF6()==1)) or (vvod_ptoc3 and (self.ptoc3.get_SGF6()==1))  
        #kpon_pusk_ptuv2 = self.ptuv2.Step(vvod_kpon2, KPONvnesh_ptuv2, UAB_ptuv2, UBC_ptuv2, UCA_ptuv2, U2_ptuv2)

        # Предварительный обсчет ступеней МТЗ
        io_A_ptoc1, io_B_ptoc1, io_C_ptoc1, kpon_pusk_ptoc1, set_changer_ptoc1 = self.ptoc1.PreStep(Ia, Ib, Ic, KZN1neipr, kpon_pusk_ptuv1, VNN1vkl)
        io_A_ptoc2, io_B_ptoc2, io_C_ptoc2, kpon_pusk_ptoc2, set_changer_ptoc2 = self.ptoc2.PreStep(Ia, Ib, Ic, KZN1neipr, kpon_pusk_ptuv1, VNN1vkl)
        io_A_ptoc3, io_B_ptoc3, io_C_ptoc3, kpon_pusk_ptoc3, set_changer_ptoc3 = self.ptoc3.PreStep(Ia, Ib, Ic, KZN1neipr, kpon_pusk_ptuv1, VNN1vkl)

        # Обсчет БНТ
        # Собираем условия ввода
        vvod_bnt = (vvod_ptoc1 and (self.ptoc1.get_SGF3()==1)) or (vvod_ptoc2 and (self.ptoc2.get_SGF3()==1)) or (vvod_ptoc3 and (self.ptoc3.get_SGF3()==1))
        ia_start_out_phar1, ib_start_out_phar1, ic_start_out_phar1, start_phar1 = self.phar1.Step(vvod_bnt, (io_A_ptoc1, io_A_ptoc2, io_A_ptoc3), (io_B_ptoc1, io_B_ptoc2, io_B_ptoc3), (io_C_ptoc1, io_C_ptoc2, io_C_ptoc3), IA, IA2harm, IB, IB2harm, IC, IC2harm)


        # Второй шаг обсчета ступеней МТЗ , с известными значениями БНТ
        mtzA_pusk_ptoc1, mtzB_pusk_ptoc1, mtzC_pusk_ptoc1, gen_pusk_ptoc1, mtz_srabsign_ptoc1, mtz_srab_ptoc1, ET_ptoc1 = self.ptoc1.AfterStep(NaSign_ptoc1, SV1vkl, io_A_ptoc1, io_B_ptoc1, io_C_ptoc1, ia_start_out_phar1, ib_start_out_phar1, ic_start_out_phar1, kpon_pusk_ptoc1, vvod_ptoc1)

        mtzA_pusk_ptoc2, mtzB_pusk_ptoc2, mtzC_pusk_ptoc2, gen_pusk_ptoc2, mtz_srabsign_ptoc2, mtz_srab_ptoc2, ET_ptoc2 = self.ptoc2.AfterStep(NaSign_ptoc2, SV1vkl, io_A_ptoc2, io_B_ptoc2, io_C_ptoc2, ia_start_out_phar1, ib_start_out_phar1, ic_start_out_phar1, kpon_pusk_ptoc2, vvod_ptoc2)

        mtzA_pusk_ptoc3, mtzB_pusk_ptoc3, mtzC_pusk_ptoc3, gen_pusk_ptoc3, mtz_srabsign_ptoc3, mtz_srab_ptoc3, ET_ptoc3 = self.ptoc3.AfterStep(NaSign_ptoc3, SV1vkl, io_A_ptoc3, io_B_ptoc3, io_C_ptoc3, ia_start_out_phar1, ib_start_out_phar1, ic_start_out_phar1, kpon_pusk_ptoc3, vvod_ptoc3)

        # Обсчет БЛЗШ
        blok_rblc1 = self.rblc1.Step(gen_pusk_ptoc1, gen_pusk_ptoc2, gen_pusk_ptoc3)

        # Сборка общего пуска
        mtz_pusk = gen_pusk_ptoc1 or gen_pusk_ptoc2 or gen_pusk_ptoc3

        return (vvod_ptoc1, oper_vyvod_ptoc1, mtzA_pusk_ptoc1, mtzB_pusk_ptoc1, mtzC_pusk_ptoc1, gen_pusk_ptoc1, mtz_srabsign_ptoc1, mtz_srab_ptoc1, io_A_ptoc1, io_B_ptoc1, io_C_ptoc1,
                vvod_ptoc2, oper_vyvod_ptoc2, mtzA_pusk_ptoc2, mtzB_pusk_ptoc2, mtzC_pusk_ptoc2, gen_pusk_ptoc2, mtz_srabsign_ptoc2, mtz_srab_ptoc2, io_A_ptoc2, io_B_ptoc2, io_C_ptoc2,
                vvod_ptoc3, oper_vyvod_ptoc3, mtzA_pusk_ptoc3, mtzB_pusk_ptoc3, mtzC_pusk_ptoc3, gen_pusk_ptoc3, mtz_srabsign_ptoc3, mtz_srab_ptoc3, io_A_ptoc3, io_B_ptoc3, io_C_ptoc3,
                kpon_pusk_ptuv1, 
                ia_start_out_phar1, ib_start_out_phar1, ic_start_out_phar1, start_phar1,
                blok_rblc1, mtz_pusk)               


