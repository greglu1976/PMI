# coding=utf-8

# Изменения - вместо генерации все уставок, если не было изменений по сравнению с предыдущем режимом. Добавляется строка - Параметры не изменились
# ВЕРСИЯ 6

import os
import pandas as pd
from docx import Document
from docx.shared import Pt, Mm
from docx.enum.section import WD_ORIENTATION
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from lxml import etree
import json
import re
from natsort import natsorted  # Импортируем natsorted для естественной сортировки

from docx.shared import Inches
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
from docx.oxml import OxmlElement
from docx.oxml.ns import qn


from analizator import start_analyze
from create_settings_from_mode2 import start_proceed_modes

# Добавляем глобальную переменную для управления выводом таблиц
GEN_MODE = 1  # Если 1 - таблицы без изменений не выводятся, если = 2 - то выводятся все таблицы режимов с изменениями, =3 - то таблицы сохраняются в свой файл
REGENERATE = 1 # Перегенерировать XLSX в JSON - если =1, иначе не перегенерируются 

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

def add_table(doc, combined_df, replacement_titles, header_row_height, is_ctrl_row=False):
    # Добавление таблицы
    table = doc.add_table(rows=len(combined_df) + 1, cols=len(combined_df.columns))
    table.style = 'Стиль3'  # Применение стиля таблицы из шаблона
    # Замена точек на запятые в combined_df
    combined_df = combined_df.applymap(lambda x: str(x).replace('.', ',') if isinstance(x, (float, int)) else x)
    #print('================>', combined_df)

    # Установка высоты первой строки (заголовок)
    header_row = table.rows[0]
    header_row.height = Mm(header_row_height)  # Устанавливаем высоту строки заголовка
    set_repeat_table_header(header_row)

    # Добавление заголовков столбцов с вертикальной ориентацией и настройкой отступов
    for i, column in enumerate(combined_df.columns):
        cell = table.cell(0, i)
        cell.paragraphs[0].style = 'Текст таблицы'
        # Используем значение из fsu_mtz_outputs.json для замены заголовка
        new_title = replacement_titles.get(column, column)  # Если нет соответствия, оставляем старое название
        run = cell.paragraphs[0].add_run(new_title)
        #run.font.size = Pt(11)
        #run.font.name = 'Arial'
        # Установка вертикальной ориентации текста
        set_vertical_text(cell)
        set_cell_vertical_alignment(cell, align="center")
        # Установка отступов в ячейке
        set_cell_margins(cell, top=0.0, bottom=0.0, left=0.0, right=0.0)

    # Добавление данных и настройка отступов в ячейках
    row_index = 1  # Начинаем с первой строки данных (после заголовка)
    for i in range(len(combined_df)):
        # Добавляем строку с данными
        for j, column in enumerate(combined_df.columns):
            cell = table.cell(row_index, j)
            cell.text = str(combined_df.iloc[i][column])
            run = cell.paragraphs[0].runs[0] if cell.paragraphs[0].runs else cell.paragraphs[0].add_run()
            #run.font.size = Pt(11)
            #run.font.name = 'Arial'
            # Установка отступов в ячейке
            set_cell_margins(cell, top=0.0, bottom=0.0, left=0.0, right=0.0)

        # Если is_ctrl_row == True, добавляем пустую строку после текущей строки
        if is_ctrl_row:
            # Добавляем новую пустую строку
            table.add_row()
            row_index += 1  # Переходим к новой строке
            mode_number = combined_df.iloc[i]['Номер режима']  # Берем номер режима из текущей строки
            for j, column in enumerate(combined_df.columns):
                cell = table.cell(row_index, j)
                if column == 'Номер режима':  # Для столбца "Номер режима" дублируем значение
                    cell.text = str(mode_number+'') # Было здесь +' (рез)'
                else:  # Для остальных столбцов оставляем пустые значения
                    cell.text = ""
                # Настройка отступов в ячейке
                set_cell_margins(cell, top=0.0, bottom=0.0, left=0.0, right=0.0)

        row_index += 1  # Переходим к следующей строке данных

    # Применяем стиль "Текст таблицы" ко всем ячейкам
    apply_style_to_all_cells(table, 'Текст таблицы', numbered_style='Текст таблицы')

    return doc

