# Орган выявления бросков тока намагничивания (БНТ) (TOCPHAR) PHAR1
# SGF1 - Перекрест_блок - Перекрестная блокировка (Не предусмотрено/ Предусмотрено)

from lib._TRIGGERS.TRIGGERS import RSTrigger
from lib._TIMERS.TIMERS import TON  

class TOCPHAR:
    def __init__(self, SGF1=0, Imax=10, Ratio=0.5):
        self.SGF1 = SGF1
        self.Imax = Imax
        self.Ratio = Ratio             
        self.T1a = TON()
        self.T1a.set_PT(0) # Здесь жесткая программная выдержка времени - в реальности 0.02 с
        self.T1b = TON()
        self.T1b.set_PT(0)
        self.T1c = TON()
        self.T1c.set_PT(0)        
        self.RSblock = RSTrigger(state=0)
        self.RSa = RSTrigger(state=0)
        self.RSb = RSTrigger(state=0)
        self.RSc = RSTrigger(state=0)        

    def Step(self, VVOD = 0, mtz_ioA = (0,0,0), mtz_ioB = (0,0,0), mtz_ioC = (0,0,0), IA=0, IA2harm=0, IB=0, IB2harm=0, IC=0, IC2harm=0):
        im = max(IA, IB, IC)
        blk = self.RSblock.run(im>=self.Imax), (im<0.95*self.Imax)

        ia_ratio = IA/IA2harm
        ia_rat_start = self.RSa.run(ia_ratio>=self.Ratio), (ia_ratio<0.95*self.Ratio)
        self.T11.IN = ia_rat_start
        Qa, ETa = self.T11.start()  # Запускаем таймер и получаем выход и прошедшее время
        ia_start = VVOD and not(blk) and any(mtz_ioA) and Qa


        return ia_start, ib_start, ic_start, start

    # Геттеры и сеттеры
    def get_SGF1(self):
        return self.SGF1
    def set_SGF1(self, value):
        self.SGF1 = value
 