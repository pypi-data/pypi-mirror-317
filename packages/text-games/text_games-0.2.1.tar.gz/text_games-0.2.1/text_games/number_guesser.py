import random

def run_number_guesser():
    number = random.randint(1, 100)
    attempts = 7

    print("Welcome to Number Guesser!")
    print("I have chosen a number between 1 and 100.")

    while attempts > 0:
        guess = int(input(f"\nYou have {attempts} attempts left. Enter your guess: "))
        if guess == number:
            print("Congratulations! You guessed the number!")
            return
        elif guess < number:
            print("Too low!")
        else:
            print("Too high!")
        attempts -= 1

    print(f"Game over! The correct number was: {number}")
