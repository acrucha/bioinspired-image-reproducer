import random

def one_cut_crossover(population, parents):
    for i in range(len(parents)):
        cut = random.randint(1,3)
        for k in range(cut, len(population[parents[i]])):
            population[parents[i]][k] = population[parents[(i + 1)%(i + 1)]][k]

    return population
