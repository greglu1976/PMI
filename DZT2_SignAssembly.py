# (DZT2_SignAssembly) Функция СС - Сборка сигналов трансформатора 35 кВ

class DZT2_SignAssembly:
    def __init__(self, SGF1=0, SGF2=0, SGF3=0, SGF4=0, SGF5=0, SGF6=0, SGF7=0, SGF8=0, SGF9=0, SGF10=0, SGF11=0, SGF12=0, SGF13=0):
        self.SGF1 = SGF1
        self.SGF2 = SGF2
        self.SGF3 = SGF3
        self.SGF4 = SGF4
        self.SGF5 = SGF5
        self.SGF6 = SGF6
        self.SGF7 = SGF7
        self.SGF8 = SGF8        
        self.SGF9 = SGF9
        self.SGF10 = SGF10
        self.SGF11 = SGF11
        self.SGF12 = SGF12
        self.SGF13 = SGF13
    def Step(self, VYVOD = 0, GZsign = (0,), NizkIsolGZ = (0,), GZzablok =(0,), TZsign=(0,), NizkIsolTZ=(0,), TZzablok=(0,), TSsign=(0,), VneshOtkl=(0,), SA1=0, SA2=0, SA3=0, SA4=0, SG1=0, SG2=0, SG3=0, OTzepeiGZ=0, OTzepeiTZ=0, OTZDZ1=0, OTZDZ2=0, OTUROV1=0, OTUROV2=0, VneshSign=(0,)):
        _GZsign = not(VYVOD) and any(GZsign)
        _NizkIsolGZ = not(VYVOD) and any(NizkIsolGZ) 
        _GZzablok = not(VYVOD) and any(GZzablok)
        _TZsign = not(VYVOD) and any(TZsign) 
        _NizkIsolTZ = not(VYVOD) and any(NizkIsolTZ)
        _TZzablok = not(VYVOD) and any(TZzablok) 
        _TSsign = not(VYVOD) and any(TSsign)
        _VneshOtkl = not(VYVOD) and any(VneshOtkl) 
        _VneshSign = not(VYVOD) and any(VneshSign)

        _SA1 = 0 if self.SGF1==0 else not(SA1)
        _SA2 = 0 if self.SGF2==0 else not(SA2)
        _SA3 = 0 if self.SGF3==0 else not(SA3)
        _SA4 = 0 if self.SGF4==0 else not(SA4)
        _VyhZepiRazobr = not(VYVOD) and (any((_SA1, _SA2, _SA3, _SA4)))

        _SG1 = 0 if self.SGF5==0 else not(SG1)               
        _SG2 = 0 if self.SGF6==0 else not(SG2)    
        _SG3 = 0 if self.SGF7==0 else not(SG3)    
        _BIvyved = not(VYVOD) and (any((_SG1, _SG2, _SG3)))

        _OTzepeiGZ = 0 if self.SGF8==0 else not(OTzepeiGZ)
        _OTzepeiTZ = 0 if self.SGF9==0 else not(OTzepeiTZ)
        _OTsign = not(VYVOD) and (_OTzepeiGZ or _OTzepeiTZ)
        _NeispOTGZ = not(VYVOD) and _OTzepeiGZ
        _NeispOTTZ = not(VYVOD) and _OTzepeiTZ

        _OTZDZ1 = 0 if self.SGF10==0 else not(OTZDZ1)
        _OTZDZ2 = 0 if self.SGF11==0 else not(OTZDZ2)
        _OTUROV1 = 0 if self.SGF12==0 else not(OTUROV1)
        _OTUROV2 = 0 if self.SGF13==0 else not(OTUROV2)
        _OTNNsign = not(VYVOD) and (any((_OTZDZ1, _OTZDZ2, _OTUROV1, _OTUROV2)))        

        return _GZsign, _NizkIsolGZ, _GZzablok, _TZsign, _NizkIsolTZ, _TZzablok, _TSsign, _VneshOtkl, _VyhZepiRazobr, _BIvyved, _OTsign, _NeispOTGZ, _NeispOTTZ, _OTNNsign, _VneshSign

    # Геттеры и сеттеры
    def get_SGF1(self):
        return self.SGF1
    def set_SGF1(self, value):
        self.SGF1 = value
    def get_SGF2(self):
        return self.SGF2
    def set_SGF2(self, value):
        self.SGF2 = value

    def get_SGF3(self):
        return self.SGF3
    def set_SGF3(self, value):
        self.SGF3 = value
    def get_SGF4(self):
        return self.SGF4
    def set_SGF4(self, value):
        self.SGF4 = value

    def get_SGF5(self):
        return self.SGF5
    def set_SGF5(self, value):
        self.SGF5 = value
    def get_SGF6(self):
        return self.SGF6
    def set_SGF6(self, value):
        self.SGF6 = value

    def get_SGF7(self):
        return self.SGF7
    def set_SGF7(self, value):
        self.SGF7 = value
    def get_SGF8(self):
        return self.SGF8
    def set_SGF8(self, value):
        self.SGF8 = value

    def get_SGF9(self):
        return self.SGF9
    def set_SGF9(self, value):
        self.SGF9 = value
    def get_SGF10(self):
        return self.SGF10
    def set_SGF10(self, value):
        self.SGF10 = value

    def get_SGF11(self):
        return self.SGF11
    def set_SGF11(self, value):
        self.SGF11 = value
    def get_SGF12(self):
        return self.SGF12
    def set_SGF12(self, value):
        self.SGF12 = value

    def get_SGF13(self):
        return self.SGF13
    def set_SGF13(self, value):
        self.SGF13 = value

if __name__ == "__main__":
    SS = DZT2_SignAssembly(SGF1=0, SGF2=0, SGF3=0, SGF4=0, SGF5=0, SGF6=0, SGF7=0, SGF8=0, SGF9=0, SGF10=0, SGF11=0, SGF12=0, SGF13=0)
    res = SS.Step(0, (0,0,0), (0,0,0), (0,0,0), (0,0,0), (0,0,0), (0,0,0), (0,0,0), (0,0,0), 0,0,0,0, 0,0,0, 0,0, 0,0,0,0, (0,0,0,0))
    print(res)
    #VYVOD, GZsign, NizkIsolGZ, GZzablok, TZsign, NizkIsolTZ, TZzablok, TSsign, VneshOtkl, SA1, SA2, SA3, SA4, SG1, SG2, SG3, OTzepeiGZ, OTzepeiTZ, OTZDZ1, OTZDZ2, OTUROV1, OTUROV2, VneshSign