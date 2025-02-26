# В этой версии добавлена естественная сортировка БНТ_1, БНТ_2 (а не БНТ_10)
# для этого пустановлен модуль natsort (pip install natsort) 

import os
import pandas as pd
from docx import Document
from docx.shared import Pt, Mm
from docx.enum.section import WD_ORIENTATION
from lxml import etree
import json
import re
from natsort import natsorted  # Импортируем natsorted для естественной сортировки

from create_settings_from_mode2 import start_proceed_modes

def horizont_A4(doc):
    # Настройка страницы формата A4 (297мм x 210мм) горизонтальной ориентации
    section = doc.sections[-1]
    section.orientation = WD_ORIENTATION.PORTRAIT  # Горизонтальная ориентация
    section.page_width = Mm(210)  # Ширина A4 в миллиметрах
    section.page_height = Mm(297)  # Высота A4 в миллиметрах
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
        if filename.endswith('.xlsx'):  # and re.match(r'БНТ_\d+\.xlsx', filename):
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
        # if column != 'Номер режима':  # Вертикальная ориентация не применяется к "Номер режима"
        set_vertical_text(cell)
        # Установка отступов в ячейке
        set_cell_margins(cell, top=0.0, bottom=0.0, left=0.0, right=0.0)

    # Добавление данных и настройка отступов в ячейках
    for i in range(len(combined_df)):
        for j, column in enumerate(combined_df.columns):
            cell = table.cell(i+1, j)
            cell.text = str(combined_df.iloc[i][column])
            run = cell.paragraphs[0].runs[0] if cell.paragraphs[0].runs else cell.paragraphs[0].add_run()
            run.font.size = Pt(11)
            run.font.name = 'Arial'
            # Установка отступов в ячейке
            set_cell_margins(cell, top=0.0, bottom=0.0, left=0.0, right=0.0)
    return doc

# Функция для добавления таблицы в документ
def add_table_set(doc, data):
    table = doc.add_table(rows=len(data) + 1, cols=6)
    table.style = 'Стиль3'  # Применяем стиль таблицы

    # Заголовки столбцов
    headers = ['Параметр', 'Обозначение ФСУ', 'Значение / Диапазон', 'Ед.изм.', 'Шаг', 'Уставка']
    for i, header in enumerate(headers):
        cell = table.cell(0, i)
        cell.text = header

    # Добавление данных в таблицу
    for row_idx, (switch, values) in enumerate(data.items(), start=1):
        table.cell(row_idx, 0).text = f"{values.get('FullDescription', '')} ({values.get('ShortDescription', '')})"
        units = values.get('units', '')
        if 'SGF' in switch:
            table.cell(row_idx, 1).text = switch
            table.cell(row_idx, 2).text = values.get('Note', '').replace(',', '\n')
        else:
            table.cell(row_idx, 1).text = values.get('AppliedDescription', '')
            if units == 'мс':
                units = 'с'
                table.cell(row_idx, 2).text = f"{str(int(values.get('minValue', ''))/1000).replace('.', ',')} ... {str(int(values.get('maxValue', ''))/1000).replace('.', ',')} "
            else:
                table.cell(row_idx, 2).text = f"{values.get('minValue', '').replace('.', ',')} ... {values.get('maxValue', '').replace('.', ',')} "                

        table.cell(row_idx, 3).text = units
        table.cell(row_idx, 4).text = values.get('step', '').replace('.', ',')
        table.cell(row_idx, 5).text = str(values.get('SetValue', '')).replace('.', ',')

    return doc

# Функция для обработки всех файлов в папке modes2/
def process_all_xlsx_in_folder(folder_path, doc):
    # Получаем список всех .xlsx файлов в папке
    xlsx_files = [f for f in os.listdir(folder_path) if f.endswith('.xlsx')]
    
    # Сортируем файлы по естественному порядку (БНТ_1, БНТ_2, ..., БНТ_10)
    xlsx_files = natsorted(xlsx_files)

    for xlsx_file in xlsx_files:
        # Полный путь к файлу
        file_path = os.path.join(folder_path, xlsx_file)

        # Обрабатываем каждый файл
        doc = process_single_xlsx(file_path, doc)

    return doc

def process_single_xlsx(file_path, doc):
    # Получаем имя файла без расширения
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    
    # Создаем заголовок для текущего файла
    paragraph = doc.add_heading(f'Таблицы для конфигурирования режимов: {base_name}', level=3)

    # Обрабатываем файл Excel и получаем result_dict.json
    start_proceed_modes(file_path)

    # Загружаем description.json
    file_path_desc = 'part/description.json'
    with open(file_path_desc, 'r', encoding='utf-8') as desc_file:
        description_data = json.load(desc_file)

    # Загружаем result_dict.json для текущего файла
    result_json_path = f'modes2/{base_name}.json'
    with open(result_json_path, 'r', encoding='utf-8') as result_file:
        general_data = json.load(result_file)

    # Итерация по словарю general_data
    for fbname, functions in general_data.items():
        # Получаем описание FB из description_data
        fb_info = description_data.get(fbname, {})
        desc = fb_info.get('desc', 'Описание не найдено')
        fb_name = fb_info.get('fbname', 'FB не найдено')

        # Добавляем заголовок для FB
        paragraph = doc.add_heading(f"{desc} ({fb_name})", level=3)

        for func_name, switches in functions.items():
            if func_name == "":  # Если ключ пустой
                # Добавляем заголовок для общих уставок
                paragraph = doc.add_heading("Общие уставки", level=4)
            else:
                # Ищем описание функции в description_data
                func_desc_info = fb_info.get(func_name, {})
                func_desc = func_desc_info.get('funcname', 'Описание функции не найдено')
                func_short_name = func_desc_info.get('func_short_name', 'Код функции не найден')

                # Добавляем заголовок для функции
                paragraph = doc.add_heading(f"{func_desc} ({func_short_name})", level=4)

            # Добавляем таблицу для переключателей (switches)
            doc = add_table_set(doc, switches)

    return doc

# Открытие шаблона документа
doc = Document('templ.docx')
horizont_A4(doc)
paragraph = doc.add_heading('Проверка БНТ', level=2)

# Путь к папке с файлами
folder_path = 'modes2'

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

paragraph = doc.add_heading('Таблицы для конфигурирования режимов', level=3)

# Обрабатываем все файлы в папке
doc = process_all_xlsx_in_folder(folder_path, doc)
# Сохранение документа
doc.save('_inouts.docx')
print("Документ успешно создан: _inouts.docx")