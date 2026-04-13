# ЧАСТЬ СХЕМЫ ФСУ ДЛЯ ПРОВЕРКИ ГАЗОВЫХ ЗАЩИТ
# ИСПОЛНЕНИЯ Т2


from lib2.FBS.TALMGASLGC import TALMGASLGC
from lib2.FBS.TTRGASLGC import TTRGASLGC
from lib2.FBS.TLTCGASLGC import TLTCGASLGC
from lib2.FBS.TOFFLVLGC import TOFFLVLGC # импорт ЛО Т
from lib2.FBS.T2_SignAssembly import T2_SignAssembly
from lib2.FBS.T2_LVALH import T2_LVALH # импорт ПС

class part_TECH_T2:
    def __init__(self, SGF1_ptrc1_talmgaslgc, SGF2_ptrc1_talmgaslgc, T1_ptrc1_talmgaslgc, SGF1_ptrc1_ttrgaslgc, SGF2_ptrc1_ttrgaslgc, T1_ptrc1_ttrgaslgc, SGF1_ptrc1_tltcgaslgc, SGF2_ptrc1_tltcgaslgc, T1_ptrc1_tltcgaslgc, SGF1_ptrc1_tofflvlgc, SGF1_rbre1_tofflvlgc, SGF2_rbre1_tofflvlgc, SGF3_rbre1_tofflvlgc, SGF1_rblc1_tofflvlgc, SGF2_rblc1_tofflvlgc, SGF3_rblc1_tofflvlgc, SGF1_t_lvalh, SGF2_t_lvalh, SGF3_t_lvalh, SGF4_t_lvalh, SGF5_t_lvalh, SGF6_t_lvalh, SGF7_t_lvalh, SGF8_t_lvalh, SGF9_t_lvalh, SGF10_t_lvalh, SGF1_t_signassembly, SGF2_t_signassembly, SGF3_t_signassembly, SGF4_t_signassembly, SGF5_t_signassembly, SGF6_t_signassembly, SGF7_t_signassembly, SGF8_t_signassembly, SGF9_t_signassembly, SGF10_t_signassembly, SGF11_t_signassembly, SGF12_t_signassembly, SGF13_t_signassembly, SGF14_t_signassembly, SGF15_t_signassembly, SGF16_t_signassembly, SGF17_t_signassembly):

        # Инициализируем ФБ ГЗ сигн
        self.talmgaslgc =  TALMGASLGC(SGF1_ptrc1_talmgaslgc, SGF2_ptrc1_talmgaslgc, T1_ptrc1_talmgaslgc)
        # Инициализируем ФБ ГЗ откл
        self.ttrgaslgc = TTRGASLGC(SGF1_ptrc1_ttrgaslgc, SGF2_ptrc1_ttrgaslgc, T1_ptrc1_ttrgaslgc)
        # Инициализируем ФБ ГЗ РПН
        self.tltcgaslgc = TLTCGASLGC(SGF1_ptrc1_tltcgaslgc, SGF2_ptrc1_tltcgaslgc, T1_ptrc1_tltcgaslgc)
        # Инициализируем ФБ ЛО Т       
        self.tofflvlgc = TOFFLVLGC(SGF1_ptrc1_tofflvlgc, SGF1_rbre1_tofflvlgc, SGF2_rbre1_tofflvlgc, SGF3_rbre1_tofflvlgc, SGF1_rblc1_tofflvlgc, SGF2_rblc1_tofflvlgc, SGF3_rblc1_tofflvlgc)
        # Инициализируем СС
        self.t_signassembly = T2_SignAssembly(SGF1_t_signassembly, SGF2_t_signassembly, SGF3_t_signassembly, SGF4_t_signassembly, SGF5_t_signassembly, SGF6_t_signassembly, SGF7_t_signassembly, SGF8_t_signassembly, SGF9_t_signassembly, SGF10_t_signassembly, SGF11_t_signassembly, SGF12_t_signassembly, SGF13_t_signassembly, SGF14_t_signassembly, SGF15_t_signassembly, SGF16_t_signassembly, SGF17_t_signassembly)
        # ИНициализируем ПС
        self.lvalh = T2_LVALH(SGF1_t_lvalh, SGF2_t_lvalh, SGF3_t_lvalh, SGF4_t_lvalh, SGF5_t_lvalh, SGF6_t_lvalh, SGF7_t_lvalh, SGF8_t_lvalh, SGF9_t_lvalh, SGF10_t_lvalh)

    def Step(self, DI_ControllerDisable, Reset, DI_TALMGASLGC, DI_TALMGASLGC_Sign, TALMGASLGC_1_SignContact, GASSignIsolOp, DI_TTRGASLGC, DI_TTRGASLGC_Sign, TTRGASLGC_1_TripContact, GASTripIsolOp, DI_TLTCGASLGC, DI_TLTCGASLGC_Sign, JetRelayContact, GASLTCIsolOp, DI_TRESOFFLVLGS, DI_PTRC1, DI_RBRE1, DI_LVCBRBLC1):

        # Вычисляем ГЗ сигн
        vvod_ptrc1_talmgaslgc, oper_vyvod_ptrc1_talmgaslgc, srab_ptrc1_talmgaslgc, srabsign_ptrc1_talmgaslgc, zablok_ptrc1_talmgaslgc, ET_ptrc1_talmgaslgc = self.talmgaslgc.Step(DI_ControllerDisable, DI_TALMGASLGC, DI_TALMGASLGC_Sign, TALMGASLGC_1_SignContact, GASSignIsolOp, Reset)
        # Вычисляем ГЗ откл
        OV_f = 0
        vvod_ptrc1_ttrgaslgc, oper_vyvod_ptrc1_ttrgaslgc, srab_ptrc1_ttrgaslgc, srabsign_ptrc1_ttrgaslgc, zablok_ptrc1_ttrgaslgc, ET_ptrc1_ttrgaslgc = self.ttrgaslgc.Step(DI_ControllerDisable, DI_TTRGASLGC, OV_f, DI_TTRGASLGC_Sign, TTRGASLGC_1_TripContact, GASTripIsolOp, Reset)
        # Вычисляем ГЗ РПН
        vvod_ptrc1_tltcgaslgc, oper_vyvod_ptrc1_tltcgaslgc, srab_ptrc1_tltcgaslgc, srabsign_ptrc1_tltcgaslgc, zablok_ptrc1_tltcgaslgc, ET_ptrc1_tltcgaslgc = self.tltcgaslgc.Step(DI_ControllerDisable, DI_TLTCGASLGC, OV_f, DI_TLTCGASLGC_Sign, JetRelayContact, GASLTCIsolOp, Reset)
        # Собираем кортеж срабатываний
        signals_tofflvlg = (srab_ptrc1_talmgaslgc, srab_ptrc1_ttrgaslgc, srab_ptrc1_tltcgaslgc) 
        # Зануляем сраб МТЗ, здесь не требуется - а передать значения нужно
        mtz2_srab_tofflvlg=0
        mtz3_srab_tofflvlg=0
        # вычисляем ЛО Т
        vvod_ptrc1_tofflvlgc, oper_vyvod_ptrc1_tofflvlgc, pusk_ptrc1_tofflvlgc, srab_ptrc1_tofflvlgc, vvod_rblc1_tofflvlgc, oper_vyvod_rblc1_tofflvlgc, zapret_rblc1_tofflvlgc, vvod_rbre1_tofflvlgc, oper_vyvod_rbre1_tofflvlgc, zapret_rbre1_tofflvlgc = self.tofflvlgc.Step(DI_ControllerDisable, DI_TRESOFFLVLGS, DI_PTRC1, signals_tofflvlg, mtz2_srab_tofflvlg, mtz3_srab_tofflvlg, DI_RBRE1, DI_LVCBRBLC1)
        # вычисляем СС
        SS_gz_sign, SS_gz_zablok, SS_gz_nizk_isol, SS_vnesh_otkl, SS_vyh_zepi_razobr, SS_bi_vyved, SS_ot_sign, SS_neispr_ot_gz, SS_neispr_ot_v, SS_ot_nn_sign, SS_prev_vrem_per_ka, SS_obsh_vnesh_sign = self.t_signassembly.Step(DI_ControllerDisable, gz_sign=(TALMGASLGC_1_SignContact, TTRGASLGC_1_TripContact, JetRelayContact), gz_zablok=(zablok_ptrc1_talmgaslgc, zablok_ptrc1_ttrgaslgc, zablok_ptrc1_tltcgaslgc), gz_ki=(GASSignIsolOp, GASTripIsolOp, GASLTCIsolOp),  vnesh_otkl=(0, 0), Polozh_SA1=0, Polozh_SA2=0, Polozh_SA3=0, Polozh_SA4=0, Polozh_SA5=0, Polozh_SA6=0,Polozh_SG1=0, Polozh_SG2=0, Polozh_SG3=0, ot_gz=0, ot_v=0, ot_zdz_nn1=0, ot_zdz_nn2=0, ot_urov_nn1=0, ot_urov_nn2=0, ot_ieu_tn1=0, ot_ieu_tn2=0, prev_vrem_ka=(0,), vnesh_sign=(0,)) # Обнулили контроль SA SG и пр. Здесь не проверяются эти цепи

        # вычисляем ПС
        pusk_lvalh = self.lvalh.Step(DI_ControllerDisable, COMM_SIGN=(srabsign_ptrc1_talmgaslgc, srabsign_ptrc1_ttrgaslgc, srabsign_ptrc1_tltcgaslgc, srab_ptrc1_tofflvlgc), sgf1_sign=SS_gz_sign, sgf2_sign=SS_gz_nizk_isol, sgf3_sign=SS_gz_zablok, sgf4_sign=SS_ot_sign, sgf5_sign=SS_ot_nn_sign, sgf6_sign=SS_vnesh_otkl, sgf7_sign=SS_vyh_zepi_razobr, sgf8_sign=SS_bi_vyved, sgf9_sign=SS_prev_vrem_per_ka, sgf10_sign=SS_obsh_vnesh_sign)

        return (vvod_ptrc1_talmgaslgc, oper_vyvod_ptrc1_talmgaslgc, srab_ptrc1_talmgaslgc, srabsign_ptrc1_talmgaslgc, zablok_ptrc1_talmgaslgc, ET_ptrc1_talmgaslgc, vvod_ptrc1_ttrgaslgc, oper_vyvod_ptrc1_ttrgaslgc, srab_ptrc1_ttrgaslgc, srabsign_ptrc1_ttrgaslgc, zablok_ptrc1_ttrgaslgc, ET_ptrc1_ttrgaslgc, vvod_ptrc1_tltcgaslgc, oper_vyvod_ptrc1_tltcgaslgc, srab_ptrc1_tltcgaslgc, srabsign_ptrc1_tltcgaslgc, zablok_ptrc1_tltcgaslgc, ET_ptrc1_tltcgaslgc, vvod_ptrc1_tofflvlgc, oper_vyvod_ptrc1_tofflvlgc, pusk_ptrc1_tofflvlgc, srab_ptrc1_tofflvlgc, vvod_rblc1_tofflvlgc, oper_vyvod_rblc1_tofflvlgc, zapret_rblc1_tofflvlgc, vvod_rbre1_tofflvlgc, oper_vyvod_rbre1_tofflvlgc, zapret_rbre1_tofflvlgc, SS_gz_sign, SS_gz_zablok, SS_gz_nizk_isol, SS_vnesh_otkl, SS_vyh_zepi_razobr, SS_bi_vyved, SS_ot_sign, SS_neispr_ot_gz, SS_neispr_ot_v, SS_ot_nn_sign, SS_prev_vrem_per_ka, SS_obsh_vnesh_sign, pusk_lvalh)
       

if __name__ == "__main__":
    part = part_TECH_T2()
    res = part.Step(0, (0,0,0), 0,0,0,0,0,0,0,0,0,0,0,0,0)
    print(res)



            


