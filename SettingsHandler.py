import json
from typing import List, Dict, Optional

class SettingsHandler:
    def __init__(self, settings_data: List[Dict[str, str]]):
        """
        Инициализирует обработчик уставок.
        
        :param settings_data: Список словарей вида {"Parameter": "...", "Value": "..."}
        """
        self._settings = {item["Parameter"]: item["Value"] for item in settings_data}
        # Сохраняем исходный порядок ключей для точного восстановления при сохранении
        self._parameter_order = [item["Parameter"] for item in settings_data]

    @classmethod
    def from_json_file(cls, filepath: str):
        """
        Создаёт экземпляр SettingsHandler из JSON-файла.
        
        :param filepath: Путь к файлу с уставками.
        :return: Экземпляр SettingsHandler
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls(data)

    def get_value_by_parameter(self, parameter_name: str) -> Optional[str]:
        """
        Возвращает значение параметра по его имени.
        
        :param parameter_name: Имя параметра (например, "LVTTOC_1_PTOC1_EnaDis_SG1")
        :return: Значение параметра как строка или None, если не найден
        """
        return self._settings.get(parameter_name)

    def set_value_to_parameter(self, parameter_name: str, value: str) -> bool:
        """
        Устанавливает новое значение для параметра.
        
        :param parameter_name: Имя параметра
        :param value: Новое значение (должно быть строкой)
        :return: True, если параметр существовал и был обновлён; False, если параметр не найден
        """
        if parameter_name in self._settings:
            self._settings[parameter_name] = str(value)
            return True
        return False

    def to_original_format(self) -> List[Dict[str, str]]:
        """
        Экспортирует текущие уставки в исходной разметке:
        список словарей в порядке, соответствующем загруженному файлу.
        """
        return [{"Parameter": name, "Value": self._settings[name]} for name in self._parameter_order]

    def save_to_json_file(self, filepath: str):
        """
        Сохраняет текущие уставки в JSON-файл в исходной разметке:
        одной строкой, без отступов и лишних пробелов (как в оригинальном файле).
        """
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.to_original_format(), f, ensure_ascii=False, separators=(',', ':'))

    def save_to_struct_json_file(self, filepath: str):
        """
        Сохраняет текущие уставки в структурированном JSON-файле.
        """
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.to_original_format(), f, ensure_ascii=False, indent=2)


if __name__ == "__main__":

    # Загрузка
    handler = SettingsHandler.from_json_file("ЮНИТ-М319 Т Уставки РЗиА.json")

    # Изменение
    handler.set_value_to_parameter("TLTCGASLGC_1_PTRC1_EnaDis_SG1", "False")

    # Сохранение в том же формате
    handler.save_to_json_file("updated_settings.json")