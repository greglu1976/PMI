import os
import pandas as pd
from docx import Document
from docx.shared import Pt, Mm
from docx.enum.section import WD_ORIENTATION
from lxml import etree
import json
import re

def horizont_A4(doc):
    # Настройка страницы формата A4 (297мм x 210мм) горизонтальной ориентации
    section = doc.sections[-1]
    section.orientation = WD_ORIENTATION.LANDSCAPE  # Горизонтальная ориентация
    section.page_width = Mm(297)  # Ширина A4 в миллиметрах
    section.page_height = Mm(210)  # Высота A4 в миллиметрах
    section.top_margin = Mm(12.7)  # Отступы в миллиметрах (примерно 0.5 дюйма)
    section.bottom_margin = Mm(12.7)
    section.left_margin = Mm(12.7)
    section.right_margin = Mm(12.7)

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

def procced_xlsx(folder_path, needed_columns, sheet_name):
    # Создаем пустой DataFrame для объединения данных
    combined_df = pd.DataFrame()
    # Итерация по всем файлам в папке
    for filename in os.listdir(folder_path):
        # Проверяем, что файл является xlsx и соответствует шаблону БНТ_#.xlsx
        if filename.endswith('.xlsx'): #and re.match(r'БНТ_\d+\.xlsx', filename):
            # Извлекаем номер режима из имени файла
            mode_number = int(filename.split('_')[1].split('.')[0])
            # Полный путь к файлу
            file_path = os.path.join(folder_path, filename)
            # Загружаем данные из Excel
            df = pd.read_excel(file_path, sheet_name=sheet_name, header=0)
            # Добавляем столбец "Номер режима"
            df.insert(0, 'Номер режима', mode_number)
            # Фильтруем DataFrame, оставляя только нужные столбцы
            needed_columns_with_mode = ['Номер режима'] + list(needed_columns.keys())
            df_filtered = df[needed_columns_with_mode]
            # Объединяем данные в общий DataFrame
            combined_df = pd.concat([combined_df, df_filtered], ignore_index=True)

    # Если DataFrame пустой, выходим
    if combined_df.empty:
        print("Нет подходящих файлов в папке.")
        exit()

    # Сортируем DataFrame по столбцу "Номер режима" по возрастанию
    combined_df = combined_df.sort_values(by='Номер режима', ascending=True).reset_index(drop=True)
    return combined_df

def add_table(doc, combined_df, replacement_titles, header_row_height):
    # Добавление таблицы
    table = doc.add_table(rows=len(combined_df)+1, cols=len(combined_df.columns))
    table.style = 'Стиль3'  # Применение стиля таблицы из шаблона

    # Установка высоты первой строки (заголовок)
    header_row = table.rows[0]
    header_row.height = Mm(header_row_height)  # Устанавливаем высоту строки заголовка в 45 мм

    # Добавление заголовков столбцов с вертикальной ориентацией и настройкой отступов
    for i, column in enumerate(combined_df.columns):
        cell = table.cell(0, i)
        # Используем значение из fsu_mtz_outputs.json для замены заголовка
        new_title = replacement_titles.get(column, column)  # Если нет соответствия, оставляем старое название
        run = cell.paragraphs[0].add_run(new_title)
        run.font.size = Pt(11)
        run.font.name = 'Arial'
        # Установка вертикальной ориентации текста
        #if column != 'Номер режима':  # Вертикальная ориентация не применяется к "Номер режима"
        set_vertical_text(cell)
        # Установка отступов в ячейке
        set_cell_margins(cell, top=0.05, bottom=0.05, left=0.05, right=0.05)

    # Добавление данных и настройка отступов в ячейках
    for i in range(len(combined_df)):
        for j, column in enumerate(combined_df.columns):
            cell = table.cell(i+1, j)
            cell.text = str(combined_df.iloc[i][column])
            run = cell.paragraphs[0].runs[0] if cell.paragraphs[0].runs else cell.paragraphs[0].add_run()
            run.font.size = Pt(11)
            run.font.name = 'Arial'
            # Установка отступов в ячейке
            set_cell_margins(cell, top=0.05, bottom=0.05, left=0.05, right=0.05)
    return doc

# Открытие шаблона документа
doc = Document('templ.docx')
horizont_A4(doc)
paragraph = doc.add_heading('Проверка БНТ', level=2)

# Путь к папке с файлами
folder_path = 'modes'

# Загрузка словаря для выборки столбцов из JSON-файла fsu_bnt_needed_inputs.json
with open('fsu_bnt_needed_inputs.json', 'r', encoding='utf-8') as f:
    needed_columns = json.load(f)
# Загрузка словаря для замены заголовков из JSON-файла fsu_mtz_inputs.json
with open('fsu_mtz_inputs.json', 'r', encoding='utf-8') as f:
    replacement_titles = json.load(f)
combined_df = procced_xlsx(folder_path, needed_columns, 'Inputs')
doc.add_paragraph('Выдаваемые сигналы', style='tablename1')
doc = add_table(doc, combined_df, replacement_titles, 25)

# Загрузка словаря для выборки столбцов из JSON-файла fsu_bnt_needed_outputs.json
with open('fsu_bnt_needed_outputs.json', 'r', encoding='utf-8') as f:
    needed_columns = json.load(f)
# Загрузка словаря для замены заголовков из JSON-файла fsu_mtz_outputs.json
with open('fsu_mtz_outputs.json', 'r', encoding='utf-8') as f:
    replacement_titles = json.load(f)
combined_df = procced_xlsx(folder_path, needed_columns, 'Outputs')
doc.add_paragraph('Контролируемые сигналы', style='tablename1')
doc = add_table(doc, combined_df, replacement_titles, 45)

# Загрузка словаря для выборки столбцов из JSON-файла fsu_mtz_sgfs.json
with open('fsu_mtz_sgfs.json', 'r', encoding='utf-8') as f:
    needed_columns = json.load(f)
# Загрузка словаря для замены заголовков из JSON-файла fsu_mtz_outputs.json
with open('fsu_mtz_sgfs.json', 'r', encoding='utf-8') as f:
    replacement_titles = json.load(f)
combined_df = procced_xlsx(folder_path, needed_columns, 'SGF_Parameters')
doc.add_paragraph('Состояние программных переключателей', style='tablename1')
doc = add_table(doc, combined_df, replacement_titles, 90)


# Сохранение документа
doc.save('_inouts.docx')
print("Документ успешно создан: _inouts.docx")