# Измерительный орган ДЗТ

from lib._TRIGGERS.TRIGGERS import RSTrigger

class ioDZT:
    def __init__(self, Isr, Isr_zagrub, It1, It2, Kt1, Kt2):
        self.Isr = Isr
        self.Isr_zagrub = Isr_zagrub
        self.It1 = It1
        self.It2 = It2 
        self.Kt1 = Kt1
        self.Kt2 = Kt2
        self.RSa1 = RSTrigger(state=0)
        self.RSa2 = RSTrigger(state=0)
        self.RSa3 = RSTrigger(state=0)        
        self.yt1 = Isr+Kt1*(It2-It1) # находим точку на оси y соответствующую It1
        self.xk1 = (Isr_zagrub - Isr + Kt1*It1)/Kt1 # точка на оси x пересечение с первой характеристикой
        self.xk2 = (Isr_zagrub - Isr + Kt2*It2-Kt1*(It2-It1))/Kt2 # точка на оси x пересечение со второй характеристикой
        self.is_k1 = self.yt1 > self.Isr_zagrub

        # вспомогательные переменные выходов каждой характеристики
        self.out1 = False
        self.out2 = False
        self.out3 = False

    def _isin_trip_area_krist(self, Ibias, Idiff, CurCirc):

        if CurCirc==True:
            I = self.Isr_zagrub
        else:
            I = self.Isr  

        _a1 = Idiff - I
        _a1_res = _a1 + 0.05
        print(_a1, _a1_res)        
        _a2 = Idiff-(self.Kt1*(Ibias-self.It1) + self.Isr)
        _a2_res = _a2 + 0.05
        _a3 = Idiff-(self.Kt2*(Ibias-self.It2) + self.Kt1*(self.It2-self.It1) + self.Isr)
        _a3_res = _a3 + 0.05

        _res_gen = (_a1_res<0) or (_a2_res<0) or (_a3_res<0)

        self.out1 = self.RSa1.run((_a1>=0), (((_a1_res<0) and self.out1) or _res_gen))
        self.out2 = self.RSa2.run((_a2>=0), (((_a2_res<0) and self.out2) or _res_gen))
        self.out3 = self.RSa3.run((_a3>=0), (((_a3_res<0) and self.out3) or _res_gen))

        return self.out1, self.out2, self.out3

    def _isin_trip_area(self, Ibias, Idiff, CurCirc):

        print(self.xk1, self.xk2, self.Isr_zagrub, self.yt1, self.is_k1)
        if Ibias<=self.It1 and Idiff>=self.Isr:
            return True
        elif Ibias>self.It1 and Ibias<=self.It2 and Idiff>=self.Kt1*(Ibias-self.It1) + self.Isr:
            print('2 участок', self.Kt1*(Ibias-self.It1), self.Isr)
            return True
        elif Ibias>self.It2 and Idiff>=self.Kt2*(Ibias-self.It2) + self.Kt1*(self.It2-self.It1) + self.Isr:
            print('3 участок', self.Kt2*(Ibias-self.It2)+ self.Kt1*(self.It2-self.It1)+ self.Isr)
            return True
        return False 

    def Step(self, IAdiff, IAbias):

        srab_ioA = self._isin_trip_area_krist(IAbias, IAdiff, CurCirc=0 )
        #srab_ioB = self._isin_trip_area(IBbias, IBdiff)
        #srab_ioC = self._isin_trip_area(ICbias, ICdiff)

        return srab_ioA #, srab_ioB, srab_ioC

      
if __name__ == "__main__":
    io = ioDZT(Isr=0.2, Isr_zagrub=1.0, It1=1.0, It2=3.0, Kt1=0.25, Kt2=0.7)
    res = io.Step(IAdiff=0.8, IBdiff=0, ICdiff=0, IAbias=3.0, IBbias=0, ICbias=0)
    print(res)     