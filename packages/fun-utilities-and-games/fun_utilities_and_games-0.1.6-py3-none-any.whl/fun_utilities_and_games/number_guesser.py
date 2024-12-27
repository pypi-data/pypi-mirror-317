import tkinter as tk
import random

def run_number_guesser():
    class NumberGuesserGame:
        def __init__(self, root):
            self.root = root
            self.root.title("Number Guesser")

            self.number = 0
            self.attempts = 7

            self.create_widgets()
            self.new_game()

        def create_widgets(self):
            self.label_title = tk.Label(self.root, text="Number Guesser", font=("Arial", 18))
            self.label_title.pack(pady=10)

            self.label_instructions = tk.Label(
                self.root,
                text="I have chosen a number between 1 and 100. Can you guess it?",
                font=("Arial", 14),
            )
            self.label_instructions.pack(pady=10)

            self.label_feedback = tk.Label(self.root, text="", font=("Arial", 14))
            self.label_feedback.pack(pady=10)

            self.entry_guess = tk.Entry(self.root, font=("Arial", 14))
            self.entry_guess.pack(pady=10)

            self.button_submit = tk.Button(self.root, text="Submit", font=("Arial", 14), command=self.check_guess)
            self.button_submit.pack(pady=10)

            self.button_new_game = tk.Button(self.root, text="New Game", font=("Arial", 14), command=self.new_game)
            self.button_new_game.pack(pady=10)

            self.button_quit = tk.Button(self.root, text="Quit", font=("Arial", 14), command=self.root.quit)
            self.button_quit.pack(pady=10)

        def new_game(self):
            self.number = random.randint(1, 100)
            self.attempts = 7
            self.label_feedback.config(text="")
            self.entry_guess.delete(0, tk.END)

        def check_guess(self):
            try:
                user_guess = int(self.entry_guess.get())
            except ValueError:
                self.label_feedback.config(text="Please enter a valid number.", fg="red")
                return

            self.attempts -= 1

            if user_guess == self.number:
                self.label_feedback.config(text="Congratulations! You guessed the number!", fg="green")
            elif self.attempts == 0:
                self.label_feedback.config(
                    text=f"Game over! The correct number was: {self.number}", fg="red"
                )
            elif user_guess < self.number:
                self.label_feedback.config(text=f"Too low! Attempts left: {self.attempts}", fg="blue")
            else:
                self.label_feedback.config(text=f"Too high! Attempts left: {self.attempts}", fg="blue")

    root = tk.Tk()
    game = NumberGuesserGame(root)
    root.mainloop()
