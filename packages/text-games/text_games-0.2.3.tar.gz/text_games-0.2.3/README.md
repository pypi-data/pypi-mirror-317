# Text Games

`text_games` is a Python module that offers a collection of simple, text-based games for fun and learning.

## Features

The module includes the following games:
1. **Hangman**: Guess the hidden word letter by letter.
2. **Number Guesser**: Guess a random number within a certain range.
3. **Rock-Paper-Scissors**: Play against the computer.
4. **Riddle Game**: Solve riddles within a limited number of attempts.
5. **Word Scramble**: Unscramble the shuffled letters to form a word.
6. **Snake Game**: A simple terminal-based version of the classic Snake game.
7. **Tic-Tac-Toe**: Play Tic-Tac-Toe (Noughts and Crosses) against the computer or another player.

## Installation

You can install the module via `pip`:

`pip install text-games`

Usage
Each game is implemented in its own file within the `text_games` folder. You can import and use them individually as needed. Here's how you can play each game:

Hangman
`from text_games.hangman import run_hangman`
`run_hangman()`

Number Gusser
`from text_games.number_guesser import run_number_guesser`
`run_number_guesser()`

Rock Paper Scissor
`from text_games.rock_paper_scissor import run_rock_paper_scissors`
`run_rock_paper_scissors()`

Riddle game
`from text_games.riddle_game import run_riddle_game`
`run_riddle_game()`

Word Scrambler
`from text_games.word_scrambler import run_word_scrambler`
`run_word_scrambler()`

Snake Game
`from text_games.snake_game import run_snake_game`
`run_snake_game()`

Tic Tac Toe
`from text_games.tic_tac_toe import run_tic_tac_toe`
`run_tic_tac_toe()`

