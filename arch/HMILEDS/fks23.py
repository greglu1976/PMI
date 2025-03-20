import tkinter as tk
import redis

class ButtonPanel:
    def __init__(self, master, button_labels, modes):
        self.master = master
        self.master.title("Button Panel")

        # Initialize Redis
        self.redis_client = redis.StrictRedis(host='192.168.11.49', port=6379, db=0)

        # Reset LED states in Redis at the start
        self.reset_leds_in_redis()

        # Dictionary for button states
        self.button_states = {i: False for i in range(1, 17)}  # False - off, True - on
        self.button_labels = button_labels
        self.modes = modes  # 'toggle' or 'momentary'

        # Create buttons
        self.buttons = []
        for i in range(1, 17):
            button = tk.Button(self.master, text=self.button_labels[i - 1])
            button.grid(row=(i-1) // 4, column=(i-1) % 4, padx=10, pady=10)
            
            # Binding both press and release events for momentary buttons
            if modes[i - 1] == 'momentary':
                button.bind('<ButtonPress-1>', lambda event, i=i: self.button_pressed_momentary(i))
                button.bind('<ButtonRelease-1>', lambda event, i=i: self.button_released_momentary(i))
            else:
                button.config(command=lambda i=i: self.button_pressed_toggle(i))
            
            self.buttons.append(button)

    def reset_leds_in_redis(self):
        # Reset all LEDs in Redis
        for i in range(1, 17):
            self.redis_client.set(f'led{i}', '0')  # Set all to OFF ('0')
        print("LEDs reset in Redis.")

    def button_pressed_momentary(self, button_id):
        """Handle momentary button press"""
        self.button_states[button_id] = True
        self.redis_client.set(f'led{button_id}', '1')
        self.update_button_color(button_id)
        print(f'Button {button_id} pressed')

    def button_released_momentary(self, button_id):
        """Handle momentary button release"""
        self.button_states[button_id] = False
        self.redis_client.set(f'led{button_id}', '0')
        self.update_button_color(button_id)
        print(f'Button {button_id} released')

    def button_pressed_toggle(self, button_id):
        """Handle toggle button press"""
        self.button_states[button_id] = not self.button_states[button_id]
        self.redis_client.set(f'led{button_id}', '1' if self.button_states[button_id] else '0')
        self.update_button_color(button_id)
        print(f'Button {button_id} {"pressed" if self.button_states[button_id] else "released"}')

    def update_button_color(self, button_id):
        button = self.buttons[button_id - 1]
        if self.button_states[button_id]:
            button.config(relief='sunken')  # Button pressed
        else:
            button.config(relief='raised')  # Button released

if __name__ == "__main__":
    # Example labels and modes for buttons
    labels = [f'Button {i}' for i in range(1, 17)]
    modes = ['toggle' if i % 2 == 0 else 'momentary' for i in range(1, 17)]  # Alternate modes

    root = tk.Tk()
    app = ButtonPanel(root, labels, modes)
    root.mainloop()
