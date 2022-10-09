from cli import *
from ImageReproducer import *

if __name__ == "__main__":
    args = generate_args()

    solution = ImageReproducer(args)

    begin = 0

    pop = solution.get_solution(begin, solution.height, solution.width)

    solution.show_solution()

    
