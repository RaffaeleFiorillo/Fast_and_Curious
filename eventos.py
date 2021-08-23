# import menu_classes as cm
import Auxiliary_Functionalities as Af
# import game_classes as gc
# import link_functions as lf
# import entity_classes as ce
import math
import time
# import pygame


def generate_input(type_i=False):
    if type_i:
        return [Af.random_choice([-1, 0, 1]) for _ in range(14)]
    else:
        return [Af.random_choice([-1, 0, 1]) for _ in range(46)]


def create_individual():
    hidden_1 = [[Af.random() * Af.choice([1, -1]) for _ in range(46)] for _ in range(46)]
    hidden_2 = [[Af.random() * Af.choice([1, -1]) for _ in range(46)] for _ in range(7)]
    output = [[Af.random() * Af.choice([1, -1]) for _ in range(7)] for _ in range(3)]
    weights_i = [hidden_1, hidden_2, output]

    hidden_1 = [Af.random() * Af.choice([1, -1]) for _ in range(46)]
    hidden_2 = [Af.random() * Af.choice([1, -1]) for _ in range(7)]
    output = [Af.random() * Af.choice([1, -1]) for _ in range(3)]
    bias_i = [hidden_1, hidden_2, output]
    return weights_i, bias_i


def activation_function(value):
    return 1/(1+math.e**(-value))


def get_layer_output(values, layer, weights_i, bias_i):
    indexation = {"layer1": 0, "layer2": 1, "output": 2}[layer]
    layer_values = []
    for ind, neuron in enumerate(weights_i[indexation]):
        result_value = 0
        for weight, value in zip(neuron, values):
            result_value += weight * value
        result_value = activation_function(result_value + bias_i[indexation][ind])
        layer_values.append(result_value)
    return layer_values


def make_prediction(inputs, weights_i, bias_i):
    decisions = {1: None, 0: "DWN", 2: "UP"}
    hidden_layer1 = get_layer_output(inputs, "layer1", weights_i, bias_i)
    hidden_layer2 = get_layer_output(hidden_layer1, "layer2", weights_i, bias_i)
    output_layer = get_layer_output(hidden_layer2, "output", weights_i, bias_i)
    output = decisions[output_layer.index(max(output_layer))]
    # print(f"output: {output_layer}  inputs: {inputs}")
    return output  # returns the  index of the greatest value in the outputs (decision)


def make_a_choice(y, inputs):
    y_values = [10, 130, 150]
    if y in y_values:
        up = inputs[:22]
        front = [inputs[22], inputs[23]]
        down = inputs[24:]
        if 1 in up and -1 not in up:
            return "UP"
        elif -1 in front:
            if y == y_values[0]:
                return "DWN"
            elif y == y_values[2]:
                return "UP"
            elif -1 not in up:
                return "UP"
            elif -1 not in down:
                return "DWN"
        elif 1 in down and -1 not in down:
            return "DWN"
        else:
            return None


def test_AI_approach(cycles=10000):
    times = []
    inputs = generate_input()
    weights, bias = create_individual()
    for i in range(cycles):
        t1 = time.time()
        make_prediction(inputs, weights, bias)
        t2= time.time()
        times.append(t2-t1)
    return sum(times)/cycles


def test_Manual_approach(cycles=10000):
    times = []
    inputs = generate_input()
    y = Af.random_choice([10, 130, 150])
    for i in range(cycles):
        t1 = time.time()
        make_a_choice(y, inputs)
        t2= time.time()
        times.append(t2-t1)
    return sum(times)/cycles


AI_time = test_AI_approach(cycles=1000000)
Manual_time = test_Manual_approach(cycles=1000000)

print(f"AI-Time: {AI_time}    |    Manual-Time: {Manual_time}")
