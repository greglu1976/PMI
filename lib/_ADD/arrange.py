# Выравнивание токов одной стороны для ДЗТ.
# для разворота звезды используется выбор соответствующей группы (например вместо 11 выбирается 5)
# похоже что внутреннее приведение амплитуды приведение к току Inom_term - вроде для всех сторон должен быть одинаковым??
# 

import numpy as np
import math

from lib._ADD.matrice import get_matrix

class Arrenger:
    def __init__(self, Sbaz, Ubaz, Iperv, Inom_term, Ivtor, k_sch, n_sch, compens_3i0):
        self.Ibaz = Sbaz/(Ubaz*math.sqrt(3))
        self.k_am = (Iperv*Inom_term)/(self.Ibaz*Ivtor*k_sch)
        self.matrix = get_matrix(n_sch, compens_3i0)
        #print('Kam=',self.k_am, ' Ibaz=', self.Ibaz )

    def run(self, IA, dIA, IB, dIB, IC, dIC):
        # Преобразуем угол из градусов в радианы
        dIa_radians = np.radians(dIA)
        dIb_radians = np.radians(dIB)
        dIc_radians = np.radians(dIC)
        # Преобразуем комплексное число в алгебраическую форму
        IA_complex = IA * (np.cos(dIa_radians) + 1j * np.sin(dIa_radians))
        IB_complex = IB * (np.cos(dIb_radians) + 1j * np.sin(dIb_radians))
        IC_complex = IC * (np.cos(dIc_radians) + 1j * np.sin(dIc_radians))
        # Определяем вектор комплексных чисел (вектор-столбец)
        currents = np.array([
            [IA_complex],  
            [IB_complex],  
            [IC_complex]  
        ])
        # Перемножаем матрицу на вектор и коэффициент
        C = np.dot(self.matrix, currents)*self.k_am  
        # Преобразуем результат C в вектор амплитуд и углов
        amplitudes = np.abs(C)  # Амплитуды комплексных чисел
        angles_radians = np.angle(C)  # Углы в радианах
        angles_degrees = np.degrees(angles_radians)  # Углы в градусах
        # Выводим результаты
        print("Амплитуды:")
        print(amplitudes)
        print("Углы (в градусах):")
        print(angles_degrees)
        return C #[0][0], C[1][0], C[2][0] # возвращаем комплексы Ia, Ib, Ic приведенный

if __name__ == "__main__":
    phsA1 = Arrenger(Sbaz=10e+6, Ubaz=36750, Iperv=1000, Inom_term=1, Ivtor=1, k_sch=1, n_sch=0, compens_3i0=False)
    Ia1_priv, Ib1_priv, Ic1_priv = phsA1.run(IA=0.157, dIA=0, IB=0.157, dIB=240, IC=0.157, dIC=120)
    #print(Ia1_priv, Ib1_priv, Ic1_priv)
    phsA2 = Arrenger(Sbaz=10e+6, Ubaz=10500, Iperv=5000, Inom_term=1, Ivtor=5, k_sch=1, n_sch=5, compens_3i0=False)
    Ia2_priv, Ib2_priv, Ic2_priv = phsA2.run(IA=0.550, dIA=30, IB=0.550, dIB=-90, IC=0.550, dIC=150)
    #print(Ia2_priv, Ib2_priv, Ic2_priv)

    sumA = Ia1_priv + Ia2_priv
    print(sumA)
    sumB = Ib1_priv + Ib2_priv
    print(abs(sumB))
    sumC = Ic1_priv - Ic2_priv
    print(abs(sumC))    