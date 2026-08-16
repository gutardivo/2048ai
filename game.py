def is_game_over(board):
    return len(available_moves(board)) == 0

def available_moves(board):
    moves = []

    for direction in ["left", "right", "up", "down"]:
        _, _, moved = move(board, direction)

        if moved:
            moves.append(direction)

    return moves

def transpose(board):
    new_board = []
    for i in range(len(board)):
        new_row = []
        for j in range(len(board[i])):
            new_row.append(board[j][i])
        new_board.append(new_row)
    return new_board

def transpose_simpler(board):
    return [
        [board[j][i] for j in range(len(board))]
        for i in range(len(board[0]))
    ]

def move_row_left(row):
    # 1. Remove os zeros
    numbers = [x for x in row if x != 0]

    # 2. Junta os números iguais
    result = []
    score = 0

    i = 0

    while i < len(numbers):
        if i + 1 < len(numbers) and numbers[i] == numbers[i + 1]:
            merged = numbers[i] * 2

            result.append(merged)
            score += merged

            i += 2
        else:
            result.append(numbers[i])
            i += 1

    # 3. Completa com zeros
    result += [0] * (4 - len(result))

    return result, score

def move_row_right(row):
    new_row, score = move_row_left(row[::-1])
    return new_row[::-1], score

def move_rows(board, move_function):
    new_board = []
    score = 0

    for row in board:
        new_row, row_score = move_function(row)

        new_board.append(new_row)
        score += row_score

    return new_board, score

def move(board, direction):
    original_board = [row[:] for row in board]

    if direction == "left":
        new_board, score = move_rows(board, move_row_left)

    elif direction == "right":
        new_board, score = move_rows(board, move_row_right)

    elif direction == "up":
        transposed = transpose(board)
        transposed, score = move_rows(transposed, move_row_left)
        new_board = transpose(transposed)

    elif direction == "down":
        transposed = transpose(board)
        transposed, score = move_rows(transposed, move_row_right)
        new_board = transpose(transposed)

    else:
        raise ValueError(f"Invalid direction: {direction}")

    moved = new_board != original_board

    return new_board, score, moved

def reset_game() -> list:
    board = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    board = add_new_tile(board)
    board = add_new_tile(board)
    return board

def add_new_tile(board) -> list:
    # Find empty cells
    empty_cells = []
    for i in range(4):
        for j in range(4):
            if board[i][j] == 0:
                empty_cells.append((i, j))
    
    if empty_cells:
        # Pick a random empty cell
        import random
        row, col = random.choice(empty_cells)
        # 90% chance of 2, 10% chance of 4
        board[row][col] = 2 if random.random() < 0.9 else 4
    
    return board
