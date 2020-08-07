import random
from termcolor import colored
import numpy as np

marks = [colored("O", 'red'), colored("O", 'blue')]


def main():
    # initialize all relevant parameters
    board = init_board()
    players = init_players()
    # red starts first?
    active_player_index = 0
    current_player = players[active_player_index]

    # loop until there is a winner or the board is full
    while not check_for_winner(board, active_player_index - 1) or not is_board_full(board):
        current_player = players[active_player_index]
        current_player_mark = marks[active_player_index]

        announce_player(current_player)
        show_board(board)
        choose_location(board, current_player_mark)

        active_player_index = (active_player_index + 1) % len(players)

    game_over_print(board, current_player, active_player_index - 1)


# set board to zero | transposed for easier checking later
def init_board():
    return [
        [None, None, None, None, None, None],
        [None, None, None, None, None, None],
        [None, None, None, None, None, None],
        [None, None, None, None, None, None],
        [None, None, None, None, None, None],
        [None, None, None, None, None, None],
        [None, None, None, None, None, None],
    ]


# enter player names and randomly select starting player
def init_players():
    players = [input("Enter player name: "), input("Enter player name: ")]
    player_1 = random.choice(players)
    player_2 = players[players.index(player_1) - 1]
    print(f"{player_1} goes 1st!")
    return [player_1, player_2]


# check after any round if there is a winner
def check_for_winner(board, active_player_index):
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


# helper function for checking if there is a winner
def check_winning_states(rows_to_be_checked, active_player_index):
    global marks
    current_player_win_check = []
    for i in range(4):
        current_player_win_check.append(marks[active_player_index])

    for row in rows_to_be_checked:
        if marks[active_player_index] in row:
            for i in range(0, len(row) - 3):
                if list(row[i:i + 4]) == current_player_win_check:
                    return True


# check if board is full, used to check if there is a tie
def is_board_full(board):
    if None not in board:
        return True


# announce player whose turn it is
def announce_player(player):
    print(f"{player}, choose a column")


# draw current state of the board
def show_board(board):
    flipped_board = zip(*board)
    for row in flipped_board:
        for cell in row:
            cell = cell if cell is not None else "_"
            print(cell, end=" ")
        print()


# let current player choose spot on board
def choose_location(board, mark):
    while True:
        try:
            column = int(input(f"Choose spot to put {mark} (1-7): "))
            if column in range(1, 8):
                if check_location(board, column - 1, mark):
                    break
        except ValueError:
            print("Spot must be between an integer between 1 and 7!")
            continue
    print()


# helper function for drop location - checks if column is ful
def check_location(board, column, mark):
    while True:
        if None in board[column]:
            for row_index in reversed(range(0, 6)):
                if not board[column][row_index]:
                    board[column][row_index] = mark
                    return True
        else:
            print("Please choose another column this one is full!")
            return False


# print game result along with final board state
def game_over_print(board, current_player, active_player_index):
    print()
    if not check_for_winner(board, active_player_index):
        print("The game is a tie!")
    else:
        print(f"Game over! {current_player} won with game state: ")
    show_board(board)


if __name__ == '__main__':
    main()
