import tkinter as tk
from tkinter import messagebox
import random

def run_word_scrambler():
    class WordScramblerGame:
        def __init__(self, root):
            self.root = root
            self.root.title("Word Scrambler")

            self.words = [
    "python", "programming", "scramble", "developer", "keyboard", "computer", "software", "hardware", "algorithm", "debugging",
    "compiler", "interpreter", "variable", "function", "loop", "condition", "syntax", "runtime", "exception", "library",
    "framework", "backend", "frontend", "database", "network", "encryption", "authentication", "authorization", "virtualization", "cloud",
    "storage", "container", "microservice", "deployment", "testing", "iteration", "recursion", "optimization", "thread", "process",
    "parallelism", "concurrency", "bit", "byte", "array", "stack", "queue", "binary", "hexadecimal", "developer", "interface",
    "protocol", "server", "client", "domain", "hosting", "debugger", "iteration", "looping", "password", "administrator"
]
            self.word = ""
            self.scrambled = ""

            self.create_widgets()
            self.new_game()

        def create_widgets(self):
            self.label_title = tk.Label(self.root, text="Word Scrambler", font=("Arial", 18))
            self.label_title.pack(pady=10)

            self.label_scrambled = tk.Label(self.root, text="", font=("Arial", 16))
            self.label_scrambled.pack(pady=10)

            self.entry_guess = tk.Entry(self.root, font=("Arial", 14))
            self.entry_guess.pack(pady=10)

            self.button_submit = tk.Button(self.root, text="Submit", font=("Arial", 14), command=self.check_guess)
            self.button_submit.pack(pady=10)

            self.button_new_game = tk.Button(self.root, text="New Game", font=("Arial", 14), command=self.new_game)
            self.button_new_game.pack(pady=10)

            self.button_quit = tk.Button(self.root, text="Quit", font=("Arial", 14), command=self.root.quit)
            self.button_quit.pack(pady=10)

            self.label_result = tk.Label(self.root, text="", font=("Arial", 14))
            self.label_result.pack(pady=20)

        def new_game(self):
            self.word = random.choice(self.words)
            self.scrambled = "".join(random.sample(self.word, len(self.word)))
            self.label_scrambled.config(text=f"Scrambled word: {self.scrambled}")
            self.entry_guess.delete(0, tk.END)
            self.label_result.config(text="")

        def check_guess(self):
            user_guess = self.entry_guess.get().strip().lower()
            if user_guess == self.word:
                self.label_result.config(text="Correct! You unscrambled the word!", fg="green")
            else:
                self.label_result.config(text=f"Wrong! The correct word was: {self.word}", fg="red")

    root = tk.Tk()
    game = WordScramblerGame(root)
    root.mainloop()
