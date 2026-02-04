import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from datetime import timedelta

# Чтение Excel файла
df = pd.read_excel('Т Журнал событий.xlsx')  # укажите имя вашего файла

# Преобразование времени в формат datetime
df['Время'] = pd.to_datetime(df['Время'], format='%d.%m.%Y %H:%M:%S,%f')

# Упорядочивание по времени
df = df.sort_values('Время')

# Группировка событий по времени
time_groups = {}
for idx, row in df.iterrows():
    time_key = row['Время']
    if time_key not in time_groups:
        time_groups[time_key] = []
    time_groups[time_key].append(row['Наименование события'])

# Создание плавного интерактивного графика
fig, ax = plt.subplots(figsize=(20, 12))

# Отображаем все временные метки
unique_times = sorted(time_groups.keys())

# Сначала рисуем все элементы графика
time_labels = [t.strftime('%H:%M:%S.%f')[:-3] for t in unique_times]
ax.set_xticks(unique_times)
ax.set_xticklabels(time_labels, rotation=90, fontsize=9)

# Вертикальные линии
vertical_lines = []
for time_key in unique_times:
    line = ax.axvline(x=time_key, color='gray', alpha=0.15, 
                     linestyle='-', linewidth=0.8, zorder=1)
    vertical_lines.append(line)

# Отображаем события с интеллектуальным размещением подписей
circles = []
text_labels = []
connectors = []

# Функция для интеллектуального размещения
label_positions = {}

