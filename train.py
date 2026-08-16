import json
import genetic
import matplotlib.pyplot as plt


def load_genome(filename="models/best_genome.json"):
    with open(filename, "r") as file:
        return json.load(file)

def plot_evolution(history):
    """
    Mostra como o fitness da população
    evoluiu ao longo das gerações.
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

    genome = load_genome()

    # Treina
    best_genome, fitness, history = genetic.evolve(
        population_size=30,
        generations=20,
        survivors_count=6,
        initial_genome=genome
    )

    print("\n==============================")
    print("TRAINING FINISHED")
    print("==============================")

    print("Best genome:")
    print(best_genome)

    print(
        f"Best fitness: {fitness:.0f}"
    )

    # Salva o genome
    with open(
        "models/best_genome.json",
        "w"
    ) as file:

        json.dump(
            best_genome,
            file,
            indent=4
        )

    # Mostra gráfico
    plot_evolution(history)


if __name__ == "__main__":
    main()