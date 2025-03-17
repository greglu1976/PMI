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
        self.triggered = False  # Флаг, указывающий, что таймер уже сработал

    def start(self):
        """Обновляет состояние таймера."""
        # Если вход включен и таймер еще не срабатывал, запускаем импульс
        if self.IN and not self.triggered:
            self.Q = True
            self.pulse_active = True
            self.start_time = time.time()
            self.triggered = True  # Устанавливаем флаг срабатывания

        # Если импульс активен, обновляем прошедшее время
        if self.pulse_active:
            self.ET = time.time() - self.start_time

            # Если прошедшее время больше или равно предустановленному, сбрасываем таймер
            if self.ET >= self.PT:
                self.Q = False
                self.pulse_active = False
                self.ET = 0
                self.start_time = None

        # Если вход выключен и импульс не активен, сбрасываем флаг срабатывания
        if not self.IN and not self.pulse_active:
            self.triggered = False

        return self.Q, self.ET  # Возвращаем состояние выхода и прошедшее время

    def reset(self):
        """Сбрасывает таймер и выходные сигналы."""
        self.Q = False
        self.ET = 0
        self.start_time = None
        self.pulse_active = False
        self.triggered = False

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


# Экспериментальные таймеры

class TP_with_R:
    def __init__(self):
        self.IN = False  # Вход (boolean)
        self.R = False   # Сигнал принудительного сброса (boolean)
        self.PT = 0      # Предустановленное время (в секундах)
        self.ET = 0      # Прошедшее время (в секундах)
        self.Q = False   # Выход (boolean)
        self.start_time = None  # Время начала отсчета
        self.pulse_active = False  # Флаг активности импульса
        self.triggered = False  # Флаг, указывающий, что таймер уже сработал
        self.reset_occurred = False  # Флаг, указывающий, что R был активен хотя бы раз

    def start(self):
        """Обновляет состояние таймера."""
        # Если сигнал R активен, сбрасываем таймер и устанавливаем флаг reset_occurred
        if self.R:
            self.reset()
            self.reset_occurred = True
            return self.Q, self.ET

        # Если вход IN включен, таймер еще не срабатывал, и R никогда не был активен, запускаем импульс
        if self.IN and not self.triggered and not self.reset_occurred:
            self.Q = True
            self.pulse_active = True
            self.start_time = time.time()
            self.triggered = True  # Устанавливаем флаг срабатывания

        # Если импульс активен, обновляем прошедшее время
        if self.pulse_active:
            self.ET = time.time() - self.start_time

            # Если прошедшее время больше или равно предустановленному, сбрасываем таймер
            if self.ET >= self.PT:
                self.reset()

        # Если вход IN выключен и импульс не активен, сбрасываем флаги срабатывания и reset_occurred
        if not self.IN and not self.pulse_active:
            self.triggered = False
            self.reset_occurred = False

        return self.Q, self.ET

    def reset(self):
        """Сбрасывает таймер."""
        self.Q = False
        self.pulse_active = False
        self.ET = 0
        self.start_time = None
        self.triggered = False

    def set_PT(self, PT):
        """Устанавливает предустановленное время."""
        self.PT = PT