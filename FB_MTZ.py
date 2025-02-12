# Функциональный блок LVTTOC
# Максимальная токовая защита с пуском по напряжению (МТЗ/U) (LVTTOC)

from LVTPTOC import LVTPTOC

class LVTTOC:
    def __init__(self, ptoc1, ptoc2, ptoc3):
        self.ptoc1 = LVTPTOC()

