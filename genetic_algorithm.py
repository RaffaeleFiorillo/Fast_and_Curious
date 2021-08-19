import random
import pygame
import math
import game_classes


class Individual:
    def __init__(self, input_number, name, mc):
        self.name = name
        self.inputs = input_number
        self.weights = []
        self.bias = []
        self.mutation_chance = mc
        self.fitness = 0
        self.time_alive = 0
        self.parts = 0

    def fitness_level(self):
        print(self.parts, self.time_alive, sep=" | ")
        self.fitness = self.parts * 2 + self.time_alive * 0.8

    def save_existence(self):
        file = open("parameters/Current_generation.txt", "a")
        file.write(f"F:{self.fitness};W:{self.weights};B:{self.bias}\n")
        file.close()

    def get_wb(self, w, b):
        self.weights = w
        self.bias = b

    def create_individual(self):
        self.weights = [random.random() * random.choice([1, -1]) for _ in range(self.inputs)]
        self.bias = [random.random() * random.choice([1, -1]) for _ in range(self.inputs)]

    def cross_over(self, individual2):
        chromosomes = [i for i in range(self.inputs)]
        chromosomes_individual_1 = []
        for i in range(random.randint(1, len(chromosomes) // 2)):
            chromosomes_individual_1.append(random.choice(chromosomes))
            chromosomes.remove(chromosomes_individual_1[-1])
        chromosomes_individual_2 = chromosomes
        weights_new_individual = [self.weights[i] for i in chromosomes_individual_1] + \
                                 [individual2.weights[y] for y in chromosomes_individual_2]

        bias_new_individual = [self.bias[i] for i in chromosomes_individual_1] + \
                              [individual2.bias[y] for y in chromosomes_individual_2]
        return [weights_new_individual, bias_new_individual]

    def activation_function(self, variables):
        soma = 0
        for i in range(len(variables) - 1):
            soma += self.weights[i] * variables[i] + self.bias[i]
        refined_value = math.tanh(soma)
        if refined_value >= 0.70:
            return 1
        elif refined_value <= -0.70:
            return -1
        else:
            return 0

    def mutation(self):
        new_w = []
        new_b = []
        for w, b in zip(self.weights, self.bias):
            if random.random() <= self.mutation_chance:
                new_w.append(w + (random.random() / 10) * random.choice([1, -1]))
            else:
                new_w.append(w)
            if random.random() <= self.mutation_chance:
                new_b.append(b + (random.random() / 10) * random.choice([1, -1]))
            else:
                new_b.append(b)
        self.weights = new_w
        self.bias = new_b

    def breed(self, individual_2, i_name):
        new_individual = Individual(self.inputs, i_name, self.mutation_chance)
        new_individual.weights, new_individual.bias = self.cross_over(individual_2)
        new_individual.mutation()
        return new_individual


class Population:
    def __init__(self, inputs, maxi, mc):
        self.internal_list = []
        self.generation = 1
        self.best_individual = None
        self.second_best = None
        self.input_number = inputs
        self.max_individuals = maxi
        self.mutation_chance = mc
        self.create_individuals_news()

    def create_individuals_news(self):
        for i in range(self.max_individuals):
            self.internal_list.append(Individual(self.input_number, i, self.mutation_chance))
            self.internal_list[-1].create_individual()
            """print(f"name: {self.internal_list[ -1].name}, weights:{self.internal_list[ -1].weights},"
                  f" bias: {self.internal_list[ -1].bias}")"""

    def show_individual_attributes(self):
        for ind in self.internal_list:
            print(f"name: {ind.name},weights:{ind.weights}, bias: {ind.bias}")

    def save_individual_attributes(self):
        file = open("parameters/best_individuals.txt", "a")
        file.write(f"Generation: {self.generation}\n")
        file.write(f"F:{self.best_individual.fitness};W:{self.best_individual.weights};B{self.best_individual.bias}\n")
        file.write(f"F:{self.second_best.fitness};W:{self.second_best.weights};B{self.second_best.bias}\n\n")
        file.close()

    def ler_attributes_individuals(self):
        file = open("parameters/current_generation.txt", "r")
        lines = file.readlines()
        index = 0
        for line in lines[1:]:
            list_line = line.split(";")
            fit = float(list_line[0][2:])
            wei = list_line[1][3:-1].split(",")
            bia = list_line[2][3:-1].split(",")
            self.internal_list[index].weights = [float(w) for w in wei]
            self.internal_list[index].bias = [float(b) for b in bia[:-1]]
            self.internal_list[index].bias.append(float(bia[-1][:-1]))
            self.internal_list[index].fitness = fit
            index += 1

        file.close()
        file = open("parameters/Current_generation.txt", "w")
        file.write(f"Generation: {self.generation + 1}\n")
        file.close()

    def select_best(self):
        fit = -1
        for individual in self.internal_list:
            if individual.fitness >= fit:
                self.second_best = self.best_individual
                self.best_individual = individual
                fit = self.best_individual.fitness

    def create_family(self):
        self.generation += 1
        self.best_individual.nome = 0
        self.second_best.nome = 1
        self.internal_list = []
        self.internal_list.append(self.best_individual)
        self.internal_list.append(self.second_best)
        for i in range((self.max_individuals - 2) // 2):
            self.internal_list.append(self.best_individual.breed(self.second_best, i + 2))
            self.internal_list.append(self.second_best.breed(self.best_individual, i + 3))


pygame.init()

# screen
screen = pygame.display.set_mode((1080, 700))
pygame.display.set_caption("Fast and Curious-AI Training")

# background
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((0, 255, 0))

# simulation
keepGoing = True
pop = Population(5, 10, 0.2)
world = game_classes.Training_World(screen)
"""w = [0.9849777777777572, 0.03444444444426724, 0.28495822222222262, 0.14811111117294833, 1.0254444434875984]
b = [0.2670813587084078, -0.6691533200275781, -0.5723370239650385, 0.25406116993577665, -0.486196069971221]
pop.select_best()
pop.create_family()"""

print(len(pop.internal_list))

while True:
    print(f"Generation: {pop.generation}")
    for p in pop.internal_list:
        if world.individual_is_perfect(p):  # returns True when AI gets good enough
            p.save_existence()
            exit("The individual has been trained successfully")
        print(p.fitness)
        world.__init__(screen)  # Prevents from making current AI continue where previous left
    pop.ler_attributes_individuals()
    pop.select_best()
    pop.save_individual_attributes()
    pop.create_family()
