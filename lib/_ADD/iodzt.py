# Измерительный орган ДЗТ

class ioDZT:
    def __init__(self, Isr, Isr_zagrub, It1, It2, Kt1, Kt2):
        self.Isr = Isr
        self.Isr_zagrub = Isr_zagrub
        self.It1 = It1
        self.It2 = It2 
        self.Kt1 = Kt1
        self.Kt2 = Kt2

    def _isin_trip_area(self, Ibias, Idiff):
        if Ibias<=self.It1 and Idiff>=self.Isr:
            return True
        elif Ibias>self.It1 and Ibias<=self.It2 and Idiff>=self.Kt1*(Ibias-self.It1) + self.Isr:
            return True
        elif Ibias>self.It2 and Idiff>=self.Kt2*(Ibias-self.It2) + self.Kt1*self.It1 + self.Isr:
            return True
        return False       

    def Step(self, IAdiff, IBdiff, ICdiff, IAbias, IBbias, ICbias):

        srab_ioA = self._isin_trip_area(IAbias, IAdiff)
        srab_ioB = self._isin_trip_area(IBbias, IBdiff)
        srab_ioC = self._isin_trip_area(ICbias, ICdiff)

        return srab_ioA, srab_ioB, srab_ioC

      
if __name__ == "__main__":
    io = ioDZT(Isr=0.2, Isr_zagrub=1.0, It1=1.0, It2=3.0, Kt1=0.25, Kt2=0.7)
    res = io.Step(IAdiff=1.0, IBdiff=0, ICdiff=0, IAbias=3.6, IBbias=0, ICbias=0)
    print(res)     