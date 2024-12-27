import tkinter as tk
from tkinter import messagebox

# List of 50+ riddles
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

# Initialize the Tkinter window
root = tk.Tk()
root.title("Riddle Game")
root.geometry("500x400")

# Initialize score
score = 0
current_riddle = 0

def next_riddle():
    global score, current_riddle
    if current_riddle >= len(riddles):
        messagebox.showinfo("Game Over", f"Game over! Your score: {score}/{len(riddles)}")
        root.quit()
    else:
        riddle, answer = riddles[current_riddle]
        riddle_label.config(text=riddle)
        answer_button1.config(command=lambda: check_answer(answer, answer_button1))
        answer_button2.config(command=lambda: check_answer(answer, answer_button2))
        answer_button3.config(command=lambda: check_answer(answer, answer_button3))
        answer_button4.config(command=lambda: check_answer(answer, answer_button4))

def check_answer(correct_answer, button):
    global score, current_riddle
    user_answer = button.cget("text").strip().lower()
    if user_answer == correct_answer:
        score += 1
        messagebox.showinfo("Correct!", "That's the correct answer!")
    else:
        messagebox.showinfo("Incorrect", f"Wrong! The correct answer was: {correct_answer}")
    
    current_riddle += 1
    next_riddle()

# Create widgets
riddle_label = tk.Label(root, text="Welcome to the Riddle Game!", font=("Helvetica", 14), wraplength=400)
riddle_label.pack(pady=20)

answer_button1 = tk.Button(root, text="Option 1", font=("Helvetica", 12))
answer_button1.pack(pady=5, fill=tk.X)

answer_button2 = tk.Button(root, text="Option 2", font=("Helvetica", 12))
answer_button2.pack(pady=5, fill=tk.X)

answer_button3 = tk.Button(root, text="Option 3", font=("Helvetica", 12))
answer_button3.pack(pady=5, fill=tk.X)

answer_button4 = tk.Button(root, text="Option 4", font=("Helvetica", 12))
answer_button4.pack(pady=5, fill=tk.X)

# Start the game
next_riddle()

# Run the Tkinter event loop
root.mainloop()
