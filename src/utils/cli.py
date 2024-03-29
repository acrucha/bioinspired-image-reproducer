import argparse
from random import randint
import random

def generate_args():
    parser = argparse.ArgumentParser(description='CLI - Bioinspired Image Reproducer', allow_abbrev=True)

    parser.add_argument('-m', '--mutation', type=str, default='gaussian',
                        help='type of mutation (options: random, rank_based_adaptive, gaussian, triangular)')
    
    parser.add_argument('-c', '--crossover', type=str, default='intermediate',
                        help='type of crossover (options: one_cut, two_point, intermediate, average)')

    parser.add_argument('-f', '--filename', type=str, required=True,
                        help='filename of the image to be reproduced')

    parser.add_argument('-p', '--population-size', type=int, default=10,
                        help='population size')

    parser.add_argument('-M', '--mutation-rate', type=float, default=0.2,
                        help='mutation rate')

    parser.add_argument('-C', '--crossover-rate', type=float, default=0.8,
                        help='crossover rate')

    parser.add_argument('-F', '--target-fitness', type=float, default=0.1,
                        help='target fitness')

    parser.add_argument('-P', '--number-of-processes', type=int, default=4,
                        help='number of processes to be used (max = 8)')

    parser.add_argument('-s', '--grid-size', type=int, default=8,
                        help='grid size')                    

    parser.add_argument('-t', '--test', action='store_true',
                        help='generates output in test mode (without output image plot)')

    parser.add_argument('-u', '--gaussian-mu', type=int, default=2,
                        help='mu, mean to be applied in the gaussian mutation')

    parser.add_argument('-d', '--gaussian-sigma', type=int, default=10,
                        help='sigma, standard deviation to be applied in the gaussian mutation')
    
    parser.add_argument('-x', '--sequence-number', type=str, default=random.randint(0,20))

    args = parser.parse_args() 

    return args
