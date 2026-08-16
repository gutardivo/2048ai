import game
import agent
import genetic
import json
import matplotlib.pyplot as plt


def play_game(genome, win_target=1024):
    """
    Makes the agent play a game.

    Returns:
        final board
        final score
        won: True if win_target was reached
    """

    board = game.reset_game()

    total_score = 0
    won = False

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

            board = game.add_new_tile(board)

            # Check if won (reached win_target)
            max_tile = max(max(row) for row in board)
            if max_tile >= win_target and not won:
                won = True

    return board, total_score, won


def save_genome(
    genome,
    filename="models/best_genome.json"
):
    """
    Saves the genome to a JSON file.
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
    Loads a saved genome.
    """

    with open(filename, "r") as file:
        return json.load(file)


def train(win_target=1024):
    """
    Trains the genetic algorithm.
    """

    best_genome, best_fitness, history = (
        genetic.evolve(
            population_size=30,
            generations=20,
            survivors_count=6,
            win_target=win_target
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
    Plots the fitness evolution
    over generations.
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


def test_agent(genome, games=50, win_target=1024):
    """
    Tests the genome in multiple games.

    Training is not considered here.
    These are new games.
    """

    scores = []
    max_tiles = []
    wins = 0

    for _ in range(games):

        board, score, won = play_game(
            genome,
            win_target
        )

        scores.append(score)

        max_tiles.append(
            max(
                max(row)
                for row in board
            )
        )

        if won:
            wins += 1

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
        f"Wins (target {win_target}): {wins}/{games} "
        f"({wins/games*100:.1f}%)"
    )


def main():

    # 1. Train
    best_genome, history = train()

    # 2. Save the best genome
    save_genome(best_genome)

    # 3. Show the evolution
    plot_evolution(history)

    # 4. Test the best genome
    test_agent(
        best_genome,
        games=50
    )


if __name__ == "__main__":
    main()