# Bioinspired Image Reproducer

# How to install
```
pip install -r requirements/r.txt 
```

# How to run
Basic run
```
python3 main.py -f target_filename 
```

## CLI Parameters
To see the parameters and what they represent, just run: 
```
python3 main.py -h
```
or
```
python3 main.py --help
```
## Filename
### ```-f``` or ```--filename```, represents the filename of the image will be reproduced (required)
example: 1.jpg
## Population Size
### ```-p``` or ```--population-size```, represents the population size
default=10
## Type of Mutation
### ```-m``` or ```--mutation```, represents the Mutation Type
options: random, rank_based_adaptive, gaussian, triangular. default='gaussian'
## Type of Crossover/Recombination
### ```-c``` or ```--crossover```, represents the Crossover Type 
options: one_cut, two_point, intermediate, average. default='one_cut'
## Mutation Probability
### ```-M``` or ```--mutation-rate```, represents the Mutation Rate or Probability (between 0 and 1)
default=0.1
## Crossover Probability
### ```-C``` or ```--crossover-rate```, represents the Crossover Rate or Probability (between 0 and 1)
default=0.9
## Output Image Grid Size
### ```-s``` or ```--grid-size```, represents the Grid size that will be used to travel the image
Indicates the precision of the algorithm and has the number 1 as the minimum value and highest precision (more pixels). default=8
## Gaussian μ (mu)
### ```-u``` or ```--gaussian-mu```, represents the mean to be applied in the gaussian mutation 
default=2
## Gaussian σ (sigma)
### ```-d``` or ```--gaussian-sigma```, represents the standard deviation to be applied in the gaussian mutation 
default=10


