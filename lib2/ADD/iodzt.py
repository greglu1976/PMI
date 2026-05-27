# Измерительный орган ДЗТ для одной фазы

from lib._TRIGGERS.TRIGGERS import RSTrigger

class ioDZT:
    def __init__(self, Isr, Isr_zagrub, It1, It2, Kt1, Kt2):
        self.Isr = Isr
        self.Isr_zagrub = Isr_zagrub
        self.It1 = It1
        self.It2 = It2 
        self.Kt1 = Kt1
        self.Kt2 = Kt2
        self.RS1 = RSTrigger(state=0)
        self.RS2 = RSTrigger(state=0)
        self.RS3 = RSTrigger(state=0)        

        # вспомогательные переменные выходов каждой характеристики
        self.out1 = False
        self.out2 = False
        self.out3 = False
        self.for_bvkz_mode = False

    def _is_in_trip_area(self, Idiff, Ibias, CurCirc):

        if CurCirc==True:
            I = self.Isr_zagrub
        else:
            I = self.Isr  

        _a1 = Idiff - I
        _a1_res = _a1 + 0.05
        _a2 = Idiff-(self.Kt1*(Ibias-self.It1) + self.Isr)
        _a2_res = _a2 + 0.05
        _a3 = Idiff-(self.Kt2*(Ibias-self.It2) + self.Kt1*(self.It2-self.It1) + self.Isr)
        _a3_res = _a3 + 0.05

        _res_gen = (_a1_res<0) or (_a2_res<0) or (_a3_res<0)

        self.out1 = self.RS1.run((_a1>=0), (((_a1_res<0) and self.out1) or _res_gen))
        self.out2 = self.RS2.run((_a2>=0), (((_a2_res<0) and self.out2) or _res_gen))
        self.out3 = self.RS3.run((_a3>=0), (((_a3_res<0) and self.out3) or _res_gen))

        return self.out1, self.out2, self.out3

    def _ctrl_bvkz(self, Ibias, srab1z, srab2z, srab3z, OpSel, EnaDisSelec):
        _is1 = Ibias - self.It1<=0
        _is2 = (Ibias - self.It2<=0) and (Ibias - self.It1>0)        
        _is3 = Ibias - self.It2>0

        _out23 = (srab2z and _is2) or (srab3z and _is3)
        self.for_bvkz_mode = (self.for_bvkz_mode or OpSel) and _out23
        if EnaDisSelec==0:
            _out_sel_bvkz = _out23
        else:
            _out_sel_bvkz =  self.for_bvkz_mode 

        Op = (srab1z and _is1) or _out_sel_bvkz
        return Op 


    def Step(self, Idiff, Ibias, CurCirc, OpSel, EnaDisSelec):
        srab_io1, srab_io2, srab_io3 = self._is_in_trip_area(Idiff, Ibias, CurCirc)
        op = self._ctrl_bvkz(Ibias, srab_io1, srab_io2, srab_io3, OpSel, EnaDisSelec)

        return op

      
if __name__ == "__main__":
    io = ioDZT(Isr=0.2, Isr_zagrub=1.0, It1=1.0, It2=3.0, Kt1=0.25, Kt2=0.7)
    res = io.Step(Idiff=0.8, Ibias=3.0)
    print(res)     