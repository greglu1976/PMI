# Меняет состояния ключей на содержимое из rules
# Создает резервную копию оригинального файла

import openpyxl
from pathlib import Path
import shutil
from datetime import datetime

def create_backup(file_path):
    """
    Создает резервную копию файла с временной меткой.
    
    Args:
        file_path: Путь к исходному файлу
    Returns:
        Path: Путь к созданной резервной копии
    """
    file_path = Path(file_path)
    
    # Создаем имя для резервной копии с временной меткой
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{file_path.stem}_backup_{timestamp}{file_path.suffix}"
    backup_path = file_path.parent / backup_name
    
    # Копируем файл
    shutil.copy2(file_path, backup_path)
    print(f"  💾 Создана резервная копия: {backup_path.name}")
    
    return backup_path

def replace_values_in_xlsx(file_path, replacement_rules, sheet_name="SGF_Parameters"):
    """
    Заменяет значения в столбцах Excel-файла согласно правилам замены.
    Создает резервную копию и обновляет исходный файл.
    
    Args:
        file_path: Путь к .xlsx файлу
        replacement_rules: Словарь вида {
            "Имя_столбца1": [{"0":"1"}, {"1":"2"}],
            "Имя_столбца2": [{"0":"1"}, {"1":"2"}, {"2":"3"}]
        }
        sheet_name: Имя листа для обработки (по умолчанию "SGF_Parameters")
    """
    # Преобразуем правила в удобный формат: {"Имя_столбца": {"0": "1", "1": "2", ...}}
    normalized_rules = {}
    for col_name, mappings in replacement_rules.items():
        mapping_dict = {}
        for item in mappings:
            mapping_dict.update(item)
        normalized_rules[col_name] = mapping_dict
    
    # Открываем файл
    wb = openpyxl.load_workbook(file_path)
    
    if sheet_name not in wb.sheetnames:
        print(f"⚠️  Лист '{sheet_name}' не найден в файле {file_path.name}. Пропускаем...")
        wb.close()
        return None
    
    sheet = wb[sheet_name]
    
    # Получаем заголовки (первая строка)
    headers = [cell.value for cell in sheet[1]]
    
    # Обрабатываем каждый столбец из правил
    modifications_made = False
    
    for col_name, mapping in normalized_rules.items():
        if col_name not in headers:
            print(f"⚠️  Столбец '{col_name}' не найден на листе '{sheet_name}' в файле {file_path.name}")
            continue
        
        col_idx = headers.index(col_name) + 1  # +1 т.к. openpyxl использует 1-based индексацию
        
        # Проходим по всем ячейкам столбца (начиная со 2-й строки)
        for row in range(2, sheet.max_row + 1):
            cell = sheet.cell(row=row, column=col_idx)
            original_value = cell.value
            
            if original_value is None:
                continue
            
            # Приводим значение к строке для сравнения (учитываем числа и строки)
            str_value = str(original_value).strip()
            
            # Если есть правило замены — применяем
            if str_value in mapping:
                new_value = mapping[str_value]
                # Сохраняем тип: если исходное значение было числом — оставляем числом
                try:
                    cell.value = int(new_value) if '.' not in new_value else float(new_value)
                except (ValueError, TypeError):
                    cell.value = new_value
                print(f"  ✓ Замена в '{col_name}' [{row},{col_idx}]: {original_value} → {cell.value}")
                modifications_made = True
    
    if modifications_made:
        # Создаем резервную копию перед сохранением
        backup_path = create_backup(file_path)
        
        # Сохраняем изменения в исходный файл
        wb.save(file_path)
        print(f"  ✅ Исходный файл обновлён: {file_path.name}")
    else:
        print(f"  ℹ️  В файле {file_path.name} не было изменений")
    
    wb.close()
    return file_path if modifications_made else None

def process_all_xlsx_files(replacement_rules, sheet_name="SGF_Parameters"):
    """
    Обрабатывает все xlsx-файлы в текущей папке.
    
    Args:
        replacement_rules: Словарь с правилами замены
        sheet_name: Имя листа для обработки
    """
    current_dir = Path.cwd()
    xlsx_files = list(current_dir.glob("*.xlsx"))
    
    # Исключаем файлы резервных копий из обработки
    xlsx_files = [f for f in xlsx_files if "_backup_" not in f.stem]
    
    if not xlsx_files:
        print("❌ В текущей папке не найдено xlsx-файлов (исключая резервные копии)")
        return
    
    print(f"Найдено файлов для обработки: {len(xlsx_files)}")
    print("-" * 50)
    
    processed_files = 0
    modified_files = 0
    
    for file_path in xlsx_files:
        print(f"\n📄 Обрабатываем файл: {file_path.name}")
        result = replace_values_in_xlsx(file_path, replacement_rules, sheet_name)
        processed_files += 1
        if result:
            modified_files += 1
    
    print("\n" + "=" * 50)
    print(f"✅ Обработка завершена!")
    print(f"   Всего обработано файлов: {processed_files}")
    print(f"   Файлов с изменениями: {modified_files}")
    print(f"   Резервные копии созданы в той же папке с суффиксом '_backup_YYYYMMDD_HHMMSS'")

# Пример использования:
if __name__ == "__main__":
    rules = {
        "LVTTOC_1_PTOC1_VolMod": [{"0": "1"}, {"1": "2"}],
        "LVTTOC_1_PTOC2_VolMod": [{"0": "1"}, {"1": "2"}],
        "LVTTOC_1_PTOC3_VolMod": [{"0": "1"}, {"1": "2"}],
        "LVTTOC_1_PTOC1_ExtVFlMod": [{"0": "1"}, {"1": "2"}],
        "LVTTOC_1_PTOC2_ExtVFlMod": [{"0": "1"}, {"1": "2"}],
        "LVTTOC_1_PTOC3_ExtVFlMod": [{"0": "1"}, {"1": "2"}],
        "LVTTOC_1_RBLC1_StepSel": [{"0": "1"}, {"1": "2"}, {"2": "3"}, {"3": "4"}]
    }
    
    # Обрабатываем все xlsx-файлы в текущей папке
    process_all_xlsx_files(rules)