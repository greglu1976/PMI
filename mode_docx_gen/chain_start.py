from docx import Document

from main import make_par, make_par2


import re


def parse_assembly_file(doc, dir):
    """
    Функция для чтения и разбора файла _assembly.txt.
    """
    file_path =dir +'/' + '_assembly.txt'

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
                dir = dir
            )
        else:
            print(f"Skipping block due to missing data: {block}")
    return doc

def parse_assembly_file2(doc, dir):
    """
    Функция для чтения и разбора файла _assembly.txt.
    """
    file_path =dir +'/' + '_assembly.txt'

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
        required_keys = ['result_heading', 'result_text', 'func_modes_dir', 'needed_inputs', 'needed_outputs']
        if all(key in data for key in required_keys):
            # Вызываем функцию make_par с извлеченными данными
            doc = make_par2(
                doc,  # Замените на ваш объект doc, если он нужен
                heading=data['result_heading'],
                intro_text=data['result_text'],
                func_modes_dir=data['func_modes_dir'],
                needed_outputs=data['needed_outputs'],
                dir = dir
            )
        else:
            print(f"Skipping block due to missing data: {block}")
    return doc

##############################################################
# ЗАПУСК
# 1. УКАЗЫВАЕМ ПАПКУ С ПМИ
dir = 'pmi_gzdzt'
# 2. Добавляем глобальную переменную для управления выводом таблиц в файле main.py
# Если 1 - таблицы без изменений не выводятся, если = 2 - то выводятся все таблицы режимов с изменениями, =3 - то таблицы сохраняются в свой файл
# 3. Указываем, нужно ли перегенерировать режимы в файле main.py
# Перегенерировать XLSX в JSON - если =1, иначе не перегенерируются 
#############################################################

doc = Document(dir +'//' +'template.docx')
# Укажите путь к файлу _assembly.txt

# Запускаем парсинг файла
doc = parse_assembly_file(doc, dir)

paragraph = doc.add_heading('РЕЗУЛЬТАТ ИСПЫТАНИЙ', level=1)
doc = parse_assembly_file2(doc, dir)

# Сохранение документа
doc.save('_pmi.docx')
print("Документ успешно создан: _pmi.docx")
