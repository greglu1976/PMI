# ФБ Логика отключения В ВН Т 35 (ЛО ВН) (HVTCBOFF) для Т (с учетом сборки Внеш откл ЗДЗ 1, 2 и УРОВ 1,2 подходит для ДЗТ2)
# НЕ ПРОВЕРЕНО!!

# SGF1 - Ввод_функции - Ввод функции в работу (Не предусмотрено/ Предусмотрено)

from lib2.FUNCS.CBPTRC import CBPTRC # импортируем функцию ЛО В ВН

class HVTCBOFF:
    def __init__(self, SGF1_hvcbptrc1_hvtcboff, T1_hvcbptrc1_hvtcboff):
        self.hvcbptrc1 = CBPTRC(SGF1_hvcbptrc1_hvtcboff, T1_hvcbptrc1_hvtcboff)

    def Step(self, VYVOD, OV_hvcbptrc1_hvtcboff, LO_t_srab, vnesh_otkl_zdz, vnesh_otkl_urov):
        vvod_hvcbptrc1_hvtcboff, oper_vyvod_hvcbptrc1_hvtcboff, otkl_hvcbptrc1_hvtcboff, otkl_avar_hvcbptrc1_hvtcboff = self.hvcbptrc1.Step(VYVOD, OV_hvcbptrc1_hvtcboff, LO_t_srab, vnesh_otkl_zdz, vnesh_otkl_urov)
        return vvod_hvcbptrc1_hvtcboff, oper_vyvod_hvcbptrc1_hvtcboff, otkl_hvcbptrc1_hvtcboff, otkl_avar_hvcbptrc1_hvtcboff

if __name__ == "__main__":
    fb = HVTCBOFF(SGF1=1, T1=0)
    res = fb.Step(0,0,0,0)
    print(res)