def set_cell_vertical_alignment(cell, align="center"):
        tc = cell._tc
        tcPr = tc.get_or_add_tcPr()
        tcValign = OxmlElement('w:vAlign')
        tcValign.set(qn('w:val'), align)
        tcPr.append(tcValign)

def set_repeat_table_header(row):
    """ set repeat table row on every new page
    """
    tr = row._tr
    trPr = tr.get_or_add_trPr()
    tblHeader = OxmlElement('w:tblHeader')
    tblHeader.set(qn('w:val'), "true")
    trPr.append(tblHeader)
    return row

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

def add_table_set(doc, data):
    # Создаем таблицу
    table = doc.add_table(rows=len(data) + 1, cols=6)

    # Установка высоты первой строки (заголовок)
    header_row = table.rows[0]
    header_row.height = Mm(5)  # Устанавливаем высоту строки заголовка в 45 мм
    set_repeat_table_header(header_row)

    # Заголовки столбцов
    headers = ['Параметр', 'Обозначение ФСУ', 'Значение / Диапазон', 'Ед.изм.', 'Шаг', 'Уставка']
    for i, header in enumerate(headers):
        cell = table.cell(0, i)
        cell.text = header
        # Делаем заголовки жирными
        cell.paragraphs[0].runs[0].bold = True
        cell.paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        cell.paragraphs[0].style = 'Текст таблицы'
        set_cell_vertical_alignment(cell, align="center")

    # Добавление данных в таблицу
    for row_idx, (switch, values) in enumerate(data.items(), start=1):
        full_desc_processed = values.get('FullDescription', '').replace('<<','«').replace('>>','»')
        table.cell(row_idx, 0).text = f"{full_desc_processed} ({values.get('ShortDescription', '')})"
        units = values.get('units', '')
        
        if 'SGF' in switch:
            table.cell(row_idx, 1).text = switch
            t = values.get('Note', '').replace('\n', '')
            t = t.replace(', ', '\n')
            table.cell(row_idx, 2).text = t.replace(',', '\n')
        else:
            table.cell(row_idx, 1).text = values.get('AppliedDescription', '')
            if units == 'мс':
                units = 'с'
                table.cell(row_idx, 2).text = f"{str(int(values.get('minValue', ''))/1000).replace('.', ',')} ... {str(int(values.get('maxValue', ''))/1000).replace('.', ',')} "
            else:
                table.cell(row_idx, 2).text = f"{values.get('minValue', '').replace('.', ',')} ... {values.get('maxValue', '').replace('.', ',')} "

        table.cell(row_idx, 3).text = units
        table.cell(row_idx, 4).text = values.get('step', '').replace('.', ',')
        set_value = str(values.get('SetValue', '')).replace('.', ',')
        table.cell(row_idx, 5).text = set_value

        # Проверка значения 'Color' и изменение фона ячейки
        if values.get('Color', '') == 'changed':
            cell = table.cell(row_idx, 5)  # Ячейка в столбце 'Уставка'
            shading_elm = parse_xml(r'<w:shd {} w:fill="FFC000"/>'.format(nsdecls('w')))
            cell._tc.get_or_add_tcPr().append(shading_elm)

        # Настройка выравнивания и отступов для первого столбца
        first_cell = table.cell(row_idx, 0)  # Ячейка первого столбца
        for paragraph in first_cell.paragraphs:
            # Устанавливаем выравнивание по левому краю
            #paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
            paragraph.style = "ЮИ_Таблица_Нумерованный"


    # Применяем стиль "Текст таблицы" ко всем ячейкам
    apply_style_to_all_cells(table, 'ЮИ_Таблица_Текст')

    table.style = 'Стиль3'
    table.allow_autofit = False
    # Задаем ширину столбцов (в дюймах)
    widths = [2.0, 1.2, 2.0, 0.7, 0.7, 0.7]  # Настройте значения под ваши нужды
    for i, width in enumerate(widths):
        for cell in table.columns[i].cells:
            cell.width = Inches(width)
    return doc

