import game
import agent


def play_game():
    board = game.reset_game()
    total_score = 0

    while not game.is_game_over(board):
        action = agent.random_agent(board)

        board, reward, moved = game.move(board, action)

        if moved:
            total_score += reward
            board = game.add_new_tile(board)

    return board, total_score


def main():
    games = 1000

    scores = []
    max_tiles = []

    for _ in range(games):
        board, score = play_game()

        scores.append(score)
        max_tiles.append(max(max(row) for row in board))

    print(f"Games: {games}")
    print(f"Average score: {sum(scores) / len(scores):.2f}")
    print(f"Best score: {max(scores)}")
    print(f"Best tile: {max(max_tiles)}")


if __name__ == "__main__":
    main()