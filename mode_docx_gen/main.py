import pandas as pd
from docx import Document
from docx.shared import Pt, Mm
from docx.enum.section import WD_ORIENTATION
from lxml import etree

# Загрузка данных из Excel с конкретного листа 'Outputs'
df = pd.read_excel('1.xlsx', sheet_name='Outputs', header=0)

# Создание нового документа Word
doc = Document()

# Настройка страницы формата B3 (500мм x 353мм) горизонтальной ориентации
section = doc.sections[-1]
section.orientation = WD_ORIENTATION.LANDSCAPE
section.page_width = Mm(500)  # Ширина B3 в миллиметрах
section.page_height = Mm(353)  # Высота B3 в миллиметрах
section.top_margin = Mm(12.7)  # Отступы в миллиметрах (примерно 0.5 дюйма)
section.bottom_margin = Mm(12.7)
section.left_margin = Mm(12.7)
section.right_margin = Mm(12.7)

# Добавление таблицы
table = doc.add_table(rows=len(df)+1, cols=len(df.columns))

# Функция для установки вертикальной ориентации текста
def set_vertical_text(cell):
    tcPr = cell._tc.get_or_add_tcPr()
    text_direction = etree.Element('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}textDirection')
    text_direction.set('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val', 'btLr')
    tcPr.append(text_direction)

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

# Установка высоты первой строки (заголовок)
header_row = table.rows[0]
header_row.height = Mm(15)  # Устанавливаем высоту строки заголовка в 15 мм

# Добавление заголовков столбцов с вертикальной ориентацией и настройкой отступов
for i, column in enumerate(df.columns):
    cell = table.cell(0, i)
    run = cell.paragraphs[0].add_run(column)
    run.font.size = Pt(10)
    run.font.name = 'Arial'
    # Установка вертикальной ориентации текста
    set_vertical_text(cell)
    # Установка отступов в ячейке
    set_cell_margins(cell, top=0.05, bottom=0.05, left=0.05, right=0.05)

# Добавление данных и настройка отступов в ячейках
for i in range(len(df)):
    for j, column in enumerate(df.columns):
        cell = table.cell(i+1, j)
        cell.text = str(df.iloc[i][column])
        run = cell.paragraphs[0].runs[0] if cell.paragraphs[0].runs else cell.paragraphs[0].add_run()
        run.font.size = Pt(10)
        run.font.name = 'Arial'
        # Установка отступов в ячейке
        set_cell_margins(cell, top=0.05, bottom=0.05, left=0.05, right=0.05)

# Сохранение документа
doc.save('output_document.docx')