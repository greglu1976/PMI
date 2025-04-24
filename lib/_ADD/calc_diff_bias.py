# Вычисляем дифференциальные и тормозные токи

from lib._ADD.arrange import Arrenger

class CalcDiffBias:
    def __init__(self, Sbaz, Ubaz_vn, Ubaz_nn, Iperv_vn, Iperv_nn, Inom_term_vn, Inom_term_nn, Ivtor_vn, Ivtor_nn, k_sch_vn, k_sch_nn, n_sch_vn, n_sch_nn, compens_3i0_vn, compens_3i0_nn):

        self.currents_vn = Arrenger(Sbaz, Ubaz_vn, Iperv_vn, Inom_term_vn, Ivtor_vn, k_sch_vn, n_sch_vn, compens_3i0_vn)
        self.currents_nn = Arrenger(Sbaz, Ubaz_nn, Iperv_nn, Inom_term_nn, Ivtor_nn, k_sch_nn, n_sch_nn, compens_3i0_nn)

    def Step(self, IA_vn, dIA_vn, IB_vn, dIB_vn, IC_vn, dIC_vn, IA_nn, dIA_nn, IB_nn, dIB_nn, IC_nn, dIC_nn):
        cur_vn_priv = self.currents_vn.run(IA_vn, dIA_vn, IB_vn, dIB_vn, IC_vn, dIC_vn)
        cur_nn_priv = self.currents_nn.run(IA_nn, dIA_nn, IB_nn, dIB_nn, IC_nn, dIC_nn)

        # рассчитываем дифференциальные токи - модуль геометрической суммы 
        diff_currs = abs(cur_vn_priv + cur_nn_priv)
        #print(abs(diff_currs))

        # рассчитываем тормозные токи - полусумма модулей токов
        bias_currs = 0.5*(abs(cur_vn_priv) + abs(cur_nn_priv))
        #print(bias_currs)
        return diff_currs, bias_currs   


