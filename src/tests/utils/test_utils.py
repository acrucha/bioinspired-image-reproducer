
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

exec_times_processes = {
    1: 26.96,
    2: 22.23,
    3: 17.99,
    4: 9.87,
    5: 8.73,
    6: 6.62,
    7: 6.67,
    8: 6.68,
}

grid = [i for i in range(1, 11)]

map = {
    'mutation': "Mutation Rate",
    'crossover': "Crossover Rate",
    'processing': "Number of Processes",
    'grid': "Grid Size"
}

PATH = './tests/'