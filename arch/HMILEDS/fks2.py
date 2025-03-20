import tkinter as tk
import redis

# Инициализация Redis
redis_client = redis.StrictRedis(host='192.168.11.49', port=6379, db=0)

# Словарь для состояния кнопок
button_states = {i: False for i in range(1, 17)}  # False - выключено, True - включено

# Функция для обработки нажатия кнопки
def button_pressed(button_id):
    # Переключение состояния кнопки
    button_states[button_id] = not button_states[button_id]

    # Установить сигнал в Redis в зависимости от состояния
    redis_client.set(f'led{button_id}', '1' if button_states[button_id] else '0')
    print(f'Button {button_id} {"pressed" if button_states[button_id] else "released"}')

    # Обновление цвета кнопки для визуального отображения состояния
    update_button_color(button_id)

# Функция для обновления цвета кнопки
def update_button_color(button_id):
    button = buttons[button_id - 1]  # Получаем кнопку по идентификатору (1-16)
    if button_states[button_id]:
        button.config(relief='sunken')  # Кнопка нажата
    else:
        button.config(relief='raised')  # Кнопка отжата

# Создание графического интерфейса
root = tk.Tk()
root.title("Button Panel")

# Создание 16 кнопок
buttons = []  # Список для хранения кнопок
for i in range(1, 17):
    button = tk.Button(root, text=f'Button {i}', command=lambda i=i: button_pressed(i))
    button.grid(row=(i-1)//4, column=(i-1)%4, padx=10, pady=10)
    buttons.append(button)  # Добавляем кнопку в список

# Запуск основного цикла графического интерфейса
root.mainloop()
