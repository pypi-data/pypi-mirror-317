import tkinter as tk
from tkinter import messagebox
import random

def run_rock_paper_scissor():
    class RockPaperScissorsGame:
        def __init__(self, root):
            self.root = root
            self.root.title("Rock, Paper, Scissors")

            self.choices = ["rock", "paper", "scissors"]

            self.create_widgets()

        def create_widgets(self):
            self.label_title = tk.Label(self.root, text="Rock, Paper, Scissors", font=("Arial", 18))
            self.label_title.pack(pady=10)

            self.label_prompt = tk.Label(self.root, text="Choose your move:", font=("Arial", 14))
            self.label_prompt.pack(pady=10)

            self.button_rock = tk.Button(self.root, text="Rock", font=("Arial", 14), command=lambda: self.play("rock"))
            self.button_rock.pack(pady=5)

            self.button_paper = tk.Button(self.root, text="Paper", font=("Arial", 14), command=lambda: self.play("paper"))
            self.button_paper.pack(pady=5)

            self.button_scissors = tk.Button(self.root, text="Scissors", font=("Arial", 14), command=lambda: self.play("scissors"))
            self.button_scissors.pack(pady=5)

            self.label_result = tk.Label(self.root, text="", font=("Arial", 14))
            self.label_result.pack(pady=20)

            self.button_quit = tk.Button(self.root, text="Quit", font=("Arial", 14), command=self.root.quit)
            self.button_quit.pack(pady=10)

        def play(self, user_choice):
            computer_choice = random.choice(self.choices)
            result = ""

            if user_choice == computer_choice:
                result = "It's a draw!"
            elif (user_choice == "rock" and computer_choice == "scissors") or \
                 (user_choice == "scissors" and computer_choice == "paper") or \
                 (user_choice == "paper" and computer_choice == "rock"):
                result = "You win!"
            else:
                result = "You lose!"

            self.label_result.config(
                text=f"You chose: {user_choice}\nComputer chose: {computer_choice}\n{result}",
                fg="green" if "win" in result else "red" if "lose" in result else "blue"
            )

    root = tk.Tk()
    game = RockPaperScissorsGame(root)
    root.mainloop()
