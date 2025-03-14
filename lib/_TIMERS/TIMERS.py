import time

class TON:
    def __init__(self):
        self.IN = False  # Вход (boolean)
        self.PT = 0      # Предустановленное время (в секундах)
        self.ET = 0      # Прошедшее время (в секундах)
        self.Q = False   # Выход (boolean)
        self.start_time = None  # Время начала отсчета

    def start(self):
        """Запускает таймер и обновляет состояние выхода."""
        if self.IN:
            if self.start_time is None:  # Если таймер не запущен
                self.start_time = time.time()  # Начинаем отсчет

            self.ET = time.time() - self.start_time  # Обновляем прошедшее время

            if self.ET >= self.PT:  # Если прошедшее время больше или равно предустановленному
                self.Q = True  # Устанавливаем состояние выхода
                self.ET = self.PT  # Ограничиваем ET до PT
        else:  # Если вход отключен
            self.reset()  # Сбрасываем таймер при отключении IN

        return self.Q, self.ET  # Возвращаем состояние выхода и прошедшее время

    def reset(self):
        """Сбрасывает таймер и выходные сигналы."""
        self.Q = False  # Сбрасываем выход
        self.ET = 0     # Сбрасываем прошедшее время
        self.start_time = None  # Сбрасываем время начала отсчета

    def set_PT(self, PT):
        """Устанавливает предустановленное время."""
        self.PT = PT

class TP:
    def __init__(self):
        self.IN = False  # Вход (boolean)
        self.PT = 0      # Предустановленное время (в секундах)
        self.ET = 0      # Прошедшее время (в секундах)
        self.Q = False   # Выход (boolean)
        self.start_time = None  # Время начала отсчета
        self.pulse_active = False  # Флаг активности импульса

    def start(self):
        """Обновляет состояние таймера."""
        if self.IN and not self.pulse_active:  # Если вход включен и импульс не активен
            self.Q = True  # Включаем выход
            self.pulse_active = True  # Устанавливаем флаг активности импульса
            self.start_time = time.time()  # Начинаем отсчет

        if self.pulse_active:
            self.ET = time.time() - self.start_time  # Обновляем прошедшее время

            if self.ET >= self.PT:  # Если прошедшее время больше или равно предустановленному
                self.Q = False  # Выключаем выход
                self.pulse_active = False  # Сбрасываем флаг активности импульса
                self.ET = 0  # Сбрасываем прошедшее время
                self.start_time = None  # Сбрасываем время начала отсчета

        return self.Q, self.ET  # Возвращаем состояние выхода и прошедшее время

    def reset(self):
        """Сбрасывает таймер и выходные сигналы."""
        self.Q = False  # Сбрасываем выход
        self.ET = 0      # Сбрасываем прошедшее время
        self.start_time = None  # Сбрасываем время начала отсчета
        self.pulse_active = False  # Сбрасываем флаг активности импульса

    def set_PT(self, PT):
        """Устанавливает предустановленное время."""
        self.PT = PT

class TOF:
    def __init__(self):
        self.IN = False  # Вход (boolean)
        self.PT = 0      # Предустановленное время (в секундах)
        self.ET = 0      # Прошедшее время (в секундах)
        self.Q = False   # Выход (boolean)
        self.start_time = None  # Время начала отсчета

    def start(self):
        """Обновляет состояние таймера."""
        if self.IN:
            self.Q = True  # Выход сразу включается при активном IN
            self.ET = 0    # Сбрасываем прошедшее время
            self.start_time = None  # Сбрасываем время начала отсчета
        else:
            if self.Q:  # Если выход был включен
                if self.start_time is None:  # Если таймер не запущен
                    self.start_time = time.time()  # Начинаем отсчет

                self.ET = time.time() - self.start_time  # Обновляем прошедшее время

                if self.ET >= self.PT:  # Если прошедшее время больше или равно предустановленному
                    self.Q = False  # Выключаем выход
                    self.ET = self.PT  # Ограничиваем ET до PT
            else:
                self.ET = 0  # Сбрасываем прошедшее время, если выход уже выключен

        return self.Q, self.ET  # Возвращаем состояние выхода и прошедшее время

    def reset(self):
        """Сбрасывает таймер и выходные сигналы."""
        self.Q = False  # Сбрасываем выход
        self.ET = 0      # Сбрасываем прошедшее время
        self.start_time = None  # Сбрасываем время начала отсчета

    def set_PT(self, PT):
        """Устанавливает предустановленное время."""
        self.PT = PT