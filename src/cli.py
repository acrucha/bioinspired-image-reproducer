import argparse


def generate_args():
    parser = argparse.ArgumentParser(description='CLI - Bioinspired Image Reproducer', allow_abbrev=True)

    parser.add_argument('-m', '--mutation', type=str, default='random',
                        help='type of mutation (options: random)')
    
    parser.add_argument('-c', '--crossover', type=str, default='one_cut',
                        help='type of crossover (options: one_cut, intermediate, average)')

    parser.add_argument('-f', '--filename', type=str, required=True,
                        help='filename of the image to be reproduced')

    parser.add_argument('-p', '--population-size', type=int, default=50,
                        help='population size')

    parser.add_argument('-M', '--mutation-rate', type=float, default=0.2,
                        help='mutation rate')

    parser.add_argument('-C', '--crossover-rate', type=float, default=0.9,
                        help='crossover rate')

    parser.add_argument('-t', '--allow-threading', type=bool, default=False,
                        help='allow multi-threading approach')

    parser.add_argument('-T', '--number-of-threads', type=int, default=5,
                        help='number of threads to be used')

    parser.add_argument('-s', '--grid-size', type=int, default=8,
                        help='grid size')                    

    parser.add_argument('-g', '--grayscale', type=bool, default=False,
                        help='generates output in grayscale mode')

    args = parser.parse_args() 

    return args
