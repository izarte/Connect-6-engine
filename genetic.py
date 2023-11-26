from defines import *
import random
from queue import Queue
import csv

class Genetic():
    def __init__(self, population_number, epochs, file=None):
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
        self.init_population(file)
    
    def init_population(self, file):
        if file != None:
            with open(file, mode='r') as file:
                reader = csv.reader(file)
                # Skip the header row
                header = next(reader)
                for row in reader:
                    chromosome = [float(v) for v in row[:-1]]
                    self.population.append(chromosome)
        else:
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
    
    def save_weights(self):
        with open("genetic.csv", mode='w', newline='') as f:
            writer = csv.writer(f)
            
            # Write the header
            writer.writerow(["safety", "possible_safety", "threats", "possible_threats", "same_stones", "opponent_stones", "my_frees", "opponent_frees", "score"])
            
            # Write data rows
            for chromosome, score in zip(self.population, self.evaluations):
                # Convert the chromosome list to a comma-separated string
                writer.writerow([*chromosome, score])
