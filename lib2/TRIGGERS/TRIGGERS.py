# Триггер с приоритетом R
class RSTrigger:
    def __init__(self, state=0):
        self.state = state  # Начальное состояние триггера

    def run(self, set, reset):
        if set and not reset:
            self.state = 1
        elif reset:
            self.state = 0
        return self.state  # Возвращаем текущее состояние
# Триггер с приоритетом S
class SRTrigger:
    def __init__(self, state=0):
        self.state = state  # Начальное состояние триггера

    def run(self, set, reset):
        if set:
            self.state = 1
        elif reset and not set:
            self.state = 0
        return self.state  # Возвращаем текущее состояние