import tkinter as tk
import redis

class ButtonPanel:
    def __init__(self, master, button_labels, modes):
        self.master = master
        self.master.title("Button Panel")
        
        # Initialize Redis
        self.redis_client = redis.StrictRedis(host='192.168.11.49', port=6379, db=0)

        # Dictionary for button states
        self.button_states = {i: False for i in range(1, 17)}  # False - off, True - on
        self.button_labels = button_labels
        self.modes = modes  # 'toggle' or 'momentary'

        # Create buttons
        self.buttons = []
        for i in range(1, 17):
            button = tk.Button(self.master, text=self.button_labels[i - 1], command=lambda i=i: self.button_pressed(i))
            button.grid(row=(i-1)//4, column=(i-1)%4, padx=10, pady=10)
            self.buttons.append(button)

    def button_pressed(self, button_id):
        # Determine button mode and update state accordingly
        if self.modes[button_id - 1] == 'momentary':
            self.button_states[button_id] = True  # Always treated as pressed
        else:
            self.button_states[button_id] = not self.button_states[button_id]  # Toggle state

        # Set signal in Redis depending on the state
        self.redis_client.set(f'led{button_id}', '1' if self.button_states[button_id] else '0')
        print(f'Button {button_id} {"pressed" if self.button_states[button_id] else "released"}')

        # Update button color
        self.update_button_color(button_id)

        # If momentary, reset state after a short delay
        if self.modes[button_id - 1] == 'momentary':
            self.master.after(100, lambda: self.reset_button(button_id))

    def update_button_color(self, button_id):
        button = self.buttons[button_id - 1]
        if self.button_states[button_id]:
            button.config(relief='sunken')  # Button pressed
        else:
            button.config(relief='raised')  # Button released

    def reset_button(self, button_id):
        self.button_states[button_id] = False  # Reset state
        self.redis_client.set(f'led{button_id}', '0')  # Update Redis
        self.update_button_color(button_id)  # Update button color

if __name__ == "__main__":
    # Example labels and modes for buttons
    labels = [f'Button {i}' for i in range(1, 17)]
    modes = ['toggle' if i % 2 == 0 else 'momentary' for i in range(1, 17)]  # Alternate modes

    root = tk.Tk()
    app = ButtonPanel(root, labels, modes)
    root.mainloop()
