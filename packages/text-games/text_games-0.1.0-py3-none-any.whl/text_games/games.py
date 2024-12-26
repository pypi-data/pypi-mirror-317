import random

def hangman():
    """Play a game of Hangman."""
    words = ["python", "hangman", "programming", "developer", "algorithm"]
    word = random.choice(words)
    guessed = ["_" for _ in word]
    attempts = 6

    print("Welcome to Hangman!")
    while attempts > 0 and "_" in guessed:
        print("Word: ", " ".join(guessed))
        guess = input("Guess a letter: ").lower()

        if guess in word:
            for i, letter in enumerate(word):
                if letter == guess:
                    guessed[i] = guess
        else:
            attempts -= 1
            print(f"Wrong guess! Attempts left: {attempts}")

    if "_" not in guessed:
        print("Congratulations! You guessed the word: ", word)
    else:
        print("Game Over! The word was: ", word)

def number_guesser():
    """Play a Number Guesser game."""
    number = random.randint(1, 100)
    attempts = 7

    print("Welcome to Number Guesser!")
    while attempts > 0:
        try:
            guess = int(input("Guess a number between 1 and 100: "))

            if guess == number:
                print("Congratulations! You guessed the number.")
                return
            elif guess < number:
                print("Too low!")
            else:
                print("Too high!")

            attempts -= 1
            print(f"Attempts left: {attempts}")
        except ValueError:
            print("Please enter a valid number.")

    print("Game Over! The number was: ", number)

def rock_paper_scissors():
    """Play a Rock-Paper-Scissors game."""
    choices = ["rock", "paper", "scissors"]

    print("Welcome to Rock-Paper-Scissors!")
    while True:
        user_choice = input("Enter rock, paper, or scissors (or 'quit' to exit): ").lower()

        if user_choice == "quit":
            break

        if user_choice not in choices:
            print("Invalid choice. Try again.")
            continue

        computer_choice = random.choice(choices)
        print(f"Computer chose: {computer_choice}")

        if user_choice == computer_choice:
            print("It's a tie!")
        elif (user_choice == "rock" and computer_choice == "scissors") or \
             (user_choice == "paper" and computer_choice == "rock") or \
             (user_choice == "scissors" and computer_choice == "paper"):
            print("You win!")
        else:
            print("You lose!")

def riddle_game():
    """Play a Riddle Game."""
    riddles = {
        "What has keys but can't open locks?": "keyboard",
        "What has to be broken before you can use it?": "egg",
        "I speak without a mouth and hear without ears. What am I?": "echo",
    }

    print("Welcome to the Riddle Game!")
    riddle, answer = random.choice(list(riddles.items()))
    print("Riddle: ", riddle)

    attempts = 3
    while attempts > 0:
        user_answer = input("Your answer: ").lower()
        if user_answer == answer:
            print("Correct! You solved the riddle.")
            return
        else:
            attempts -= 1
            print(f"Wrong answer. Attempts left: {attempts}")

    print("Game Over! The answer was: ", answer)

def word_scramble():
    """Play a Word Scramble game."""
    words = ["python", "developer", "algorithm", "hangman", "programming"]
    word = random.choice(words)
    scrambled = ''.join(random.sample(word, len(word)))

    print("Welcome to Word Scramble!")
    print("Scrambled word: ", scrambled)

    attempts = 3
    while attempts > 0:
        guess = input("Your guess: ").lower()
        if guess == word:
            print("Congratulations! You unscrambled the word.")
            return
        else:
            attempts -= 1
            print(f"Wrong guess. Attempts left: {attempts}")

    print("Game Over! The word was: ", word)

# Expose games as a module for import
__all__ = ["hangman", "number_guesser", "rock_paper_scissors", "riddle_game", "word_scramble"]