# Вспомогательная функция для создания XML-элемента с заданным цветом фона
def parse_xml(xml_string):
    return etree.fromstring(xml_string)

# Этап 1: Генерация JSON для всех файлов
def generate_json_for_all_xlsx(folder_path, root_dir=''):
    # Получаем список всех .xlsx файлов в папке
    xlsx_files = [f for f in os.listdir(folder_path) if f.endswith('.xlsx')]
    
    # Сортируем файлы по естественному порядку (БНТ_1, БНТ_2, ..., БНТ_10)
    xlsx_files = natsorted(xlsx_files)

    for xlsx_file in xlsx_files:
        # Полный путь к файлу
        file_path = os.path.join(folder_path, xlsx_file)

        # Обрабатываем каждый файл и генерируем JSON
        start_proceed_modes(file_path, root_dir)


# Этап 2: Добавление данных из JSON в документ - при этом приводятся только таблицы с изменениями
def add_json_data_to_doc(folder_path, doc, root_dir=''):
    # Получаем список всех .json файлов в папке
    json_files = [f for f in os.listdir(folder_path) if f.endswith('.json')]
    
    # Сортируем файлы по естественному порядку (БНТ_1.json, БНТ_2.json, ..., БНТ_10.json)
    json_files = natsorted(json_files)

    previous_general_data = None  # Переменная для хранения данных предыдущего режима

    # Загружаем description.json
    file_path_desc = root_dir + 'part/description.json'
    with open(file_path_desc, 'r', encoding='utf-8') as desc_file:
        description_data = json.load(desc_file)

    for idx, json_file in enumerate(json_files):
        # Полный путь к файлу
        file_path = os.path.join(folder_path, json_file)

        # Получаем имя файла без расширения
        base_name = os.path.splitext(json_file)[0]
        base_name_parts = base_name.split('_')

        # Создаем заголовок для текущего файла
        paragraph = doc.add_heading(f'Параметры для проверки функции: {base_name_parts[0]}. Режим №{base_name_parts[1]}', level=3)

        # Загружаем result_dict.json для текущего файла
        with open(file_path, 'r', encoding='utf-8') as result_file:
            current_general_data = json.load(result_file)

        # Проверяем, есть ли изменения в текущем режиме
        has_changes = False
        if previous_general_data is not None:
            for fbname, functions in current_general_data.items():
                if fbname in previous_general_data:
                    prev_functions = previous_general_data[fbname]
                    for func_name, switches in functions.items():
                        if func_name in prev_functions:
                            prev_switches = prev_functions[func_name]
                            for switch, values in switches.items():
                                if switch in prev_switches and values.get('Color', '') == 'changed':
                                    has_changes = True
                                    break
                        else:
                            has_changes = True  # Новая функция появилась
                else:
                    has_changes = True  # Новый FB появился
        else:
            # Для первого режима всегда добавляем таблицы
            has_changes = True

        # Если это первый режим, выводим все таблицы
        if idx == 0:
            # Итерация по словарю current_general_data
            for fbname, functions in current_general_data.items():
                # Получаем описание FB из description_data
                fb_info = description_data.get(fbname, {})
                desc = fb_info.get('desc', 'Описание не найдено')
                fb_name = fb_info.get('fbname', 'FB не найдено')

                # Добавляем заголовок для FB
                paragraph = doc.add_heading(f"{desc} ({fb_name})", level=4)

                for func_name, switches in functions.items():
                    if func_name == "":  # Если ключ пустой
                        # Добавляем заголовок для общих уставок
                        doc.add_paragraph('Общие уставки', style='ЮИ_Таблица_Название')
                    else:
                        # Ищем описание функции в description_data
                        func_desc_info = fb_info.get(func_name, {})
                        func_desc = func_desc_info.get('funcname', 'Описание функции не найдено')
                        func_short_name = func_desc_info.get('func_short_name', 'Код функции не найден')

                        # Добавляем заголовок для функции
                        doc.add_paragraph(f"{func_desc} ({func_short_name})", style='ЮИ_Таблица_Название')

                    # Добавляем таблицу для переключателей (switches)
                    doc = add_table_set(doc, switches)

        # Если это не первый режим и нет изменений, добавляем сообщение
        elif not has_changes:
            doc.add_heading(f"Параметры режима идентичны предыдущему.", level=4)
            previous_general_data = current_general_data  # Обновляем данные предыдущего режима
            continue  # Пропускаем вывод таблиц для этого режима

        # Если это не первый режим и есть изменения, выводим только измененные таблицы
        else:
            # Итерация по словарю current_general_data
            for fbname, functions in current_general_data.items():
                # Получаем описание FB из description_data
                fb_info = description_data.get(fbname, {})
                desc = fb_info.get('desc', 'Описание не найдено')
                fb_name = fb_info.get('fbname', 'FB не найдено')

                # Проверяем, есть ли изменения в текущем FB
                has_changes_in_fb = any(
                    any(values.get('Color', '') == 'changed' for values in switches.values())
                    for switches in functions.values()
                )

                # Если в FB нет изменений, пропускаем вывод
                if not has_changes_in_fb:
                    continue

                # Добавляем заголовок для FB
                paragraph = doc.add_heading(f"{desc} ({fb_name})", level=4)

                for func_name, switches in functions.items():
                    # Проверяем, есть ли изменения в текущей функции
                    has_changes_in_func = any(values.get('Color', '') == 'changed' for values in switches.values())

                    # Если в функции нет изменений, пропускаем вывод
                    if not has_changes_in_func:
                        continue

                    if func_name == "":  # Если ключ пустой
                        # Добавляем заголовок для общих уставок
                        doc.add_paragraph('Общие уставки', style='ЮИ_Таблица_Название')
                    else:
                        # Ищем описание функции в description_data
                        func_desc_info = fb_info.get(func_name, {})
                        func_desc = func_desc_info.get('funcname', 'Описание функции не найдено')
                        func_short_name = func_desc_info.get('func_short_name', 'Код функции не найден')

                        # Добавляем заголовок для функции
                        doc.add_paragraph(f"{func_desc} ({func_short_name})", style='ЮИ_Таблица_Название')

                    # Добавляем таблицу для переключателей (switches)
                    doc = add_table_set(doc, switches)

        # Обновляем данные предыдущего режима
        previous_general_data = current_general_data

    return doc

