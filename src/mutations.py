import random
from utils import *

def random_mutation(population):
    for chromosome in population:
        for move in range(len(chromosome)):
            r = random.uniform(0, 1)
            if r < MUTATION_RATE:
                chromosome[move] = random.randint(MIN_RGB, MAX_RGB)
    return population
