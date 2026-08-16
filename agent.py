import random

import game
import genetic


def random_agent(board):
    """
    Agente baseline.

    Não possui inteligência.

    Escolhe aleatoriamente entre os movimentos possíveis.

    Serve para termos uma referência de desempenho.
    """

    moves = game.available_moves(board)

    if not moves:
        return None

    return random.choice(moves)


def genetic_agent(board, genome):
    """
    Agente que utiliza um genome para decidir.

    O genome contém os pesos que determinam
    como o agente avalia um board.

    O agente testa todos os movimentos possíveis
    e escolhe aquele que produz o melhor board
    segundo o genome.
    """

    return genetic.choose_move(
        board,
        genome
    )