# Функция УВ в составе УВ
# Управление выключателем (УВ) (HVCSWI) CBCSWI1

# SGF1 - Ввод_функции - Ввод функции в работу (Не предусмотрено/ Предусмотренно)
# Т1 

from lib2.TIMERS.TIMERS import TP 
from lib2.TRIGGERS.TRIGGERS import RSTrigger

class HVCSWI:
    def __init__(self, SGF1, T1):
        self.SGF1 = SGF1
        self.T1 = TP()
        self.T1.set_PT(T1)
        self.RS1 = RSTrigger(state=0)        

        # Инициализация переменных
        self.uv_vkl = False

    def Step(self, VYVOD, OV, oper_vkl_v, ksv_blok_vkl):

        vvod = (not(OV or VYVOD)) and (self.SGF1==1) # УВ: Ввод
        oper_vyvod = (OV or VYVOD) and (self.SGF1==1) # УВ: Оперативный вывод

        self.T1.IN = oper_vkl_v
        _p001, ET_t1 = self.T1.start()

        self.uv_vkl = self.RS1.run(_p001, (ksv_blok_vkl or self.uv_vkl  or not(vvod)))
        return vvod, oper_vyvod, self.uv_vkl #, ET_t1, _p001  

    # Геттеры и сеттеры
    def get_SGF1(self):
        return self.SGF1
    def set_SGF1(self, value):
        self.SGF1 = value

    def get_T1(self):
        return self.T1.PT  # Предустановленное время таймера
    # Сеттер для времени таймера
    def set_T1(self, T):
        self.T1.set_PT(T)  # Устанавливаем предустановленное время таймера

