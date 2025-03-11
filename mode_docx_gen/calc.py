import numpy as np

def polar_to_rectangular(amplitude, angle_deg):
    """Преобразует полярные координаты (амплитуда, угол) в прямоугольные (x + jy)."""
    angle_rad = np.deg2rad(angle_deg)
    return amplitude * (np.cos(angle_rad) + 1j * np.sin(angle_rad))

def rectangular_to_polar(z):
    """Преобразует прямоугольные координаты (x + jy) в полярные (амплитуда, угол)."""
    amplitude = np.abs(z)
    angle_rad = np.angle(z)
    angle_deg = np.rad2deg(angle_rad)
    return amplitude, angle_deg

def calculate_line_voltages(Ua, Ub, Uc):
    """Вычисляет линейные напряжения Uab, Ubc, Uca."""
    Uab = Ua - Ub
    Ubc = Ub - Uc
    Uca = Uc - Ua
    return Uab, Ubc, Uca

def calculate_symmetric_components(Ua, Ub, Uc):
    """Вычисляет симметричные составляющие U0, U1, U2."""
    a = np.exp(1j * np.deg2rad(120))  # Оператор поворота 120°
    a_squared = a ** 2

    U0 = (Ua + Ub + Uc) / 3
    U1 = (Ua + a * Ub + a_squared * Uc) / 3
    U2 = (Ua + a_squared * Ub + a * Uc) / 3

    return U0, U1, U2

def main():
    # Входные данные: амплитуды и углы фазных напряжений
    Ua_amplitude = 57.74
    Ua_angle = 90

    Ub_amplitude = 38.19
    Ub_angle = 310.89

    Uc_amplitude = 38.19
    Uc_angle = 229.11

    # Преобразуем фазные напряжения в прямоугольную форму
    Ua = polar_to_rectangular(Ua_amplitude, Ua_angle)
    Ub = polar_to_rectangular(Ub_amplitude, Ub_angle)
    Uc = polar_to_rectangular(Uc_amplitude, Uc_angle)

    # Вычисляем линейные напряжения
    Uab, Ubc, Uca = calculate_line_voltages(Ua, Ub, Uc)

    # Вычисляем симметричные составляющие
    U0, U1, U2 = calculate_symmetric_components(Ua, Ub, Uc)

    # Преобразуем результаты обратно в полярную форму
    Uab_amplitude, Uab_angle = rectangular_to_polar(Uab)
    Ubc_amplitude, Ubc_angle = rectangular_to_polar(Ubc)
    Uca_amplitude, Uca_angle = rectangular_to_polar(Uca)

    U0_amplitude, U0_angle = rectangular_to_polar(U0)
    U1_amplitude, U1_angle = rectangular_to_polar(U1)
    U2_amplitude, U2_angle = rectangular_to_polar(U2)

    # Выводим результаты
    print("Линейные напряжения:")
    print(f"Uab: Амплитуда = {Uab_amplitude:.2f} В, Угол = {Uab_angle:.2f}°")
    print(f"Ubc: Амплитуда = {Ubc_amplitude:.2f} В, Угол = {Ubc_angle:.2f}°")
    print(f"Uca: Амплитуда = {Uca_amplitude:.2f} В, Угол = {Uca_angle:.2f}°")
    print("\nСимметричные составляющие:")
    print(f"U0: Амплитуда = {U0_amplitude:.2f} В, Угол = {U0_angle:.2f}°")
    print(f"U1: Амплитуда = {U1_amplitude:.2f} В, Угол = {U1_angle:.2f}°")
    print(f"U2: Амплитуда = {U2_amplitude:.2f} В, Угол = {U2_angle:.2f}°")

if __name__ == "__main__":
    main()