import random

from utils.utils import *


def mutate_chromosome(chromosome, mutation_rate, GAUSS_MU=2, GAUSS_SIGMA=10, type='random'):
    for i in range(len(chromosome)):
        r = random.uniform(0, 1)
        if r < mutation_rate:
            if type == 'random':
                chromosome[i] = random.randint(MIN_RGB, MAX_RGB)
            elif type == 'gaussian':
                chromosome[i] = gaussian(chromosome[i], GAUSS_MU, GAUSS_SIGMA)
            elif type == 'triangular':
                chromosome[i] = triangular(chromosome[i])
    return chromosome

def gaussian_mutation(population, mutation_rate, GAUSS_MU, GAUSS_SIGMA):
    for i in range(len(population)):
        population[i] = mutate_chromosome(
                            population[i], 
                            mutation_rate, 
                            GAUSS_MU, 
                            GAUSS_SIGMA,
                            type='gaussian'
                        )
    return population

def gaussian(gene, GAUSS_MU, GAUSS_SIGMA):
    gene += random.gauss(GAUSS_MU, GAUSS_SIGMA)
    gene = abs(int(gene))
    return gene

def triangular_mutation(population, mutation_rate):
    for i in range(len(population)):
        population[i] = mutate_chromosome(population[i], mutation_rate, type='triangular')
    return population

def triangular(gene):
    gene = random.triangular(MIN_RGB, MAX_RGB, gene)
    return int(gene)

def random_mutation(population, mutation_rate):
    for i in range(len(population)):
        population[i] = mutate_chromosome(population[i], mutation_rate)
    return population

def rank_based_adaptive_mutation(population, mutation_rate, CHROMOSOMES_NUMBER, image, coord):
    fitness, _ = get_population_fitness(
        CHROMOSOMES_NUMBER, 
        image, 
        coord, 
        population, 
        [None] * CHROMOSOMES_NUMBER,
        [0.0, []] 
    )
    population = sort_by_fitness(population, fitness)
    new_population = []
    rank = 1
    for chromosome in population:
        adaptive_mutation_rate = mutation_rate * (1 - ((rank - 1)/(CHROMOSOMES_NUMBER - 1)))
        chromosome = mutate_chromosome(chromosome, adaptive_mutation_rate, type='gaussian')
        new_population.append(chromosome)
        rank+=1

    return new_population