# Этап 2 СТАРЫЙ: Добавление данных из JSON в документ при этом если есть хоть одно изменение в режиме то приводятся все таблицы режима
def add_json_data_to_doc_old(folder_path, doc, root_dir=''):
    # Получаем список всех .json файлов в папке
    json_files = [f for f in os.listdir(folder_path) if f.endswith('.json')]
    
    # Сортируем файлы по естественному порядку (БНТ_1.json, БНТ_2.json, ..., БНТ_10.json)
    json_files = natsorted(json_files)

    previous_general_data = None  # Переменная для хранения данных предыдущего режима

    # Загружаем description.json
    file_path_desc = root_dir + 'part/description.json'
    with open(file_path_desc, 'r', encoding='utf-8') as desc_file:
        description_data = json.load(desc_file)

    for idx, json_file in enumerate(json_files):
        # Полный путь к файлу
        file_path = os.path.join(folder_path, json_file)

        # Получаем имя файла без расширения
        base_name = os.path.splitext(json_file)[0]
        base_name_parts = base_name.split('_')

        # Создаем заголовок для текущего файла
        paragraph = doc.add_heading(f'Параметры для проверки функции: {base_name_parts[0]}. Режим №{base_name_parts[1]}', level=3)

        # Загружаем result_dict.json для текущего файла
        with open(file_path, 'r', encoding='utf-8') as result_file:
            current_general_data = json.load(result_file)

        # Проверяем, есть ли изменения в текущем режиме
        has_changes = False
        if previous_general_data is not None:
            for fbname, functions in current_general_data.items():
                if fbname in previous_general_data:
                    prev_functions = previous_general_data[fbname]
                    for func_name, switches in functions.items():
                        if func_name in prev_functions:
                            prev_switches = prev_functions[func_name]
                            for switch, values in switches.items():
                                if switch in prev_switches and values.get('Color', '') == 'changed':
                                    has_changes = True
                                    break
                        else:
                            has_changes = True  # Новая функция появилась
                else:
                    has_changes = True  # Новый FB появился
        else:
            # Для первого режима всегда добавляем таблицы
            has_changes = True

        # Если нет изменений, добавляем сообщение об идентичности режима
        if not has_changes:
            doc.add_heading(f"Параметры режима идентичны предыдущему.", level=4)
            previous_general_data = current_general_data  # Обновляем данные предыдущего режима
            continue

        # Итерация по словарю current_general_data
        for fbname, functions in current_general_data.items():
            # Получаем описание FB из description_data
            fb_info = description_data.get(fbname, {})
            desc = fb_info.get('desc', 'Описание не найдено')
            fb_name = fb_info.get('fbname', 'FB не найдено')

            # Добавляем заголовок для FB
            paragraph = doc.add_heading(f"{desc} ({fb_name})", level=4)

            for func_name, switches in functions.items():
                if func_name == "":  # Если ключ пустой
                    # Добавляем заголовок для общих уставок
                    doc.add_paragraph('Общие уставки', style='ЮИ_Таблица_Название')
                else:
                    # Ищем описание функции в description_data
                    func_desc_info = fb_info.get(func_name, {})
                    func_desc = func_desc_info.get('funcname', 'Описание функции не найдено')
                    func_short_name = func_desc_info.get('func_short_name', 'Код функции не найден')

                    # Добавляем заголовок для функции
                    doc.add_paragraph(f"{func_desc} ({func_short_name})", style='ЮИ_Таблица_Название')

                # Добавляем таблицу для переключателей (switches)
                doc = add_table_set(doc, switches)

        # Обновляем данные предыдущего режима
        previous_general_data = current_general_data

    return doc

