# Вычисляем дифференциальные и тормозные токи

from lib2.ADD.arrange import Arrenger

class CalcDiffBias:
    def __init__(self, Sbaz, Ubaz_vn, Ubaz_nn, Iperv_vn, Iperv_nn, Inom_term_vn, Inom_term_nn, Ivtor_vn, Ivtor_nn, k_sch_vn, k_sch_nn, n_sch_vn, n_sch_nn, compens_3i0_vn, compens_3i0_nn, Ubaz_nn2, Iperv_nn2, Inom_term_nn2, Ivtor_nn2, k_sch_nn2, n_sch_nn2, compens_3i0_nn2):

        self.currents_vn = Arrenger(Sbaz, Ubaz_vn, Iperv_vn, Inom_term_vn, Ivtor_vn, k_sch_vn, n_sch_vn, compens_3i0_vn)
        self.currents_nn = Arrenger(Sbaz, Ubaz_nn, Iperv_nn, Inom_term_nn, Ivtor_nn, k_sch_nn, n_sch_nn, compens_3i0_nn)
        self.currents_nn2 = Arrenger(Sbaz, Ubaz_nn2, Iperv_nn2, Inom_term_nn2, Ivtor_nn2, k_sch_nn2, n_sch_nn2, compens_3i0_nn2)

    def Step(self, IA_vn, dIA_vn, IB_vn, dIB_vn, IC_vn, dIC_vn, IA_nn, dIA_nn, IB_nn, dIB_nn, IC_nn, dIC_nn, IA_nn2, dIA_nn2, IB_nn2, dIB_nn2, IC_nn2, dIC_nn2):
        cur_vn_priv = self.currents_vn.run(IA_vn, dIA_vn, IB_vn, dIB_vn, IC_vn, dIC_vn)
        cur_nn_priv = self.currents_nn.run(IA_nn, dIA_nn, IB_nn, dIB_nn, IC_nn, dIC_nn)
        cur_nn2_priv = self.currents_nn2.run(IA_nn2, dIA_nn2, IB_nn2, dIB_nn2, IC_nn2, dIC_nn2)
        # рассчитываем дифференциальные токи - модуль геометрической суммы 
        diff_currs = abs(cur_vn_priv + cur_nn_priv + cur_nn2_priv)

        # рассчитываем тормозные токи - полусумма модулей токов
        bias_currs = 0.5*(abs(cur_vn_priv) + abs(cur_nn_priv)+ abs(cur_nn2_priv))
        
        return diff_currs, bias_currs   


