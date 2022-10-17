import os
import json
from matplotlib import pyplot as plt
import numpy as np
from termcolor import colored
import time
from tests.utils.test_utils import *
import sys

def get_time(s):
    return s['Execution Time']

def run(file, j, mr, cr, x, g, fi=0.01):

    with open(f"{PATH}testing-{x}.json", 'r') as f:
        list = json.load(f)

    start_time = time.time()
    os.system(f'python3 main.py -f {file} -s {g} -M {mr} -C {cr} -P 8 -F {fi} --test -x {j}')
    exec_time = time.time() - start_time

    print(f'#{j} Execution', colored('OK', 'green',  attrs=['bold']))

    list.append({
        'Execution Nº': j,
        'Mutation Rate': mr,
        'Crossover Rate': cr,
        'Execution Time': exec_time,
        'Grid Size': g,
        'Target Fitness': fi,
        'File': file
    })

    list.sort(key=get_time)
    with open(f"{PATH}testing-{x}.json", 'w') as f:
        json.dump(list, f, ensure_ascii=False, indent=4)

    f.close()

def test_crossovers(crossover_rates, m, f):
    for j in range(1, 31):
        for cr in crossover_rates:
            run(f, j, m, cr, "crossover")

def test_mutations(mutation_rates, c, f):
    for j in range(1, 31):
        for mr in mutation_rates:
            run(f, j, mr, c, "mutation")

def generate_means(rates, test, b, e, i):
    list = []

    with open(f"{PATH}testing-{test}.json", 'r') as f:
        list = json.load(f)
    f.close()

    means = {}
    r = map[test]

    for rate in rates:
        s = []  
        for m in list:
            if m[r] == rate:
                s.append(m["Execution Time"]) 
        means[rate] = np.average(s)
        print(f"{rate}: mean = {means[rate]}")
    
    plots(means, r, test, b, e, i)

def plots(means, r, file, b, e, i):
    plt.plot(means.keys(), means.values())
    plt.xlabel(r)
    plt.ylabel("Execution Time (segundos)")
    plt.yticks(np.arange(b, e, i))
    plt.savefig(f"../img/graphs/{file}-graph.png")
    plt.clf()

def generate_gif(frame_folder):
    frames = [Image.open(image) for image in sorted(glob.glob(f"{frame_folder}/*.jpg"), reverse=True)]
    frame_one = frames[0]
    frame_one.save(f"{frame_folder}/story.gif", format="GIF", append_images=frames[1:],
               save_all=True, duration=200, loop=0)

def plot_target_fitness(gridsize):
    with open(f"{PATH}testing-fitness.json", 'r') as f:
        list = json.load(f)
    f.close()
    times = []
    fits = []
    for i in list:
        if i["Grid Size"] == gridsize:
            times.append(i["Execution Time"]/60)
            fits.append(i["Target Fitness"]) 

    plt.plot(fits, times)
    plt.xlabel("Target Fitness")
    plt.ylabel("Execution Time (minutos)")
    plt.savefig(f"../img/graphs/fitness-target-graph.png")

if __name__ == "__main__":

    f, m, c, g, type, r = sys.argv[1:6]

    if type == "mutation":
        test_mutations(mutation_rates, c, f)
    elif type == "crossover":
        test_crossovers(crossover_rates, c, f)
    elif type == "mean":
        b, e, i = input("Range:")
        generate_means(map_rate[r], r, b, e, i)
    elif type == "gif":
        generate_gif(f'../img/outputs/{f}')
    elif type == 'fit':
        plot_target_fitness(g) 