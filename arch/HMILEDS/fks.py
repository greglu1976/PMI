import tkinter as tk
import redis

# Инициализация Redis
redis_client = redis.StrictRedis(host='192.168.11.49', port=6379, db=0)

# Функция для обработки нажатия кнопки
def button_pressed(button_id):
    redis_client.set(f'led{button_id}', '1')  # Включаем соответствующий LED
    print(f'Button {button_id} pressed')

# Создание графического интерфейса
root = tk.Tk()
root.title("Button Panel")

# Создание 16 кнопок
for i in range(1, 17):
    button = tk.Button(root, text=f'Button {i}', command=lambda i=i: button_pressed(i))
    button.grid(row=(i-1)//4, column=(i-1)%4, padx=10, pady=10)

# Запуск основного цикла графического интерфейса
root.mainloop()
