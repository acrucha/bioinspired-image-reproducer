import time
import cv2
import random

from math import ceil

import numpy as np
from mutations import *
from crossovers import *
from selections import *
from utils import *

def selection(population, fitness):
    new_population = roulette_selection(population, fitness)
    return new_population

def crossover(population, coord, source_img, type='one_cut'):
    
    parents = generate_parents()

    if type == 'one_cut':
        population = one_cut_crossover(population, parents)
    elif type == 'intermediate':
        population = intermediate_recombination(population, parents)
    elif type == 'two_point':
        population = two_point_ordered_crossover(population, parents, coord, source_img)
    else:
        population = average_recombination(population, parents)

    return population

def mutation(population):

    population = random_mutation(population)

    return population

def get_chromosome(coord, source_img):

    population = [[random.randint(MIN_RGB, MAX_RGB), random.randint(MIN_RGB, MAX_RGB), random.randint(MIN_RGB, MAX_RGB)].copy() for i in range(CHROMOSOMES_NUMBER)]
    score = [None] * CHROMOSOMES_NUMBER
    
    best_score = 0.0
    while(True):
        for i in range(CHROMOSOMES_NUMBER):
            score[i] = fitness(population[i], coord, source_img)
            if score[i] > best_score:
                best_score = score[i]
                best_chromosome = population[i]
                if best_score >= 0.1:
                    return best_chromosome      
        
        population = selection(population, score)
        population = crossover(population, coord, source_img)
        population = mutation(population)


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
        exec_time /= 60
        print(f'--- {"%.2f" % exec_time} minutes ---') 
    else:
        print(f'--- {"%.2f" % exec_time} seconds ---') 

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