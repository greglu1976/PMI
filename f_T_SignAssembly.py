# СС для исполнения Т

class T_SignAssembly:
    def __init__(self, SGF1_t_signassembly, SGF2_t_signassembly, SGF3_t_signassembly, SGF4_t_signassembly, SGF5_t_signassembly, SGF6_t_signassembly, SGF7_t_signassembly, SGF8_t_signassembly, SGF9_t_signassembly, SGF10_t_signassembly, SGF11_t_signassembly, SGF12_t_signassembly, SGF13_t_signassembly):
        self.SGF1 = SGF1_t_signassembly
        self.SGF2 = SGF2_t_signassembly
        self.SGF3 = SGF3_t_signassembly
        self.SGF4 = SGF4_t_signassembly
        self.SGF5 = SGF5_t_signassembly
        self.SGF6 = SGF6_t_signassembly
        self.SGF7 = SGF7_t_signassembly
        self.SGF8 = SGF8_t_signassembly
        self.SGF9 = SGF9_t_signassembly
        self.SGF10 = SGF10_t_signassembly
        self.SGF11 = SGF11_t_signassembly
        self.SGF12 = SGF12_t_signassembly
        self.SGF13 = SGF13_t_signassembly

    def Step(self, VYVOD, gz_sign, gz_zablok, gz_ki, tz_sign, tz_ki, tz_zablok, ts_sign, vnesh_otkl, Polozh_SA1, Polozh_SA2, Polozh_SA3, Polozh_SA4, Polozh_SA5, Polozh_SG1, Polozh_SG2, ot_gz, ot_tz, ot_v, ot_zdz_nn, ot_urov_nn, ot_ieu_tn, prev_vrem_ka, vnesh_sign):
        SS_gz_sign = any(gz_sign) and (not VYVOD)
        SS_gz_zablok = any(gz_zablok) and (not VYVOD)
        SS_gz_nizk_isol = any(gz_ki) and (not VYVOD)
        SS_tz_sign = any(tz_sign) and (not VYVOD)
        SS_tz_nizk_isol = any(tz_ki) and (not VYVOD)
        SS_tz_zablok = any(tz_zablok) and (not VYVOD)
        SS_ts_sign = any(ts_sign) and (not VYVOD)
        SS_vnesh_otkl = any(vnesh_otkl) and (not VYVOD)
        SS_vyh_zepi_razobr = ((0 if self.SGF1==0 else (not Polozh_SA1)) or (0 if self.SGF2==0 else (not Polozh_SA2)) or (0 if self.SGF3==0 else (not Polozh_SA3)) or (0 if self.SGF4==0 else (not Polozh_SA4)) or (0 if self.SGF5==0 else (not Polozh_SA5))) and (not VYVOD)
        SS_bi_vyved = ((0 if self.SGF6==0 else (not Polozh_SG1)) or (0 if self.SGF7==0 else (not Polozh_SG2))) and (not VYVOD)
        SS_neispr_ot_gz = (0 if self.SGF8==0 else (not ot_gz)) and (not VYVOD) 
        SS_neispr_ot_tz = (0 if self.SGF9==0 else (not ot_tz)) and (not VYVOD)
        SS_neispr_ot_v = (0 if self.SGF10==0 else (not ot_v)) and (not VYVOD)
        SS_ot_sign = SS_neispr_ot_gz or SS_neispr_ot_tz or SS_neispr_ot_v
        SS_ot_nn_sign = ((0 if self.SGF11==0 else (not ot_zdz_nn)) or (0 if self.SGF12==0 else (not ot_urov_nn)) or (0 if self.SGF13==0 else (not ot_ieu_tn))) and (not VYVOD)
        SS_prev_vrem_per_ka = any(prev_vrem_ka) and (not VYVOD)
        SS_obsh_vnesh_sign = any(vnesh_sign) and (not VYVOD)
        return (SS_gz_sign, SS_gz_zablok, SS_gz_nizk_isol, SS_tz_sign, SS_tz_nizk_isol, SS_tz_zablok, SS_ts_sign, SS_vnesh_otkl, SS_vyh_zepi_razobr, SS_bi_vyved, SS_ot_sign, SS_neispr_ot_gz,  SS_neispr_ot_tz, SS_neispr_ot_v, SS_ot_nn_sign, SS_prev_vrem_per_ka, SS_obsh_vnesh_sign)

        
                  