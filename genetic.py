import random

import game


# ============================================================
# GENOME
# ============================================================

def create_genome():
    """
    Creates an individual.

    The genome contains 4 weights:

        [0] empty_cells
        [1] max_tile
        [2] monotonicity
        [3] smoothness

    These weights determine how the agent evaluates
    a board.

    The genetic algorithm will try to find
    good values for these weights.
    """

    return [
        random.uniform(-10, 10),
        random.uniform(-10, 10),
        random.uniform(-10, 10),
        random.uniform(-10, 10),
    ]


# ============================================================
# POPULATION
# ============================================================

def create_population(size):
    """
    Creates a population containing multiple genomes.

    Each genome starts with random weights.
    """

    return [
        create_genome()
        for _ in range(size)
    ]


# ============================================================
# BOARD EVALUATION
# ============================================================

def count_empty_cells(board):
    """
    Counts how many empty cells exist.
    """

    return sum(
        cell == 0
        for row in board
        for cell in row
    )


def get_max_tile(board):
    """
    Returns the largest existing tile.
    """

    return max(
        max(row)
        for row in board
    )


def calculate_smoothness(board):
    """
    Measures how close the values of neighboring tiles are.

    We use log2 because:

        2, 4, 8, 16, 32...

    have more significant differences
    on a logarithmic scale.

    The closer the neighbors are,
    the higher the smoothness.
    """

    smoothness = 0

    for i in range(4):
        for j in range(4):

            value = board[i][j]

            if value == 0:
                continue

            log_value = value.bit_length() - 1

            # Right neighbor
            if j + 1 < 4:

                neighbor = board[i][j + 1]

                if neighbor != 0:
                    neighbor_log = neighbor.bit_length() - 1

                    smoothness -= abs(
                        log_value - neighbor_log
                    )

            # Bottom neighbor
            if i + 1 < 4:

                neighbor = board[i + 1][j]

                if neighbor != 0:
                    neighbor_log = neighbor.bit_length() - 1

                    smoothness -= abs(
                        log_value - neighbor_log
                    )

    return smoothness


def calculate_monotonicity(board):
    """
    Measures if the board values follow a consistent
    direction.

    Good example:

        128 64 32 16
        64  32 16  8
        32  16 8   4
        16  8  4   2

    The idea is to encourage the agent to organize tiles
    in one direction.

    The result can be positive or negative.
    """

    totals = [0, 0, 0, 0]

    # Evaluate rows
    for row in board:

        for i in range(3):

            current = row[i]
            next_value = row[i + 1]

            if current == 0 or next_value == 0:
                continue

            current_log = current.bit_length() - 1
            next_log = next_value.bit_length() - 1

            if current > next_value:
                totals[0] += next_log - current_log

            elif next_value > current:
                totals[1] += current_log - next_log

    # Evaluate columns
    for j in range(4):

        for i in range(3):

            current = board[i][j]
            next_value = board[i + 1][j]

            if current == 0 or next_value == 0:
                continue

            current_log = current.bit_length() - 1
            next_log = next_value.bit_length() - 1

            if current > next_value:
                totals[2] += next_log - current_log

            elif next_value > current:
                totals[3] += current_log - next_log

    return max(totals[0], totals[1]) + max(
        totals[2],
        totals[3]
    )


def evaluate_board(board, genome):
    """
    Calculates the value of a board using a genome.

    The genome contains the weights.

    Example:

        genome = [
            5.0,
            2.0,
            3.0,
            1.0
        ]

    Then:

        evaluation =
            5 * empty_cells
          + 2 * max_tile
          + 3 * monotonicity
          + 1 * smoothness

    The higher the result,
    the better the agent considers the board.
    """

    empty_cells = count_empty_cells(board)

    max_tile = get_max_tile(board)

    monotonicity = calculate_monotonicity(board)

    smoothness = calculate_smoothness(board)

    return (
        genome[0] * empty_cells
        + genome[1] * max_tile
        + genome[2] * monotonicity
        + genome[3] * smoothness
    )


# ============================================================
# AGENT
# ============================================================

def choose_move(board, genome):
    """
    Uses a genome to choose the next move.

    For each possible move:

        1. Executes the move.
        2. Looks at the new board.
        3. Evaluates the new board.
        4. Chooses the move with the highest evaluation.

    This is the "brain" of our agent.
    """

    moves = game.available_moves(board)

    if not moves:
        return None

    best_move = None
    best_value = float("-inf")

    for move in moves:

        new_board, _, _ = game.move(
            board,
            move
        )

        value = evaluate_board(
            new_board,
            genome
        )

        if value > best_value:

            best_value = value
            best_move = move

    return best_move


# ============================================================
# FITNESS
# ============================================================

