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
