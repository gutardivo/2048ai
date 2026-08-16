import json

import agent
import game


def load_genome():

    with open(
        "models/best_genome.json",
        "r"
    ) as file:

        return json.load(file)


def play_game(genome):

    board = game.reset_game()

    score = 0

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

            score += reward

            game.add_new_tile(board)

    return board, score


def main():

    genome = load_genome()

    print("Loaded genome:")
    print(genome)

    games = 50

    scores = []
    max_tiles = []

    for i in range(games):

        board, score = play_game(
            genome
        )

        scores.append(score)

        max_tile = max(
            max(row)
            for row in board
        )

        max_tiles.append(max_tile)

    print("\n==============================")
    print("TEST")
    print("==============================")

    print(f"Games: {games}")

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


if __name__ == "__main__":
    main()