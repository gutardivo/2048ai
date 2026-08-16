import random

import game
import genetic


def random_agent(board):
    """
    Baseline agent.

    Has no intelligence.

    Randomly chooses among possible moves.

    Serves as a performance reference.
    """

    moves = game.available_moves(board)

    if not moves:
        return None

    return random.choice(moves)


def genetic_agent(board, genome):
    """
    Agent that uses a genome to make decisions.

    The genome contains the weights that determine
    how the agent evaluates a board.

    The agent tests all possible moves
    and chooses the one that produces the best board
    according to the genome.
    """

    return genetic.choose_move(
        board,
        genome
    )