
from lib._FUNCS.DIFRCTR import DIFRCTR


rtcr1 = DIFRCTR(SGF1=1, SGF2=1, T1=0, T2=0, Inom=1, Imin=0.1, Ksym=0.5, LIsym=1)
res = rtcr1.Step(VYVOD=0, OV=0, OVst=0, IA=0.5, IB=1, IC=1)
print(res)

 

 