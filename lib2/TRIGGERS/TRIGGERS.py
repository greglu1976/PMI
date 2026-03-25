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
    


# Счетчик по восходящему фронту
class RisingEdgeCounter:
    def __init__(self):
        self.count = 0
        self.last_state = False
    
    def update(self, current_state):
        """Обновляет счетчик при обнаружении восходящего фронта"""
        # Восходящий фронт: предыдущее состояние False, текущее True
        if not self.last_state and current_state:
            self.count += 1
            return True  # Возвращаем True при обнаружении фронта
        self.last_state = current_state
        return False
    
    def reset(self):
        self.count = 0
        self.last_state = False

# Триггер восходящего фронта (Rising Edge Trigger)
class R_TRIG:
    def __init__(self):
        self._M = False  # Внутренняя память предыдущего состояния
        self.Q = False   # Выход: True при обнаружении фронта

    def run(self, CLK):
        # Вычисляем новое состояние выхода
        self.Q = not self._M and CLK
        # Сохраняем текущее состояние для следующего вызова
        self._M = CLK
        return self.Q


# Триггер нисходящего фронта (Falling Edge Trigger)
class F_TRIG:
    def __init__(self):
        self._M = False  # Внутренняя память предыдущего состояния
        self.Q = False   # Выход: True при обнаружении фронта

    def run(self, CLK):
        # Вычисляем новое состояние выхода
        self.Q = self._M and not CLK
        # Сохраняем текущее состояние для следующего вызова
        self._M = CLK
        return self.Q
    

class R_TRIG_Counter:
    """Счетчик с встроенным детектором восходящего фронта"""
    def __init__(self, count = 0):
        self._M = False
        self.count = count
    
    def run(self, CLK):
        # Детектируем восходящий фронт
        edge = not self._M and CLK
        self._M = CLK
        
        # Увеличиваем счетчик при обнаружении фронта
        if edge:
            self.count += 1
        
        return self.count
    
    def get_count(self):
        return self.count

    def reset(self, count = 0):
        """Сброс счетчика и внутреннего состояния"""
        self.count = count
        self._M = False  # Важно: сбрасываем и память состояния!