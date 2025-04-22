
from lib._FUNCS.RESPDIF import RESPDIF

pdif1 = RESPDIF(SGF1=1, SGF2=4, SGF3=1, T1=0, Isr=0.2, Isr_zagrub=1.0, It1=1.0, It2=3.0, Kt1=0.25, Kt2=0.7)

VYVOD = OV = OVst = 0
NaSign = 0
IAdiff = IBdiff = ICdiff = 0.6 
IAbias = IBbias = ICbias = 2.3
CurCirc = 0
OpSelA = OpSelB = OpSelC = 1
d2g_pusk_A = d2g_pusk_B = d2g_pusk_C = 0
d5g_pusk_A = d5g_pusk_B = d5g_pusk_C = 1

r1 = pdif1.Step(VYVOD, OV, OVst, NaSign, IAdiff, IBdiff, ICdiff, IAbias, IBbias, ICbias, CurCirc, OpSelA, OpSelB, OpSelC, d2g_pusk_A, d2g_pusk_B, d2g_pusk_C, d5g_pusk_A, d5g_pusk_B, d5g_pusk_C)

#vod, oper_vyvod, pusk_A, srab_A, srabsign_A, io_A, pusk_B, srab_B, srabsign_B, io_B, pusk_C, srab_C, srabsign_C, io_C, pusk, srabsign, srab

print(r1)

