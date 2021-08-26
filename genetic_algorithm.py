import math
import pygame
import entity_classes as ce
import Auxiliary_Functionalities as Af

M_C = 0.8  # mutation chance
game_over_sound = Af.load_sound("game/game_over.WAV")            # sound of the match ending


def normalize(max_value, min_value, value):
    return (value-min_value) / (max_value-min_value)


def activation_function(value):
    return 1/(1+math.e**(-value))


def mutate_value(value, mutation_chance=M_C):
    if Af.random() > mutation_chance:  # invert value's signal
        value *= Af.random_choice([-1, 1])
    if Af.random() > mutation_chance:  # increase or decrease value
        value += Af.random_choice([-1, 1]) * (Af.random() / Af.random_choice([1000, 100, 10]))
    if Af.random() > M_C:
        return Af.random_choice([-1, 1]) * (Af.random() / Af.random_choice([100, 10]))
    return value


# Creates a world where the AI can be trained
class Training_World:
    def __init__(self, screen_i):
        self.screen = screen_i
        # Game objects
        self.car = ce.Car()
        self.road = ce.Road()
        self.obstacles_list = ce.Obstacles()
        self.parts_list = ce.parts()
        self.parts_collected = 0
        self.individual = None
        self.hud_image = Af.load_image("HUD/HUD_background.png")
        # loop stuff
        self.clock = pygame.time.Clock()
        self.frame_rate = Af.FRAME_RATE  # must not be multiple of 10
        self.run = True
        self.time_passed = 0
        self.total_time = 0.0
        self.choice_delay = 0
        self.choice = None
        self.resistance = True

    def refresh_game(self):
        entities = [self.road, self.parts_list, self.obstacles_list, self.car]
        self.screen.blit(self.hud_image, (0, 308))
        for entity in entities:
            entity.draw(self.screen)
        pygame.display.update()

    def update_individual(self):
        self.individual.parts = self.parts_collected
        self.individual.time_alive = self.time_passed
        self.individual.fitness_level()

    def make_movement_choice(self):
        if self.car.y in self.car.y_values:  # car only makes choice if in the middle of one of the tracks
            if self.choice_delay >= 20:
                self.choice = self.individual.make_prediction(self.car.seen_values)
                self.choice_delay = 0
            self.choice_delay += 1
        else:
            self.choice = None

    def car_movement_y(self):
        self.car.vision(self.screen)
        self.make_movement_choice()
        self.car.movement(self.choice)

    def manage_buttons(self, button):
        if button == pygame.K_UP:
            self.car.movement("UP")
        elif button == pygame.K_DOWN:
            self.car.movement("DWN")
        elif button == pygame.K_PLUS:
            if self.frame_rate < 90:
                self.frame_rate += 10
        elif button == pygame.K_MINUS:
            if self.frame_rate > 10:
                self.frame_rate -= 10

    def continue_game(self):
        return self.resistance

    def individual_is_perfect(self, individual):
        self.individual = individual
        while self.run:
            # terminate execution
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                if event.type == pygame.KEYDOWN:
                    self.manage_buttons(event.key)
    # parts effects
            self.parts_list.remover_parts(self.obstacles_list.internal_list)
            self.parts_list.create_parts()
    # car movement
            self.car_movement_y()
    # collision & damage
            if self.car.obstacle_collision(self.obstacles_list.internal_list):
                self.resistance = False
            self.parts_list.internal_list, value = self.car.parts_collision(self.parts_list.internal_list)
            self.parts_collected += value
    # obstacles effects
            self.obstacles_list.remove_obstacles()
            self.obstacles_list.create_obstacles()
    # Refresh screen
            if self.run:
                self.run = self.continue_game()
            self.refresh_game()
            self.time_passed += self.clock.tick(self.frame_rate) / 990
        self.update_individual()
        Af.stop_all_sounds()
        Af.play(game_over_sound)
        return False  # if it gets here, it means it not good enough


