
import glob
from PIL import Image


mutations = [
    'random',
    'triangular',
    'rank_based_adaptive',
    'gaussian'
]

crossovers = [
    'one_cut',
    'two_point',
    'intermediate',
    'average'
]

crossover_rates = [
    0.6, 
    0.7, 
    0.8, 
    0.9
]
mutation_rates = [
    0.05,
    0.09,
    0.1,
    0.2, 
]

pop_sizes = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

processes = [8,7,6,5,4,3,2,1]

grid = [i for i in range(1, 11)]

map = {
    'mutation': "Mutation Rate",
    'crossover': "Crossover Rate",
    'processing': "Number of Processes",
    'grid': "Grid Size",
    'fitness': "Target Fitness"
}

map_rate = {
    "mutation": mutation_rates,
    "crossover": crossover_rates,
    "processing": processes
}

PATH = './tests/'

fit = [1e-1, 1e-2, 6e-3, 1e-3, 6e-4, 2e-4, 1e-4, 5e-5, 1e-6, 5e-7, 3e-7, 1e-7, 8e-8, 5e-9, 3e-9, 1e-9, 8e-10]

