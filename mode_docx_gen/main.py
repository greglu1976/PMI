import pandas as pd
from docx import Document
from docx.shared import Pt, Mm
from docx.enum.section import WD_ORIENTATION
from lxml import etree
import json

# Загрузка данных из Excel с конкретного листа 'Outputs'
df = pd.read_excel('1.xlsx', sheet_name='Outputs', header=0)

# Загрузка словаря для выборки столбцов из JSON-файла fsu_bnt_needed_outputs.json
with open('fsu_bnt_needed_outputs.json', 'r', encoding='utf-8') as f:
    needed_columns = json.load(f)

# Загрузка словаря для замены заголовков из JSON-файла fsu_mtz_outputs.json
with open('fsu_mtz_outputs.json', 'r', encoding='utf-8') as f:
    replacement_titles = json.load(f)

# Добавление столбца "Номер режима" в начало DataFrame
df.insert(0, 'Номер режима', range(1, len(df) + 1))

# Фильтрация DataFrame, оставляя только нужные столбцы (ключи из fsu_bnt_needed_outputs.json + "Номер режима")
needed_columns_with_mode = ['Номер режима'] + list(needed_columns.keys())
df_filtered = df[needed_columns_with_mode]

# Открытие шаблона документа
doc = Document('templ.docx')

# Настройка страницы формата A4 (297мм x 210мм) горизонтальной ориентации
section = doc.sections[-1]
section.orientation = WD_ORIENTATION.LANDSCAPE  # Горизонтальная ориентация
section.page_width = Mm(297)  # Ширина A4 в миллиметрах
section.page_height = Mm(210)  # Высота A4 в миллиметрах
section.top_margin = Mm(12.7)  # Отступы в миллиметрах (примерно 0.5 дюйма)
section.bottom_margin = Mm(12.7)
section.left_margin = Mm(12.7)
section.right_margin = Mm(12.7)

# Добавление таблицы
table = doc.add_table(rows=len(df_filtered)+1, cols=len(df_filtered.columns))
table.style = 'Стиль3'  # Применение стиля таблицы из шаблона

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
header_row.height = Mm(45)  # Устанавливаем высоту строки заголовка в 45 мм

# Добавление заголовков столбцов с вертикальной ориентацией и настройкой отступов
for i, column in enumerate(df_filtered.columns):
    cell = table.cell(0, i)
    # Используем значение из fsu_mtz_outputs.json для замены заголовка
    new_title = replacement_titles.get(column, column)  # Если нет соответствия, оставляем старое название
    run = cell.paragraphs[0].add_run(new_title)
    run.font.size = Pt(12)
    run.font.name = 'Arial'
    # Установка вертикальной ориентации текста
    if column != 'Номер режима':  # Вертикальная ориентация не применяется к "Номер режима"
        set_vertical_text(cell)
    # Установка отступов в ячейке
    set_cell_margins(cell, top=0.05, bottom=0.05, left=0.05, right=0.05)

# Добавление данных и настройка отступов в ячейках
for i in range(len(df_filtered)):
    for j, column in enumerate(df_filtered.columns):
        cell = table.cell(i+1, j)
        cell.text = str(df_filtered.iloc[i][column])
        run = cell.paragraphs[0].runs[0] if cell.paragraphs[0].runs else cell.paragraphs[0].add_run()
        run.font.size = Pt(12)
        run.font.name = 'Arial'
        # Установка отступов в ячейке
        set_cell_margins(cell, top=0.05, bottom=0.05, left=0.05, right=0.05)

# Сохранение документа
doc.save('output_document.docx')
print("Документ успешно создан: output_document.docx")