# Этап 2 ОПТИМИЗИРОВАННЫЙ: Добавление данных из JSON в документ сохранение в свой файл с настройками
def add_json_data_to_doc_opt(folder_path, doc, root_dir=''):

    doc_set = Document('template_set.docx') # загружаем шаблон для уставок

    # Получаем список всех .json файлов в папке
    json_files = [f for f in os.listdir(folder_path) if f.endswith('.json')]
    
    # Сортируем файлы по естественному порядку (БНТ_1.json, БНТ_2.json, ..., БНТ_10.json)
    json_files = natsorted(json_files)

    previous_general_data = None  # Переменная для хранения данных предыдущего режима

    # Загружаем description.json
    file_path_desc = root_dir + 'part/description.json'
    with open(file_path_desc, 'r', encoding='utf-8') as desc_file:
        description_data = json.load(desc_file)

    for idx, json_file in enumerate(json_files):
        # Полный путь к файлу
        file_path = os.path.join(folder_path, json_file)

        # Получаем имя файла без расширения
        base_name = os.path.splitext(json_file)[0]
        base_name_parts = base_name.split('_')

        # Создаем заголовок для текущего файла
        paragraph = doc.add_heading(f'Параметры для проверки функции: {base_name_parts[0]}. Режим №{base_name_parts[1]}', level=3)
        paragraph = doc_set.add_heading(f'Параметры для проверки функции: {base_name_parts[0]}. Режим №{base_name_parts[1]}', level=9)
        set_file_name = f'{base_name_parts[0]}. Режим №{base_name_parts[1]}'

        # Загружаем result_dict.json для текущего файла
        with open(file_path, 'r', encoding='utf-8') as result_file:
            current_general_data = json.load(result_file)

        # Проверяем, есть ли изменения в текущем режиме
        has_changes = False
        if previous_general_data is not None:
            for fbname, functions in current_general_data.items():
                if fbname in previous_general_data:
                    prev_functions = previous_general_data[fbname]
                    for func_name, switches in functions.items():
                        if func_name in prev_functions:
                            prev_switches = prev_functions[func_name]
                            for switch, values in switches.items():
                                if switch in prev_switches and values.get('Color', '') == 'changed':
                                    has_changes = True
                                    break
                        else:
                            has_changes = True  # Новая функция появилась
                else:
                    has_changes = True  # Новый FB появился
        else:
            # Для первого режима всегда добавляем таблицы
            has_changes = True

        # Если нет изменений, добавляем сообщение об идентичности режима
        if not has_changes:
            doc.add_heading(f"Параметры режима идентичны предыдущему.", level=4)
            previous_general_data = current_general_data  # Обновляем данные предыдущего режима
            continue
        paragraph = doc.add_heading("Данные режима приведены в документе по ссылке", level=4)
        # Итерация по словарю current_general_data
        for fbname, functions in current_general_data.items():
            # Получаем описание FB из description_data
            fb_info = description_data.get(fbname, {})
            desc = fb_info.get('desc', 'Описание не найдено')
            fb_name = fb_info.get('fbname', 'FB не найдено')

            # Добавляем заголовок для FB
            paragraph = doc_set.add_heading(f"{desc} ({fb_name})", level=2)
            
            for func_name, switches in functions.items():
                if func_name == "":  # Если ключ пустой
                    # Добавляем заголовок для общих уставок
                    doc_set.add_paragraph('Общие уставки', style='ЮИ_Таблица_Название')
                else:
                    # Ищем описание функции в description_data
                    func_desc_info = fb_info.get(func_name, {})
                    func_desc = func_desc_info.get('funcname', 'Описание функции не найдено')
                    func_short_name = func_desc_info.get('func_short_name', 'Код функции не найден')

                    # Добавляем заголовок для функции
                    doc_set.add_paragraph(f"{func_desc} ({func_short_name})", style='ЮИ_Таблица_Название')

                # Добавляем таблицу для переключателей (switches)
                doc_set = add_table_set(doc_set, switches)

        # Обновляем данные предыдущего режима
        previous_general_data = current_general_data
        doc_set.save(set_file_name+'.docx')

    return doc



