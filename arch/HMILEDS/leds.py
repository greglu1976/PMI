import tkinter as tk
import redis
import threading
import time

# Инициализация Redis
redis_client = redis.StrictRedis(host='192.168.11.49', port=6379, db=0)

# Словарь с обозначениями светодиодов
led_labels = {'led1': 'Ready', 'led2': 'Start', 'led3': 'Error', 'led4': 'Warning',
              'led5': 'Active', 'led6': 'Idle', 'led7': 'Standby', 'led8': 'Off',
              'led9': 'On', 'led10': 'Pending', 'led11': 'Complete', 'led12': 'Failed',
              'led13': 'Running', 'led14': 'Stopped', 'led15': 'Paused', 'led16': 'Resumed'}

# Функция для обновления состояния светодиодов
def update_leds():
    while True:
        # Получение текущего состояния светодиодов из Redis
        led_states = {key: redis_client.get(key) for key in led_labels.keys()}
        
        # Обновление графического интерфейса
        for led, state in led_states.items():
            if state == b'1':
                canvas.itemconfig(led_circles[led], fill='green')
            else:
                canvas.itemconfig(led_circles[led], fill='red')
        
        # Задержка перед следующей итерацией
        time.sleep(0.2)

# Функция для обработки нажатия кнопки Start
def start_polling():
    threading.Thread(target=update_leds, daemon=True).start()

# Создание графического интерфейса
root = tk.Tk()
root.title("LED Indicator Module")

canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()

# Создание графических элементов для светодиодов
led_circles = {}
for i, (led, label) in enumerate(led_labels.items()):
    x = 50 + (i % 4) * 80
    y = 50 + (i // 4) * 80
    led_circles[led] = canvas.create_oval(x, y, x+30, y+30, fill='red')
    canvas.create_text(x+15, y+50, text=label)

# Кнопка Start
start_button = tk.Button(root, text="Start", command=start_polling)
start_button.pack()

# Запуск основного цикла графического интерфейса
root.mainloop()