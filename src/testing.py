import os
import json
from matplotlib import pyplot as plt
import numpy as np
from termcolor import colored
import time
from tests.utils.test_utils import *

def get_time(s):
    return s['Execution Time']

def run(file, j, mr, cr, x, g):

    with open(f"./test/testing-{x}.json", 'r') as f:
        list = json.load(f)

    start_time = time.time()
    os.system(f'python3 main.py -f {file} -s {g} -M {mr} -C {cr} -P 8 --test')
    exec_time = time.time() - start_time

    print(f'#{j} Execution', colored('OK', 'green',  attrs=['bold']))

    list.append({
        'Execution Nº': j,
        'Mutation Rate': mr,
        'Crossover Rate': cr,
        'Execution Time': exec_time,
        'Grid Size': g
    })

    list.sort(key=get_time)
    with open(f"{PATH}testing-{x}.json", 'w') as f:
        json.dump(list, f, ensure_ascii=False, indent=4)

    f.close()

def test_crossovers(crossover_rates, f):
    for j in range(1, 31):
        for cr in crossover_rates:
            run(f, j, 0.09, cr, "crossover")

def test_mutations(mutation_rates, f):
    for j in range(1, 31):
        for mr in mutation_rates:
            run(f, j, mr, 0.9, "mutation")

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

if __name__ == "__main__":
    
    generate_means(crossover_rates, 'crossover', 22, 23, 0.1)
    generate_means(mutation_rates, 'mutation', 16, 31, 4)
    # generate_means(processes, 'processing', 3, 15, 2)
