# genetic.py

import random


# ============================================================
# GENOME
# ============================================================

def create_genome():
    """
    Cria um indivíduo da população.

    O genome representa uma estratégia para avaliar um board.

    Cada número é um peso que determina o quanto uma
    característica do board importa para o agente.

    Exemplo:

        [
            10.5,  # empty cells
            1.2,   # max tile
            4.8,   # monotonicity
            2.1    # smoothness
        ]

    O algoritmo genético vai tentar descobrir quais valores
    produzem as melhores partidas.
    """

    return [
        random.uniform(0, 10),  # empty_cells_weight
        random.uniform(0, 10),  # max_tile_weight
        random.uniform(0, 10),  # monotonicity_weight
        random.uniform(0, 10),  # smoothness_weight
    ]


# ============================================================
# POPULATION
# ============================================================

def create_population(size):
    """
    Cria a população inicial.

    Uma população é simplesmente um conjunto de genomes.

    Exemplo:

        population = [
            genome_1,
            genome_2,
            genome_3,
            ...
        ]

    Cada genome representa uma estratégia diferente.
    """

    return [create_genome() for _ in range(size)]


# ============================================================
# FITNESS
# ============================================================

def fitness(genome):
    """
    Mede o quão bom é um genome.

    Quanto maior o fitness, melhor é a estratégia.

    IMPORTANTE:

    Aqui ainda não sabemos o fitness.

    Precisaremos colocar esse genome para jogar 2048
    e medir seu desempenho.

    Futuramente algo como:

        fitness =
            score médio
            + bônus por alcançar tiles maiores
            + outros critérios

    Por enquanto é apenas um placeholder.
    """

    return 0


# ============================================================
# SELECTION
# ============================================================

def selection(population):
    """
    Escolhe os melhores indivíduos da população.

    A ideia é:

        população
            ↓
        avaliar fitness
            ↓
        selecionar melhores
            ↓
        usar os melhores para gerar a próxima geração

    Indivíduos com fitness maior terão maior chance
    de continuar para a próxima geração.
    """

    return population


# ============================================================
# CROSSOVER
# ============================================================

def crossover(genome1, genome2):
    """
    Combina dois genomes para criar um novo genome.

    Exemplo:

        Parent 1:
        [10, 2, 8, 3]

        Parent 2:
        [4, 9, 1, 7]

        Filho:
        [10, 9, 8, 7]

    A ideia é que características boas dos pais
    possam ser combinadas no filho.
    """

    return genome1


# ============================================================
# MUTATION
# ============================================================

def mutation(genome):
    """
    Faz pequenas alterações aleatórias em um genome.

    Exemplo:

        antes:
        [10, 2, 8, 3]

        depois:
        [10, 2.7, 8, 3]

    A mutação introduz diversidade na população.

    Sem mutação, a população pode convergir muito cedo
    para uma estratégia ruim.
    """

    return genome