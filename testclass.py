
from lib._TRIGGERS.TRIGGERS import RSTrigger

class TestClass1:
    def execute(self, enabled: bool, threshold: float, count: int):
        """Пример тестового класса"""
        return {
            'output1': enabled and (threshold > 5.0),
            'output2': count % 2 == 0,
            'status': 'active' if enabled else 'inactive'
        }

class TestClass2:
    def execute(self, inputA: bool, inputB: bool):
        """Логический элемент ИЛИ"""
        return {'result': inputA or inputB}
    

class STRPTOC:
    def __init__(self):
        """Инициализация с параметрами по умолчанию"""
        self.SGF1 = 1  # Значение по умолчанию
        self.Iset = 5.0  # Значение по умолчанию
        self.RS = RSTrigger(state=0)
    
    def execute(self, VYVOD: bool, OV: bool, OVst: bool, 
               IA: float, IB: float, IC: float) -> dict:
        """
        Основной метод для визуализатора
        Принимает параметры с аннотациями типов
        Возвращает словарь с результатами
        """
        vvod = (not (OV or VYVOD or OVst)) and (self.SGF1 == 1)
        oper_vyvod = (OV or VYVOD or OVst) and (self.SGF1 == 1)
        
        I = max(IA, IB, IC)
        io = (self.SGF1 == 1) and (self.RS.run((I >= self.Iset), (I < 0.95 * self.Iset)))
        pusk = vvod and io
        
        return {
            'vvod': vvod,
            'oper_vyvod': oper_vyvod,
            'pusk': pusk,
            'io': io,
            'I': I  # Дополнительный выход для информации
        }
    
    def get_parameters(self) -> dict:
        """Возвращает текущие параметры для настройки"""
        return {
            'SGF1': {'type': 'bool', 'value': self.SGF1 == 1, 'description': 'Сигнал готовности'},
            'Iset': {'type': 'float', 'value': self.Iset, 'min': 0, 'max': 100, 'description': 'Уставка тока'}
        }
    
    def set_parameters(self, params: dict):
        """Устанавливает параметры"""
        if 'SGF1' in params:
            self.SGF1 = 1 if params['SGF1'] else 0
        if 'Iset' in params:
            self.Iset = float(params['Iset'])
