# (T_LVALH) Функция ПС - предупредительная сигнализация трансформатора 35 кВ исполнение Т

class T_LVALH:
    def __init__(self, SGF1=0, SGF2=0, SGF3=0, SGF4=0, SGF5=0, SGF6=0, SGF7=0, SGF8=0, SGF9=0, SGF10=0, SGF11=0, SGF12=0, SGF13=0, SGF14=0):
        self.SGF1 = SGF1 # ГЗ сигн
        self.SGF2 = SGF2 # Низк.изол.ГЗ
        self.SGF3 = SGF3 # ГЗ заблокирована
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
        self.SGF14 = SGF14

    def Step(self, VYVOD, sign_ps_tuple, sgf1_sign = 0, sgf2_sign = 0, sgf3_sign = 0, sgf4_sign = 0, sgf5_sign = 0, sgf6_sign = 0, sgf7_sign = 0, sgf8_sign = 0, sgf9_sign = 0, sgf10_sign = 0, sgf11_sign = 0, sgf12_sign = 0, sgf13_sign = 0, sgf14_sign = 0):
        sign_ps = any(sign_ps_tuple)
        sign1 = 0 if self.SGF1==0 else sgf1_sign 
        sign2 = 0 if self.SGF2==0 else sgf2_sign 
        sign3 = 0 if self.SGF3==0 else sgf3_sign
        sign4 = 0 if self.SGF4==0 else sgf4_sign 
        sign5 = 0 if self.SGF5==0 else sgf5_sign 
        sign6 = 0 if self.SGF6==0 else sgf6_sign
        sign7 = 0 if self.SGF7==0 else sgf7_sign 
        sign8 = 0 if self.SGF8==0 else sgf8_sign 
        sign9 = 0 if self.SGF9==0 else sgf9_sign
        sign10 = 0 if self.SGF10==0 else sgf10_sign 
        sign11 = 0 if self.SGF11==0 else sgf11_sign 
        sign12 = 0 if self.SGF12==0 else sgf12_sign
        sign13 = 0 if self.SGF13==0 else sgf13_sign
        sign14 = 0 if self.SGF14==0 else sgf14_sign
        pusk = not(VYVOD) and (sign_ps or any((sign1,sign2,sign3,sign4,sign5,sign6,sign7,sign8,sign9,sign10,sign11,sign12,sign13,sign14)))
        return pusk

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
    def get_SGF14(self):
        return self.SGF14
    def set_SGF14(self, value):
        self.SGF14 = value


if __name__ == "__main__":
    ps = T_LVALH()
    res = ps.Step(0, (0,0,0), 0,0,0,0,0,0,0,0,0,0,0,0,0)
    print(res)