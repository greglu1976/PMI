# Орган КПОН в составе МТЗ трансформатора
# SGF1 - Реж_пуска - Режим пуска (По Uмин/ Комбинированный/ Внешний)
# ПРОВЕРЕНО!

from lib2.TRIGGERS.TRIGGERS import RSTrigger

class VCPTUV:
    def __init__(self, SGF1=0, Uop=40, U2op=5):
        self.SGF1 = SGF1
        self.Uop = Uop
        self.U2op = U2op              
        self.RSu = RSTrigger(state=0)
        self.RSu2 = RSTrigger(state=0)

    def Step(self, VVOD, KPONvnesh, UAB, UBC, UCA, U2):

        Umin = min(UAB, UBC, UCA)
        io_Umin = self.RSu.run((Umin<=self.Uop), (Umin>1.05*self.Uop))
        io_U2 = self.RSu2.run((U2>=self.U2op), (U2<0.95*self.U2op))
        kpon_pusk = VVOD and (io_Umin if (self.SGF1==0) else (io_Umin or io_U2) if (self.SGF1==1) else KPONvnesh)

        return kpon_pusk

    # Геттеры и сеттеры
    def get_SGF1(self):
        return self.SGF1
    def set_SGF1(self, value):
        self.SGF1 = value
 