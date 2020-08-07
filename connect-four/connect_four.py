import random
from termcolor import colored
import numpy as np

# red starts first?
marks = [colored("O", 'red'), colored("O", 'blue')]


def main():
    # initialize all relevant parameters
    board = init_board()
    players = init_players()
    active_player_index = 0
    current_player = players[active_player_index]

    # loop until there is a winner or the board is full
    while not check_for_winner(board, active_player_index - 1):
        current_player = players[active_player_index]
        current_player_mark = marks[active_player_index]

        announce_player(current_player)
        show_board(board)
        choose_location(board, current_player_mark)
        if is_board_full(board):
            break

        active_player_index = (active_player_index + 1) % len(players)

    game_over_print(board, current_player, active_player_index - 1)


def init_board():
    """Set board to zero | transposed for easier checking later"""
    return [
        [None, None, None, None, None, None],
        [None, None, None, None, None, None],
        [None, None, None, None, None, None],
        [None, None, None, None, None, None],
        [None, None, None, None, None, None],
        [None, None, None, None, None, None],
        [None, None, None, None, None, None],
    ]


def init_players():
    """Enter player names and randomly select starting player"""
    players = [input("Enter player name: "), input("Enter player name: ")]
    player_1 = random.choice(players)
    player_2 = players[players.index(player_1) - 1]
    print(f"{player_1} goes 1st!")
    return [player_1, player_2]


def check_for_winner(board, active_player_index):
    """Check after any round if there is a winner"""
    # check for winner by columns (because it's transposed)
    if check_winning_states(board, active_player_index):
        return True

    # check for winner by rows (TT = original)
    flipped_board = np.transpose(board)
    if check_winning_states(flipped_board, active_player_index):
        return True

    # check for winner by diagonals
    # add -45° diagonals
    diagonals = [np.diagonal(board, offset=i) for i in range(-3, 3)]
    # flip it vertically (left-right) and check 45° diagonals
    flipped_board = np.fliplr(board)
    diagonals += [np.diagonal(flipped_board, offset=i) for i in range(-3, 3)]
    if check_winning_states(diagonals, active_player_index):
        return True


def check_winning_states(rows_to_be_checked, active_player_index):
    """Helper function for checking if there is a winner"""
    global marks
    current_player_win_check = [marks[active_player_index]] * 4

    for row in rows_to_be_checked:
        if marks[active_player_index] in row:
            for i in range(0, len(row) - 3):
                if list(row[i:i + 4]) == current_player_win_check:
                    return True


def is_board_full(board):
    """Check if board is full, used to check if there is a tie"""
    if any(None in row for row in board):
        return False


def announce_player(player):
    """Announce player whose turn it is"""
    print(f"{player}, choose a column")


def show_board(board):
    """Draw current state of the board"""
    flipped_board = np.transpose(board)
    for row in flipped_board:
        for cell in row:
            cell = cell if cell is not None else "_"
            print(cell, end=" ")
        print()


def choose_location(board, mark):
    """Let current player choose spot in array"""
    while True:
        try:
            column = int(input(f"Choose spot to drop {mark} (1-7): "))
            if column in range(1, 8):
                if check_location(board, column - 1, mark):
                    break
        except ValueError:
            print("Spot must be between an integer between 1 and 7!")
            continue
    print()


def check_location(board, column, mark):
    """Helper function for drop location - checks if column is full"""
    while True:
        if None in board[column]:
            for row_index in reversed(range(0, 6)):
                if not board[column][row_index]:
                    board[column][row_index] = mark
                    return True
        else:
            print("Please choose another column this one is full!")
            return False


def game_over_print(board, current_player, active_player_index):
    """Print game result along with final board state"""
    print()
    if not check_for_winner(board, active_player_index):
        print("The game is a tie!")
    else:
        print(f"Game over! {current_player} won with game state: ")
    show_board(board)


if __name__ == '__main__':
    main()
