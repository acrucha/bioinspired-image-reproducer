import os
import time
import numpy as np
from termcolor import colored


MAX_RGB = 255
MIN_RGB = 0
CHROMOSOME_SIZE = 3
RATIO = 4

def fitness(chromosome, coord, source_img):

    means = source_img[coord[1]:coord[3], coord[0]:coord[2]].mean(axis=(0,1))

    score = 0.0
    for i in range(len(chromosome)):
        score += (chromosome[i] - means[i]) * (chromosome[i] - means[i])
    
    return 1 / (1 + score)

def count_convergence(fitness, TARGET_FITNESS):
    count = 0
    for i in fitness:
        if i >= TARGET_FITNESS:
            count+=1
    return count

def print_execution_time(start_time):
    exec_time = time.time() - start_time
    if exec_time > 60:
        exec_time /= 60
        print(colored(f'--- {"%.2f" % exec_time} minutos ---', attrs=['bold'])) 
    else:
        print(colored(f'--- {"%.2f" % exec_time} segundos ---', attrs=['bold'])) 

def evaluate_executions(all_gen, all_fitness, all_convergence, exec_time, bests):
    mean_gen = np.average(all_gen)
    reshaped_bests = reshape(mean_gen, bests)
    mean_bests = np.average(reshaped_bests, axis=1)
    std_gen = np.std(all_gen)
    mean_fitness = np.average(all_fitness)
    std_fitness = np.std(all_fitness)
    convergences = np.sum(all_convergence)
    mean_convergence = np.average(all_convergence)
    mean_exec_time = np.average(exec_time)
    return [mean_gen, std_gen, convergences, mean_fitness, std_fitness, mean_convergence, mean_exec_time, mean_bests]

def reshape(mean_gen, bests):
    reshaped = []
    for i in range(int(mean_gen)):
        aux = []
        for j in bests:
            if i >= len(j):
                aux.append(j[-1])
            else:
                aux.append(j[i])
        reshaped.append(aux)
    return reshaped

def check_path(f0):
    if not os.path.exists(f'../img/outputs/{f0}'):
        os.makedirs(f'../img/outputs/{f0}')


def print_evaluation(mean_gen, std_gen, convergences, mean_fitness, std_fitness, mean_convergence, mean_exec_time, n_pixel, n_individuals):
    print(f"Em quantas execuções o algoritmo convergiu: {colored(min(convergences, n_pixel), 'green',  attrs=['bold'])}/{colored(n_pixel, 'green',  attrs=['bold'])}")
    print(f"Número de indivíduos que convergiram no total: {colored(convergences, 'green',  attrs=['bold'])}/{colored(n_individuals, 'green',  attrs=['bold'])}")
    print(f"Em que iteração o algoritmo convergiu, em média: {colored(round(mean_gen, 3), 'green',  attrs=['bold'])}")
    print(f"Desvio Padrão de em quantas iterações o algoritmo convergiu: {colored(round(std_gen, 3), 'green',  attrs=['bold'])}")
    print(f"Fitness médio alcançado em todos os pixels: {colored(round(mean_fitness, 5), 'green',  attrs=['bold'])}")
    print(f"Desvio padrão dos Fitness alcançados em todos os pixels: {colored(round(std_fitness, 5), 'green',  attrs=['bold'])}")
    print(f"Número de indivíduos que convergiram por execução, em média: {colored(round(mean_convergence, 3), 'green',  attrs=['bold'])}")
    print(f"Tempo médio de execução em cada pixel: {colored(round(mean_exec_time, 3), 'green',  attrs=['bold'])} segundos")
    print(f"A quantidade de pixels na imagem é de: {colored(n_pixel, 'green',  attrs=['bold'])} pixels")

def get_fit(p):
    return p[1]

def sort_by_fitness(pop, fitness):
    pop_with_fitness = []
    j = 0
    for i in pop:
        pop_with_fitness.append([i, fitness[j]])
        j+=1
    
    pop_with_fitness.sort(key=get_fit, reverse=True)

    new_population = []
    for chromosome in pop_with_fitness:
        new_population.append(chromosome[0])

    return new_population

def get_population_fitness(CHROMOSOMES_NUMBER, image, coord, population, score, best_chromosome):
    for i in range(CHROMOSOMES_NUMBER):
        score[i] = fitness(population[i], coord, image)
        if score[i] > best_chromosome[0]:
            best_chromosome = [score[i], population[i]]
    return [score, best_chromosome]