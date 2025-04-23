
from lib._FBS.TDIF import TDIF

tdif1 = TDIF(
        Sbaz=10e+6, Ubaz_vn=36750, Ubaz_nn=10500, Iperv_vn = 1000, Iperv_nn = 5000, Inom_term_vn =1, Inom_term_nn =1, Ivtor_vn =1, Ivtor_nn =5, k_sch_vn =1, k_sch_nn =1, n_sch_vn =0, n_sch_nn=5, compens_3i0_vn=False, compens_3i0_nn=False,
        SGF1_pdif1_tdif=1, SGF2_pdif1_tdif=1, SGF3_pdif1_tdif=0, T1_pdif1_tdif=0, Isr_pdif1_tdif=0.2, Isr_zagrub_pdif1_tdif=1.0, It1_pdif1_tdif=1, It2_pdif1_tdif=3, Kt1_pdif1_tdif=0.25, Kt2_pdif1_tdif=0.7,
        SGF1_pdif2_tdif=1, T1_pdif2_tdif=0, Iset_pdif2_tdif=6,
        SGF1_hf2phar1_tdif=0, T1_hf2phar1_tdif=1, T2_hf2phar1_tdif=1, Ratio_hf2phar1_tdif=0.3,
        SGF1_hf5phar1_tdif=0, T1_hf5phar1_tdif=1, T2_hf5phar1_tdif=1, Ratio_hf5phar1_tdif=0.2,
        SGF1_rctr1_tdif=1, T1_rctr1_tdif=0, Iset_rctr1_tdif=0.1)


VYVOD = OV_tdif = OV_pdif2_tdif = OV_pdif1_tdif = OV_rctr1_tdif = 0
NaSign_pdif2_tdif = NaSign_pdif1_tdif = 0
'''
IA_vn = 0.157
dIA_vn = 0
IB_vn = 0.157
dIB_vn = 240
IC_vn = 0.157
dIC_vn = 120
IA_nn = 0.55
dIA_nn = 30
IB_nn = 0.55
dIB_nn = -90
IC_nn = 0.55
dIC_nn = 150
'''
IA_vn = 0.157
dIA_vn = 0
IB_vn = 0.0
dIB_vn = 240
IC_vn = 0.0
dIC_vn = 120
IA_nn = 0.55
dIA_nn = 30
IB_nn = 0.0
dIB_nn = -90
IC_nn = 0.0
dIC_nn = 150


IAdiff2h = 0
IBdiff2h = ICdiff2h = 0.0
IAdiff5h = IBdiff5h = ICdiff5h = 0.0
CurCirc = 0


vvod_pdif2_tdif, oper_vyvod_pdif2_tdif, pusk_A_pdif2_tdif, srab_A_pdif2_tdif, srabsign_A_pdif2_tdif, io_A_pdif2_tdif, pusk_B_pdif2_tdif, srab_B_pdif2_tdif, srabsign_B_pdif2_tdif, io_B_pdif2_tdif, pusk_C_pdif2_tdif, srab_C_pdif2_tdif, srabsign_C_pdif2_tdif, io_C_pdif2_tdif, pusk_pdif2_tdif, srabsign_pdif2_tdif, srab_pdif2_tdif, vvod_pdif1_tdif, oper_vyvod_pdif1_tdif, pusk_A_pdif1_tdif, srab_A_pdif1_tdif, srabsign_A_pdif1_tdif, io_A_pdif1_tdif, pusk_B_pdif1_tdif, srab_B_pdif1_tdif, srabsign_B_pdif1_tdif, io_B_pdif1_tdif, pusk_C_pdif1_tdif, srab_C_pdif1_tdif, srabsign_C_pdif1_tdif, io_C_pdif1_tdif, pusk_pdif1_tdif, srabsign_pdif1_tdif, srab_pdif1_tdif, pusk_A_hf2phar1_tdif, pusk_B_hf2phar1_tdif, pusk_C_hf2phar1_tdif, pusk_hf2phar1_tdif, pusk_A_hf5phar1_tdif, pusk_B_hf5phar1_tdif, pusk_C_hf5phar1_tdif, pusk_hf5phar1_tdif, vvod_rctr1_tdif, oper_vyvod_rctr1_tdif, srab_A_rctr1_tdif, srab_B_rctr1_tdif, srab_C_rctr1_tdif, srab_rctr1_tdif, neispr_rctr1_tdif = tdif1.Step(VYVOD, IA_vn, dIA_vn, IB_vn, dIB_vn, IC_vn, dIC_vn, IA_nn, dIA_nn, IB_nn, dIB_nn, IC_nn, dIC_nn, OV_tdif, OV_pdif2_tdif, NaSign_pdif2_tdif, OV_pdif1_tdif, NaSign_pdif1_tdif, CurCirc, IAdiff2h, IBdiff2h, ICdiff2h, IAdiff5h, IBdiff5h, ICdiff5h, OV_rctr1_tdif)

#print(vvod_pdif2_tdif, oper_vyvod_pdif2_tdif, pusk_A_pdif2_tdif, srab_A_pdif2_tdif, srabsign_A_pdif2_tdif, io_A_pdif2_tdif, pusk_B_pdif2_tdif, srab_B_pdif2_tdif, srabsign_B_pdif2_tdif, io_B_pdif2_tdif, pusk_C_pdif2_tdif, srab_C_pdif2_tdif, srabsign_C_pdif2_tdif, io_C_pdif2_tdif, pusk_pdif2_tdif, srabsign_pdif2_tdif, srab_pdif2_tdif, vvod_pdif1_tdif, oper_vyvod_pdif1_tdif, pusk_A_pdif1_tdif, srab_A_pdif1_tdif, srabsign_A_pdif1_tdif, io_A_pdif1_tdif, pusk_B_pdif1_tdif, srab_B_pdif1_tdif, srabsign_B_pdif1_tdif, io_B_pdif1_tdif, pusk_C_pdif1_tdif, srab_C_pdif1_tdif, srabsign_C_pdif1_tdif, io_C_pdif1_tdif, pusk_pdif1_tdif, srabsign_pdif1_tdif, srab_pdif1_tdif, pusk_A_hf2phar1_tdif, pusk_B_hf2phar1_tdif, pusk_C_hf2phar1_tdif, pusk_hf2phar1_tdif, pusk_A_hf5phar1_tdif, pusk_B_hf5phar1_tdif, pusk_C_hf5phar1_tdif, pusk_hf5phar1_tdif, vvod_rctr1_tdif, oper_vyvod_rctr1_tdif, srab_A_rctr1_tdif, srab_B_rctr1_tdif, srab_C_rctr1_tdif, srab_rctr1_tdif, neispr_rctr1_tdif)

print(pusk_A_pdif1_tdif, srab_A_pdif1_tdif, srabsign_A_pdif1_tdif, io_A_pdif1_tdif, pusk_B_pdif1_tdif, srab_B_pdif1_tdif, srabsign_B_pdif1_tdif, io_B_pdif1_tdif, pusk_C_pdif1_tdif, srab_C_pdif1_tdif, srabsign_C_pdif1_tdif, io_C_pdif1_tdif, pusk_pdif1_tdif, srabsign_pdif1_tdif, srab_pdif1_tdif) 

