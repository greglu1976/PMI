import time

class IntegralTON:
    def __init__(self):
        self.IN = False  # Вход (boolean)
        self.PT = 0      # Предустановленное время (в секундах)
        self.ET = 0      # Прошедшее время (в секундах)
        self.Q = False   # Выход (boolean)
        self.start_time = None  # Время начала отсчета
        self.last_ET = 0  # Последнее значение прошедшего времени
        self.return_delay = 2  # Выдержка возврата (в секундах)
        self.return_start_time = None  # Время начала выдержки возврата

    def start(self):
        """Запускает таймер и обновляет состояние выхода."""
        if self.IN:
            if self.start_time is None:  # Если таймер не запущен
                self.start_time = time.time() - self.last_ET  # Начинаем отсчет с учетом прошлого ET

            self.ET = time.time() - self.start_time  # Обновляем прошедшее время

            if self.ET >= self.PT:  # Если прошедшее время больше или равно предустановленному
                self.Q = True  # Устанавливаем состояние выхода
                self.ET = self.PT  # Ограничиваем ET до PT

            # Сброс выдержки возврата, если она была начата ранее
            self.return_start_time = None
        else:  # Если вход отключен
            if self.Q:  # Если выход был активен
                if self.return_start_time is None:  # Если выдержка возврата еще не начата
                    self.return_start_time = time.time()  # Запускаем выдержку возврата

                # Проверяем, прошло ли достаточно времени для сброса
                if time.time() - self.return_start_time >= self.return_delay:
                    self.reset()
            else:
                # Если выход уже был сброшен, сохраняем текущее значение ET
                if self.start_time is not None:
                    self.last_ET = self.ET
                self.start_time = None  # Сбрасываем время начала отсчета
                self.Q = False  # Сбрасываем выход

        return self.Q, self.ET  # Возвращаем состояние выхода и прошедшее время

    def reset(self):
        """Сбрасывает таймер и выходные сигналы."""
        self.Q = False  # Сбрасываем выход
        self.ET = 0     # Сбрасываем прошедшее время
        self.start_time = None  # Сбрасываем время начала отсчета
        self.last_ET = 0  # Сбрасываем последнее значение ET
        self.return_start_time = None  # Сбрасываем время начала выдержки возврата

    def set_PT(self, PT):
        """Устанавливает предустановленное время."""
        self.PT = PT

    def set_return_delay(self, delay):
        """Устанавливает выдержку возврата."""
        self.return_delay = delay

# Пример использования
timer = IntegralTON()
timer.set_PT(3)  # Устанавливаем предустановленное время 5 секунд
timer.set_return_delay(2)  # Устанавливаем выдержку возврата 2 секунды

modes = (1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0)

# Симуляция работы таймера
for intimer in modes:
    timer.IN = intimer
    time.sleep(0.5)  # Ждем 1 секунду
    Q, ET = timer.start()
    print(f"Time: IN: {timer.IN}, Q: {Q}, ET: {ET}")