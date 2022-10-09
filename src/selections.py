import random
from utils import CHROMOSOMES_NUMBER

def roulette_selection(population, fitness):
    total = sum(fitness)
    fitness = [(i/total) for i in fitness]

    cumulative_fitness = []
    prev = 0
    for fit in fitness:
        prev += fit
        cumulative_fitness.append(prev)

    new_population = []
    for i in range(CHROMOSOMES_NUMBER):
        r = random.uniform(0,1)
        for j in range(CHROMOSOMES_NUMBER):
            if j == 0:
                if 0 <= r and r < cumulative_fitness[j]:
                    new_population.append(population[j].copy())
            else:
                if cumulative_fitness[j-1] <= r and r < cumulative_fitness[j]:
                    new_population.append(population[j].copy())

    return new_population
