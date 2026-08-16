import random

from game import available_moves


def random_agent(board):
    moves = available_moves(board)

    if not moves:
        return None

    return random.choice(moves)