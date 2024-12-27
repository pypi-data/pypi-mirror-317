import tkinter as tk
from tkinter import ttk
import random
import string

def run_password_generator():
    class PasswordGenerator:
        def __init__(self, root):
            self.root = root
            self.root.title("Password Generator")
            self.root.geometry("500x400")
            self.root.resizable(False, False)
            self.create_widgets()

        def create_widgets(self):
            tk.Label(self.root, text="Password Generator", font=("Arial", 20, "bold")).pack(pady=20)

            tk.Label(self.root, text="Password Length:", font=("Arial", 14)).place(x=50, y=80)
            self.length_var = tk.IntVar(value=12)
            self.length_entry = tk.Spinbox(
                self.root, from_=4, to=50, textvariable=self.length_var, font=("Arial", 12), width=5
            )
            self.length_entry.place(x=250, y=80)

            self.include_uppercase = tk.BooleanVar(value=True)
            self.include_lowercase = tk.BooleanVar(value=True)
            self.include_numbers = tk.BooleanVar(value=True)
            self.include_special = tk.BooleanVar(value=True)

            options = [
                ("Include Uppercase Letters (A-Z)", self.include_uppercase),
                ("Include Lowercase Letters (a-z)", self.include_lowercase),
                ("Include Numbers (0-9)", self.include_numbers),
                ("Include Special Characters (@#$%)", self.include_special),
            ]

            for i, (text, var) in enumerate(options):
                tk.Checkbutton(self.root, text=text, variable=var, font=("Arial", 12)).place(x=50, y=130 + i * 30)

            tk.Button(
                self.root,
                text="Generate Password",
                font=("Arial", 14),
                bg="#4CAF50",
                fg="white",
                command=self.generate_password,
            ).place(x=150, y=270)

            self.password_output = tk.Entry(
                self.root, font=("Arial", 14), bd=5, relief=tk.SUNKEN, justify="center", width=30
            )
            self.password_output.place(x=50, y=330)

            tk.Button(
                self.root,
                text="Copy",
                font=("Arial", 12),
                bg="#2196F3",
                fg="white",
                command=self.copy_password,
            ).place(x=400, y=325)

        def generate_password(self):
            length = self.length_var.get()
            if length < 4:
                self.password_output.delete(0, tk.END)
                self.password_output.insert(0, "Password too short!")
                return

            characters = ""
            if self.include_uppercase.get():
                characters += string.ascii_uppercase
            if self.include_lowercase.get():
                characters += string.ascii_lowercase
            if self.include_numbers.get():
                characters += string.digits
            if self.include_special.get():
                characters += string.punctuation

            if not characters:
                self.password_output.delete(0, tk.END)
                self.password_output.insert(0, "Select at least one option!")
                return

            password = "".join(random.choice(characters) for _ in range(length))
            self.password_output.delete(0, tk.END)
            self.password_output.insert(0, password)

        def copy_password(self):
            password = self.password_output.get()
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            self.root.update()
            self.password_output.delete(0, tk.END)
            self.password_output.insert(0, "Password Copied!")

    root = tk.Tk()
    PasswordGenerator(root)
    root.mainloop()
