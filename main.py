import game
import agent
import genetic


def play_game(genome):
    """
    Faz o melhor agente jogar uma partida.

    Retorna o board final e o score.
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


def train():
    """
    Treina o algoritmo genético.
    """

    best_genome, best_fitness = genetic.evolve(
        population_size=30,
        generations=20,
        survivors_count=6
    )

    print("\n==============================")
    print("TRAINING FINISHED")
    print("==============================")

    print(
        f"Best fitness: {best_fitness:.0f}"
    )

    print(
        "Best genome:"
    )

    print(best_genome)

    return best_genome


def test_agent(genome, games=20):
    """
    Testa o melhor genome encontrado
    em várias partidas novas.

    Isso é importante porque o fitness usado
    durante o treinamento também possui aleatoriedade.
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


def main():

    # 1. Evolui a população
    best_genome = train()

    # 2. Testa o melhor indivíduo
    test_agent(
        best_genome,
        games=20
    )


if __name__ == "__main__":
    main()