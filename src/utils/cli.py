import argparse

def generate_args():
    parser = argparse.ArgumentParser(description='CLI - Bioinspired Image Reproducer', allow_abbrev=True)

    parser.add_argument('-m', '--mutation', type=str, default='gaussian',
                        help='type of mutation (options: random, rank_based_adaptive, gaussian, triangular)')
    
    parser.add_argument('-c', '--crossover', type=str, default='intermediate',
                        help='type of crossover (options: one_cut, two_point, intermediate, average)')

    parser.add_argument('-f', '--filename', type=str, required=True,
                        help='filename of the image to be reproduced')

    parser.add_argument('-p', '--population-size', type=int, default=50,
                        help='population size')

    parser.add_argument('-M', '--mutation-rate', type=float, default=0.4,
                        help='mutation rate')

    parser.add_argument('-C', '--crossover-rate', type=float, default=0.9,
                        help='crossover rate')

    parser.add_argument('-t', '--allow-multiprocessing', type=bool, default=False,
                        help='allow multi-multiprocessing approach')

    parser.add_argument('-P', '--number-of-processes', type=int, default=5,
                        help='number of processes to be used')

    parser.add_argument('-s', '--grid-size', type=int, default=8,
                        help='grid size')                    

    parser.add_argument('-g', '--grayscale', type=bool, default=False,
                        help='generates output in grayscale mode')

    parser.add_argument('-u', '--gaussian-mu', type=int, default=2,
                        help='mu, mean to be applied in the gaussian mutation')

    parser.add_argument('-d', '--gaussian-sigma', type=int, default=10,
                        help='sigma, standard deviation to be applied in the gaussian mutation')

    args = parser.parse_args() 

    return args
