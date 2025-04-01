import base64
import gzip
from io import BytesIO

# 1. Загрузка XML-файла
with open("1.dseq", "r", encoding="utf-8") as file:
    xml_content = file.read()

# 2. Извлечение Base64-данных из тега <Data>
import re
base64_data_match = re.search(r"<Data>(.*?)</Data>", xml_content, re.DOTALL)
if not base64_data_match:
    raise ValueError("Тег <Data> не найден в XML-файле.")
base64_data = base64_data_match.group(1).strip()

# 3. Декодирование Base64
try:
    decoded_data = base64.b64decode(base64_data)
except Exception as e:
    print(f"Ошибка при декодировании Base64: {e}")
    exit()

# 4. Проверка, сжаты ли данные (gzip)
try:
    # Попытка распаковать gzip
    with gzip.GzipFile(fileobj=BytesIO(decoded_data)) as gz_file:
        unpacked_data = gz_file.read()
    print("Данные успешно распакованы.")
except OSError:
    # Если данные не сжаты gzip, используем их как есть
    unpacked_data = decoded_data
    print("Данные не сжаты gzip, используется исходный формат.")

# 5. Обработка распакованных данных
#try:
    # Преобразование в строку (если данные текстовые)
    #text_data = unpacked_data.decode("utf-8")
    #print("Текстовые данные:")
    #print(text_data)
#except UnicodeDecodeError:
    #print("Данные не являются текстовыми (возможно, бинарные).")

# 6. Сохранение в файл (если данные бинарные)
with open("output.bin", "wb") as file:
    file.write(unpacked_data)
print("Данные сохранены в output.bin")