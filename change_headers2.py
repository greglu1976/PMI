
# Не тестировалась вообще! сгенерирована ИИ

import os
import sys
from pathlib import Path
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter

class ExcelHeadersReplacer:
    def __init__(self, example_file: str, target_folder: str = None):
        """
        Инициализирует замену заголовков в Excel файлах.
        
        Args:
            example_file: путь к файлу example.xlsx с эталонными заголовками
            target_folder: папка для поиска файлов (по умолчанию текущая папка)
        """
        self.example_file = example_file
        self.target_folder = target_folder or os.getcwd()
        self.headers_data = {}
        self.sheet_names = ["Inputs", "Outputs"]
        
    def load_headers_from_example(self) -> bool:
        """Загружает заголовки из example.xlsx"""
        if not os.path.exists(self.example_file):
            print(f"❌ Файл не найден: {self.example_file}")
            return False
        
        try:
            workbook = load_workbook(self.example_file)
            
            for sheet_name in self.sheet_names:
                if sheet_name not in workbook.sheetnames:
                    print(f"⚠️  Лист '{sheet_name}' не найден в {self.example_file}")
                    continue
                
                sheet = workbook[sheet_name]
                headers = []
                
                # Получаем первую строку с заголовками
                for cell in sheet[1]:
                    headers.append(cell.value)
                
                self.headers_data[sheet_name] = {
                    "values": headers,
                    "formatting": self._extract_formatting(sheet, 1),
                    "count": len(headers)
                }
                print(f"✅ Загружены заголовки из '{sheet_name}': {len(headers)} столбцов")
                print(f"   Последний заголовок: {headers[-1] if headers else 'Нет'}")
            
            workbook.close()
            return True
            
        except Exception as e:
            print(f"❌ Ошибка при загрузке {self.example_file}: {e}")
            return False
    
    def _extract_formatting(self, sheet, row: int):
        """Извлекает форматирование ячеек из строки"""
        formatting = {}
        for col_idx, cell in enumerate(sheet[row], 1):
            if cell.has_style or cell.value:
                formatting[col_idx] = {
                    "font": cell.font.copy() if cell.font else None,
                    "fill": cell.fill.copy() if cell.fill else None,
                    "border": cell.border.copy() if cell.border else None,
                    "alignment": cell.alignment.copy() if cell.alignment else None,
                    "number_format": cell.number_format
                }
        return formatting
    
    def _apply_formatting(self, sheet, row: int, formatting: dict, max_col: int):
        """Применяет форматирование к строке до указанного столбца"""
        for col_idx, format_dict in formatting.items():
            if col_idx <= max_col:
                cell = sheet.cell(row=row, column=col_idx)
                if format_dict["font"]:
                    cell.font = format_dict["font"]
                if format_dict["fill"]:
                    cell.fill = format_dict["fill"]
                if format_dict["border"]:
                    cell.border = format_dict["border"]
                if format_dict["alignment"]:
                    cell.alignment = format_dict["alignment"]
                cell.number_format = format_dict["number_format"]
    
    def find_xlsx_files(self) -> list:
        """Находит все xlsx файлы в папке (кроме example.xlsx)"""
        xlsx_files = []
        example_name = os.path.basename(self.example_file)
        
        try:
            for file in os.listdir(self.target_folder):
                if file.endswith(".xlsx") and file != example_name:
                    xlsx_files.append(os.path.join(self.target_folder, file))
            
            print(f"📁 Найдено {len(xlsx_files)} файлов для обработки")
            return xlsx_files
            
        except Exception as e:
            print(f"❌ Ошибка при поиске файлов: {e}")
            return []
    
    def replace_headers_in_file(self, file_path: str) -> bool:
        """Заменяет заголовки в одном файле"""
        if not os.path.exists(file_path):
            print(f"❌ Файл не найден: {file_path}")
            return False
        
        try:
            workbook = load_workbook(file_path)
            changes_made = False
            
            for sheet_name in self.sheet_names:
                if sheet_name not in self.headers_data:
                    continue
                
                if sheet_name not in workbook.sheetnames:
                    print(f"   ⚠️  Лист '{sheet_name}' не найден, пропускаем")
                    continue
                
                sheet = workbook[sheet_name]
                headers_data = self.headers_data[sheet_name]
                new_headers = headers_data["values"]
                formatting = headers_data["formatting"]
                
                # Определяем реальное количество столбцов в целевом файле
                target_max_col = sheet.max_column
                example_col_count = len(new_headers)
                
                print(f"   📊 Лист '{sheet_name}':")
                print(f"      Столбцов в целевом файле: {target_max_col}")
                print(f"      Столбцов в example.xlsx: {example_col_count}")
                
                # Проверяем первые несколько заголовков для отладки
                old_headers = []
                for col in range(1, min(6, target_max_col + 1)):
                    val = sheet.cell(row=1, column=col).value
                    old_headers.append(str(val) if val else "None")
                print(f"      Старые заголовки (первые 5): {old_headers}")
                
                # Заменяем заголовки ТОЛЬКО в первой строке
                # Данные во второй строке и далее не трогаем
                for col_idx, value in enumerate(new_headers, 1):
                    if col_idx <= target_max_col:
                        sheet.cell(row=1, column=col_idx).value = value
                    else:
                        print(f"      ⚠️  Внимание: example.xlsx имеет больше столбцов ({example_col_count}), чем целевой файл ({target_max_col})")
                        print(f"      Столбец {col_idx} ('{value}') не может быть добавлен")
                        break
                
                # Применяем форматирование только к существующим столбцам
                self._apply_formatting(sheet, 1, formatting, min(target_max_col, example_col_count))
                
                print(f"   ✅ Заголовки заменены в листе '{sheet_name}'")
                changes_made = True
                
                # Проверяем результат
                new_headers_check = []
                for col in range(1, min(6, target_max_col + 1)):
                    val = sheet.cell(row=1, column=col).value
                    new_headers_check.append(str(val) if val else "None")
                print(f"      Новые заголовки (первые 5): {new_headers_check}")
            
            if changes_made:
                workbook.save(file_path)
                print(f"💾 Файл сохранен: {os.path.basename(file_path)}")
            
            workbook.close()
            return True
            
        except Exception as e:
            print(f"❌ Ошибка при обработке {file_path}: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def process_all_files(self) -> dict:
        """Обрабатывает все найденные файлы"""
        if not self.headers_data:
            print("❌ Заголовки не загружены. Запустите load_headers_from_example() первым.")
            return {"success": 0, "failed": 0, "skipped": 0}
        
        xlsx_files = self.find_xlsx_files()
        
        if not xlsx_files:
            print("❌ Файлы для обработки не найдены")
            return {"success": 0, "failed": 0, "skipped": 0}
        
        stats = {"success": 0, "failed": 0, "skipped": 0}
        
        print("\n" + "="*60)
        print("🔄 Начало замены заголовков...")
        print("="*60 + "\n")
        
        for file_path in xlsx_files:
            file_name = os.path.basename(file_path)
            print(f"📄 Обработка: {file_name}")
            
            if self.replace_headers_in_file(file_path):
                stats["success"] += 1
            else:
                stats["failed"] += 1
            print()
        
        return stats
    
    def print_summary(self, stats: dict):
        """Выводит итоговый отчет"""
        print("="*60)
        print("📊 ИТОГОВЫЙ ОТЧЕТ")
        print("="*60)
        print(f"✅ Успешно обработано: {stats['success']}")
        print(f"❌ Ошибок: {stats['failed']}")
        print(f"⏭️  Пропущено: {stats['skipped']}")
        total = stats['success'] + stats['failed'] + stats['skipped']
        print(f"📌 Всего: {total}")
        print("="*60)


def main():
    """Главная функция"""
    example_file = "example.xlsx"
    target_folder = os.getcwd()
    
    # Можно указать конкретный файл для тестирования
    if len(sys.argv) > 1:
        target_folder = sys.argv[1]
    
    replacer = ExcelHeadersReplacer(example_file, target_folder)
    
    if not replacer.load_headers_from_example():
        print("❌ Не удалось загрузить заголовки. Завершение работы.")
        input("\nНажмите Enter для выхода...")  # <--- ДОБАВЛЕНО
        return 1
    
    stats = replacer.process_all_files()
    replacer.print_summary(stats)
    
    if stats["success"] > 0:
        print("\n✨ Замена заголовков успешно завершена!")
    else:
        print("\n⚠️  Не удалось обработать файлы")
    
    input("\nНажмите Enter для выхода...")  # <--- ДОБАВЛЕНО
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)