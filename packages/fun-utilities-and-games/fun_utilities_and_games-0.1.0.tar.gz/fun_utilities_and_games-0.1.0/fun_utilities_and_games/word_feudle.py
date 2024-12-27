import tkinter as tk
from tkinter import messagebox
import random

def run_wordle_game():
    class WordleGame:
        def __init__(self, root):
            self.root = root
            self.root.title("Wordle Game")
            self.root.geometry("600x800")
            self.root.resizable(False, False)
            self.words = self.load_words()
            self.target_word = random.choice(self.words).upper()
            self.word_length = len(self.target_word)
            self.attempts = 0
            self.max_attempts = 6
            self.create_widgets()

        def load_words(self):
            return [
                "bat", "cat", "dog", "fox", "owl", "sun", "man", "pan", "red", "bed",
                "big", "lid", "tip", "cap", "pen", "cup", "map", "web", "jar", "box",
                "fish", "blue", "frog", "tree", "fire", "coal", "door", "milk", "star", "gold",
                "iron", "wolf", "crow", "sand", "rain", "wind", "ship", "pond", "nest", "rock",
                "apple", "grape", "mango", "peach", "plums", "lemon", "melon", "chili", "bread", "cloud",
                "table", "chair", "brick", "horse", "water", "mouse", "dance", "paint", "proud", "smart",
                "sword", "thing", "might", "camel", "zebra", "wheat", "eagle", "tiger", "flame", "piano",
                "banana", "dragon", "butter", "orange", "violet", "forest", "planet", "silver", "anchor", "bridge",
                "castle", "window", "garden", "gloves", "helmet", "shield", "pencil", "basket", "violet", "ribbon",
                "iceberg", "diamond", "rainbow", "vulture", "picture", "journey", "chimney", "courage", "cabinet", "emerald",
                "holiday", "machine", "railway", "sailors", "trainer", "treacle", "chamber", "musical", "beehive", "monster",
                "pineapple", "elephant", "dinosaur", "sentence", "sunlight", "football", "hospital", "computer", "airplane", "sandwich",
                "cupboard", "playroom", "passport", "daughter", "necklace", "umbrella", "firework", "volcanoe", "mountain", "notebook",
                "watermelon", "grasshopper", "blacksmith", "motorcycle", "peppermint", "rainforest", "windshield", "blockchain", "spaceship", "chocolate",
                "blueberry", "strawberry", "earthquake", "mastermind", "highlighter", "crossroads", "turbulence", "microscope", "skyscraper", "historical",
                "extraordinary", "unbelievable", "indestructible", "supercalifragilistic", "misunderstanding", "communication", "comprehensive", "countermeasure",
                "knowledgeable", "interconnected", "microcontroller", "responsibility", "multiplication", "representation", "appreciation", "international",
                "misinterpretation", "overexaggeration", "multidimensional", "extraordinarily", "professionalism"
            ]

        def create_widgets(self):
            tk.Label(self.root, text="Wordle Game", font=("Arial", 24, "bold")).pack(pady=20)

            tk.Label(
                self.root,
                text=f"Guess the {self.word_length}-letter word!",
                font=("Arial", 14),
            ).pack(pady=10)

            self.guess_entry = tk.Entry(self.root, font=("Arial", 14), justify="center", width=15)
            self.guess_entry.pack(pady=10)
            self.guess_entry.bind("<Return>", lambda _: self.check_guess())

            tk.Button(
                self.root, text="Submit Guess", font=("Arial", 14), bg="#4CAF50", fg="white", command=self.check_guess
            ).pack(pady=10)

            self.feedback_frame = tk.Frame(self.root)
            self.feedback_frame.pack(pady=20)

            self.attempts_label = tk.Label(
                self.root, text=f"Attempts Left: {self.max_attempts - self.attempts}", font=("Arial", 14)
            )
            self.attempts_label.pack(pady=10)

        def check_guess(self):
            guess = self.guess_entry.get().strip().upper()

            if len(guess) != self.word_length:
                messagebox.showerror(
                    "Invalid Guess", f"Your guess must be exactly {self.word_length} letters long."
                )
                return

            self.display_feedback(guess)
            self.attempts += 1
            self.attempts_label.config(text=f"Attempts Left: {self.max_attempts - self.attempts}")

            if guess == self.target_word:
                messagebox.showinfo("Congratulations!", f"You guessed the word: {self.target_word}")
                self.reset_game()
            elif self.attempts == self.max_attempts:
                messagebox.showinfo("Game Over", f"The correct word was: {self.target_word}")
                self.reset_game()

            self.guess_entry.delete(0, tk.END)

        def display_feedback(self, guess):
            feedback = tk.Frame(self.feedback_frame)
            feedback.pack()

            for i, char in enumerate(guess):
                color = "gray"
                if char == self.target_word[i]:
                    color = "green"
                elif char in self.target_word:
                    color = "yellow"

                tk.Label(
                    feedback,
                    text=char,
                    font=("Arial", 16, "bold"),
                    bg=color,
                    fg="white",
                    width=3,
                    height=2,
                ).pack(side="left", padx=2)

        def reset_game(self):
            self.target_word = random.choice(self.words).upper()
            self.word_length = len(self.target_word)
            self.attempts = 0
            self.feedback_frame.destroy()
            self.feedback_frame = tk.Frame(self.root)
            self.feedback_frame.pack(pady=20)
            self.attempts_label.config(text=f"Attempts Left: {self.max_attempts - self.attempts}")
            tk.Label(
                self.root,
                text=f"Guess the {self.word_length}-letter word!",
                font=("Arial", 14),
            ).pack(pady=10)

    root = tk.Tk()
    WordleGame(root)
    root.mainloop()
