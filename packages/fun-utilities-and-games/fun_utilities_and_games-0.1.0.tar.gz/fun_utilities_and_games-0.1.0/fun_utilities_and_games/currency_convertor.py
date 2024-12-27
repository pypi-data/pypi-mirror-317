import tkinter as tk
from tkinter import ttk
import requests

def run_currency_converter():
    class CurrencyConverter:
        def __init__(self, root):
            self.root = root
            self.root.title("Currency Converter")
            self.root.geometry("500x400")
            self.root.resizable(False, False)
            self.api_url = "https://api.exchangerate-api.com/v4/latest/USD"
            self.create_widgets()
            self.fetch_exchange_rates()

        def fetch_exchange_rates(self):
            try:
                response = requests.get(self.api_url)
                response.raise_for_status()
                data = response.json()
                self.rates = data["rates"]
            except requests.RequestException:
                self.rates = {"USD": 1.0}
                self.error_label.config(text="Error fetching exchange rates, using default values.")

        def create_widgets(self):
            # Labels and Entries
            tk.Label(self.root, text="Currency Converter", font=("Arial", 20, "bold")).pack(pady=20)

            tk.Label(self.root, text="Amount:", font=("Arial", 14)).place(x=50, y=80)
            self.amount_entry = tk.Entry(self.root, font=("Arial", 14), bd=5, width=15)
            self.amount_entry.place(x=150, y=80)

            tk.Label(self.root, text="From:", font=("Arial", 14)).place(x=50, y=140)
            self.from_currency = ttk.Combobox(self.root, font=("Arial", 12), state="readonly", width=12)
            self.from_currency.place(x=150, y=140)

            tk.Label(self.root, text="To:", font=("Arial", 14)).place(x=50, y=200)
            self.to_currency = ttk.Combobox(self.root, font=("Arial", 12), state="readonly", width=12)
            self.to_currency.place(x=150, y=200)

            self.result_label = tk.Label(self.root, text="", font=("Arial", 14), fg="blue")
            self.result_label.place(x=50, y=320)

            self.error_label = tk.Label(self.root, text="", font=("Arial", 12), fg="red")
            self.error_label.place(x=50, y=350)

            # Buttons
            tk.Button(
                self.root, text="Convert", font=("Arial", 14), bg="#4CAF50", fg="white", command=self.convert_currency
            ).place(x=150, y=260)

            tk.Button(
                self.root, text="Clear", font=("Arial", 14), bg="#f44336", fg="white", command=self.clear_fields
            ).place(x=260, y=260)

        def convert_currency(self):
            try:
                amount = float(self.amount_entry.get())
                from_curr = self.from_currency.get()
                to_curr = self.to_currency.get()

                if not from_curr or not to_curr:
                    self.error_label.config(text="Please select both currencies.")
                    return

                if from_curr not in self.rates or to_curr not in self.rates:
                    self.error_label.config(text="Invalid currency selected.")
                    return

                converted_amount = (amount / self.rates[from_curr]) * self.rates[to_curr]
                self.result_label.config(
                    text=f"{amount:.2f} {from_curr} = {converted_amount:.2f} {to_curr}"
                )
                self.error_label.config(text="")
            except ValueError:
                self.error_label.config(text="Invalid amount entered.")
            except Exception as e:
                self.error_label.config(text="An error occurred during conversion.")

        def clear_fields(self):
            self.amount_entry.delete(0, tk.END)
            self.from_currency.set("")
            self.to_currency.set("")
            self.result_label.config(text="")
            self.error_label.config(text="")

        def populate_currency_dropdowns(self):
            if self.rates:
                currency_list = sorted(self.rates.keys())
                self.from_currency["values"] = currency_list
                self.to_currency["values"] = currency_list

    root = tk.Tk()
    app = CurrencyConverter(root)
    app.populate_currency_dropdowns()
    root.mainloop()

