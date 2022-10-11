from asyncio import sleep
import cv2
import random

from math import ceil
from PIL import Image, ImageDraw
from matplotlib import pyplot as plt
from numpy import size
from termcolor import colored
from multiprocessing import Lock, Process,Pool
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
        self.CHROMOSOMES_NUMBER = args.population_size

        self.allow_threading = args.allow_threading
        self.grayscale = args.grayscale
        self.number_of_threads = args.number_of_threads

        self.GAUSS_MU = args.gaussian_mu
        self.GAUSS_SIGMA = args.gaussian_sigma

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
        new_population = roulette_selection(population, fitness, self.CHROMOSOMES_NUMBER)
        return new_population

    def crossover(self, population, coord):
        
        parents = self.generate_parents()

        if self.crossover_type == 'one_cut':
            population = one_cut_crossover(population, parents)
        elif self.crossover_type == 'intermediate':
            population = intermediate_recombination(population, parents, self.CHROMOSOMES_NUMBER)
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
                            self.CHROMOSOMES_NUMBER, 
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
        population = [[random.randint(MIN_RGB, MAX_RGB), random.randint(MIN_RGB, MAX_RGB), random.randint(MIN_RGB, MAX_RGB)].copy() for i in range(self.CHROMOSOMES_NUMBER)]
        score = [None] * self.CHROMOSOMES_NUMBER
        
        best_chromosome = [0.0, []]
        while(True):

            score, best_chromosome = get_population_fitness(
                                        self.CHROMOSOMES_NUMBER, 
                                        self.image, 
                                        coord, 
                                        population, 
                                        score, 
                                        best_chromosome
                                    )      

            if best_chromosome[0] >= 0.1:
                return best_chromosome[1]
            population = self.selection(population, score)
            population = self.crossover(population, coord)
            population = self.mutation(population, coord)
    
    def get_solution(self,begin, end_y, end_x):
        vetor = []
        with Pool(4) as pool:
            for x in range(begin, end_x, self.GRID_SIZE):
                for y in range(begin, end_y, self.GRID_SIZE):  
                    vetor.append((x,y))
            
            for result in pool.starmap(self.get_task,vetor):
                self.draw.rectangle([result[1], (x+self.GRID_SIZE, y+self.GRID_SIZE)], fill=result[0])
    def get_task(self, x,y):
        
        pop = []    
        # for y in range(begin, end_y, self.GRID_SIZE):
        #     for x in range(begin, end_x, self.GRID_SIZE):                    
        coord = (x,y)
        print(f"Pixel #{len(pop)+1} = {coord}")
        solution = self.get_chromosome((x, y, x + self.GRID_SIZE, y + self.GRID_SIZE))
        color = (solution[0], solution[1], solution[2])
        pop.append(solution)
        print ("\033[A                             \033[A")
        
        return [color,coord]


    def generate_parents(self):
        parents = []
        for i in range(self.CHROMOSOMES_NUMBER):
            r = random.uniform(0,1)
            if r < self.CROSSOVER_RATE:
                parents.append(i)
                
        return parents

    def show_solution(self):

        print(colored("Done!", 'green'))
        print_execution_time(self.start_time)

        self.im.save(f'../img/outputs/output_grid[{self.GRID_SIZE}]_{self.filename}')  
    
        plt.title(f"{self.filename} - Output - Grid size = {self.GRID_SIZE}")
        plt.axis(False)
        plt.imshow(self.im)
        plt.show()
        