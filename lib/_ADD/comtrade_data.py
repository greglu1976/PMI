import pandas as pd
from typing import List, Tuple, Dict
import os

class ComtradeData:
    def __init__(self, file_path: str):
        """
        Инициализация класса для чтения данных COMTRADE из XLSX файла
        
        Args:
            file_path (str): Путь к файлу Excel (.xlsx)
        """
        self.file_path = file_path
        self.data: List[Tuple] = []
        self._load_data()
        self._validate_data()

    def _load_data(self) -> None:
        """Загружает данные из XLSX-файла с использованием pandas"""
        try:
            # Проверка существования файла
            if not os.path.exists(self.file_path):
                print(f"Ошибка: Файл {self.file_path} не найден")
                return

            # Читаем все листы из файла
            sheets_dict = pd.read_excel(self.file_path, sheet_name=None, engine='openpyxl')
            print(f"Файл {self.file_path} успешно загружен")
            
            sheet_data = {}
            required_columns = ['Base_Amplitude', 'Base_Angle', 
                              'Second_Amplitude', 'Fifth_Amplitude']
            
            # Обрабатываем каждый лист
            for sheet_name, df in sheets_dict.items():
                if not sheet_name.startswith('Channel_'):
                    continue
                    
                # Проверяем наличие необходимых столбцов
                missing_cols = [col for col in required_columns if col not in df.columns]
                if missing_cols:
                    print(f"Предупреждение: В листе {sheet_name} отсутствуют столбцы: {missing_cols}")
                    continue
                
                # Округляем все числовые столбцы до 1 знака
                df = df.round(1) 

                # Преобразуем данные в словарь
                sheet_data[sheet_name] = {
                    'Base_Amplitude': df['Base_Amplitude'].fillna(0).tolist(),
                    'Base_Angle': df['Base_Angle'].fillna(0).tolist(),
                    'Second_Amplitude': df['Second_Amplitude'].fillna(0).tolist(),
                    'Fifth_Amplitude': df['Fifth_Amplitude'].fillna(0).tolist()
                }
                print(f"Лист {sheet_name} обработан, записей: {len(df)}")
            
            if not sheet_data:
                print("Ошибка: Не найдено ни одного корректного листа Channel_*")
                return
            
            # Определяем максимальное количество записей
            max_len = max(len(v['Base_Amplitude']) for v in sheet_data.values())
            print(f"Максимальное количество записей среди всех каналов: {max_len}")
            
            # Формируем кортежи данных
            self.data = self._create_tuples(sheet_data, max_len)
            
        except Exception as e:
            print(f"Критическая ошибка при загрузке файла: {str(e)}")
            self.data = []

    def _create_tuples(self, sheet_data: Dict, max_len: int) -> List[Tuple]:
        """
        Создает кортежи данных в заданном формате
        
        Args:
            sheet_data: Данные из всех листов
            max_len: Максимальное количество записей
            
        Returns:
            Список кортежей с данными
        """
        result = []
        
        for i in range(max_len):
            tuple_data = []
            
            # 1. Добавляем Base_Amplitude и Base_Angle для каналов 1-3
            for channel in [f'Channel_{i}' for i in range(1, 4)]:
                if channel in sheet_data:
                    data = sheet_data[channel]
                    tuple_data.append(data['Base_Amplitude'][i] if i < len(data['Base_Amplitude']) else 0)
                    tuple_data.append(data['Base_Angle'][i] if i < len(data['Base_Angle']) else 0)
                else:
                    tuple_data.extend([0, 0])  # Заполняем нулями при отсутствии данных
            
            # 2. Second_Amplitude для каналов 1-3
            for channel in [f'Channel_{i}' for i in range(1, 4)]:
                if channel in sheet_data:
                    data = sheet_data[channel]
                    tuple_data.append(data['Second_Amplitude'][i] if i < len(data['Second_Amplitude']) else 0)
                else:
                    tuple_data.append(0)
            
            # 3. Fifth_Amplitude для каналов 1-3
            for channel in [f'Channel_{i}' for i in range(1, 4)]:
                if channel in sheet_data:
                    data = sheet_data[channel]
                    tuple_data.append(data['Fifth_Amplitude'][i] if i < len(data['Fifth_Amplitude']) else 0)
                else:
                    tuple_data.append(0)
            
            # 4. Base_Amplitude и Base_Angle для каналов 4-6
            for channel in [f'Channel_{i}' for i in range(4, 7)]:
                if channel in sheet_data:
                    data = sheet_data[channel]
                    tuple_data.append(data['Base_Amplitude'][i] if i < len(data['Base_Amplitude']) else 0)
                    tuple_data.append(data['Base_Angle'][i] if i < len(data['Base_Angle']) else 0)
                else:
                    tuple_data.extend([0, 0])
            
            # 5. Second_Amplitude для каналов 4-6
            for channel in [f'Channel_{i}' for i in range(4, 7)]:
                if channel in sheet_data:
                    data = sheet_data[channel]
                    tuple_data.append(data['Second_Amplitude'][i] if i < len(data['Second_Amplitude']) else 0)
                else:
                    tuple_data.append(0)
            
            # 6. Fifth_Amplitude для каналов 4-6
            for channel in [f'Channel_{i}' for i in range(4, 7)]:
                if channel in sheet_data:
                    data = sheet_data[channel]
                    tuple_data.append(data['Fifth_Amplitude'][i] if i < len(data['Fifth_Amplitude']) else 0)
                else:
                    tuple_data.append(0)
            
            result.append(tuple(tuple_data))
        
        return result

    def _validate_data(self) -> None:
        """Проверяет корректность загруженных данных"""
        if not self.data:
            print("\nНе удалось загрузить данные. Возможные причины:")
            print("1. Файл не существует или имеет неправильный формат")
            print("2. В файле отсутствуют листы с именами Channel_1, Channel_2, ..., Channel_6")
            print("3. В листах отсутствуют необходимые столбцы:")
            print("   - Base_Amplitude")
            print("   - Base_Angle")
            print("   - Second_Amplitude")
            print("   - Fifth_Amplitude")
            print("\nПример правильной структуры файла:")
            print("""
Channel_1:
| Base_Amplitude | Base_Angle | Second_Amplitude | Fifth_Amplitude |
|----------------|------------|------------------|-----------------|
| 120.5          | 30.2       | 15.1             | 5.3             |
| 115.3          | 31.5       | 14.8             | 5.1             |
| ...            | ...        | ...              | ...             |
""")

    def get_data(self) -> List[Tuple]:
        """Возвращает список кортежей с данными"""
        return self.data

    def __len__(self) -> int:
        """Возвращает количество записей"""
        return len(self.data)

    def __getitem__(self, index: int) -> Tuple:
        """Возвращает запись по индексу"""
        if not self.data:
            raise IndexError("Данные не загружены")
        return self.data[index]

    def __iter__(self):
        """Возвращает итератор по данным"""
        return iter(self.data)


if __name__ == "__main__":
    # Пример использования
    file_path = "1.xlsx"  # Укажите правильный путь к файлу
    
    print(f"Попытка загрузить файл {file_path}...")
    comtrade = ComtradeData(file_path)
    
    if comtrade:
        print(f"\nУспешно загружено {len(comtrade)} записей")
        print("\nПервая запись:")
        print(comtrade[0])
    else:
        print("\nНе удалось загрузить данные. Проверьте файл.")