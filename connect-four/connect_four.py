import random
from termcolor import colored
import numpy as np

marks = [colored("O", 'blue'), colored("O", 'red')]
board = []
players = []


def main():
    # initialize all relevant parameters
    set_players()
    set_initial_board_state()
    current_player_index = 1

    # loop until there is a winner or the board is full
    while not (check_for_winner(current_player_index) or is_board_full()):
        current_player_index = (current_player_index + 1) % len(players)
        current_player = players[current_player_index]
        current_player_mark = marks[current_player_index]

        announce_player(current_player)
        show_board()
        set_drop_location(current_player_mark)

    game_over_print(current_player_index)


def set_initial_board_state():
    """Set board to zero | transposed for easier checking later"""
    global board
    board = [
        [None, None, None, None, None, None],
        [None, None, None, None, None, None],
        [None, None, None, None, None, None],
        [None, None, None, None, None, None],
        [None, None, None, None, None, None],
        [None, None, None, None, None, None],
        [None, None, None, None, None, None],
    ]


def set_players():
    """Enter player names and randomly select starting player"""
    global players
    players = [input("Enter player name: "), input("Enter player name: ")]
    player_1 = random.choice(players)
    player_2 = players[players.index(player_1) - 1]
    print(f"{player_1} goes 1st!")
    players = [player_1, player_2]


def check_for_winner(active_player_index):
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
    current_player_win_check = [marks[active_player_index]] * 4

    for row in rows_to_be_checked:
        if marks[active_player_index] in row:
            for i in range(0, len(row) - 3):
                if list(row[i:i + 4]) == current_player_win_check:
                    return True


def is_board_full():
    """Check if board is full, used to check if there is a tie"""
    if not any(None in row for row in board):
        return True


def announce_player(player):
    """Announce player whose turn it is"""
    print(f"{player}, choose a column")


def show_board():
    """Draw current state of the board"""
    flipped_board = np.transpose(board)
    for row in flipped_board:
        for cell in row:
            cell = cell if cell is not None else "_"
            print(cell, end=" ")
        print()


def set_drop_location(mark):
    """Let current player choose drop spot in array"""
    while True:
        try:
            column = int(input(f"Choose spot to drop {mark} (1-7): "))
            if column in range(1, 8):
                if check_location(column - 1, mark):
                    break
        except ValueError:
            print("Spot must be between an integer between 1 and 7!")
            continue
    print()


def check_location(column, mark):
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


def game_over_print(current_player_index):
    """Print game result along with final board state"""
    print()
    if not check_for_winner(current_player_index):
        print("The game is a tie!")
    else:
        print(f"Game over! {players[current_player_index]} won with game state: ")
    show_board()


if __name__ == '__main__':
    main()
