
from lib2.FUNCS.MFTO import MFTO

class PolarComplex:
    def __init__(self, amplitude, angle_deg=0):
        self.amp = amplitude
        self.ang = angle_deg


# Тестирование
if __name__ == "__main__":
    mfto = MFTO(SGF1=1, SGF2=1, T=0, Iset=5)
    
    # Создаем тестовые токи как PolarComplex объекты
    IA = PolarComplex(4)  # ток > Iset
    IB = PolarComplex(4)
    IC = PolarComplex(4)
    
    res = mfto.Step(VYVOD=0, BSTO=0, IA=IA, IB=IB, IC=IC)
    print(res)