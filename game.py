import random


DIRECTIONS = ["left", "right", "up", "down"]


def transpose(board):
    """
    Transforma linhas em colunas.

    Exemplo:

    1 2 3
    4 5 6
    7 8 9

    vira:

    1 4 7
    2 5 8
    3 6 9
    """

    return [
        [board[j][i] for j in range(len(board))]
        for i in range(len(board[0]))
    ]


def move_row_left(row):
    """
    Move uma única linha para a esquerda.

    Também realiza os merges e calcula o score
    gerado por essa linha.

    Retorna:

        new_row, score
    """

    # Remove os zeros
    numbers = [x for x in row if x != 0]

    result = []
    score = 0

    i = 0

    while i < len(numbers):

        # Dois números iguais podem ser combinados
        if (
            i + 1 < len(numbers)
            and numbers[i] == numbers[i + 1]
        ):
            merged = numbers[i] * 2

            result.append(merged)

            # O score recebido é o valor da peça criada
            score += merged

            i += 2

        else:
            result.append(numbers[i])
            i += 1

    # Completa a linha com zeros
    result += [0] * (4 - len(result))

    return result, score


def move_row_right(row):
    """
    Faz o movimento para direita reutilizando
    a lógica de movimento para esquerda.
    """

    reversed_row = row[::-1]

    new_row, score = move_row_left(reversed_row)

    return new_row[::-1], score


def move_rows(board, move_function):
    """
    Aplica uma função de movimento em todas as linhas.

    Também soma o score de todas as linhas.
    """

    new_board = []
    score = 0

    for row in board:
        new_row, row_score = move_function(row)

        new_board.append(new_row)

        score += row_score

    return new_board, score


def move(board, direction):
    """
    Executa um movimento.

    Retorna:

        new_board
        reward
        moved

    reward = score ganho neste movimento.

    moved = indica se o tabuleiro realmente mudou.
    """

    original_board = [row[:] for row in board]

    if direction == "left":

        new_board, score = move_rows(
            board,
            move_row_left
        )

    elif direction == "right":

        new_board, score = move_rows(
            board,
            move_row_right
        )

    elif direction == "up":

        transposed = transpose(board)

        transposed, score = move_rows(
            transposed,
            move_row_left
        )

        new_board = transpose(transposed)

    elif direction == "down":

        transposed = transpose(board)

        transposed, score = move_rows(
            transposed,
            move_row_right
        )

        new_board = transpose(transposed)

    else:
        raise ValueError(
            f"Invalid direction: {direction}"
        )

    moved = new_board != original_board

    return new_board, score, moved


def available_moves(board):
    """
    Retorna os movimentos que realmente alterariam
    o tabuleiro.
    """

    moves = []

    for direction in DIRECTIONS:

        _, _, moved = move(board, direction)

        if moved:
            moves.append(direction)

    return moves


def is_game_over(board):
    """
    O jogo acabou quando não existe nenhum movimento possível.
    """

    return len(available_moves(board)) == 0


def add_new_tile(board):
    """
    Adiciona uma nova peça:

    90% -> 2
    10% -> 4

    Cria uma cópia do board para não modificar o original.
    """

    board = [row[:] for row in board]

    empty_cells = []

    for i in range(4):
        for j in range(4):

            if board[i][j] == 0:
                empty_cells.append((i, j))

    if empty_cells:

        row, col = random.choice(empty_cells)

        board[row][col] = (
            2 if random.random() < 0.9 else 4
        )

    return board


def reset_game():
    """
    Cria um novo tabuleiro com duas peças iniciais.
    """

    board = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]

    add_new_tile(board)
    add_new_tile(board)

    return board