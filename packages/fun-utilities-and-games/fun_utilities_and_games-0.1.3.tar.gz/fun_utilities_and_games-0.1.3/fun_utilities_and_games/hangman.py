import random

def run_hangman():
    words = ["python", "java", "kotlin", "hangman", "programming"]
    word = random.choice(words)
    guessed_word = ["_"] * len(word)
    attempts = 6
    guessed_letters = set()

    print("Welcome to Hangman!")

    while attempts > 0 and "_" in guessed_word:
        print("\nWord:", " ".join(guessed_word))
        print(f"Attempts left: {attempts}")
        print(f"Guessed letters: {', '.join(guessed_letters)}")
        guess = input("Guess a letter: ").lower()

        if guess in guessed_letters:
            print("You already guessed that letter.")
        elif guess in word:
            for idx, letter in enumerate(word):
                if letter == guess:
                    guessed_word[idx] = guess
        else:
            print("Incorrect guess!")
            attempts -= 1

        guessed_letters.add(guess)

    if "_" not in guessed_word:
        print(f"Congratulations! You guessed the word: {word}")
    else:
        print(f"Game over! The word was: {word}")
