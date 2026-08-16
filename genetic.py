import random

import game


# ============================================================
# GENOME
# ============================================================

def create_genome():
    """
    Cria um indivíduo.

    O genome contém 4 pesos:

        [0] empty_cells
        [1] max_tile
        [2] monotonicity
        [3] smoothness

    Esses pesos determinam como o agente avalia
    um tabuleiro.

    O algoritmo genético vai tentar encontrar
    bons valores para esses pesos.
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
    Cria uma população contendo vários genomes.

    Cada genome começa com pesos aleatórios.
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
    Conta quantas células vazias existem.
    """

    return sum(
        cell == 0
        for row in board
        for cell in row
    )


def get_max_tile(board):
    """
    Retorna o maior tile existente.
    """

    return max(
        max(row)
        for row in board
    )


def calculate_smoothness(board):
    """
    Mede o quão próximos são os valores dos tiles vizinhos.

    Usamos log2 porque:

        2, 4, 8, 16, 32...

    possuem diferenças mais significativas
    em escala logarítmica.

    Quanto mais próximos forem os vizinhos,
    maior será a smoothness.
    """

    smoothness = 0

    for i in range(4):
        for j in range(4):

            value = board[i][j]

            if value == 0:
                continue

            log_value = value.bit_length() - 1

            # Vizinho da direita
            if j + 1 < 4:

                neighbor = board[i][j + 1]

                if neighbor != 0:
                    neighbor_log = neighbor.bit_length() - 1

                    smoothness -= abs(
                        log_value - neighbor_log
                    )

            # Vizinho de baixo
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
    Mede se os valores do tabuleiro seguem uma direção
    consistente.

    Exemplo bom:

        128 64 32 16
        64  32 16  8
        32  16 8   4
        16  8  4   2

    A ideia é incentivar o agente a organizar os tiles
    em uma direção.

    O resultado pode ser positivo ou negativo.
    """

    totals = [0, 0, 0, 0]

    # Avalia as linhas
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

    # Avalia as colunas
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
    Calcula o valor de um tabuleiro usando um genome.

    O genome contém os pesos.

    Exemplo:

        genome = [
            5.0,
            2.0,
            3.0,
            1.0
        ]

    Então:

        avaliação =
            5 * empty_cells
          + 2 * max_tile
          + 3 * monotonicity
          + 1 * smoothness

    Quanto maior o resultado,
    melhor o agente considera o tabuleiro.
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
    Usa um genome para escolher o próximo movimento.

    Para cada movimento possível:

        1. Executa o movimento.
        2. Olha o novo board.
        3. Avalia o novo board.
        4. Escolhe o movimento com maior avaliação.

    Esse é o "cérebro" do nosso agente.
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

def play_game(genome):
    """
    Faz um genome jogar uma partida completa.

    O score final da partida será utilizado
    como medida de fitness.
    """

    board = game.reset_game()

    total_score = 0

    while not game.is_game_over(board):

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

            game.add_new_tile(board)

    return total_score


def fitness(genome, games=10):
    """
    Calcula o fitness médio de um genome.

    Jogamos várias partidas porque o 2048 possui
    aleatoriedade.

    Um único jogo pode dar um resultado muito ruim
    ou muito bom simplesmente por sorte.

    Portanto usamos a média.
    """

    scores = []

    for _ in range(games):
        score = play_game(genome)
        scores.append(score)

    return sum(scores) / len(scores)


# ============================================================
# SELECTION
# ============================================================

def selection(population, fitnesses, survivors):
    """
    Seleciona os melhores indivíduos.

    population:
        lista de genomes

    fitnesses:
        fitness correspondente a cada genome

    survivors:
        quantidade de indivíduos que queremos manter

    Retorna os melhores genomes.
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
    Cria um filho combinando dois pais.

    Para cada gene:

        50% chance de pegar do pai 1
        50% chance de pegar do pai 2
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
    Faz pequenas alterações aleatórias no genome.

    mutation_rate = chance de cada gene sofrer mutação.

    Exemplo:

        [5.0, 2.0, 3.0, 1.0]

    pode virar:

        [5.0, 2.0, 3.7, 1.0]

    A mutação mantém diversidade na população.
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
    initial_genome=None
):
    """
    Executa o algoritmo genético completo.

    Em cada geração:

        1. Calcula fitness de todos.
        2. Seleciona os melhores.
        3. Faz crossover.
        4. Faz mutation.
        5. Cria uma nova população.

    Retorna o melhor genome encontrado.
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
                games=10
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

        # Guarda o melhor indivíduo encontrado
        best_index = fitnesses.index(
            generation_best
        )

        if generation_best > best_fitness:

            best_fitness = generation_best

            best_genome = population[
                best_index
            ][:]

        # Seleciona os melhores
        survivors = selection(
            population,
            fitnesses,
            survivors_count
        )

        # Começamos a nova população
        new_population = [
            genome[:]
            for genome in survivors
        ]

        # Preenche o restante com filhos
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