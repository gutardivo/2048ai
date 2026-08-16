import game
import agent
import genetic
import json
import matplotlib.pyplot as plt


def play_game(genome):
    """
    Faz o agente jogar uma partida.

    Retorna:
        board final
        score final
    """

    board = game.reset_game()

    total_score = 0

    while not game.is_game_over(board):

        action = agent.genetic_agent(
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

    return board, total_score


def save_genome(
    genome,
    filename="models/best_genome.json"
):
    """
    Salva o genome em um arquivo JSON.
    """

    with open(filename, "w") as file:
        json.dump(
            genome,
            file,
            indent=4
        )


def load_genome(
    filename="models/best_genome.json"
):
    """
    Carrega um genome salvo.
    """

    with open(filename, "r") as file:
        return json.load(file)


def train():
    """
    Treina o algoritmo genético.
    """

    best_genome, best_fitness, history = (
        genetic.evolve(
            population_size=30,
            generations=20,
            survivors_count=6
        )
    )

    print("\n==============================")
    print("TRAINING FINISHED")
    print("==============================")

    print(
        f"Best fitness: {best_fitness:.0f}"
    )

    print("Best genome:")
    print(best_genome)

    return best_genome, history


def plot_evolution(history):
    """
    Plota a evolução do fitness
    ao longo das gerações.
    """

    generations = range(
        1,
        len(history["best"]) + 1
    )

    plt.plot(
        generations,
        history["best"],
        label="Best fitness"
    )

    plt.plot(
        generations,
        history["average"],
        label="Average fitness"
    )

    plt.xlabel("Generation")
    plt.ylabel("Fitness")

    plt.title(
        "Genetic Algorithm Evolution"
    )

    plt.legend()
    plt.grid()

    plt.show()


def test_agent(genome, games=50):
    """
    Testa o genome em várias partidas.

    O treinamento não é considerado aqui.
    São partidas novas.
    """

    scores = []
    max_tiles = []

    for _ in range(games):

        board, score = play_game(
            genome
        )

        scores.append(score)

        max_tiles.append(
            max(
                max(row)
                for row in board
            )
        )

    print("\n==============================")
    print("TEST")
    print("==============================")

    print(
        f"Games: {games}"
    )

    print(
        f"Average score: "
        f"{sum(scores) / len(scores):.0f}"
    )

    print(
        f"Best score: "
        f"{max(scores)}"
    )

    print(
        f"Best tile: "
        f"{max(max_tiles)}"
    )

    print(
        f"Won the game: "
        f"{max(max_tiles) >= 2048}"
    )


def main():

    # 1. Treina
    best_genome, history = train()

    # 2. Salva o melhor genome
    save_genome(best_genome)

    # 3. Mostra a evolução
    plot_evolution(history)

    # 4. Testa o melhor genome
    test_agent(
        best_genome,
        games=50
    )


if __name__ == "__main__":
    main()