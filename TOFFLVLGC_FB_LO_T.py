# (TOFFLVLGC) Функция ЛО Т - Логика отключения трансформатора 35 кВ (в составе устройства ЮНИТ-М3-Т)


from T_TJNTPTRC import T_TJNTPTRC
from T_JNTRBRE import T_JNTRBRE
from T_BTS1RBLC import T_BTS1RBLC


class TOFFLVLGC:
    def __init__(self, SGF1_ptrc1, SGF1_rbre1, SGF2_rbre1, SGF3_rbre1, SGF1_rblc1, SGF2_rblc1, SGF3_rblc1):
        self.ptrc1 = T_TJNTPTRC(SGF1_ptrc1)
        self.rbre1 = T_JNTRBRE(SGF1_rbre1, SGF2_rbre1, SGF3_rbre1)
        self.rblc1 = T_BTS1RBLC(SGF1_rblc1, SGF2_rblc1, SGF3_rblc1)

    def Step(self,  VYVOD, OV, OVlo, signals, mtz2_srab, mtz3_srab, OVzapv, OVzavr):

        # Предпредварительный обсчет ступеней МТЗ
        vvod_ptoc1, oper_vyvod_ptoc1 = self.ptoc1.PrePreStep(VYVOD, OV, OVst_ptoc1)
        vvod_ptoc2, oper_vyvod_ptoc2 = self.ptoc2.PrePreStep(VYVOD, OV, OVst_ptoc2)
        vvod_ptoc3, oper_vyvod_ptoc3 = self.ptoc3.PrePreStep(VYVOD, OV, OVst_ptoc3)

        # Обсчет КПОН
        # Собираем условия ввода
        vvod_kpon1 = (vvod_ptoc1 and (self.ptoc1.get_SGF5()==1)) or (vvod_ptoc2 and (self.ptoc2.get_SGF5()==1)) or (vvod_ptoc3 and (self.ptoc3.get_SGF5()==1))      
        kpon_pusk_ptuv1 = self.ptuv1.Step(vvod_kpon1, KPONvnesh_ptuv1, UAB_ptuv1, UBC_ptuv1, UCA_ptuv1, U2_ptuv1)
        vvod_kpon2 = (vvod_ptoc1 and (self.ptoc1.get_SGF6()==1)) or (vvod_ptoc2 and (self.ptoc2.get_SGF6()==1)) or (vvod_ptoc3 and (self.ptoc3.get_SGF6()==1))  
        kpon_pusk_ptuv2 = self.ptuv2.Step(vvod_kpon2, KPONvnesh_ptuv2, UAB_ptuv2, UBC_ptuv2, UCA_ptuv2, U2_ptuv2)

        # Предварительный обсчет ступеней МТЗ
        io_A_ptoc1, io_B_ptoc1, io_C_ptoc1, kpon_pusk_ptoc1, set_changer_ptoc1 = self.ptoc1.PreStep(Ia, Ib, Ic, KZN1neipr, kpon_pusk_ptuv1, VNN1vkl, KZN2neipr, kpon_pusk_ptuv2, VNN2vkl)
        io_A_ptoc2, io_B_ptoc2, io_C_ptoc2, kpon_pusk_ptoc2, set_changer_ptoc2 = self.ptoc2.PreStep(Ia, Ib, Ic, KZN1neipr, kpon_pusk_ptuv1, VNN1vkl, KZN2neipr, kpon_pusk_ptuv2, VNN2vkl)
        io_A_ptoc3, io_B_ptoc3, io_C_ptoc3, kpon_pusk_ptoc3, set_changer_ptoc3 = self.ptoc3.PreStep(Ia, Ib, Ic, KZN1neipr, kpon_pusk_ptuv1, VNN1vkl, KZN2neipr, kpon_pusk_ptuv2, VNN2vkl)

        # Обсчет БНТ
        # Собираем условия ввода
        vvod_bnt = (vvod_ptoc1 and (self.ptoc1.get_SGF3()==1)) or (vvod_ptoc2 and (self.ptoc2.get_SGF3()==1)) or (vvod_ptoc3 and (self.ptoc3.get_SGF3()==1))
        ia_start_out_phar1, ib_start_out_phar1, ic_start_out_phar1, start_phar1 = self.phar1.Step(vvod_bnt, (io_A_ptoc1, io_A_ptoc2, io_A_ptoc3), (io_B_ptoc1, io_B_ptoc2, io_B_ptoc3), (io_C_ptoc1, io_C_ptoc2, io_C_ptoc3), IA, IA2harm, IB, IB2harm, IC, IC2harm)

        # Второй шаг обсчета ступеней МТЗ , с известными значениями БНТ
        mtzA_pusk_ptoc1, mtzB_pusk_ptoc1, mtzC_pusk_ptoc1, gen_pusk_ptoc1, mtz_srabsign_ptoc1, mtz_srab_ptoc1, ET_ptoc1 = self.ptoc1.AfterStep(NaSign_ptoc1, SV1vkl, SV2vkl, io_A_ptoc1, io_B_ptoc1, io_C_ptoc1, ia_start_out_phar1, ib_start_out_phar1, ic_start_out_phar1, kpon_pusk_ptoc1, vvod_ptoc1)

        mtzA_pusk_ptoc2, mtzB_pusk_ptoc2, mtzC_pusk_ptoc2, gen_pusk_ptoc2, mtz_srabsign_ptoc2, mtz_srab_ptoc2, ET_ptoc2 = self.ptoc2.AfterStep(NaSign_ptoc2, SV1vkl, SV2vkl, io_A_ptoc2, io_B_ptoc2, io_C_ptoc2, ia_start_out_phar1, ib_start_out_phar1, ic_start_out_phar1, kpon_pusk_ptoc2, vvod_ptoc2)

        mtzA_pusk_ptoc3, mtzB_pusk_ptoc3, mtzC_pusk_ptoc3, gen_pusk_ptoc3, mtz_srabsign_ptoc3, mtz_srab_ptoc3, ET_ptoc3 = self.ptoc3.AfterStep(NaSign_ptoc3, SV1vkl, SV2vkl, io_A_ptoc3, io_B_ptoc3, io_C_ptoc3, ia_start_out_phar1, ib_start_out_phar1, ic_start_out_phar1, kpon_pusk_ptoc3, vvod_ptoc3)

        # Обсчет БЛЗШ
        blok_rblc1 = self.rblc1.Step(gen_pusk_ptoc1, gen_pusk_ptoc2, gen_pusk_ptoc3)

        # Сборка общего пуска
        mtz_pusk = gen_pusk_ptoc1 or gen_pusk_ptoc2 or gen_pusk_ptoc3

        return pusk             


