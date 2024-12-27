import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import os

def run_student_form():
    class StudentRecordForm:
        def __init__(self, root):
            self.root = root
            self.root.title("Student Records Form")
            self.root.geometry("600x700")
            self.root.resizable(False, False)
            self.create_widgets()

        def create_widgets(self):
            # Title
            tk.Label(self.root, text="Student Records Form", font=("Arial", 24, "bold")).pack(pady=10)

            # Frame for form
            form_frame = tk.Frame(self.root, padx=20, pady=10)
            form_frame.pack(fill="both", expand=True)

            # Name
            tk.Label(form_frame, text="Name:", font=("Arial", 12)).grid(row=0, column=0, sticky="w", pady=5)
            self.name_entry = tk.Entry(form_frame, font=("Arial", 12), width=30)
            self.name_entry.grid(row=0, column=1, pady=5)

            # DOB
            tk.Label(form_frame, text="Date of Birth (DD/MM/YYYY):", font=("Arial", 12)).grid(row=1, column=0, sticky="w", pady=5)
            self.dob_entry = tk.Entry(form_frame, font=("Arial", 12), width=30)
            self.dob_entry.grid(row=1, column=1, pady=5)

            # Age
            tk.Label(form_frame, text="Age:", font=("Arial", 12)).grid(row=2, column=0, sticky="w", pady=5)
            self.age_entry = tk.Entry(form_frame, font=("Arial", 12), width=30)
            self.age_entry.grid(row=2, column=1, pady=5)

            # SSLC Score
            tk.Label(form_frame, text="SSLC Score (%):", font=("Arial", 12)).grid(row=3, column=0, sticky="w", pady=5)
            self.sslc_entry = tk.Entry(form_frame, font=("Arial", 12), width=30)
            self.sslc_entry.grid(row=3, column=1, pady=5)

            # Higher Studies Score
            tk.Label(form_frame, text="Higher Studies Score (%):", font=("Arial", 12)).grid(row=4, column=0, sticky="w", pady=5)
            self.higher_entry = tk.Entry(form_frame, font=("Arial", 12), width=30)
            self.higher_entry.grid(row=4, column=1, pady=5)

            # Department
            tk.Label(form_frame, text="Department:", font=("Arial", 12)).grid(row=5, column=0, sticky="w", pady=5)
            self.department_entry = tk.Entry(form_frame, font=("Arial", 12), width=30)
            self.department_entry.grid(row=5, column=1, pady=5)

            # College
            tk.Label(form_frame, text="College:", font=("Arial", 12)).grid(row=6, column=0, sticky="w", pady=5)
            self.college_entry = tk.Entry(form_frame, font=("Arial", 12), width=30)
            self.college_entry.grid(row=6, column=1, pady=5)

            # Email
            tk.Label(form_frame, text="Email:", font=("Arial", 12)).grid(row=7, column=0, sticky="w", pady=5)
            self.email_entry = tk.Entry(form_frame, font=("Arial", 12), width=30)
            self.email_entry.grid(row=7, column=1, pady=5)

            # Address
            tk.Label(form_frame, text="Address:", font=("Arial", 12)).grid(row=8, column=0, sticky="w", pady=5)
            self.address_entry = tk.Text(form_frame, font=("Arial", 12), height=4, width=30)
            self.address_entry.grid(row=8, column=1, pady=5)

            # Buttons
            tk.Button(
                self.root, text="Save Record", font=("Arial", 14), bg="#4CAF50", fg="white", command=self.save_record
            ).pack(pady=10)

        def save_record(self):
            # Gather inputs
            name = self.name_entry.get().strip()
            dob = self.dob_entry.get().strip()
            age = self.age_entry.get().strip()
            sslc_score = self.sslc_entry.get().strip()
            higher_score = self.higher_entry.get().strip()
            department = self.department_entry.get().strip()
            college = self.college_entry.get().strip()
            email = self.email_entry.get().strip()
            address = self.address_entry.get("1.0", tk.END).strip()

            # Validate inputs
            if not name or not dob or not age or not sslc_score or not higher_score or not department or not college or not email or not address:
                messagebox.showerror("Input Error", "All fields are mandatory!")
                return

            if not sslc_score.isdigit() or not higher_score.isdigit() or not age.isdigit():
                messagebox.showerror("Input Error", "Age and scores must be valid numbers!")
                return

            # Save to file
            record = (
                f"Name: {name}\n"
                f"Date of Birth: {dob}\n"
                f"Age: {age}\n"
                f"SSLC Score: {sslc_score}%\n"
                f"Higher Studies Score: {higher_score}%\n"
                f"Department: {department}\n"
                f"College: {college}\n"
                f"Email: {email}\n"
                f"Address: {address}\n"
                "----------------------------------------\n"
            )

            file_path = filedialog.asksaveasfilename(
                title="Save Record As", defaultextension=".txt", filetypes=[("Text Files", "*.txt")]
            )
            if file_path:
                try:
                    with open(file_path, "a") as file:
                        file.write(record)
                    messagebox.showinfo("Success", "Record saved successfully!")
                    self.clear_form()
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred while saving the file: {e}")

        def clear_form(self):
            """Clear all input fields."""
            self.name_entry.delete(0, tk.END)
            self.dob_entry.delete(0, tk.END)
            self.age_entry.delete(0, tk.END)
            self.sslc_entry.delete(0, tk.END)
            self.higher_entry.delete(0, tk.END)
            self.department_entry.delete(0, tk.END)
            self.college_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)
            self.address_entry.delete("1.0", tk.END)

    root = tk.Tk()
    StudentRecordForm(root)
    root.mainloop()
