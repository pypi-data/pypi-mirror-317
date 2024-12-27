import tkinter as tk
from tkinter import messagebox

def run_bmi_calculator():
    class BMICalculator:
        def __init__(self, root):
            self.root = root
            self.root.title("BMI Calculator")
            self.root.geometry("400x500")
            self.root.resizable(False, False)
            self.create_widgets()

        def create_widgets(self):
            
            tk.Label(self.root, text="BMI Calculator", font=("Arial", 24, "bold")).pack(pady=20)

            tk.Label(self.root, text="Enter your height (cm):", font=("Arial", 14)).pack(pady=10)
            self.height_entry = tk.Entry(self.root, font=("Arial", 14), justify="center")
            self.height_entry.pack(pady=5)

            tk.Label(self.root, text="Enter your weight (kg):", font=("Arial", 14)).pack(pady=10)
            self.weight_entry = tk.Entry(self.root, font=("Arial", 14), justify="center")
            self.weight_entry.pack(pady=5)

            tk.Button(
                self.root,
                text="Calculate BMI",
                font=("Arial", 14),
                bg="#4CAF50",
                fg="white",
                command=self.calculate_bmi
            ).pack(pady=20)

            self.result_label = tk.Label(self.root, text="", font=("Arial", 16), fg="blue")
            self.result_label.pack(pady=10)

            self.interpretation_label = tk.Label(self.root, text="", font=("Arial", 14), wraplength=350, justify="center")
            self.interpretation_label.pack(pady=10)

        def calculate_bmi(self):
            try:
                height_cm = float(self.height_entry.get())
                weight_kg = float(self.weight_entry.get())
                if height_cm <= 0 or weight_kg <= 0:
                    raise ValueError("Height and weight must be positive numbers.")

                height_m = height_cm / 100 
                bmi = weight_kg / (height_m ** 2)
                bmi = round(bmi, 2)

                self.result_label.config(text=f"Your BMI: {bmi}")

                if bmi < 18.5:
                    interpretation = "You are underweight. Consider consulting with a healthcare provider."
                elif 18.5 <= bmi < 24.9:
                    interpretation = "You have a normal weight. Keep maintaining a healthy lifestyle!"
                elif 25 <= bmi < 29.9:
                    interpretation = "You are overweight. Consider adopting a healthy diet and exercise plan."
                else:
                    interpretation = "You are obese. It is recommended to seek medical advice."

                self.interpretation_label.config(text=interpretation)
            except ValueError as e:
                messagebox.showerror("Input Error", f"Invalid input: {e}")

    root = tk.Tk()
    BMICalculator(root)
    root.mainloop()

