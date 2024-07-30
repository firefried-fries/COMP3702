import random

def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 5)

def check_winner(board, symbol):
    for row in board:
        if all([cell == symbol for cell in row]):
            return True

    for col in range(3):
        if all([board[row][col] == symbol for row in range(3)]):
            return True

    if all([board[i][i] == symbol for i in range(3)]) or all([board[i][2-i] == symbol for i in range(3)]):
        return True

    return False

def is_board_full(board):
    return all(cell != ' ' for row in board for cell in row)

def get_available_moves(board):
    return [(r, c) for r in range(3) for c in range(3) if board[r][c] == ' ']

def player_move(board):
    while True:
        try:
            row, col = map(int, input("Enter your move (row and column): ").split())
            if board[row][col] == ' ':
                board[row][col] = 'O'
                break
            else:
                print("Cell already taken, choose another one.")
        except (ValueError, IndexError):
            print("Invalid input. Please enter row and column as two numbers between 0 and 2.")

def ai_move(board):
    available_moves = get_available_moves(board)
    move = random.choice(available_moves)
    board[move[0]][move[1]] = 'X'

def is_valid_state(board):
    o_count = sum(row.count('O') for row in board)
    x_count = sum(row.count('X') for row in board)
    return o_count == x_count or o_count == x_count + 1

def count_valid_states(board=None, turn='O'):
    """
    (Recall that the formula of ordered selection with repetition is n ** r in MATH1061.)

    We have 3 possible choice at each cell - X, O, and ' ' (blank), and 3x3 = 9 cells in total.
    Therefore, upper bound of valid states = total number of possible states = 3 ** 9 = 19683

    ChatGPT attempts to count the number of valid state recursively. However, it made a grave mistake.

    The first mistake it made is that it would count the same state multiple times.
    For example, X first placed in (0,0), then O placed at (0,1), then X placed at (0,2); and
    X first placed in (0,2), then O placed at (0,1), then X placed at (0,0) will result in the same state as below:
    X|O|X
     | |
     | |
    but ChatGPT counts it multiple times.

    How do we prevent that?
    """
    if board is None:
        board = [[' ' for _ in range(3)] for _ in range(3)]
    
    if check_winner(board, 'O') or check_winner(board, 'X'):  #this GPT answer thinks that winning states are not counted to the valid states
        return 0

    if is_board_full(board): 
        return 1 if is_valid_state(board) else 0

    valid_states = 0
    for r in range(3):
        for c in range(3):
            if board[r][c] == ' ':
                board[r][c] = turn
                valid_states += count_valid_states(board, 'X' if turn == 'O' else 'O')
                board[r][c] = ' '

    return valid_states # what other mistakes had it make?

def main():
    board = [[' ' for _ in range(3)] for _ in range(3)]
    print("Welcome to Tic-Tac-Toe!")
    print_board(board)

    while True:
        player_move(board)
        print_board(board)
        if check_winner(board, 'O'):
            print("Congratulations! You win!")
            break
        if is_board_full(board):
            print("It's a draw!")
            break

        ai_move(board)
        print("AI has made its move:")
        print_board(board)
        if check_winner(board, 'X'):
            print("AI wins! Better luck next time.")
            break
        if is_board_full(board):
            print("It's a draw!")
            break

    valid_states = count_valid_states()
    print(f"The number of valid Tic-Tac-Toe states is: {valid_states}")

if __name__ == "__main__":
    main()


