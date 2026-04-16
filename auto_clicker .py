import threading
import time
import tkinter as tk
from tkinter import ttk
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode

# Ініціалізація миші
mouse = Controller()

class UltimateClicker:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Clicker Pro")
        self.root.geometry("350x400")
        self.root.attributes("-topmost", True)
        self.root.configure(bg="#121212")

        # Налаштування
        self.running = False
        self.delay = 0.02  # 50 кліків/сек за замовчуванням
        self.mouse_button = Button.left
        self.start_key = KeyCode(char=']')
        self.exit_key = KeyCode(char='[')

        self.create_widgets()

        # Фоновий потік для кліків
        threading.Thread(target=self.click_loop, daemon=True).start()
        # Прослуховування клавіш
        self.listener = Listener(on_press=self.on_press)
        self.listener.start()

    def create_widgets(self):
        # Заголовок
        tk.Label(self.root, text="АВТО КЛІКЕР", font=("Arial", 16, "bold"), 
                 bg="#121212", fg="#00f260").pack(pady=15)

        # Статус
        self.status_label = tk.Label(self.root, text="СТАТУС: ПАУЗА", font=("Arial", 12, "bold"), 
                                     bg="#121212", fg="#ff4b2b")
        self.status_label.pack(pady=5)

        # Вибір кнопки миші
        tk.Label(self.root, text="Кнопка миші:", bg="#121212", fg="white").pack(pady=5)
        self.mouse_var = tk.StringVar(value="Ліва (ЛКМ)")
        combo = ttk.Combobox(self.root, textvariable=self.mouse_var, values=["Ліва (ЛКМ)", "Права (ПКМ)"], state="readonly")
        combo.pack()
        combo.bind("<<ComboboxSelected>>", self.update_mouse)

        # Налаштування швидкості
        tk.Label(self.root, text="\nШвидкість (кліків/сек):", bg="#121212", fg="white").pack()
        self.speed_slider = tk.Scale(self.root, from_=1, to=100, orient="horizontal", 
                                     bg="#121212", fg="white", highlightthickness=0, command=self.update_speed)
        self.speed_slider.set(50)
        self.speed_slider.pack(fill="x", padx=40, pady=10)

        # Підказки
        info_text = f"Старт/Стоп: [ {self.start_key.char} ]\nВихід: [ {self.exit_key.char} ]"
        tk.Label(self.root, text=info_text, bg="#121212", fg="#888", font=("Arial", 9)).pack(pady=20)

    def update_speed(self, val):
        self.delay = 1 / int(val)

    def update_mouse(self, event):
        self.mouse_button = Button.left if "Ліва" in self.mouse_var.get() else Button.right

    def on_press(self, key):
        if key == self.start_key:
            self.running = not self.running
            self.status_label.config(text="СТАТУС: КЛІКАЮ" if self.running else "СТАТУС: ПАУЗА", 
                                     fg="#00f260" if self.running else "#ff4b2b")
        elif key == self.exit_key:
            self.root.destroy()

    def click_loop(self):
        while True:
            if self.running:
                mouse.click(self.mouse_button)
                time.sleep(self.delay)
            else:
                time.sleep(0.1)

if __name__ == "__main__":
    root = tk.Tk()
    # Налаштування стилю для Combobox (щоб не був білим на фоні)
    style = ttk.Style()
    style.theme_use('alt')
    app = UltimateClicker(root)
    root.mainloop()