# Creates a world where Car-movement-data can be extracted
class Data_World:
    def __init__(self, screen_i):
        self.screen = screen_i
        # Game objects
        self.car = ce.Car()
        self.road = ce.Road()
        self.obstacles_list = ce.Obstacles()
        self.parts_list = ce.parts()
        self.parts_collected = 0
        self.hud_image = Af.load_image("HUD/HUD_background.png")
        # loop stuff
        self.clock = pygame.time.Clock()
        self.frame_rate = 5  # must not be multiple of 10
        self.run = True
        self.choice = None
        self.time_passed = 0
        self.total_time = 0.0
        self.resistance = True
        self.seen_values = []
        self.choices_made = []

    def refresh_game(self):
        entities = [self.road, self.parts_list, self.obstacles_list, self.car]
        self.screen.blit(self.hud_image, (0, 308))
        for entity in entities:
            entity.draw(self.screen)
        pygame.display.update()

    def make_a_choice(self):
        if self.car.y in self.car.y_values:
            up = self.car.seen_values[:22]
            front = [self.car.seen_values[22], self.car.seen_values[23]]
            down = self.car.seen_values[24:]
            if 1 in up and -1 not in up:
                return "UP"
            elif -1 in front:
                if self.car.y == self.car.y_values[0]:
                    return "DWN"
                elif self.car.y == self.car.y_values[2]:
                    return "UP"
                elif -1 not in up:
                    return "UP"
                elif -1 not in down:
                    return "DWN"
            elif 1 in down and -1 not in down:
                return "DWN"
            else:
                return None

    def car_movement_y(self):
        self.car.vision(self.screen)
        self.choice = self.make_a_choice()
        self.car.movement(self.choice)

    def manage_buttons(self, button):
        self.car.vision(self.screen)
        self.seen_values.append(self.car.seen_values)
        if button == pygame.K_UP:
            self.choices_made.append("UP")
            self.car.movement("UP")
        elif button == pygame.K_DOWN:
            self.choices_made.append("DWN")
            self.car.movement("DWN")
        elif button == pygame.K_PLUS:
            if self.frame_rate < 90:
                self.frame_rate += 10
        elif button == pygame.K_MINUS:
            if self.frame_rate > 10:
                self.frame_rate -= 10

    def save_data(self):
        file = open("training data.txt", "a")
        for line in self.seen_values:
            file.write(str(line))
            file.write("\n")
        file.write(str(self.choices_made))

    def continue_game(self):
        return self.resistance

    def get_data(self):
        while self.run:
            # terminate execution
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                if event.type == pygame.KEYDOWN:
                    self.manage_buttons(event.key)
    # parts effects
            self.parts_list.remover_parts(self.obstacles_list.internal_list)
            self.parts_list.create_parts()
    # car movement
            self.car_movement_y()
    # collision & damage
            if self.car.obstacle_collision(self.obstacles_list.internal_list):
                self.resistance = False
            self.parts_list.internal_list, value = self.car.parts_collision(self.parts_list.internal_list)
            self.parts_collected += value
    # obstacles effects
            self.obstacles_list.remove_obstacles()
            self.obstacles_list.create_obstacles()
    # Refresh screen
            if self.run:
                self.run = self.continue_game()
            self.refresh_game()
            self.time_passed += self.clock.tick(self.frame_rate) / 990
        self.save_data()
        Af.stop_all_sounds()
        Af.play(game_over_sound)
        return False  # if it gets here, it means it not good enough


class Individual:
    def __init__(self, input_number, name):
        self.name = name
        self.inputs = input_number
        self.weights = []
        self.bias = []
        self.fitness = 0
        self.time_alive = 0
        self.moves_number = 0
        self.parts = 0

    def fitness_level(self):
        parts_contribute = normalize(3500, 0, self.parts) * 0.3  # contribute of parts collected between 0 and 1
        time_contribute = normalize(100, 0, self.time_alive)  # contribute of time survived between 0 and 1
        # moves_contribute = ((1.5 - self.moves_number/self.time_alive)**2)**(1/2) * 0.2  # contribute of moves  " " "
        """print(f"parts: {self.parts} | contribute: {parts_contribute}"
              f"|| time: {self.time_alive} | contribute: {time_contribute}")"""
        self.fitness = parts_contribute + time_contribute  # + moves_contribute

    def __str__(self):
        return f"Name: {self.name} | Fitness: {self.fitness} \n W: {self.weights}\n B: {self.bias}\n\n"

    def __copy__(self):
        new_individual = Individual(self.inputs, self.name)
        new_individual.get_wb(self.weights, self.bias)
        return new_individual

    def save_existence(self):
        file = open("parameters/Current_generation.txt", "a")
        file.write(f"\n\nF:{self.fitness};\nW:{self.weights};\nB:{self.bias}\n\n")
        file.close()

    def get_wb(self, we, bi):
        self.weights = we
        self.bias = bi

    def create_individual(self):
        hidden_1 = [[Af.random() * Af.choice([1, -1]) for _ in range(self.inputs)] for _ in range(self.inputs)]
        hidden_2 = [[Af.random() * Af.choice([1, -1]) for _ in range(self.inputs)] for _ in range(7)]
        output = [[Af.random() * Af.choice([1, -1]) for _ in range(7)] for _ in range(3)]
        self.weights = [hidden_1, hidden_2, output]

        hidden_1 = [Af.random() * Af.choice([1, -1]) for _ in range(self.inputs)]
        hidden_2 = [Af.random() * Af.choice([1, -1]) for _ in range(7)]
        output = [Af.random() * Af.choice([1, -1]) for _ in range(3)]
        self.bias = [hidden_1, hidden_2, output]

    @staticmethod
    def cross_over_layers(layers1, layers2):
        new_values = []
        for layer1, layer2 in zip(layers1, layers2):
            new_layer = []
            for values1, values2 in zip(layer1, layer2):
                if Af.random() >= 0.5:
                    new_layer.append(values1)
                else:
                    new_layer.append(values2)
            new_values.append(new_layer)
        return new_values

    def cross_over(self, individual2):
        new_weights = self.cross_over_layers(self.weights, individual2.weights)
        new_bias = self.cross_over_layers(self.bias, individual2.bias)
        return new_weights, new_bias

    def get_layer_output(self, values, layer):
        indexation = {"layer1": 0, "layer2": 1, "output": 2}[layer]
        layer_values = []
        for ind, neuron in enumerate(self.weights[indexation]):
            result_value = 0
            for weight, value in zip(neuron, values):
                result_value += weight*value
            result_value = activation_function(result_value+self.bias[indexation][ind])
            layer_values.append(result_value)
        return layer_values

    def make_prediction(self, inputs):
        decisions = {1: None, 0: "DWN", 2: "UP"}
        hidden_layer1 = self.get_layer_output(inputs, "layer1")
        hidden_layer2 = self.get_layer_output(hidden_layer1, "layer2")
        output_layer = self.get_layer_output(hidden_layer2, "output")
        output = decisions[output_layer.index(max(output_layer))]
        # print(f"output: {output_layer}  inputs: {inputs}")
        return output  # returns the  index of the greatest value in the outputs (decision)

    def mutate_bias(self):
        group = []
        for layer in self.bias:
            new_layer = []
            for bias in layer:
                new_bias = mutate_value(bias)
                new_layer.append(new_bias)
            group.append(new_layer)
        self.bias = group

    def mutate_weights(self):
        group = []
        for layer in self.weights:
            new_layer = []
            for weights in layer:
                new_weights = list(map(mutate_value, weights))
                new_layer.append(new_weights)
            group.append(new_layer)
        self.weights = group

    def mutate(self):
        self.mutate_weights()
        self.mutate_bias()

    def breed(self, individual_2, i_name):
        new_individual = Individual(self.inputs, i_name)
        new_individual.weights, new_individual.bias = self.cross_over(individual_2)
        new_individual.mutate()
        return new_individual


