# для переименовывания группы файлов


import os

# Укажите путь к папке с файлами
folder_path = r'.'

# Перебираем все файлы в папке
for filename in os.listdir(folder_path):
    if filename.startswith("МТЗ_"):
        # Разбиваем имя файла по "_", чтобы получить номер
        parts = filename.split("_")
        number = parts[1].split(".")[0]  # получаем номер без расширения
        extension = filename.split(".")[-1]  # расширение файла
        
        # Формируем новое имя
        new_name = f"МТЗ 2 ст_{number}.{extension}"
        
        # Полные пути для переименования
        old_file = os.path.join(folder_path, filename)
        new_file = os.path.join(folder_path, new_name)
        
        # Переименовываем файл
        os.rename(old_file, new_file)
        print(f"Переименован: {filename} -> {new_name}")