import os
import json
from termcolor import colored
import time

mutations = [
    # 'random',
    # 'triangular',
    # 'rank_based_adaptive',
    'gaussian'
]

crossovers = [
    # 'one_cut',
    # 'two_point',
    'intermediate',
    # 'average'
]

crossover_rates = [
    # 0.5, 
    # 0.6, 
    # 0.8, 
    0.9
]
mutation_rates = [
    0.08,
    0.07,
    0.09,
    0.06,
    0.05,
    # 0.4, 
    # 0.3, 
    # 0.2, 
    0.1,
    # 0.8,
    # 0.5,
    # 0.6,
    # 0.7
]

pop_sizes = {
    10,
    # 20,
    # 30,
    # 40,
    # 50,
    # 60,
    # 70,
    # 80,
    # 90,
    # 100
}

story = []

def get_time(s):
    return s['Execution Time']

if __name__ == "__main__":
    # i = 0

    for j in range(1, 31):
        for m in mutations:
            for c in crossovers:
                for mr in mutation_rates:
                    for cr in crossover_rates:
                        for p in pop_sizes:
                            # i+=1
                            start_time = time.time()
                            os.system(f'python3 main.py -f 4.jpg -m {m} -c {c} -M {mr} -C {cr} -P 8 -p {p}')
                            exec_time = time.time() - start_time

                            print(f'#{j} Execution', colored('OK', 'green'))

                            story.append({
                                'Execution Nº': j,
                                'Mutation': m,
                                'Mutation Rate': mr,
                                'Crossover': c,
                                'Crossover Rate': cr,
                                'Execution Time': exec_time,
                                'Population Size': p
                            })

                            story.sort(key=get_time)
                            with open("./test/testing.json", 'w') as f:
                                json.dump(story, f, ensure_ascii=False, indent=4)
    
    

    f.close()