from docx import Document

from main import make_par


import re

def parse_assembly_file(doc, file_path):
    """
    Функция для чтения и разбора файла _assembly.txt.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Разделяем содержимое файла на блоки по разделителю '#'
    blocks = re.split(r'\n\s*#\s*', content.strip())

    # Проходим по каждому блоку
    for block in blocks:
        if not block.strip():
            continue  # Пропускаем пустые блоки

        # Извлекаем данные из блока
        data = {}
        for line in block.split('\n'):
            if '=' in line:
                key, value = map(str.strip, line.split('=', 1))
                data[key] = value.strip("'\"")  # Убираем кавычки, если они есть

        # Проверяем, что все необходимые данные есть в блоке
        required_keys = ['heading', 'intro_text', 'func_modes_dir', 'needed_inputs', 'needed_outputs']
        if all(key in data for key in required_keys):
            # Вызываем функцию make_par с извлеченными данными
            doc = make_par(
                doc,  # Замените на ваш объект doc, если он нужен
                heading=data['heading'],
                intro_text=data['intro_text'],
                func_modes_dir=data['func_modes_dir'],
                needed_inputs=data['needed_inputs'],
                needed_outputs=data['needed_outputs']
            )
        else:
            print(f"Skipping block due to missing data: {block}")
    return doc


doc = Document('template.docx')
# Укажите путь к файлу _assembly.txt
file_path = '_assembly.txt'

# Запускаем парсинг файла
doc = parse_assembly_file(doc, file_path)

# Сохранение документа
doc.save('_pmi.docx')
print("Документ успешно создан: _pmi.docx")
