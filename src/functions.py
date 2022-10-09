import time
import cv2
import random

from math import ceil

import numpy as np
from mutations import *
from crossovers import *
from utils import *

def fitness(chromosome, coord, source_img):

    means = source_img[coord[1]:coord[3], coord[0]:coord[2]].mean(axis=(0,1))

    score = 0.0
    for i in range(len(chromosome)):
        score += (chromosome[i] - means[i]) * (chromosome[i] - means[i])
    
    return 1 / (1 + score)


def selection(population, probability):
    total = 0.0
    for i in range(CHROMOSOMES_NUMBER):
        total += probability[i]

    for i in range(CHROMOSOMES_NUMBER):
        probability[i] /= total

    new_population = [None] * CHROMOSOMES_NUMBER

    cumulative_probability = [None] * CHROMOSOMES_NUMBER
    cumulative_probability[0] = probability[0]
    for i in range(1,CHROMOSOMES_NUMBER):
        cumulative_probability[i] = probability[i] + cumulative_probability[i-1]

    for i in range(CHROMOSOMES_NUMBER):
        r = random.uniform(0,1)
        for j in range(CHROMOSOMES_NUMBER):
            if j == 0:
                if 0 <= r and r < cumulative_probability[j]:
                    new_population[i] = population[j].copy()
            else:
                if cumulative_probability[j-1] <= r and r < cumulative_probability[j]:
                    new_population[i] = population[j].copy()

    return new_population


def crossover(population):
    
    parents = generate_parents()

    population = one_cut_crossover(population, parents)

    return population

def mutation(population):

    population = random_mutation(population)

    return population

def get_chromosome(coord, source_img):

    population = [[random.randint(MIN_RGB, MAX_RGB), random.randint(MIN_RGB, MAX_RGB), random.randint(MIN_RGB, MAX_RGB)].copy() for i in range(CHROMOSOMES_NUMBER)]
    score = [None] * CHROMOSOMES_NUMBER
    
    best_score = 0.0
    while(best_score < 0.1):

        for i in range(CHROMOSOMES_NUMBER):
            score[i] = fitness(population[i], coord, source_img)
            if score[i] > best_score:
                best_score = score[i]
                best_chromosome = population[i]
        
        population = selection(population, score)
        population = crossover(population)
        population = mutation(population)

    return best_chromosome


def get_image(filename):
    image = cv2.imread(f'../img/{filename}')
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    height, width, _ = image.shape
    height_offset = ceil(height / GRID_SIZE) * GRID_SIZE - height
    width_offset = ceil(width / GRID_SIZE) * GRID_SIZE - width
    image = cv2.copyMakeBorder(image, 0, height_offset, 0, width_offset, cv2.BORDER_REFLECT)

    height, width, _ = image.shape
    return [image, height, width]

def print_execution_time(start_time):
    exec_time = time.time() - start_time
    if exec_time > 60:
        print(f'--- {exec_time/60} minutes ---') 
    else:
        print(f'--- {exec_time} seconds ---') 

def get_solution(image, begin, end_y, end_x, draw):
    pop = []
    for y in range(begin, end_x, GRID_SIZE):
        for x in range(begin, end_y, GRID_SIZE):
            coord = (x,y)
            print(f"Pixel #{len(pop)+1} = {coord}")
            solution = get_chromosome((x, y, x + GRID_SIZE, y + GRID_SIZE), image)
            color = (solution[0], solution[1], solution[2])
            draw.rectangle([coord, (x+GRID_SIZE, y+GRID_SIZE)], fill=color)
            pop.append(solution)
    return pop

def generate_parents():
    parents = []
    for i in range(CHROMOSOMES_NUMBER):
        r = random.uniform(0,1)
        if r < CROSSOVER_RATE:
            parents.append(i)
            
    return parents


def evaluate_executions(all_gen, all_fitness, counter, exec_time):
    mean_gen = np.average(all_gen)
    std_gen = np.std(all_gen)
    mean_fitness = np.average(all_fitness)
    std_fitness = np.std(all_fitness)
    convergences = sum(counter)
    mean_convergence = np.average(counter)
    mean_exec_time = np.average(exec_time)
    return [mean_gen, std_gen, convergences, mean_fitness, std_fitness, mean_convergence, mean_exec_time]


def print_evaluation(mean_gen, std_gen, convergences, mean_fitness, std_fitness, mean_convergence, mean_exec_time):
    print("Em que iteração o algoritmo convergiu, em média: ", round(mean_gen, 3))
    print("Desvio Padrão de em quantas iterações o algoritmo convergiu: ", round(std_gen, 3))
    print("Fitness médio alcançado nas 30 execuções : ", round(mean_fitness, 3))
    print("Desvio padrão dos Fitness alcançados nas 30 execuções: ", round(std_fitness, 3))
    print("Em quantas execuções o algoritmo convergiu: ", str(min(convergences, 30)) + "/30")
    print("Número de indivíduos que convergiram: ", convergences)
    print("Número de indivíduos que convergiram por execução, em média: ", round(mean_convergence, 3))
    print("Tempo médio de execução das 30 execuções: ", round(mean_exec_time, 3), " segundos")