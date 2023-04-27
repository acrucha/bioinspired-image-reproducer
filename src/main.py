from utils.cli import *
from classes.ImageReproducer import *


if __name__ == "__main__":
    args = generate_args()

    solution = ImageReproducer(args)

    begin = 0
    solution.get_solution(begin)

    solution.show_solution()

    
