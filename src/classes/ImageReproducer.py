import cv2
import random

from math import ceil
from PIL import Image, ImageDraw
from matplotlib import pyplot as plt
from termcolor import colored
from multiprocessing import Process, Manager
from utils.mutations import *
from utils.crossovers import *
from utils.selections import *
from utils.utils import *

class ImageReproducer():
    
    def __init__(self, args):
        self.filename = args.filename
        self.GRID_SIZE = args.grid_size

        self.image, self.height, self.width = self.get_image()
        self.im = Image.new('RGB', (self.width, self.height), 'black')
        self.draw = ImageDraw.Draw(self.im)

        self.mutation_type = args.mutation
        self.MUTATION_RATE = args.mutation_rate 

        self.crossover_type = args.crossover
        self.CROSSOVER_RATE = args.crossover_rate
        self.population_size = args.population_size
        
        self.test = args.test

        self.number_of_processes = args.number_of_processes if args.number_of_processes <= 8 else 8

        self.GAUSS_MU = args.gaussian_mu
        self.GAUSS_SIGMA = args.gaussian_sigma

        self.n_pixel = int((self.width/self.GRID_SIZE)*(self.height/self.GRID_SIZE))
        self.n_individuals = self.population_size * self.n_pixel

        self.all_fitness = []
        self.all_generations = []
        self.all_exec_time = []
        self.all_convergence = []
        self.bests = []
        
        self.start_time = time.time()

    def get_image(self):
        image = cv2.imread(f'../img/{self.filename}')
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        height, width, _ = image.shape
        height_offset = ceil(height / self.GRID_SIZE) * self.GRID_SIZE - height
        width_offset = ceil(width / self.GRID_SIZE) * self.GRID_SIZE - width
        image = cv2.copyMakeBorder(image, 0, height_offset, 0, width_offset, cv2.BORDER_REFLECT)

        height, width, _ = image.shape
        return [image, height, width]

    def selection(self, population, fitness):
        new_population = roulette_selection(population, fitness, self.population_size)
        return new_population

    def crossover(self, population, coord):
        
        parents = self.generate_parents()

        if self.crossover_type == 'one_cut':
            population = one_cut_crossover(population, parents)
        elif self.crossover_type == 'intermediate':
            population = intermediate_recombination(population, parents, self.population_size)
        elif self.crossover_type == 'two_point':
            population = two_point_ordered_crossover(population, parents, coord, self.image)
        elif self.crossover_type == 'average':
            population = average_recombination(population, parents)

        return population

    def mutation(self, population, coord):

        if self.mutation_type == 'random':
            population = random_mutation(population, self.MUTATION_RATE)
        elif self.mutation_type == 'triangular':
            population = triangular_mutation(population, self.MUTATION_RATE)
        elif self.mutation_type == 'rank_based_adaptive':
            population = rank_based_adaptive_mutation(
                            population, 
                            self.MUTATION_RATE, 
                            self.population_size, 
                            self.image, 
                            coord
                        )
        elif self.mutation_type == 'gaussian':
            population = gaussian_mutation(
                            population, 
                            self.MUTATION_RATE, 
                            self.GAUSS_MU, 
                            self.GAUSS_SIGMA
                        )

        return population

    def get_chromosome(self, coord):
        population = [[random.randint(MIN_RGB, MAX_RGB), random.randint(MIN_RGB, MAX_RGB), random.randint(MIN_RGB, MAX_RGB)].copy() for i in range(self.population_size)]
        fitness = [None] * self.population_size

        bests = []
        
        best_chromosome = [0.0, []]
        generation = 1
        start_time = time.time()
        while(True):

            fitness, best_chromosome = get_population_fitness(
                                        self.population_size, 
                                        self.image, 
                                        coord, 
                                        population, 
                                        fitness, 
                                        best_chromosome
                                    )      
            bests.append(best_chromosome[0])
            if best_chromosome[0] >= TARGET_FITNESS:
                exec_time = time.time() - start_time
                return [best_chromosome[1], fitness, generation, exec_time, bests]
            population = self.selection(population, fitness)
            population = self.crossover(population, coord)
            population = self.mutation(population, coord)

            generation+=1
    
    def get_solution(self,begin):
        pixels = []
        for x in range(begin, self.width, self.GRID_SIZE):
            for y in range(begin, self.height, self.GRID_SIZE):  
                pixels.append((x,y))   

        n = self.number_of_processes
        list = self.generate_list(pixels, n)

        manager = Manager()
        return_list = manager.list()
        result = [Process(target=self.get_pixels_solution,args=(list[i],return_list)) for i in range(n)]

        for results in result:
            results.start()

        for results in result:
            results.join()        
            
        for color, pixel, fitness, generation, exec_time, best in return_list:
            self.draw.rectangle([pixel, (pixel[0]+self.GRID_SIZE, pixel[1]+self.GRID_SIZE)], fill=color)
            self.all_fitness.append(np.average(fitness))
            count = count_convergence(fitness)
            self.bests.append(best)
            self.all_convergence.append(count)
            self.all_generations.append(generation)
            self.all_exec_time.append(exec_time)

        

    def generate_list(self, pixels, n):
        list = []
        begin = 0
        for i in range(1, n+1):
            end = (len(pixels)*i)/n
            list.append(pixels[int(begin):int(end)])
            begin = end
        return list
        
    def get_pixels_solution(self, a, return_list):   
        pop = []
        for (x,y) in a :                    
            coord = (x,y)
            print(f"Pixel #{len(pop)+1} = {coord}")
            solution, fitness, generation, exec_time, bests = self.get_chromosome((x, y, x + self.GRID_SIZE, y + self.GRID_SIZE))
            color = (solution[0], solution[1], solution[2])
            pop.append(solution)
            return_list.append((color, coord, fitness, generation, exec_time, bests))
            print ("\033[A                             \033[A")
        

    def generate_parents(self):
        parents = []
        for i in range(self.population_size):
            r = random.uniform(0,1)
            if r < self.CROSSOVER_RATE:
                parents.append(i)
                
        return parents

    def show_solution(self):

        [
            mean_gen, 
            std_gen, 
            convergences, 
            mean_fitness, 
            std_fitness, 
            mean_convergence, 
            mean_exec_time,
            mean_bests
        ] = evaluate_executions(
            self.all_generations, 
            self.all_fitness, 
            self.all_convergence, 
            self.all_exec_time,
            self.bests
        )

        self.save_fitness_graph(mean_bests)

        print_evaluation(
            mean_gen, std_gen, convergences, 
            mean_fitness, std_fitness, mean_convergence, 
            mean_exec_time, self.n_pixel, self.n_individuals
        )

        print(colored("Done!", 'green',  attrs=['bold']))
        print_execution_time(self.start_time)
        self.im.save(f'../img/outputs/output_grid[{self.GRID_SIZE}]_{self.filename}')  

        if not self.test:
            plt.title(f"{self.filename} - Output - Grid size = {self.GRID_SIZE}")
            plt.axis(False)
            plt.imshow(self.im)
            plt.show()

    def save_fitness_graph(self, mean_bests):
        f0, f1 = self.filename.split('.')
        plt.plot([i for i in range(1, mean_bests.size+1)], mean_bests)
        plt.xlabel("Generation")
        plt.ylabel("Fitness")
        plt.savefig(f"../img/graphs/fitnessGraph_grid[{self.GRID_SIZE}]_{f0}.png")