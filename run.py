# Запуск файлов из папки TO35
#VYVOD, OV, NaSign, IA, IB, IC, IAB, IBC, ICA
#vvod, oper_vyvod, pusk, io, srabsign, srab, ET

from lib._FUNCS.LVPTOC import LVPTOC

if __name__ == "__main__":
    ptoc1 = LVPTOC(SGF1=1, SGF2=0, T1=0, Iset=1)
    res = ptoc1.Step(0,0,0,2,0,2,0,0,0)
    print(res)