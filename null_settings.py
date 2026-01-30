import json
from typing import List, Dict, Optional, Any

from SettingsHandler import SettingsHandler
from MainConfigHandler import MainConfigHandler

# --- Классы SettingsHandler и MainConfigHandler здесь (уже определены выше) ---

def apply_min_values_to_settings(settings_path: str, meta_path: str, output_path: str):
    """
    Заменяет значения в файле уставок на minValue из метаданных (если задано).
    
    :param settings_path: путь к файлу уставок (формат [{"Parameter": "...", "Value": "..."}, ...])
    :param meta_path: путь к файлу метаданных (список параметров с minValue)
    :param output_path: путь для сохранения обновлённого файла уставок
    """
    # Загружаем уставки
    settings = SettingsHandler.from_json_file(settings_path)
    
    # Загружаем метаданные
    meta = MainConfigHandler.from_json_file(meta_path)

    updated_count = 0

    # Проходим по всем параметрам в уставках
    for param_name in settings._settings:
        param_info = meta.get_param_info(param_name)
        if not param_info:
            continue  # параметр отсутствует в метаданных — пропускаем
        
        min_val = param_info.get("minValue")
        if min_val is not None and min_val != "null":  # JSON null → Python None
            # Устанавливаем minValue как новое значение
            success = settings.set_value_to_parameter(param_name, str(min_val))
            if success:
                updated_count += 1

    # Сохраняем в исходной разметке (одна строка)
    settings.save_to_json_file(output_path)

    print(f"✅ Обновлено {updated_count} параметров. Результат сохранён в '{output_path}'")

if __name__ == "__main__":
    apply_min_values_to_settings(
        settings_path="updated_settings.json",
        meta_path="meta.json",  # ваш файл с метаданными
        output_path="settings_with_min_values.json"
    )