

from lib._ADD.iodzt import ioDZT

io = ioDZT(Isr=0.2, Isr_zagrub=1.0, It1=1.0, It2=3.0, Kt1=0.25, Kt2=0.7)
res1 = io.Step(IAdiff=1.1, IBdiff=0, ICdiff=0, IAbias=3.1, IBbias=0, ICbias=0)
#res2 = io.Step(IAdiff=0.5, IBdiff=0, ICdiff=0, IAbias=1.3, IBbias=0, ICbias=0)
#res3 = io.Step(IAdiff=0.5, IBdiff=0, ICdiff=0, IAbias=1.3, IBbias=0, ICbias=0)
#print(res1, res2, res3)   

print(res1)