def play_game(genome, win_target=1024):
    """
    Makes a genome play a complete game.

    Returns:
        score: total score of the game
        won: True if win_target was reached, False otherwise
    """

    board = game.reset_game()

    total_score = 0
    won = False
    moves_count = 0
    max_moves = 5000  # Safety limit

    while not game.is_game_over(board) and moves_count < max_moves:

        action = choose_move(
            board,
            genome
        )

        if action is None:
            break

        board, reward, moved = game.move(
            board,
            action
        )

        if moved:

            total_score += reward

            board = game.add_new_tile(board)

            # Check if won (reached win_target)
            max_tile = get_max_tile(board)
            if max_tile >= win_target and not won:
                won = True

        moves_count += 1

    return total_score, won


def fitness(genome, games=3, win_target=1024):
    """
    Calculates the average fitness of a genome.

    We play multiple games because 2048 has
    randomness.

    A single game can give a very bad result
    or a very good result simply by luck.

    Therefore we use the average.

    Victory has much more weight than score:
    - Victory: +100000 points per game
    - Score: normal game value
    """

    total_fitness = 0
    wins = 0

    for _ in range(games):
        score, won = play_game(genome, win_target)

        if won:
            wins += 1
            total_fitness += 100000  # Huge bonus for winning

        total_fitness += score

    return total_fitness / games


# ============================================================
# SELECTION
# ============================================================

def selection(population, fitnesses, survivors):
    """
    Selects the best individuals.

    population:
        list of genomes

    fitnesses:
        fitness corresponding to each genome

    survivors:
        number of individuals we want to keep

    Returns the best genomes.
    """

    ranked = sorted(
        zip(population, fitnesses),
        key=lambda item: item[1],
        reverse=True
    )

    return [
        genome
        for genome, _ in ranked[:survivors]
    ]


# ============================================================
# CROSSOVER
# ============================================================

def crossover(genome1, genome2):
    """
    Creates a child by combining two parents.

    For each gene:

        50% chance to get from parent 1
        50% chance to get from parent 2
    """

    child = []

    for gene1, gene2 in zip(
        genome1,
        genome2
    ):

        if random.random() < 0.5:
            child.append(gene1)
        else:
            child.append(gene2)

    return child


# ============================================================
# MUTATION
# ============================================================

def mutation(genome, mutation_rate=0.1):
    """
    Makes small random changes to the genome.

    mutation_rate = chance of each gene suffering mutation.

    Example:

        [5.0, 2.0, 3.0, 1.0]

    can become:

        [5.0, 2.0, 3.7, 1.0]

    Mutation maintains diversity in the population.
    """

    mutated = genome[:]

    for i in range(len(mutated)):

        if random.random() < mutation_rate:

            mutated[i] += random.gauss(
                0,
                1
            )

    return mutated


# ============================================================
# EVOLUTION
# ============================================================

def evolve(
    population_size=30,
    generations=20,
    survivors_count=6,
    initial_genome=None,
    win_target=1024
):
    """
    Executes the complete genetic algorithm.

    In each generation:

        1. Calculates fitness of all.
        2. Selects the best.
        3. Performs crossover.
        4. Performs mutation.
        5. Creates a new population.

    Returns the best genome found.
    """

    history = {
        "best": [],
        "average": []
    }

    if initial_genome:
        print("Using initial genome:", initial_genome)
        population = [
            mutation(
                initial_genome,
                mutation_rate=0.5
            )
            for _ in range(population_size)
        ]
    else:
        population = create_population(
            population_size
        )

    best_genome = None
    best_fitness = float("-inf")

    for generation in range(generations):

        print(
            f"\nGeneration {generation + 1}/{generations}"
        )

        fitnesses = []

        for genome in population:

            score = fitness(
                genome,
                games=10,
                win_target=win_target
            )

            fitnesses.append(score)

        generation_best = max(fitnesses)

        generation_average = (
            sum(fitnesses)
            / len(fitnesses)
        )

        history["best"].append(generation_best)
        history["average"].append(generation_average)

        print(
            f"Best: {generation_best:.0f}"
        )

        print(
            f"Average: {generation_average:.0f}"
        )

        # Store the best individual found
        best_index = fitnesses.index(
            generation_best
        )

        if generation_best > best_fitness:

            best_fitness = generation_best

            best_genome = population[
                best_index
            ][:]

        # Select the best
        survivors = selection(
            population,
            fitnesses,
            survivors_count
        )

        # Start the new population
        new_population = [
            genome[:]
            for genome in survivors
        ]

        # Fill the rest with children
        while len(new_population) < population_size:

            parent1 = random.choice(
                survivors
            )

            parent2 = random.choice(
                survivors
            )

            child = crossover(
                parent1,
                parent2
            )

            child = mutation(child)

            new_population.append(child)

        population = new_population

    return best_genome, best_fitness, history