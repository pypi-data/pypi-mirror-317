import tkinter as tk
from tkinter import messagebox

def run_palindrome_checker():
    class PalindromeChecker:
        def __init__(self, root):
            self.root = root
            self.root.title("Palindrome Checker")
            self.root.geometry("400x400")
            self.root.resizable(False, False)
            self.create_widgets()

        def create_widgets(self):
            
            tk.Label(self.root, text="Palindrome Checker", font=("Arial", 24, "bold")).pack(pady=20)

            tk.Label(self.root, text="Enter a string to check if it's a palindrome:", font=("Arial", 14)).pack(pady=10)

            self.input_entry = tk.Entry(self.root, font=("Arial", 14), justify="center", width=30)
            self.input_entry.pack(pady=10)

            tk.Button(
                self.root,
                text="Check",
                font=("Arial", 14),
                bg="#4CAF50",
                fg="white",
                command=self.check_palindrome
            ).pack(pady=20)

            self.result_label = tk.Label(self.root, text="", font=("Arial", 16), wraplength=350, justify="center")
            self.result_label.pack(pady=10)

        def check_palindrome(self):
            input_text = self.input_entry.get().strip()
            if not input_text:
                messagebox.showerror("Input Error", "Please enter a valid string.")
                return

            normalized_text = ''.join(char.lower() for char in input_text if char.isalnum())
            is_palindrome = normalized_text == normalized_text[::-1]

            if is_palindrome:
                self.result_label.config(
                    text=f"'{input_text}' is a Palindrome! 🎉", fg="green"
                )
            else:
                self.result_label.config(
                    text=f"'{input_text}' is NOT a Palindrome.", fg="red"
                )

    root = tk.Tk()
    PalindromeChecker(root)
    root.mainloop()
