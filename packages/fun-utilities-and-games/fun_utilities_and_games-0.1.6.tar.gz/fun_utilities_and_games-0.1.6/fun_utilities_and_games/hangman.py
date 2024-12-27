import tkinter as tk
from tkinter import messagebox
import random

def run_hangman():
    class HangmanGame:
        def __init__(self, root):
            self.root = root
            self.root.title("Hangman Game")

            self.words = [
    "python", "java", "kotlin", "hangman", "programming", "javascript", "algorithm", "database", "network", "security",
    "framework", "function", "variable", "object", "inheritance", "polymorphism", "encapsulation", "recursion", "iteration", "compiler",
    "interpreter", "debugging", "syntax", "runtime", "exception", "development", "deployment", "frontend", "backend", "middleware",
    "repository", "version", "integration", "testing", "deployment", "virtualization", "container", "microservice", "encryption", "authentication",
    "authorization", "optimization", "thread", "process", "parallelism", "concurrency", "loadbalancer", "cloud", "machinelearning", "datascience"
]
            self.word = random.choice(self.words)
            self.guessed_word = ["_"] * len(self.word)
            self.attempts = 6
            self.guessed_letters = set()

            self.create_widgets()

        def create_widgets(self):
            self.label_word = tk.Label(self.root, text="Word: " + " ".join(self.guessed_word), font=("Arial", 16))
            self.label_word.pack(pady=10)

            self.label_attempts = tk.Label(self.root, text=f"Attempts left: {self.attempts}", font=("Arial", 14))
            self.label_attempts.pack(pady=5)

            self.label_guessed = tk.Label(self.root, text="Guessed letters: None", font=("Arial", 14))
            self.label_guessed.pack(pady=5)

            self.entry_guess = tk.Entry(self.root, font=("Arial", 14))
            self.entry_guess.pack(pady=10)

            self.button_guess = tk.Button(self.root, text="Guess", font=("Arial", 14), command=self.make_guess)
            self.button_guess.pack(pady=10)

            self.button_reset = tk.Button(self.root, text="Reset Game", font=("Arial", 14), command=self.reset_game)
            self.button_reset.pack(pady=10)

        def make_guess(self):
            guess = self.entry_guess.get().lower()
            self.entry_guess.delete(0, tk.END)

            if not guess or len(guess) != 1 or not guess.isalpha():
                messagebox.showerror("Error", "Please enter a valid single letter.")
                return

            if guess in self.guessed_letters:
                messagebox.showinfo("Info", "You already guessed that letter.")
                return

            self.guessed_letters.add(guess)

            if guess in self.word:
                for idx, letter in enumerate(self.word):
                    if letter == guess:
                        self.guessed_word[idx] = guess
            else:
                self.attempts -= 1

            self.update_display()

            if "_" not in self.guessed_word:
                messagebox.showinfo("Congratulations", f"You guessed the word: {self.word}")
                self.reset_game()
            elif self.attempts == 0:
                messagebox.showinfo("Game Over", f"The word was: {self.word}")
                self.reset_game()

        def update_display(self):
            self.label_word.config(text="Word: " + " ".join(self.guessed_word))
            self.label_attempts.config(text=f"Attempts left: {self.attempts}")
            guessed_letters_text = ", ".join(sorted(self.guessed_letters)) if self.guessed_letters else "None"
            self.label_guessed.config(text=f"Guessed letters: {guessed_letters_text}")

        def reset_game(self):
            self.word = random.choice(self.words)
            self.guessed_word = ["_"] * len(self.word)
            self.attempts = 6
            self.guessed_letters = set()
            self.update_display()

    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()
