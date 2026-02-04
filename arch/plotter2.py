import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side

# Читаем исходный файл
df = pd.read_excel('input.xlsx')  # замените 'input.xlsx' на имя вашего файла

# Преобразуем время к нужному формату: секунды.миллисекунды
df['Время'] = pd.to_datetime(df['Время'], format='%d.%m.%Y %H:%M:%S,%f')
df['Время_формат'] = df['Время'].dt.strftime('%S.%f').str[:6]  # СС.МММ (6 символов: СС.МММ)

# Создаем сводную таблицу, группируя события по времени
pivot_data = []
time_objects = []  # Для хранения объектов datetime для расчета интервалов

for time_str, group in df.groupby('Время_формат'):
    # Получаем первое время из группы (все времена в группе одинаковы)
    time_dt = group.iloc[0]['Время']
    time_objects.append(time_dt)
    
    events = []
    has_non_zero = False
    
    # Проверяем значения для каждого события
    for _, row in group.iterrows():
        event_name = row['Наименование события']
        value = row['Значение']
        
        # Если значение не 0, добавляем пометку
        if pd.notna(value) and value != 0:
            events.append(f"{event_name} [{value}]")  # Добавляем значение в квадратных скобках
            has_non_zero = True
        else:
            events.append(event_name)
    
    pivot_data.append({
        'Время': time_str,
        'Время_dt': time_dt,  # Сохраняем объект datetime для расчета интервалов
        'События': '\n'.join(events),
        'Есть_ненулевые': has_non_zero
    })

# Создаем DataFrame из сгруппированных данных
pivot_df = pd.DataFrame(pivot_data)

# Сортируем по времени
pivot_df = pivot_df.sort_values('Время_dt')

# Рассчитываем временные интервалы
time_intervals = []
for i in range(len(pivot_df)):
    if i == 0:
        # Для первого события интервал = 0
        time_intervals.append('0.000')
    else:
        # Вычисляем разницу в секундах с миллисекундами
        time_diff = (pivot_df.iloc[i]['Время_dt'] - pivot_df.iloc[i-1]['Время_dt']).total_seconds()
        time_intervals.append(f"{time_diff:.3f}")  # Форматируем до 3 знаков после запятой

# Создаем списки для строк
time_row = pivot_df['Время'].tolist()
events_row = pivot_df['События'].tolist()
flags_row = pivot_df['Есть_ненулевые'].tolist()

# Создаем Excel файл
output_file = 'events_timeline_output.xlsx'
wb = Workbook()
ws = wb.active
ws.title = "Таймлайн событий"

# Заполняем первую строку (время)
for col_idx, time_value in enumerate(time_row, 1):
    ws.cell(row=1, column=col_idx, value=time_value)

# Заполняем вторую строку (события)
for col_idx, events_value in enumerate(events_row, 1):
    ws.cell(row=2, column=col_idx, value=events_value)

# Заполняем третью строку (временные интервалы)
for col_idx, interval_value in enumerate(time_intervals, 1):
    ws.cell(row=3, column=col_idx, value=interval_value)

# Заполняем четвертую строку (флаги ненулевых значений)
for col_idx, flag_value in enumerate(flags_row, 1):
    ws.cell(row=4, column=col_idx, value=flag_value)

# Определяем стили
time_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
time_font = Font(color="FFFFFF", bold=True, size=10)
interval_fill = PatternFill(start_color="F2E0D6", end_color="F2E0D6", fill_type="solid")  # Бежевый для интервалов
interval_font = Font(color="000000", size=9)
normal_fill = PatternFill(start_color="F2F2F2", end_color="F2F2F2", fill_type="solid")
normal_font = Font(color="000000", size=9)
red_fill = PatternFill(start_color="FFCCCC", end_color="FFCCCC", fill_type="solid")  # Красный фон
red_font = Font(color="FF0000", bold=True, size=9)  # Красный текст

# Границы для ячеек
thin_border = Border(
    left=Side(style='thin'),
    right=Side(style='thin'),
    top=Side(style='thin'),
    bottom=Side(style='thin')
)

