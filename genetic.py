from defines import *
import random
from queue import Queue

class Genetic():
    def __init__(self, population_number, epochs):
        self.population_number = population_number
        self.epochs = epochs
        self.mutation_porb = 0.1
        self.param_range = {
            'safety': (0, 10),
            'possible_safety': (0, 10),
            'threats': (-20, 0),
            'possible_threats': (-10, 0),
            'same_stones': (0, 5),
            'opponent_stones': (0, 5),
            'my_frees': (0, 2),
            'opponent_frees': (-2, 0)
        }
        self.population = []
        self.evaluations = []
        self.init_population()
    
    def init_population(self):
        for i in range(self.population_number):
            chromosome = []
            for param in self.param_range:
                chromosome.append(random.uniform(self.param_range[param][0], self.param_range[param][1]))
            self.population.append(chromosome)

    def set_evaluations(self, evaluations):
        self.evaluations = evaluations


    def reproduction(self):
        print("PARENTS: ", self.population)
        print("===================================")
        parents = []
        for chromosome, score in zip(self.population, self.evaluations):
            if score > 0:
                parents.append({'chromosome': chromosome, 'score': score})
        children = Queue()
        chromosome_len = len(parents[0]['chromosome'])
        for i in range(0, len(parents), 2):
            indexes = [i for i in range(chromosome_len)]
            random.shuffle(indexes)
            cross_point = (chromosome_len // 2) + (parents[i + 1]['score'] - parents[i]['score'])
            child_1 = [
                parents[i]['chromosome'][index] if index in indexes[:cross_point]
                else parents[i + 1]['chromosome'][index]
                for index in range(chromosome_len)
            ]
            child_2 = [
                parents[i]['chromosome'][chromosome_len - 1 - index] if index in indexes[:cross_point]
                else parents[i + 1]['chromosome'][chromosome_len - 1 - index]
                for index in range(chromosome_len - 1, -1, -1)
            ]
            # child_1 = parents[i]['chromosome'][indexes[:cross_point]] + parents[i + 1]['chromosome'][indexes[cross_point:]]
            # child_2 = parents[i]['chromosome'][indexes[:(chromosome_len-cross_point)]] + parents[i + 1]['chromosome'][indexes[(chromosome_len-cross_point):]]
            for child in [child_1, child_2]:
                if random.random() < self.mutation_porb:
                    allele = random.choice([0, 1, 2, 3])
                    child[allele] += random.uniform(-5, 5)
            children.put(child_1)
            children.put(child_2)
            i = 0
            while not children.empty():
                if self.evaluations[i] == 0:
                    chromosome = children.get()
                    self.population[i] = chromosome
                i += 1
        print(self.population)

    # def reproduction(self):
    #     parents = []
    #     for chromosome, score in zip(self.population, self.evaluations):
    #         if score > 0:
    #             parents.append({'chromosome': chromosome, 'score': score})
    #     children = Queue()
    #     for i in range(0, len(parents), 2):
    #         if parents[i]['score'] == parents[i + 1]['score']:
    #             cross_point = 2
    #         elif parents[i]['score'] > parents[i + 1]['score']:
    #             cross_point = 3
    #         else:
    #             cross_point = 1
    #         child_1 = parents[i]['chromosome'][:cross_point] + parents[i + 1]['chromosome'][cross_point:]
    #         child_2 = parents[i]['chromosome'][:(4-cross_point)] + parents[i + 1]['chromosome'][(4-cross_point):]
    #         for child in [child_1, child_2]:
    #             if random.random() < self.mutation_porb:
    #                 allele = random.choice([0, 1, 2, 3])
    #                 child[allele] += random.uniform(-5, 5)
    #         children.put(child_1)
    #         children.put(child_2)
    #     i = 0
    #     while not children.empty():
    #         if self.evaluations[i] == 0:
    #             chromosome = children.get()
    #             self.population[i] = chromosome
    #         i += 1
    
    def save_weights(self):
        with open("genetic.txt", "w") as f:
            for chromosome, score in zip(self.population, self.evaluations):
                f.write(f"{chromosome} SCORE: {score}\n")