# Основной код
def make_par(doc, heading, intro_text, func_modes_dir, needed_inputs, needed_outputs):
    # Корень
    root_dir = 'pmi_mtz\\'

    #print('========================================', heading, intro_text, func_modes_dir, needed_inputs, needed_outputs)
    # Параметры описания
    #heading = 'Проверка МТЗ 3 ступень'
    #intro_text = 'Для проверки функции третьей ступени в составе МТЗ предусматривается 20 режимов. Перечень подаваемых воздействий для каждого режима приводится в таблице XXX. Контроль выходных сигналов для каждого из режимов осуществляется в соответствии с таблицей XXX по осциллограмме, либо (в случае автоматизированной проверки) по контактам выходных реле (см. таблицу XXX).'
    #func_modes_dir = 'mtz3_modes'
    #needed_inputs = 'fsu_mtz3_needed_inputs.json'
    #needed_outputs = 'fsu_mtz3_needed_outputs.json'


    # Путь к папке с файлами
    #folder_path = root_dir + 'bnt_modes' # ПАПКА УКАЗЫВАЕТСЯ ТОЛЬКО ЗДЕСЬ - к режимам в xlsx
    folder_path = root_dir + func_modes_dir


    if REGENERATE==1:
        # Этап 1: Генерация JSON
        generate_json_for_all_xlsx(folder_path, root_dir)
        # Этап 1.1: Контроль режимов в JSON
        start_analyze(folder_path)

    # Открытие шаблона документа
    #doc = Document('templ1.docx')
    #doc = Document('template.docx')
    #horizont_A4(doc)
    paragraph = doc.add_heading(heading, level=2)
    paragraph = doc.add_heading(intro_text, level=3)

    # Загрузка словаря для выборки столбцов из JSON-файла fsu_bnt_needed_inputs.json
    with open(root_dir + needed_inputs, 'r', encoding='utf-8') as f:
        needed_columns = json.load(f)
    # Загрузка словаря для замены заголовков из JSON-файла fsu_mtz_inputs.json
    with open(root_dir+'fsu_mtz_inputs.json', 'r', encoding='utf-8') as f:
        replacement_titles = json.load(f)
    combined_df = procced_xlsx(folder_path, needed_columns, 'Inputs')
    
    doc.add_paragraph('Подаваемые воздействия при проверке', style='ЮИ_Таблица_Название')
    doc = add_table(doc, combined_df, replacement_titles, 25)

    # Этап 2: Добавление данных из JSON в документ
    if GEN_MODE==1:
        doc = add_json_data_to_doc(folder_path, doc, root_dir)
    elif GEN_MODE==2:
        doc = add_json_data_to_doc_old(folder_path, doc, root_dir)
    else:
        doc = add_json_data_to_doc_opt(folder_path, doc, root_dir)    

    return doc

