import numpy as np
from genetic import Genetic
from tournament import Tournament
import math


POPULATION = 8
EPOCHS = 5
genetic = Genetic(POPULATION, 5)
iterations = int(math.log2(POPULATION))  
print(f"Iterations: {iterations} for {len(genetic.population)} chromosomes")    

for epoch in range(EPOCHS):
    # print(genetic.population) 
    tournament = Tournament(genetic.population)
    for i in range(iterations):
        tournament.create_matches(score_requisite=i)
        tournament.dummy()
        # print(tournament.scores)
    genetic.set_evaluations(tournament.scores)
    genetic.reproduction()
    input()