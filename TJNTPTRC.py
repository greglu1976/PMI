# класс применителен для всех типовых функций , которые получают на вход какое-то количесвто сигналов опервывода - кортеж OPVYVOD = () и много аргументов в кортеже ARGS = (), есть сигнал pusk без блокировки

class TJNTPTRC:
    def __init__(self, SGF1=0):
        self.SGF1 = SGF1

    def Step(self, OPVYVOD, ARGS):
        vvod = (not(any(OPVYVOD))) and (self.SGF1==1)
        oper_vyvod = (any(OPVYVOD)) and (self.SGF1==1)
        pusk = any(ARGS)
        srab = pusk and vvod
        return vvod, oper_vyvod, srab, pusk

    # Геттер для SGF1
    def get_SGF1(self):
        return self.SGF1
    # Сеттер для SGF1
    def set_SGF1(self, value):
        self.SGF1 = value


if __name__ == "__main__":
    lo = TJNTPTRC(0)
    res = lo.Step((0,0,0), (0,0,0,0,0,0,0,0,0))
    print(res)