def make_par2(doc, heading, intro_text, func_modes_dir, needed_inputs, needed_outputs):
    # Корень
    root_dir = 'pmi_mtz\\'

    # Параметры описания
    #heading = 'Проверка МТЗ 3 ступень'
    #intro_text = 'Для проверки функции третьей ступени в составе МТЗ предусматривается 20 режимов. Перечень подаваемых воздействий для каждого режима приводится в таблице XXX. Контроль выходных сигналов для каждого из режимов осуществляется в соответствии с таблицей XXX по осциллограмме, либо (в случае автоматизированной проверки) по контактам выходных реле (см. таблицу XXX).'
    #func_modes_dir = 'mtz3_modes'
    #needed_inputs = 'fsu_mtz3_needed_inputs.json'
    #needed_outputs = 'fsu_mtz3_needed_outputs.json'

    # Путь к папке с файлами

    folder_path = root_dir + func_modes_dir

    #horizont_A4(doc)
    paragraph = doc.add_heading(heading, level=2)
    paragraph = doc.add_heading(intro_text, level=3)

    # Загрузка словаря для выборки столбцов из JSON-файла fsu_bnt_needed_outputs.json
    with open(root_dir + needed_outputs, 'r', encoding='utf-8') as f:
        needed_columns = json.load(f)
    # Загрузка словаря для замены заголовков из JSON-файла fsu_mtz_outputs.json
    with open(root_dir+'fsu_mtz_outputs.json', 'r', encoding='utf-8') as f:
        replacement_titles = json.load(f)
    combined_df = procced_xlsx(folder_path, needed_columns, 'Outputs')
    doc.add_paragraph('Контролируемые сигналы при проверке', style='ЮИ_Таблица_Название')
    doc = add_table(doc, combined_df, replacement_titles, 45, is_ctrl_row=True)
    #paragraph = doc.add_heading('Таблицы для конфигурирования режимов', level=3)

    return doc