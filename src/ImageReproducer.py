import cv2
import random

from math import ceil
from PIL import Image, ImageDraw
from matplotlib import pyplot as plt


from mutations import *
from crossovers import *
from selections import *
from utils import *

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
            population = intermediate_recombination(population, parents)
        elif self.crossover_type == 'two_point':
            population = two_point_ordered_crossover(population, parents, coord, self.image)
        else:
            population = average_recombination(population, parents)

        return population

    def mutation(self, population):

        if self.mutation_type == 'random':
            population = random_mutation(population, self.MUTATION_RATE)

        return population

    def get_chromosome(self, coord):

        population = [[random.randint(MIN_RGB, MAX_RGB), random.randint(MIN_RGB, MAX_RGB), random.randint(MIN_RGB, MAX_RGB)].copy() for i in range(self.CHROMOSOMES_NUMBER)]
        score = [None] * self.CHROMOSOMES_NUMBER
        
        best_score = 0.0
        while(True):
            for i in range(self.CHROMOSOMES_NUMBER):
                score[i] = fitness(population[i], coord, self.image)
                if score[i] > best_score:
                    best_score = score[i]
                    best_chromosome = population[i]
                    if best_score >= 0.1:
                        return best_chromosome      
            
            population = self.selection(population, score)
            population = self.crossover(population, coord)
            population = self.mutation(population)

    def get_solution(self, begin, end_y, end_x):
        pop = []
        for y in range(begin, end_x, self.GRID_SIZE):
            for x in range(begin, end_y, self.GRID_SIZE):
                coord = (x,y)
                print(f"Pixel #{len(pop)+1} = {coord}")
                solution = self.get_chromosome((x, y, x + self.GRID_SIZE, y + self.GRID_SIZE))
                color = (solution[0], solution[1], solution[2])
                self.draw.rectangle([coord, (x+self.GRID_SIZE, y+self.GRID_SIZE)], fill=color)
                pop.append(solution)
        
        return pop

    def generate_parents(self):
        parents = []
        for i in range(self.CHROMOSOMES_NUMBER):
            r = random.uniform(0,1)
            if r < self.CROSSOVER_RATE:
                parents.append(i)
                
        return parents

    def show_solution(self):
        print_execution_time(self.start_time)

        self.im.save(f'../img/outputs/output_{self.filename}')  
    
        plt.title(f"{self.filename} - Output")
        plt.imshow(self.im)
        plt.show()
        