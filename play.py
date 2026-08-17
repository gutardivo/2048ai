import json

import agent
import game

def load_genome():
    with open(
        "models/best_genome.json",
        "r"
    ) as file:
        return json.load(file)


def play_game(genome, win_target=1024):
    board = game.reset_game()

    score = 0
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
            score += reward

            board = game.add_new_tile(board)

            # Check if won (reached win_target)
            max_tile = max(max(row) for row in board)
            if max_tile >= win_target and not won:
                won = True

    return board, score, won

def main():
    genome = load_genome()

    print("Loaded genome:")
    print(genome)

    games = 500
    win_target = 1024

    scores = []
    max_tiles = []
    wins = 0

    for i in range(games):

        board, score, won = play_game(
            genome,
            win_target
        )

        scores.append(score)

        max_tile = max(
            max(row)
            for row in board
        )

        max_tiles.append(max_tile)

        if won:
            wins += 1

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

    print(
        f"Wins (target {win_target}): {wins}/{games} "
        f"({wins/games*100:.1f}%)"
    )


if __name__ == "__main__":
    main()