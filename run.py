# Запуск файлов из папки TO35
#VYVOD, OV, NaSign, IA, IB, IC, IAB, IBC, ICA
#vvod, oper_vyvod, pusk, io, srabsign, srab, ET

from lib._FBS.TOVCTOC import TOVCTOC

#vvod_hvptoc1_lovctoc, oper_vyvod_hvptoc1_lovctoc, pusk_hvptoc1_lovctoc, io_hvptoc1_lovctoc, srab_hvptoc1_lovctoc, srabotkl_hvptoc1_lovctoc, ET_hvptoc1_lovctoc
#VYVOD, OV_hvptoc1_lovctoc, NaOtkl_hvptoc1_lovctoc, IA, IB, IC
if __name__ == "__main__":
    toc = TOVCTOC(SGF1_hvptoc1_lovctoc=1, T1_hvptoc1_lovctoc=0, Iset_hvptoc1_lovctoc=1)
    res = toc.Step(1,0,0,2,0,2)
    print(res)