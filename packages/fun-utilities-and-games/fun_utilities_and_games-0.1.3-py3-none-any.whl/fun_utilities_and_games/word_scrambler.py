import random

def run_word_scrambler():
    words = ["python", "programming", "scramble", "developer", "keyboard"]
    word = random.choice(words)
    scrambled = "".join(random.sample(word, len(word)))

    print("Welcome to Word Scrambler!")
    print(f"Scrambled word: {scrambled}")

    user_guess = input("Your guess: ").strip().lower()
    if user_guess == word:
        print("Correct! You unscrambled the word!")
    else:
        print(f"Wrong! The correct word was: {word}")
