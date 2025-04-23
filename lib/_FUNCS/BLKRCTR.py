# БВКЗ - блокировка при внешних КЗ (BLKRCTR) на одну фазу

# ЗАГЛУШКА

class BLKRCTR:
 
    def Step(self, vvod, sgf3):
        srab_A = False
        srab_B = False  
        srab_C = False
        srab = (srab_A or srab_B or srab_C) and  (vvod and sgf3==1)          
        return srab_A, srab_B, srab_C, srab 
