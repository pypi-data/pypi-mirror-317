import tkinter as tk
from time import strftime

def run_digital_clock():
    class DigitalClock:
        def __init__(self, root):
            self.root = root
            self.root.title("Digital Clock")
            self.root.geometry("600x300")
            self.root.configure(bg="#2E2E2E")
            self.root.resizable(False, False)
            self.create_widgets()
            self.update_clock()

        def create_widgets(self):
            # Title
            self.title_label = tk.Label(
                self.root,
                text="Digital Clock",
                font=("Arial", 28, "bold"),
                fg="#00FF00",
                bg="#2E2E2E",
            )
            self.title_label.pack(pady=10)

            self.time_label = tk.Label(
                self.root,
                text="",
                font=("Helvetica", 64, "bold"),
                fg="#FFFFFF",
                bg="#2E2E2E",
            )
            self.time_label.pack(pady=20)

            self.date_label = tk.Label(
                self.root,
                text="",
                font=("Helvetica", 24),
                fg="#FFD700",
                bg="#2E2E2E",
            )
            self.date_label.pack(pady=10)

            self.footer_label = tk.Label(
                self.root,
                text="Time is Precious. Use it Wisely!",
                font=("Arial", 14, "italic"),
                fg="#B0E0E6",
                bg="#2E2E2E",
            )
            self.footer_label.pack(pady=20)

        def update_clock(self):
            current_time = strftime("%H:%M:%S %p")
            current_date = strftime("%A, %d %B %Y") 

            self.time_label.config(text=current_time)
            self.date_label.config(text=current_date)

            self.time_label.after(1000, self.update_clock)

    root = tk.Tk()
    DigitalClock(root)
    root.mainloop()

