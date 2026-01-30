import json
from typing import List, Dict, Optional, Any

class MainConfigHandler:
    def __init__(self, metadata_data: Dict[str, Any]):
        """
        Инициализирует обработчик метаданных параметров.
        
        :param metadata_data: Словарь, загруженный из JSON-файла с описанием параметров.
        """
        self.config_version = metadata_data.get("ConfigurationVersion")
        self.model_version = metadata_data.get("ModelPackageVersion")
        self.model_regex = metadata_data.get("ModelRegex")
        # Создаём словарь по имени параметра
        self._params = {p["name"]: p for p in metadata_data.get("Parameters", [])}

    @classmethod
    def from_json_file(cls, filepath: str):
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls(data)

    def get_param_info(self, name: str) -> Optional[Dict[str, Any]]:
        """Возвращает полное описание параметра по его имени."""
        return self._params.get(name)

    def is_readonly(self, name: str) -> bool:
        """Проверяет, является ли параметр доступным только для чтения."""
        info = self.get_param_info(name)
        return info.get("readonly", True) if info else True

    def is_command(self, name: str) -> bool:
        """Проверяет, является ли параметр командой."""
        info = self.get_param_info(name)
        return info.get("command", False) if info else False

    def get_group(self, name: str) -> Optional[str]:
        """Возвращает группу параметра (например, 'Measurement', 'Command')."""
        info = self.get_param_info(name)
        return info.get("group") if info else None

    def validate_value(self, name: str, value: str) -> bool:
        """
        Базовая валидация значения (по типу и диапазону).
        Поддерживает типы: 3 (bool/int), 6 (int32), 130 (enum).
        """
        info = self.get_param_info(name)
        if not info:
            return False

        try:
            val = int(value)
        except (ValueError, TypeError):
            return False

        # Проверка диапазона, если задан
        min_val = info.get("minValue")
        max_val = info.get("maxValue")

        if min_val is not None and val < int(min_val):
            return False
        if max_val is not None and val > int(max_val):
            return False

        return True
    
    def get_first_parameter_name_by_description(self, description: str, use_full: bool = False) -> Optional[str]:
        """
        Ищет имя параметра по его описанию.

        :param description: Строка для поиска в 'description' (или 'fullDescription', если use_full=True).
        :param use_full: Если True — искать в полном описании ('fullDescription'), иначе — в кратком ('description').
        :return: Имя параметра (ключ 'name'), если найдено; иначе None.
        """
        target_key = "fullDescription" if use_full else "description"
        for name, param in self._params.items():
            if param.get(target_key) == description:
                return name
        return None

    def find_parameter_names_by_description_substring(self, substring: str, use_full: bool = False) -> List[str]:
        """
        Ищет все параметры, чьё описание содержит указанную подстроку.
        """
        target_key = "fullDescription" if use_full else "description"
        matches = []
        for name, param in self._params.items():
            desc = param.get(target_key, "")
            if substring in desc:
                matches.append(name)
        return matches

    def find_parameter_names_by_description(self, description: str, use_full: bool = False) -> List[str]:
        """
        Ищет все параметры, чьё описание (краткое или полное) совпадает с заданным.
        
        :param description: Искомая строка описания.
        :param use_full: Если True — искать в 'fullDescription', иначе — в 'description'.
        :return: Список имён параметров (может быть пустым, содержать 1 или несколько элементов).
        """
        target_key = "fullDescription" if use_full else "description"
        matches = []
        for name, param in self._params.items():
            if param.get(target_key) == description:
                matches.append(name)
        return matches

    def find_parameters_by_rus_name(self, partial_description: str) -> List[str]:
        """
        Ищет параметры, у которых начало поля 'description' (до первого '_') 
        совпадает с заданной строкой.
        
        Пример:
            description = "ЛО ГЗ РПН_Ввод_функции" → сравнивается как "ЛО ГЗ РПН"
            Если partial_description == "ЛО ГЗ РПН", параметр будет найден.
        
        :param partial_description: Строка для поиска (без части после '_')
        :return: Список имён параметров (name), удовлетворяющих условию.
        """
        matches = []
        for name, param in self._params.items():
            desc = param.get("description", "")
            # Обрезаем до первого '_'
            base_desc = desc.split('_', 1)[0]  # split('_', 1) — только первое вхождение
            if base_desc == partial_description:
                matches.append(name)
        return matches


    def find_parameter_name_by_rus_name_and_full_desc_in_settings(
        self,
        rus_name: str = "",
        full_desc: str = "",
        setting_group: int = 0
    ) -> List[str]:
        """
        Ищет параметры по:
        - началу 'description' (до первого '_') == rus_name,
        - началу 'fullDescription' (до первого '_') == full_desc,
        - и (опционально) суффиксу группы уставок (_SG1, _SG2, ...).

        Если setting_group == 0 — возвращаются все совпадения.
        Если setting_group == 1..4 — только параметры с соответствующим суффиксом.
        Пустые строки для rus_name/full_desc означают «не учитывать это поле».

        :param rus_name: Ожидаемое начало поля 'description'
        :param full_desc: Ожидаемое начало поля 'fullDescription'
        :param setting_group: Номер группы уставок (0 — без фильтрации)
        :return: Список имён параметров
        """
        matches = []
        target_suffix = f"_SG{setting_group}" if setting_group in (1, 2, 3, 4) else None

        for name, param in self._params.items():
            # Фильтрация по группе уставок
            if target_suffix and not name.endswith(target_suffix):
                continue

            # Проверка по description
            desc_ok = True
            if rus_name:
                base_desc = param.get("description", "").split('_', 1)[0]
                desc_ok = (base_desc == rus_name)

            # Проверка по fullDescription
            full_ok = True
            if full_desc:
                base_full = param.get("fullDescription", "").split('_', 1)[0]
                full_ok = (base_full == full_desc)

            if desc_ok and full_ok:
                matches.append(name)

        return matches

if __name__ == "__main__":
    # Загрузка
    #settings = SettingsHandler.from_json_file("settings.json")          # уставки
    meta = MainConfigHandler.from_json_file("meta.json")           # описание

    # Пример безопасной записи
    param_name = "APTTECHLGC_1_OILIsolOp"

    #print(meta.get_param_info(param_name))
    '''
    names = meta.find_parameter_names_by_description("Блокировка от низкой изоляции", use_full=True)
    if len(names) == 0:
        print("Не найдено")
    elif len(names) == 1:
        print("Найден:", names[0])
    else:
        print("Несколько совпадений:", names)

    '''
    print(meta.find_parameter_name_by_rus_name_and_full_desc_in_settings("ЛО ГЗ РПН", "Ввод функции в работу",1))



