import tkinter as tk
from tkinter import ttk

def run_temperature_converter():
    class TemperatureConverter:
        def __init__(self, root):
            self.root = root
            self.root.title("Temperature Converter")
            self.root.geometry("500x400")
            self.root.resizable(False, False)
            self.create_widgets()

        def create_widgets(self):
            tk.Label(self.root, text="Temperature Converter", font=("Arial", 20, "bold")).pack(pady=20)

            tk.Label(self.root, text="Enter Temperature:", font=("Arial", 14)).place(x=50, y=80)
            self.input_temp = tk.Entry(self.root, font=("Arial", 14), width=10, bd=5)
            self.input_temp.place(x=250, y=80)

            tk.Label(self.root, text="From:", font=("Arial", 14)).place(x=50, y=140)
            self.from_unit = ttk.Combobox(self.root, font=("Arial", 12), state="readonly", width=10)
            self.from_unit["values"] = ["Celsius (°C)", "Fahrenheit (°F)", "Kelvin (K)"]
            self.from_unit.place(x=250, y=140)

            tk.Label(self.root, text="To:", font=("Arial", 14)).place(x=50, y=200)
            self.to_unit = ttk.Combobox(self.root, font=("Arial", 12), state="readonly", width=10)
            self.to_unit["values"] = ["Celsius (°C)", "Fahrenheit (°F)", "Kelvin (K)"]
            self.to_unit.place(x=250, y=200)

            tk.Button(
                self.root,
                text="Convert",
                font=("Arial", 14),
                bg="#4CAF50",
                fg="white",
                command=self.convert_temperature,
            ).place(x=150, y=260)

            self.result_label = tk.Label(self.root, text="", font=("Arial", 14), fg="blue")
            self.result_label.place(x=50, y=320)

            
            tk.Button(
                self.root,
                text="Clear",
                font=("Arial", 14),
                bg="#f44336",
                fg="white",
                command=self.clear_fields,
            ).place(x=250, y=260)

        def convert_temperature(self):
            try:
                temp = float(self.input_temp.get())
                from_unit = self.from_unit.get()
                to_unit = self.to_unit.get()

                if not from_unit or not to_unit:
                    self.result_label.config(text="Please select both units!")
                    return

                result = self.calculate_conversion(temp, from_unit, to_unit)
                self.result_label.config(text=f"Result: {result:.2f} {to_unit.split()[0]}")
            except ValueError:
                self.result_label.config(text="Invalid temperature input!")

        def calculate_conversion(self, temp, from_unit, to_unit):
            if from_unit == to_unit:
                return temp

            if from_unit.startswith("Celsius"):
                if to_unit.startswith("Fahrenheit"):
                    return temp * 9/5 + 32
                elif to_unit.startswith("Kelvin"):
                    return temp + 273.15
            elif from_unit.startswith("Fahrenheit"):
                if to_unit.startswith("Celsius"):
                    return (temp - 32) * 5/9
                elif to_unit.startswith("Kelvin"):
                    return (temp - 32) * 5/9 + 273.15
            elif from_unit.startswith("Kelvin"):
                if to_unit.startswith("Celsius"):
                    return temp - 273.15
                elif to_unit.startswith("Fahrenheit"):
                    return (temp - 273.15) * 9/5 + 32

        def clear_fields(self):
            self.input_temp.delete(0, tk.END)
            self.from_unit.set("")
            self.to_unit.set("")
            self.result_label.config(text="")

    root = tk.Tk()
    TemperatureConverter(root)
    root.mainloop()
