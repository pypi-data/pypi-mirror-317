import tkinter as tk

def run_basic_calculator():
    class EnhancedCalculator:
        def __init__(self, root):
            self.root = root
            self.root.title("Basic Calculator")
            self.root.geometry("400x600")
            self.root.resizable(False, False)
            self.current_input = ""
            self.create_widgets()

        def create_widgets(self):
            
            self.display = tk.Entry(
                self.root, font=("Arial", 24), bd=10, relief=tk.RIDGE, justify="right", bg="#f5f5f5"
            )
            self.display.grid(row=0, column=0, columnspan=4, ipady=15, pady=20)

            buttons = [
                ("C", 1, 0), ("⌫", 1, 1), ("%", 1, 2), ("/", 1, 3),
                ("7", 2, 0), ("8", 2, 1), ("9", 2, 2), ("*", 2, 3),
                ("4", 3, 0), ("5", 3, 1), ("6", 3, 2), ("-", 3, 3),
                ("1", 4, 0), ("2", 4, 1), ("3", 4, 2), ("+", 4, 3),
                ("00", 5, 0), ("0", 5, 1), (".", 5, 2), ("=", 5, 3),
            ]

            for (text, row, col) in buttons:
                tk.Button(
                    self.root,
                    text=text,
                    font=("Arial", 18),
                    bg="#e0e0e0",
                    fg="#000",
                    activebackground="#d4d4d4",
                    activeforeground="#000",
                    width=5,
                    height=2,
                    command=lambda t=text: self.on_button_click(t),
                ).grid(row=row, column=col, padx=5, pady=5)

        def on_button_click(self, button_text):
            if button_text == "C":
                self.current_input = ""
                self.update_display()
            elif button_text == "⌫":
                self.current_input = self.current_input[:-1]
                self.update_display()
            elif button_text == "=":
                try:
                    result = str(eval(self.current_input))
                    self.current_input = result
                    self.update_display()
                except Exception:
                    self.current_input = "Error"
                    self.update_display()
                    self.current_input = ""
            else:
                self.current_input += button_text
                self.update_display()

        def update_display(self):
            self.display.delete(0, tk.END)
            self.display.insert(0, self.current_input)

    root = tk.Tk()
    EnhancedCalculator(root)
    root.mainloop()
