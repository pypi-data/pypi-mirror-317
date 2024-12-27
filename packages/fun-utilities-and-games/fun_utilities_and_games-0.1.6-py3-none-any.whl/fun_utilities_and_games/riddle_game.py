import tkinter as tk
from tkinter import messagebox
import random
riddles = [
    ("What has keys but can't open locks?", "keyboard"),
    ("What has to be broken before you can use it?", "egg"),
    ("What gets wetter the more it dries?", "towel"),
    ("I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?", "echo"),
    ("What can travel around the world while staying in the corner?", "stamp"),
    ("What has a heart that doesn't beat?", "artichoke"),
    ("What comes once in a minute, twice in a moment, but never in a thousand years?", "the letter m"),
    ("What has one head, one foot, and four legs?", "bed"),
    ("What can you catch but not throw?", "cold"),
    ("What is full of holes but still holds a lot of weight?", "net"),
    ("What is always in front of you but can't be seen?", "future"),
    ("The more of this there is, the less you see. What is it?", "darkness"),
    ("What can be broken but never held?", "promise"),
    ("What is as light as a feather, yet the strongest man can't hold it for more than a few minutes?", "breath"),
    ("What is always coming but never arrives?", "tomorrow"),
    ("I am tall when I am young, and I am short when I am old. What am I?", "candle"),
    ("What has an eye but can't see?", "needle"),
    ("What has cities, but no houses; forests, but no trees; and rivers, but no water?", "map"),
    ("What is so fragile that saying its name breaks it?", "silence"),
    ("What is black when it’s clean and white when it’s dirty?", "chalkboard"),
    ("What can be cracked, made, told, and played?", "joke"),
    ("What comes down but never goes up?", "rain"),
    ("What can you hear but not touch or see?", "sound"),
    ("What is always moving but never moves?", "clock"),
    ("What runs but never walks?", "water"),
    ("What has a neck but no head?", "bottle"),
    ("What has a face but no eyes?", "clock"),
    ("What begins with T, ends with T, and has T in it?", "teapot"),
    ("What has a bed but never sleeps?", "river"),
    ("What is orange and sounds like a parrot?", "carrot"),
    ("What has legs but doesn't walk?", "table"),
    ("What has an ear but can't hear?", "corn"),
    ("What has teeth but can't bite?", "comb"),
    ("What can be eaten but never chewed?", "plate"),
    ("What comes up but never goes down?", "age"),
    ("What is bigger than an elephant but doesn't weigh anything?", "shadow"),
    ("What has no beginning, end, or middle?", "circle"),
    ("What gets sharper the more you use it?", "brain"),
    ("What is hard to hold but easy to throw?", "water"),
    ("What is the longest word in the dictionary?", "smiles (there's a mile between the s's)"),
    ("What is white when it's dirty?", "blackboard"),
    ("What has four fingers and a thumb but isn’t alive?", "glove"),
    ("What is taken before you can leave?", "picture"),
    ("What is inside a bottle but never touches the liquid?", "air"),
    ("What can be heard but never seen?", "music"),
    ("What never asks a question but gets answered?", "telephone"),
    ("What has a thumb but no hand?", "glove"),
    ("What goes up and down but doesn’t move?", "stairs"),
    ("What’s black and white and red all over?", "newspaper"),
    ("What has many keys but can’t open a single door?", "piano"),
    ("What comes once in a year, twice in a week, but never in a day?", "e"),
]

def run_riddle_game():
    root = tk.Tk()
    root.title("Riddle Game")
    root.geometry("600x400")

    score = 0
    current_riddle_index = 0

    random.shuffle(riddles)

    def next_riddle():
        nonlocal current_riddle_index
        if current_riddle_index >= len(riddles):
            messagebox.showinfo("Game Over", f"Game over! Your score: {score}/{len(riddles)}")
            root.quit()
        else:
            riddle, correct_answer = riddles[current_riddle_index]
            riddle_label.config(text=riddle)
            user_answer_entry.delete(0, tk.END)

    def check_answer():
        nonlocal score, current_riddle_index
        user_answer = user_answer_entry.get().strip().lower()
        correct_answer = riddles[current_riddle_index][1].lower()

        if user_answer == correct_answer:
            messagebox.showinfo("Correct!", "That's the correct answer!")
            score += 1
        else:
            messagebox.showinfo("Incorrect", f"Wrong! The correct answer was: {correct_answer}")

        current_riddle_index += 1
        next_riddle()

    riddle_label = tk.Label(root, text="Welcome to the Riddle Game!", font=("Helvetica", 14), wraplength=500, justify="center")
    riddle_label.pack(pady=20)

    user_answer_entry = tk.Entry(root, font=("Helvetica", 12), width=30)
    user_answer_entry.pack(pady=10)

    submit_button = tk.Button(root, text="Submit Answer", font=("Helvetica", 12), command=check_answer)
    submit_button.pack(pady=20)

    next_riddle()

    root.mainloop()
