"""
Tic Tac Toe Player
"""

import math
import copy
import numpy
import random

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def count_XO(board, player):
    """
    Returns count of player elements in board
    """
    count = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if player == board[i][j]:
                count +=1
    return count


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    if board == initial_state():
        return X
    elif count_XO(board, X) > count_XO(board, O):
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    acts = set()
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                acts.add((i,j))
    return acts


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    copy_board = copy.deepcopy(board)
    p = player(board)
    try:
        copy_board[action[0]][action[1]] = p
        return copy_board
    except Exception as e:
        print(e)
        raise e


def replace_XO(board, player):
    """
    Returns an 0 1 board depending of player is X or O
    """
    copy_board = copy.deepcopy(board)
    for i in range(len(copy_board)):
        for j in range(len(copy_board[i])):
            if copy_board[i][j] == player:
                copy_board[i][j] = 1
            else:
                copy_board[i][j] = 0
    return copy_board


def win(board):
    """
    Check vertically, horizontally and diagonal for win
    """
    npa = numpy.asarray(board)
    if 3 in npa.sum(axis=1): # look for a horizontal victory
        return True
    elif 3 in npa.sum(axis=0): # look for a vertical victory
        return True
    elif 3 == npa.diagonal().sum(): # look in principal diagonal
        return True
    elif 3 == numpy.fliplr(npa).diagonal().sum(): # look in reverse diagonal
        return True
    else:
        return False


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if win(replace_XO(board, X)):
        return X
    elif win(replace_XO(board, O)):
        return O
    else:
        None


def check_empty(board):
    """
    Returns True if empty space available, false if not
    """
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                return True
    return False


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):
        return True
    elif not check_empty(board):
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def max_value(board):
    """
    Recursive function to maximize until terminal.
    Returns (utility, action)
    """
    if terminal(board):
        return (utility(board), None)

    v = -math.inf
    best_action = None

    for action in actions(board):
        rec = min_value(result(board, action))
        if rec[0] > v:
            print("max", rec, v)
            v = rec[0]
            best_action = action

    return (v, best_action)

def min_value(board):
    """
    Recursive function to min until terminal.
    Returns (utility, action)
    """
    if terminal(board):
        return (utility(board), None)

    v = math.inf
    best_action = None

    for action in actions(board):
        rec = max_value(result(board, action))
        if rec[0] < v:
            print("min", rec, v)
            v = rec[0]
            best_action = action

    return (v, best_action)


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    
    if count_XO(board, X) < 2: # any movement in the beginning is good
        action = random.choice(list(actions(board)))
        return action

    best_action = None

    if player(board) == X:
        best_action = max_value(board)[1]
    elif player(board) == O:
        best_action = min_value(board)[1]
    
    return best_action
    
