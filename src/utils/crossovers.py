import random

import numpy as np

from utils.utils import *


def one_cut_crossover(population, parents):
    for i in range(len(parents)):
        cut = random.randint(1,3)
        for k in range(cut, len(population[parents[i]])):
            population[parents[i]][k] = population[parents[(i + 1)%(i + 1)]][k]

    return population

def intermediate_recombination(population, parents):
    for i in range(0, len(parents)-1, 2):
        parent1 = population[parents[i]]
        parent2 = population[parents[i+1]]
        child1 = []
        child2 = []
        for g in range(CHROMOSOME_SIZE):
            ratio = random.randint(0, RATIO)
            child1.append(parent1[g] + ratio * (parent2[g] - parent1[g]))
            ratio = random.randint(0, RATIO)
            child2.append(parent2[g] + ratio * (parent1[g] - parent2[g]))

        population.append(child1)
        population.append(child2)

    return population

def average_recombination(population, parents):
    parents = random.sample(parents, len(parents)) 
    for i in range(0, len(parents)-1):
        parent1 = population[parents[i]]
        parent2 = population[parents[i+1]]

        child = []
        for j in range(CHROMOSOME_SIZE):
            avg = [np.mean([parent1[j], parent2[j]])]
            child.append(avg)

        population.append(child)
    return population

def two_point_ordered_crossover(population, parents, coord, source_img):
    
    for i in range(0, len(parents)-1, 2):
        parent1 = population[parents[i]]
        parent2 = population[parents[i+1]]

        children = []
        fit = []
        for j in range(3):
            r1, r2, r3 = random.sample([0,1,2], 3)

            child1 = [parent2[r1], parent1[r2], parent2[r3]]
            child2 = [parent1[r1], parent2[r2], parent1[r3]]
            
            children.append(child1)
            children.append(child2)
            
            fit.append(fitness(child1, coord, source_img))
            fit.append(fitness(child2, coord, source_img))

        children_with_fitness = sort_by_fitness(children, fit)

        for j in range(3):
            c = children_with_fitness[j][0]
            population.append(c)
            
    return population

    
def getFit(p):
    return p[1]

def sort_by_fitness(parents_choice, fitness):
    parents_with_fitness = []
    j = 0
    for i in parents_choice:
        parents_with_fitness.append([i, fitness[j]])
        j+=1
    
    parents_with_fitness.sort(key=getFit, reverse=True)
    return parents_with_fitness