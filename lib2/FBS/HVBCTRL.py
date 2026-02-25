# ФБ Управление выключателем (HVBCTRL)
# НЕ ПРОВЕРЕНО!!

# SGF1_cbcswi1_hvbctrl - Ввод_функции - Ввод функции в работу (Не предусмотрено/ Предусмотренно)
# T1_cbcswi1_hvbctrl - время импульса ограничения сигнала входа  

from lib2.FUNCS.HVCSWI import HVCSWI # импортируем функцию УВ

class HVBCTRL:
    def __init__(self, SGF1_cbcswi1_hvbctrl, T1_cbcswi1_hvbctrl):
        self.cbcswi1 = HVCSWI(SGF1_cbcswi1_hvbctrl, T1_cbcswi1_hvbctrl)

    def Step(self, VYVOD, OV_cbcswi1_hvbctrl, oper_vkl_v, ksv_blok_vkl):
        vvod_cbcswi1_hvbctrl, oper_vyvod_cbcswi1_hvbctrl, uv_vkl_cbcswi1_hvbctrl = self.cbcswi1.Step(VYVOD, OV_cbcswi1_hvbctrl, oper_vkl_v, ksv_blok_vkl)
        return vvod_cbcswi1_hvbctrl, oper_vyvod_cbcswi1_hvbctrl, uv_vkl_cbcswi1_hvbctrl

if __name__ == "__main__":
    fb = HVBCTRL(SGF1=1, T1=0)
    res = fb.Step(0,0,0,0)
    print(res)