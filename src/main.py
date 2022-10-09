import time
import matplotlib.pyplot as plt

from PIL import Image, ImageDraw
from utils import *
from functions import *

if __name__ == "__main__":

    start_time = time.time()
    begin = 0

    filename = input("Filename: ")
    image, height, width = get_image(filename)

    im = Image.new('RGB', (width, height), 'black')
    draw = ImageDraw.Draw(im)

    pop = get_solution(image, begin, height, width, draw)

    print_execution_time(start_time)

    plt.title(f"{filename} - Output")
    plt.imshow(im)
    plt.show()
    
    im.save(f'../img/outputs/output_{filename}')  
