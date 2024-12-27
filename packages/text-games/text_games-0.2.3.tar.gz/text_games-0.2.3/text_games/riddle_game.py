def run_riddle_game():
    riddles = {
        "What has keys but can't open locks?": "keyboard",
        "What has to be broken before you can use it?": "egg",
        "What gets wetter the more it dries?": "towel",
    }

    print("Welcome to the Riddle Game!")
    score = 0

    for riddle, answer in riddles.items():
        print("\nRiddle:", riddle)
        user_answer = input("Your answer: ").strip().lower()
        if user_answer == answer:
            print("Correct!")
            score += 1
        else:
            print(f"Wrong! The correct answer was: {answer}")

    print(f"\nGame over! Your score: {score}/{len(riddles)}")
