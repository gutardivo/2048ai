import json
import genetic
import matplotlib.pyplot as plt
import os

def load_genome(filename="models/best_genome.json"):
    with open(filename, "r") as file:
        return json.load(file)

def plot_evolution(history):
    """
    Shows how the population fitness
    evolved over generations.
    """

    generations = range(
        1,
        len(history["best"]) + 1
    )

    plt.plot(
        generations,
        history["best"],
        label="Best"
    )

    plt.plot(
        generations,
        history["average"],
        label="Average"
    )

    plt.xlabel("Generation")
    plt.ylabel("Fitness")

    plt.title(
        "Genetic Algorithm Evolution"
    )

    plt.legend()
    plt.grid()

    plt.show()

def create_population_from_genome(
    genome,
    size
):
    population = []

    for _ in range(size):
        mutated = genetic.mutation(
            genome,
            mutation_rate=0.5
        )

        population.append(mutated)

    return population

def main():
    if os.path.exists("models/best_genome.json"):
        genome = load_genome()
    else:
        genome = genetic.create_genome()

    win_target = 1024

    # Train
    best_genome, fitness, history = genetic.evolve(
        population_size=100,
        generations=50,
        survivors_count=6,
        initial_genome=genome,
        win_target=win_target
    )

    print("\n==============================")
    print("TRAINING FINISHED")
    print("==============================")

    print("Best genome:")
    print(best_genome)

    print(
        f"Best fitness: {fitness:.0f}"
    )

    # Save the genome
    with open(
        "models/best_genome.json",
        "w"
    ) as file:

        json.dump(
            best_genome,
            file,
            indent=4
        )

    # Show graph
    plot_evolution(history)


if __name__ == "__main__":
    main()