# для разворота звезды используется выбор соответствующей группы (например вместо 11 выбирается 5)
# похоже что внутреннее приведение амплитуды приведение к току Inom_term - вроде для всех сторон должен быть одинаковым??
# 

import numpy as np
import math

from lib._ADD.calc_diff_bias import CalcDiffBias


if __name__ == "__main__":

    a = CalcDiffBias(Sbaz=10e+6, Ubaz_vn=36750, Ubaz_nn=10500, Iperv_vn=1000, Iperv_nn=5000, Inom_term_vn=1, Inom_term_nn=1, Ivtor_vn=1, Ivtor_nn=5, k_sch_vn=1, k_sch_nn=1, n_sch_vn=0, n_sch_nn=5, compens_3i0_vn=False, compens_3i0_nn=False)

    a.Step(IA_vn=0.157, dIA_vn=0, IB_vn=0.157, dIB_vn=240, IC_vn=0.157, dIC_vn=120, IA_nn=0.55, dIA_nn=30, IB_nn=0.55, dIB_nn=-90, IC_nn=0.55, dIC_nn=150)
 

 