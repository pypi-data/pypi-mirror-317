def run_tic_tac_toe():
    def print_board(board):
        for row in board:
            print(" | ".join(row))
            print("-" * 5)

    def check_winner(board, mark):
        for row in board:
            if all(cell == mark for cell in row):
                return True
        for col in range(3):
            if all(board[row][col] == mark for row in range(3)):
                return True
        if all(board[i][i] == mark for i in range(3)) or all(board[i][2 - i] == mark for i in range(3)):
            return True
        return False

    print("Welcome to Tic Tac Toe!")
    board = [[" " for _ in range(3)] for _ in range(3)]
    turns = 0
    current_player = "X"

    while turns < 9:
        print_board(board)
        print(f"Player {current_player}'s turn.")
        try:
            row, col = map(int, input("Enter row and column (0-2, space-separated): ").split())
            if board[row][col] != " ":
                print("Cell already occupied!")
                continue
            board[row][col] = current_player
            if check_winner(board, current_player):
                print_board(board)
                print(f"Player {current_player} wins!")
                return
            current_player = "O" if current_player == "X" else "X"
            turns += 1
        except (ValueError, IndexError):
            print("Invalid input! Try again.")
    
    print_board(board)
    print("It's a draw!")