def find_free_position(time_key, base_y, max_attempts=10):
    """Ищет свободную вертикальную позицию для подписи"""
    for offset in range(max_attempts):
        if offset % 2 == 0:
            test_y = base_y + (offset // 2) * 0.4
        else:
            test_y = base_y - ((offset + 1) // 2) * 0.4
        
        position_key = (time_key, round(test_y, 2))
        if position_key not in label_positions:
            return test_y
    return base_y

# Отрисовка всех событий
for time_idx, (time_key, event_list) in enumerate(sorted(time_groups.items())):
    for event_idx, event in enumerate(event_list):
        base_y = event_idx
        
        # Ищем свободную позицию для подписи
        label_y = find_free_position(time_key, base_y)
        position_key = (time_key, round(label_y, 2))
        label_positions[position_key] = True
        
        # Кружок события
        circle = ax.plot(time_key, base_y, 'ro', markersize=10, 
                        alpha=0.8, markeredgecolor='black', 
                        markeredgewidth=1, zorder=5)[0]
        circles.append(circle)
        
        # Подпись
        short_event = event[:35] + ('...' if len(event) > 35 else '')
        text_offset_x = pd.Timedelta(milliseconds=15)
        
        label = ax.text(time_key + text_offset_x, label_y, short_event,
                       fontsize=8, ha='left', va='center',
                       bbox=dict(boxstyle="round,pad=0.2",
                                facecolor="lightyellow",
                                edgecolor="orange",
                                alpha=0.8),
                       zorder=4)
        text_labels.append(label)
        
        # Соединительная линия
        connector = ax.plot([time_key, time_key + text_offset_x], 
                          [base_y, label_y], 'k:', 
                          alpha=0.3, linewidth=0.8, dashes=(2, 2),
                          zorder=3)[0]
        connectors.append(connector)

# Настройка осей и заголовка
ax.set_xlabel('Время событий', fontsize=12)
ax.set_ylabel('Позиция события', fontsize=12)
ax.set_title('Плавная интерактивная диаграмма событий\nКолесико: масштаб | ЛКМ: панорамирование', 
             fontsize=14, fontweight='bold')

# Настройка сетки
ax.grid(True, alpha=0.2, linestyle='--', axis='y')
ax.set_axisbelow(True)

# Сохраняем исходные пределы
xlim_original = ax.get_xlim()
ylim_original = ax.get_ylim()

# Настраиваем начальные пределы
if time_groups:
    max_y = max(len(events) for events in time_groups.values()) - 1
    ax.set_ylim(-1.5, max_y + 1.5)

# Переменные для панорамирования
pan_start = None
pan_button = None
last_xlim = ax.get_xlim()
last_ylim = ax.get_ylim()

# Оптимизация: кэш для форматера времени
time_formatter_cache = {}

def get_time_formatter(time_range_seconds):
    """Возвращает подходящий форматтер времени (с кэшированием)"""
    if time_range_seconds in time_formatter_cache:
        return time_formatter_cache[time_range_seconds]
    
    if time_range_seconds < 1:
        formatter = mdates.DateFormatter('%H:%M:%S.%f')
    elif time_range_seconds < 10:
        formatter = mdates.DateFormatter('%H:%M:%S')
    elif time_range_seconds < 60:
        formatter = mdates.DateFormatter('%H:%M:%S')
    elif time_range_seconds < 300:
        formatter = mdates.DateFormatter('%H:%M:%S')
    else:
        formatter = mdates.DateFormatter('%H:%M')
    
    time_formatter_cache[time_range_seconds] = formatter
    return formatter

# Счетчик для дебаг-информации
frame_count = 0
last_update_time = 0

# Плавное масштабирование
def on_scroll(event):
    """Плавное масштабирование колесиком мыши"""
    global frame_count, last_update_time
    
    if event.inaxes != ax:
        return
    
    # Плавный коэффициент масштабирования
    scale_factor = 1.08 if event.button == 'up' else 0.92
    
    # Текущие пределы
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    
    # Координаты курсора
    xdata = event.xdata
    ydata = event.ydata
    
    if xdata is None or ydata is None:
        return
    
    # Масштабирование относительно курсора
    new_width = (xlim[1] - xlim[0]) * scale_factor
    new_height = (ylim[1] - ylim[0]) * scale_factor
    
    # Плавно вычисляем новые пределы
    new_xlim = (xdata - new_width / 2, xdata + new_width / 2)
    new_ylim = (ydata - new_height / 2, ydata + new_height / 2)
    
    # Применяем новые пределы
    ax.set_xlim(new_xlim)
    ax.set_ylim(new_ylim)
    
    # Обновляем только при значительном изменении (для плавности)
    current_time = event.time
    if current_time - last_update_time > 10:  # миллисекунды
        update_time_labels_smoothly()
        last_update_time = current_time
    
    frame_count += 1
    
    # Быстрая перерисовка (без полного обновления)
    fig.canvas.draw_idle()

# Плавное панорамирование
def on_press(event):
    """Начало панорамирования"""
    global pan_start, pan_button
    
    if event.inaxes != ax:
        return
    
    # ЛКМ для панорамирования
    if event.button == 1:
        pan_start = (event.xdata, event.ydata)
        pan_button = event.button
        fig.canvas.cursor = 13  # Курсор рука
        return True
    
    # ПКМ для сброса масштаба
    elif event.button == 3:
        reset_zoom()
        return True
    
    return False

def on_motion(event):
    """Плавное панорамирование"""
    global pan_start, pan_button, last_xlim, last_ylim, last_update_time
    
    if pan_start is None or event.inaxes != ax:
        return
    
    dx = event.xdata - pan_start[0]
    dy = event.ydata - pan_start[1]
    
    if dx is None or dy is None:
        return
    
    # Получаем текущие пределы
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    
    # Вычисляем новые пределы
    new_xlim = (xlim[0] - dx, xlim[1] - dx)
    new_ylim = (ylim[0] - dy, ylim[1] - dy)
    
    # Применяем с небольшим запаздыванием для плавности
    ax.set_xlim(new_xlim)
    ax.set_ylim(new_ylim)
    
    # Обновляем стартовую позицию
    pan_start = (event.xdata, event.ydata)
    
    # Обновляем метки времени только если изменился масштаб
    current_time_range = new_xlim[1] - new_xlim[0]
    last_time_range = last_xlim[1] - last_xlim[0]
    
    if abs(current_time_range - last_time_range) / last_time_range > 0.1:
        update_time_labels_smoothly()
        last_xlim = new_xlim
        last_ylim = new_ylim
    
    # Быстрая перерисовка
    fig.canvas.draw_idle()

def on_release(event):
    """Конец панорамирования"""
    global pan_start, pan_button
    
    if pan_button == event.button:
        pan_start = None
        pan_button = None
        fig.canvas.cursor = 0  # Обычный курсор
        update_time_labels_smoothly()  # Финальное обновление меток
        return True
    
    return False

def reset_zoom():
    """Сброс масштаба к исходному"""
    ax.set_xlim(xlim_original)
    
    if time_groups:
        max_y = max(len(events) for events in time_groups.values()) - 1
        ax.set_ylim(-1.5, max_y + 1.5)
    
    update_time_labels_smoothly()
    fig.canvas.draw_idle()

def update_time_labels_smoothly():
    """Плавное обновление меток времени"""
    try:
        xlim = ax.get_xlim()
        
        # Конвертируем в datetime
        xmin = mdates.num2date(xlim[0])
        xmax = mdates.num2date(xlim[1])
        
        # Вычисляем диапазон времени в секундах
        time_range_seconds = (xmax - xmin).total_seconds()
        
        # Получаем подходящий форматтер
        formatter = get_time_formatter(time_range_seconds)
        ax.xaxis.set_major_formatter(formatter)
        
        # Автоматический выбор интервала
        if time_range_seconds < 1:
            locator = mdates.AutoDateLocator(minticks=3, maxticks=10)
        elif time_range_seconds < 10:
            locator = mdates.SecondLocator(interval=max(1, int(time_range_seconds / 5)))
        elif time_range_seconds < 60:
            locator = mdates.SecondLocator(interval=5)
        elif time_range_seconds < 300:
            locator = mdates.SecondLocator(interval=30)
        else:
            locator = mdates.MinuteLocator(interval=max(1, int(time_range_seconds / 300)))
        
        ax.xaxis.set_major_locator(locator)
        
        # Оптимизация: обновляем только если нужно
        plt.setp(ax.get_xticklabels(), rotation=90, fontsize=8)
        
    except Exception as e:
        print(f"Ошибка обновления меток: {e}")

# Подключаем обработчики событий
fig.canvas.mpl_connect('scroll_event', on_scroll)
fig.canvas.mpl_connect('button_press_event', on_press)
fig.canvas.mpl_connect('motion_notify_event', on_motion)
fig.canvas.mpl_connect('button_release_event', on_release)

# Добавляем обработчик двойного клика для быстрого сброса
def on_dbl_click(event):
    """Сброс масштаба по двойному клику"""
    if event.inaxes == ax and event.dblclick:
        reset_zoom()
        return True
    return False

fig.canvas.mpl_connect('button_press_event', on_dbl_click)

# Включаем улучшенную производительность
plt.rcParams['path.simplify'] = True
plt.rcParams['path.simplify_threshold'] = 1.0
plt.rcParams['agg.path.chunksize'] = 10000

# Информационная панель
info_text = ax.text(0.02, 0.98, '',
                   transform=ax.transAxes,
                   fontsize=9,
                   bbox=dict(boxstyle="round,pad=0.2", 
                            facecolor="white", alpha=0.7),
                   verticalalignment='top')

def update_info_panel():
    """Обновление информационной панели"""
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    
    try:
        xmin_str = mdates.num2date(xlim[0]).strftime('%H:%M:%S.%f')[:-3]
        xmax_str = mdates.num2date(xlim[1]).strftime('%H:%M:%S.%f')[:-3]
        
        # Считаем видимые события
        visible_events = 0
        for time_key, event_list in time_groups.items():
            time_num = mdates.date2num(time_key)
            if xlim[0] <= time_num <= xlim[1]:
                visible_events += len(event_list)
        
        zoom_percent = ((xlim[1] - xlim[0]) / (xlim_original[1] - xlim_original[0])) * 100
        
        info = f"Диапазон: {xmin_str} - {xmax_str}\n" \
               f"Событий: {visible_events}/{len(df)}\n" \
               f"Масштаб: {zoom_percent:.1f}%"
        
        info_text.set_text(info)
    except:
        pass

# Обновляем информационную панель при изменении
def on_axes_change(event):
    """Обновление при изменении осей"""
    update_info_panel()

ax.callbacks.connect('xlim_changed', on_axes_change)
ax.callbacks.connect('ylim_changed', on_axes_change)

# Начальное обновление
update_info_panel()
update_time_labels_smoothly()

plt.tight_layout()
plt.show()

# ВАРИАНТ 2: Используем встроенные инструменты Matplotlib для максимальной плавности
fig2, ax2 = plt.subplots(figsize=(20, 10))

# Простая отрисовка событий (для лучшей производительности)
for time_key, event_list in time_groups.items():
    ax2.axvline(x=time_key, color='gray', alpha=0.2, linestyle='-', linewidth=0.5)
    for i, event in enumerate(event_list):
        ax2.plot(time_key, i, 'o', markersize=8, alpha=0.7, 
                markeredgecolor='black', markerfacecolor='blue')
        
        # Простые подписи
        short_event = event[:25] + ('...' if len(event) > 25 else '')
        offset = pd.Timedelta(milliseconds=10)
        label_y = i + (0.3 if hash(str(time_key)) % 2 == 0 else -0.3)
        
        ax2.text(time_key + offset, label_y, short_event,
                fontsize=7, ha='left', va='center')

# Настройка
unique_times = sorted(time_groups.keys())
time_labels = [t.strftime('%H:%M:%S') for t in unique_times]
ax2.set_xticks(unique_times)
ax2.set_xticklabels(time_labels, rotation=90, fontsize=8)

ax2.set_xlabel('Время событий')
ax2.set_ylabel('События')
ax2.set_title('Оптимизированная диаграмма (используйте стандартные инструменты Matplotlib)')
ax2.grid(True, alpha=0.2)

# Включаем стандартную навигацию (очень плавную)
from matplotlib.widgets import Cursor
cursor = Cursor(ax2, useblit=True, color='red', linewidth=1)

# Добавляем кнопку сброса
from matplotlib.widgets import Button

reset_ax = plt.axes([0.85, 0.01, 0.12, 0.05])
reset_button = Button(reset_ax, 'Сброс масштаба', color='lightblue')

def reset_view(event):
    ax2.set_xlim([mdates.date2num(min(unique_times)) - 0.001, 
                  mdates.date2num(max(unique_times)) + 0.001])
    if time_groups:
        max_y = max(len(events) for events in time_groups.values()) - 1
        ax2.set_ylim(-1, max_y + 1)
    fig2.canvas.draw()

reset_button.on_clicked(reset_view)

plt.tight_layout(rect=[0, 0.07, 1, 1])
plt.show()

print("=" * 100)
print("ИНСТРУКЦИЯ ПО УПРАВЛЕНИЮ:")
print("=" * 100)
print("ПЕРВЫЙ ГРАФИК (основной):")
print("  • Колесико мыши - плавное масштабирование")
print("  • ЛКМ + движение - плавное панорамирование")
print("  • ПКМ - сброс масштаба")
print("  • Двойной клик - быстрый сброс")
print()
print("ВТОРОЙ ГРАФИК (оптимизированный):")
print("  • Используйте стандартные кнопки навигации Matplotlib")
print("  • Кнопка 'Сброс масштаба' внизу")
print("  • Более плавная работа за счет упрощенной отрисовки")
print("=" * 100)