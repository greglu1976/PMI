# РАБОЧАЯ ВЕРСИЯ

import tkinter as tk
import redis
import threading
import time

class LEDIndicatorModule:
    def __init__(self, master, led_labels):
        self.master = master
        self.master.title("LED Indicator Module")

        # Initialize Redis
        self.redis_client = redis.StrictRedis(host='192.168.11.49', port=6379, db=0)

        # LED labels passed during initialization
        self.led_labels = led_labels

        # Set up canvas and LED circles
        self.canvas = tk.Canvas(self.master, width=400, height=400)
        self.canvas.pack()
        self.led_circles = self.create_led_circles()

        # Start button
        self.start_button = tk.Button(self.master, text="Start", command=self.start_polling)
        self.start_button.pack()

    def create_led_circles(self):
        led_circles = {}
        for i, (led, label) in enumerate(self.led_labels.items()):
            x = 50 + (i % 4) * 80
            y = 50 + (i // 4) * 80
            led_circles[led] = self.canvas.create_oval(x, y, x + 30, y + 30, fill='green')
            self.canvas.create_text(x + 15, y + 50, text=label)
        return led_circles

    def update_leds(self):
        while True:
            led_states = {key: self.redis_client.get(key) for key in self.led_labels.keys()}
            for led, state in led_states.items():
                if state == b'1':
                    self.canvas.itemconfig(self.led_circles[led], fill='red')
                else:
                    self.canvas.itemconfig(self.led_circles[led], fill='green')
            time.sleep(0.1)

    def start_polling(self):
        threading.Thread(target=self.update_leds, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    
    # Example LED labels
    led_labels = {
        'led1': 'Ready', 'led2': 'Start', 'led3': 'Error', 'led4': 'Warning',
        'led5': 'Active', 'led6': 'Idle', 'led7': 'Standby', 'led8': 'Off',
        'led9': 'On', 'led10': 'Pending', 'led11': 'Complete', 'led12': 'Failed',
        'led13': 'Running', 'led14': 'Stopped', 'led15': 'Paused', 'led16': 'Resumed'
    }

    app = LEDIndicatorModule(root, led_labels)
    root.mainloop()
