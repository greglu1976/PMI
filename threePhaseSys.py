# класс описывающий трехфазную систему

import numpy as np

class ThreePhaseSystem:
    def __init__(self, Ua_amplitude, Ua_angle, Ub_amplitude, Ub_angle, Uc_amplitude, Uc_angle):
        """
        Инициализация трехфазной системы.
        :param Ua_amplitude: Амплитуда фазы A (В)
        :param Ua_angle: Угол фазы A (градусы)
        :param Ub_amplitude: Амплитуда фазы B (В)
        :param Ub_angle: Угол фазы B (градусы)
        :param Uc_amplitude: Амплитуда фазы C (В)
        :param Uc_angle: Угол фазы C (градусы)
        """
        self.Ua = self._polar_to_rectangular(Ua_amplitude, Ua_angle)
        self.Ub = self._polar_to_rectangular(Ub_amplitude, Ub_angle)
        self.Uc = self._polar_to_rectangular(Uc_amplitude, Uc_angle)

    @staticmethod
    def _polar_to_rectangular(amplitude, angle_deg):
        """
        Преобразует полярные координаты (амплитуда, угол) в прямоугольные (x + jy).
        """
        angle_rad = np.deg2rad(angle_deg)
        return amplitude * (np.cos(angle_rad) + 1j * np.sin(angle_rad))

    @staticmethod
    def _rectangular_to_polar(z):
        """
        Преобразует прямоугольные координаты (x + jy) в полярные (амплитуда, угол).
        """
        amplitude = np.abs(z)
        angle_rad = np.angle(z)
        angle_deg = np.rad2deg(angle_rad)
        return amplitude, angle_deg

    def calculate_line_voltages(self):
        """
        Вычисляет линейные напряжения Uab, Ubc, Uca.
        :return: Словарь с амплитудами и углами линейных напряжений.
        """
        Uab = self.Ua - self.Ub
        Ubc = self.Ub - self.Uc
        Uca = self.Uc - self.Ua

        Uab_amplitude, Uab_angle = self._rectangular_to_polar(Uab)
        Ubc_amplitude, Ubc_angle = self._rectangular_to_polar(Ubc)
        Uca_amplitude, Uca_angle = self._rectangular_to_polar(Uca)

        return {
            "Uab": {"amplitude": Uab_amplitude, "angle": Uab_angle},
            "Ubc": {"amplitude": Ubc_amplitude, "angle": Ubc_angle},
            "Uca": {"amplitude": Uca_amplitude, "angle": Uca_angle},
        }

    def calculate_symmetric_components(self):
        """
        Вычисляет симметричные составляющие U0, U1, U2.
        :return: Словарь с амплитудами и углами симметричных составляющих.
        """
        a = np.exp(1j * np.deg2rad(120))  # Оператор поворота 120°
        a_squared = a ** 2

        U0 = (self.Ua + self.Ub + self.Uc) / 3
        U1 = (self.Ua + a * self.Ub + a_squared * self.Uc) / 3
        U2 = (self.Ua + a_squared * self.Ub + a * self.Uc) / 3

        U0_amplitude, U0_angle = self._rectangular_to_polar(U0)
        U1_amplitude, U1_angle = self._rectangular_to_polar(U1)
        U2_amplitude, U2_angle = self._rectangular_to_polar(U2)

        return {
            "U0": {"amplitude": U0_amplitude, "angle": U0_angle},
            "U1": {"amplitude": U1_amplitude, "angle": U1_angle},
            "U2": {"amplitude": U2_amplitude, "angle": U2_angle},
        }

    def print_results(self):
        """
        Выводит результаты расчетов линейных напряжений и симметричных составляющих.
        """
        line_voltages = self.calculate_line_voltages()
        symmetric_components = self.calculate_symmetric_components()

        print("Линейные напряжения:")
        for key, value in line_voltages.items():
            print(f"{key}: Амплитуда = {value['amplitude']:.2f} В, Угол = {value['angle']:.2f}°")

        print("\nСимметричные составляющие:")
        for key, value in symmetric_components.items():
            print(f"{key}: Амплитуда = {value['amplitude']:.2f} В, Угол = {value['angle']:.2f}°")


# Пример использования
if __name__ == "__main__":
    # Задаем параметры трехфазной системы
    Ua_amplitude = 57.74
    Ua_angle = 90

    Ub_amplitude = 38
    Ub_angle = 310

    Uc_amplitude = 38
    Uc_angle = 229

    # Создаем объект трехфазной системы
    system = ThreePhaseSystem(Ua_amplitude, Ua_angle, Ub_amplitude, Ub_angle, Uc_amplitude, Uc_angle)

    # Выводим результаты
    system.print_results()