# Форматирование строки времени (первая строка)
for col_idx in range(1, len(time_row) + 1):
    cell = ws.cell(row=1, column=col_idx)
    cell.fill = time_fill
    cell.font = time_font
    cell.alignment = Alignment(horizontal="center", vertical="center")
    cell.border = thin_border

# Форматирование строки интервалов (третья строка)
for col_idx in range(1, len(time_intervals) + 1):
    cell = ws.cell(row=3, column=col_idx)
    cell.fill = interval_fill
    cell.font = interval_font
    cell.alignment = Alignment(horizontal="center", vertical="center")
    cell.border = thin_border
    
    # Добавляем пояснение для первого интервала
    if col_idx == 1:
        cell.value = f"0.000 (начало)"
    else:
        # Проверяем, большой ли интервал (больше 0.1 секунды)
        interval_val = float(cell.value)
        if interval_val > 0.1:
            cell.font = Font(color="FF0000", bold=True, size=9)  # Красный для больших интервалов

# Форматирование строки событий (вторая строка)
for col_idx in range(1, len(events_row) + 1):
    cell = ws.cell(row=2, column=col_idx)
    flag_cell = ws.cell(row=4, column=col_idx)
    has_non_zero = flag_cell.value
    
    if has_non_zero:
        cell.fill = red_fill
        cell.font = red_font
    else:
        cell.fill = normal_fill
        cell.font = normal_font
    
    cell.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
    cell.border = thin_border

# Скрываем четвертую строку с флагами
ws.row_dimensions[4].hidden = True

# Настройка размеров столбцов
for col_idx in range(1, len(time_row) + 1):
    # Максимальная длина в столбце
    max_length = 0
    for row in range(1, 4):  # Первые три строки (время, события, интервалы)
        cell_value = ws.cell(row=row, column=col_idx).value
        if cell_value:
            # Для многострочного текста берем максимальную длину строки
            if "\n" in str(cell_value):
                lines = str(cell_value).split("\n")
                max_line_length = max(len(line) for line in lines)
                max_length = max(max_length, max_line_length)
            else:
                max_length = max(max_length, len(str(cell_value)))
    
    # Устанавливаем ширину столбца
    column_letter = ws.cell(row=1, column=col_idx).column_letter
    ws.column_dimensions[column_letter].width = min(max_length + 3, 40)  # Увеличил макс ширину до 40

# Настройка высоты строк
ws.row_dimensions[1].height = 25  # Строка времени
ws.row_dimensions[2].height = 80  # Строка событий
ws.row_dimensions[3].height = 25  # Строка интервалов

# Добавляем заголовки строк слева (опционально, если нужно)
header_fill = PatternFill(start_color="E6E6E6", end_color="E6E6E6", fill_type="solid")
header_font = Font(bold=True)

# Если нужно добавить заголовки строк:
# ws.cell(row=1, column=1, value="Время").fill = header_fill
# ws.cell(row=1, column=1).font = header_font
# ws.cell(row=2, column=1, value="События").fill = header_fill
# ws.cell(row=2, column=1).font = header_font
# ws.cell(row=3, column=1, value="Интервал").fill = header_fill
# ws.cell(row=3, column=1).font = header_font

# Сохраняем файл
wb.save(output_file)

# Выводим статистику
print(f"Таблица успешно создана: {output_file}")
print(f"Количество временных меток: {len(pivot_df)}")
print(f"Колонок с ненулевыми значениями: {pivot_df['Есть_ненулевые'].sum()}")

# Статистика по интервалам
if len(time_intervals) > 1:
    intervals_numeric = [float(x) for x in time_intervals[1:]]  # Пропускаем первый (0)
    max_interval = max(intervals_numeric)
    min_interval = min(intervals_numeric)
    avg_interval = sum(intervals_numeric) / len(intervals_numeric)
    
    print(f"\nСтатистика временных интервалов:")
    print(f"  Максимальный интервал: {max_interval:.3f} сек")
    print(f"  Минимальный интервал: {min_interval:.3f} сек")
    print(f"  Средний интервал: {avg_interval:.3f} сек")
    
    # Подсчет интервалов больше 0.1 сек
    long_intervals = [x for x in intervals_numeric if x > 0.1]
    print(f"  Интервалов > 0.1 сек: {len(long_intervals)}")