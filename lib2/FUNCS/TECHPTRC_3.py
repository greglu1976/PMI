# для датчиков технологических защит с контролем сигн и откл ступеней

from lib._TIMERS.TIMERS import TON  
from lib._TRIGGERS.TRIGGERS import SRTrigger, RSTrigger

class TECHPTRC_3:
    def __init__(self, SGF1=0, SGF2=0, T=0):
        self.SGF1 = SGF1
        self.SGF2 = SGF2
        self.T1 = TON()
        self.T1.set_PT(T)
        self.SR = SRTrigger(state=0)
        self.RS_special = RSTrigger(state=0)

    def Step(self, VYVOD, OV_fb, OV_func, NaSign, srabKontOtkl, srabKontSign, srabKI, Sbros):
        self.T1.IN = srabKI
        Q, ET = self.T1.start()  # Запускаем таймер и получаем выход и прошедшее время
        vvod = (not(OV_func or OV_fb or VYVOD)) and (self.SGF1==1)
        oper_vyvod = (OV_func or OV_fb or VYVOD) and (self.SGF1==1)

        # Обсчитываем первый триггер
        _s_SR1 = srabKontOtkl and (not srabKontSign)
        _r_SR1 = (not vvod) or ((not srabKontOtkl) and (not srabKontSign))
        _q_SR1 = self.RS_special.run(_s_SR1, _r_SR1)

        # Обсчитываем второй триггер
        _s_SR2 = vvod and Q
        _r_SR2 = (not vvod) or Sbros
        _q_SR2 = self.SR.run(_s_SR2, _r_SR2)

        _in_Or = 0 if (self.SGF2==0) else _q_SR2

        zablok = _q_SR1 or _in_Or
        srabsign = vvod and srabKontOtkl and (not zablok)
        srab = not(NaSign) and srabsign
        return vvod, oper_vyvod, srab, srabsign, zablok, ET

        # Геттер для SGF1
    def get_SGF1(self):
        return self.SGF1
    # Сеттер для SGF1
    def set_SGF1(self, value):
        self.SGF1 = value
    # Геттер для SGF2
    def get_SGF2(self):
        return self.SGF2
    # Сеттер для SGF2
    def set_SGF2(self, value):
        self.SGF2 = value
        # Геттер для времени таймера
    def get_T1(self):
        return self.T1.PT  # Предустановленное время таймера
    # Сеттер для времени таймера
    def set_T1(self, T):
        self.T1.set_PT(T)  # Устанавливаем предустановленное время таймера