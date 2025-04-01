import base64
import gzip
from io import BytesIO

def is_gzipped(data):
    """Проверяет, сжаты ли данные gzip"""
    return len(data) >= 2 and data[:2] == b'\x1f\x8b'

# 1. Чтение бинарных данных из файла output.bin
with open("output.bin", "rb") as file:
    binary_data = file.read()

# 2. Определяем, нужно ли сжимать данные
if is_gzipped(binary_data):
    # Данные уже сжаты, используем как есть
    data_to_encode = binary_data
else:
    # Данные не сжаты, сжимаем их
    data_to_encode = gzip.compress(binary_data)

# 3. Кодирование данных в Base64
base64_encoded_data = base64.b64encode(data_to_encode).decode("utf-8")

# 4. Создание XML-структуры
xml_content = f"""<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<Root version="1.0.9.11151">
  <Data>
    {base64_encoded_data}
  </Data>
</Root>
"""

# 5. Сохранение XML-файла
with open("restored_file.xml", "w", encoding="utf-8") as file:
    file.write(xml_content)

print("Обратное преобразование завершено. XML-файл сохранен как restored_file.xml.")