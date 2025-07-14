# Вынесена генерация таблиц
from docx.shared import Pt, Mm

from docx.oxml import OxmlElement
from docx.oxml.ns import qn

from lxml import etree

# Функция для применения стиля ко всем параграфам в ячейках таблицы
def apply_style_to_all_cells(table, style_name, numbered_style="ЮИ_Таблица_Нумерованный"):
    for row_idx, row in enumerate(table.rows):
        for col_idx, cell in enumerate(row.cells):
            # Пропускаем первую строку (заголовок таблицы)
            if row_idx == 0:
                continue  # Не применяем стили к строке заголовка

            for paragraph in cell.paragraphs:
                # Применяем специальный стиль для первого столбца
                if col_idx == 0:  # Проверяем, является ли это ячейкой первого столбца
                    paragraph.style = numbered_style
                else:
                    # Применяем указанный стиль ко всем остальным ячейкам
                    paragraph.style = style_name

def set_cell_vertical_alignment(cell, align="center"):
        tc = cell._tc
        tcPr = tc.get_or_add_tcPr()
        tcValign = OxmlElement('w:vAlign')
        tcValign.set(qn('w:val'), align)
        tcPr.append(tcValign)


# Функция для установки отступов в ячейке
def set_cell_margins(cell, top=0.05, bottom=0.05, left=0.05, right=0.05):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    
    nsmap = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    tcMar = etree.SubElement(tcPr, '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}tcMar', nsmap=nsmap)
    
    for position, value in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        element = etree.SubElement(tcMar, f'{{http://schemas.openxmlformats.org/wordprocessingml/2006/main}}{position}')
        element.set('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}w', str(int(value * 1440)))  # 1440 EMUs в 1 мм
        element.set('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}type', 'dxa')

# Функция для установки вертикальной ориентации текста
def set_vertical_text(cell):
    tcPr = cell._tc.get_or_add_tcPr()
    text_direction = etree.Element('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}textDirection')
    text_direction.set('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val', 'btLr')
    tcPr.append(text_direction)


def set_repeat_table_header(row):
    """ set repeat table row on every new page
    """
    tr = row._tr
    trPr = tr.get_or_add_trPr()
    tblHeader = OxmlElement('w:tblHeader')
    tblHeader.set(qn('w:val'), "true")
    trPr.append(tblHeader)
    return row

# Функция для форматирования числовых значений
def format_number(value):
    try:
        # Пробуем преобразовать в число
        num = float(str(value).replace(',', '.'))
        if num.is_integer():
            return str(int(num))  # Без дробной части
        return str(num).replace('.', ',')  # С дробной частью
    except (ValueError, TypeError):
        return str(value)  # Если не число, возвращаем как есть

def add_table_infuences(doc, table_rows):

    doc.add_paragraph('Подаваемые воздействия при проверке', style='ЮИ_Таблица_Название')
    table = doc.add_table(rows=1, cols=len(table_rows[0]))
    table.style = 'Стиль3'  # Применение стиля таблицы из шаблона


    # Рассчитываем высоту заголовка
    header_row_height = 25  # Базовая высота (для 'Номер режима')
    
    # Проверяем необходимость увеличения высоты
    if len(table_rows[0]) <= 17:  # Если столбцов <= 17, не меняем высоту
        pass
    else:
        # Ищем самый длинный заголовок
        max_length = max(len(str(header)) for header in table_rows[0])
        if max_length > 12:
            # Увеличиваем высоту на 2мм за каждый символ сверх 12
            additional_height = (max_length - 12) * 2
            header_row_height += additional_height

    # Установка высоты первой строки (заголовок)
    header_row = table.rows[0]
    header_row.height = Mm(header_row_height)  # Устанавливаем высоту строки заголовка
    set_repeat_table_header(header_row)

    # Добавление заголовков
    for i, header in enumerate(table_rows[0]):
        cell = header_row.cells[i]
        run = cell.paragraphs[0].add_run(header)
        set_vertical_text(cell)
        set_cell_vertical_alignment(cell, align="center")
        set_cell_margins(cell, top=0.0, bottom=0.0, left=0.0, right=0.0)

    # Добавление данных
    for row_data in table_rows[1:]:
        row_cells = table.add_row().cells
        for j, value in enumerate(row_data):
            cell = row_cells[j]
            cell.text = format_number(value)
            set_cell_margins(cell, top=0.0, bottom=0.0, left=0.0, right=0.0)
    
    # Применяем стиль ко всем ячейкам
    apply_style_to_all_cells(table, 'Текст таблицы', numbered_style='Текст таблицы')

    return doc

def add_table_results(doc, table_rows):

    doc.add_paragraph('Контролируемые сигналы при проверке', style='ЮИ_Таблица_Название')
    table = doc.add_table(rows=1, cols=len(table_rows[0]))
    table.style = 'Стиль3'  # Применение стиля таблицы из шаблона


    # Рассчитываем высоту заголовка
    header_row_height = 25  # Базовая высота (для 'Номер режима')
    
    # Проверяем необходимость увеличения высоты
    if len(table_rows[0]) <= 17:  # Если столбцов <= 17, не меняем высоту
        pass
    else:
        # Ищем самый длинный заголовок
        max_length = max(len(str(header)) for header in table_rows[0])
        if max_length > 12:
            # Увеличиваем высоту на 2мм за каждый символ сверх 12
            additional_height = (max_length - 12) * 2
            header_row_height += additional_height

    # Установка высоты первой строки (заголовок)
    header_row = table.rows[0]
    header_row.height = Mm(header_row_height)  # Устанавливаем высоту строки заголовка
    set_repeat_table_header(header_row)

    # Добавление заголовков
    for i, header in enumerate(table_rows[0]):
        cell = header_row.cells[i]
        run = cell.paragraphs[0].add_run(header)
        set_vertical_text(cell)
        set_cell_vertical_alignment(cell, align="center")
        set_cell_margins(cell, top=0.0, bottom=0.0, left=0.0, right=0.0)

    # Добавляем строки с данными и пустые строки после КАЖДОЙ строки
    for row_data in table_rows[1:]:
        # 1. Добавляем строку с данными
        data_row = table.add_row()
        for j, value in enumerate(row_data):
            cell = data_row.cells[j]
            cell.text = format_number(value)
            set_cell_margins(cell, top=0.0, bottom=0.0, left=0.0, right=0.0)
        
        # 2. Добавляем пустую строку с тем же номером режима
        empty_row = table.add_row()
        for j in range(len(table_rows[0])):
            cell = empty_row.cells[j]
            if j == 0:  # Первый столбец - номер режима
                cell.text = str(row_data[0])  # Сохраняем номер режима
            else:
                cell.text = ""  # Пустые ячейки
            set_cell_margins(cell, top=0.0, bottom=0.0, left=0.0, right=0.0)

    # Применяем стиль ко всем ячейкам
    apply_style_to_all_cells(table, 'Текст таблицы', numbered_style='Текст таблицы')

    return doc