class Population:
    def __init__(self, inputs, maxi):
        self.internal_list = []
        self.generation = 1
        self.best_individual = None
        self.second_best = None
        self.third_best = None
        self.input_number = inputs
        self.max_individuals = maxi
        self.create_individuals_news()

    def create_individuals_news(self):
        for i in range(self.max_individuals):
            self.internal_list.append(Individual(self.input_number, i))
            self.internal_list[-1].create_individual()
            """print(f"name: {self.internal_list[ -1].name}, weights:{self.internal_list[ -1].weights},"
                  f" bias: {self.internal_list[ -1].bias}")"""

    def show_individual_attributes(self):
        for ind in self.internal_list:
            print(ind)

    def save_best_individuals(self):
        file = open("parameters/best_individuals.txt", "a")
        file.write(f"Generation: {self.generation}\n")
        file.write(self.best_individual.__str__())
        file.write(self.second_best.__str__())
        file.write(self.third_best.__str__())
        file.close()

    def select_best(self):
        self.internal_list.sort(key=lambda individual: individual.fitness)
        self.best_individual, self.second_best, self.third_best, *rest = self.internal_list

    def create_family(self):
        self.generation += 1
        self.best_individual.nome = 0
        self.second_best.nome = 1
        self.third_best.nome = 2
        self.internal_list = []

        if self.best_individual.fitness >= 0.08:
            self.best_individual.save_existence()

        self.internal_list.append(self.best_individual)
        self.internal_list.append(self.best_individual)
        self.internal_list.append(self.second_best)
        self.internal_list.append(self.second_best)
        self.internal_list.append(self.third_best)

        for i in range(3):
            new1 = self.best_individual.__copy__()
            new1.mutate()
            self.internal_list.append(new1)

        new2 = self.second_best.__copy__()
        new2.mutate()
        self.internal_list.append(new2)
        new3 = self.third_best.__copy__()
        new3.mutate()
        self.internal_list.append(new3)

        self.internal_list.append(self.best_individual.breed(self.second_best, 3))
        self.internal_list.append(self.second_best.breed(self.best_individual, 5))
        self.internal_list.append(self.best_individual.breed(self.third_best, 7))

        for i in range(self.max_individuals - len(self.internal_list)):
            new_individual = Individual(self.input_number, i+13)
            new_individual.create_individual()
            self.internal_list.append(new_individual)


pygame.init()

# screen stuff
screen = pygame.display.set_mode((1080, 700))
pygame.display.set_caption("Fast and Curious-AI Training")

# simulation stuff
keepGoing = True
pop = Population(14, 20)
world = Training_World(screen)

"""w = f.WEIGHTS
b = f.BIAS
perfect_being = Individual(14, 0)
perfect_being.create_individual()


perfect_being2 = Individual(14, 0)
perfect_being2.create_individual()

perfect_being.cross_over(perfect_being2)

# world.individual_is_perfect(perfect_being)
# print(perfect_being)"""

"""
while True:
    print(f"Generation: {pop.generation}")
    for p in pop.internal_list:
        if world.individual_is_perfect(p):  # returns True when AI gets good enough
            p.save_existence()
            exit("The individual has been trained successfully")
        print(f"Name: {p.name} | Fitness: {p.fitness}")
        world.__init__(screen)  # Prevents from making current AI continue where previous left
    pop.select_best()
    pop.create_family()
    if not pop.generation % 10:
        pop.save_best_individuals()"""

w = Data_World(screen)
w.get_data()
