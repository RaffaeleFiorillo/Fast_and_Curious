import random
import pygame
import math
import classes_entidades
import funcoes


def treino_jogo_autom (screen, background, individuo):
# Entidades
    print(individuo.weights, individuo.bias)
    car = classes_entidades.carro((0, 0, 255))
    estrada = classes_entidades.estrada()
    lista_obstaculos = classes_entidades.obstaculos()
    lista_parts = classes_entidades.parts()
# loop stuff
    clock = pygame.time.Clock()
    keepGoing2 = True
    time_passed = 0
    escolha = 0
# Loop
    while keepGoing2:
        time_passed += clock.tick(100) / (33 * 30)
        # terminate execution
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
# player effects
        if not car.keepmoving and car.y in car.valores_y:
            car.visao(screen)
            escolha = individuo.activation_function(car.valores_vistos)
        if escolha == 1:
            car.movimento("DWN")
            car.direction = "DWN"
        elif escolha == -1:
            car.movimento("UP")
            car.direction = "UP"
        car.contin_mov()
# colisao
        keepGoing2 = car.colisao_obstaculo(lista_obstaculos.lista)
        lista_parts.lista = car.colisao_parts(lista_parts.lista)
# parts effects
        lista_parts.remover_parts(lista_obstaculos.lista)
        lista_parts.criar_parts()
# obstacles effects
        lista_obstaculos.remover_obstaculos()
        lista_obstaculos.criar_obstaculos()
# Refresh screen
        funcoes.refresh(screen, background, [estrada, lista_parts, lista_obstaculos, car])
        #print(time_passed)
        if time_passed >= 500:
            break
# Individuo
    #individuo.time_alive = time_passed
    #individuo.parts = car.pecas
    #individuo.fitness_level()
    #individuo.gravar_existencia()


class _individuo:
    def __init__(self, input_number, name, mc):
        self.name = name
        self.inputs = input_number
        self.weights = []
        self.bias = []
        self.mutation_chance = mc
        self.fitness = 0
        self.time_alive = 0
        self.parts = 0
        self.necessidade = True

    def fitness_level(self):
        self.fitness = self.parts * 0.2 + self.time_alive * 0.8

    def gravar_existencia(self):
        ficheiro = open("parameters/geracao_atual.txt", "a")
        ficheiro.write(f"F:{self.fitness};W:{self.weights};B:{self.bias}\n")
        ficheiro.close()

    def get_wb(self, w, b):
        self.weights = w
        self.bias = b

    def criar_individuo(self):
        self.weights = [random.random() * random.choice([1, -1]) for w in range(self.inputs)]
        self.bias = [random.random() * random.choice([1, -1]) for b in range(self.inputs)]

    def cross_over(self, individuo2):
        cromossoms = [i for i in range(self.inputs)]
        cromossoms_individuo_1 = []
        for i in range(random.randint(1, len(cromossoms) // 2)):
            cromossoms_individuo_1.append(random.choice(cromossoms))
            cromossoms.remove(cromossoms_individuo_1[-1])
        cromossoms_individuo_2 = cromossoms
        weights_new_individuo = [self.weights[i] for i in cromossoms_individuo_1] + [individuo2.weights[y] for y in cromossoms_individuo_2]
        bias_new_individuo = [self.bias[i] for i in cromossoms_individuo_1] + [individuo2.bias[y] for y in cromossoms_individuo_2]
        return [weights_new_individuo, bias_new_individuo]

    def activation_function(self, variables):
        soma = 0
        #print(variables)
        if self.necessidade:
            for i in range(len(variables)):
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

    def breed(self, individuo_2, i_name):
        novo_individuo = _individuo(self.inputs, i_name, self.mutation_chance)
        novo_individuo.weights, novo_individuo.bias = self.cross_over(individuo_2)
        novo_individuo.mutation()
        return novo_individuo


class Populacao:
    def __init__(self, inputs, maxi, mc):
        self.lista = []
        self.generacao = 1
        self.best_indiv = None
        self.second_best = None
        self.numero_input = inputs
        self.max_indiv = maxi
        self.mutation_chance = mc
        self.criar_individuos_novos()

    def criar_individuos_novos(self):
        for i in range(self.max_indiv):
            self.lista.append(_individuo(self.numero_input, i, self.mutation_chance))
            self.lista[-1].criar_individuo()
            #print(f"name: {self.lista[ -1].name},weights:{self.lista[ -1].weights}, bias: {self.lista[ -1].bias}")

    def mostrar_atributos_individuos(self):
        for ind in self.lista:
            print(f"name: {ind.name},weights:{ind.weights}, bias: {ind.bias}")

    def gravar_atributos_individuo(self):
        ficheiro = open("parameters/best_individuos.txt", "a")
        ficheiro.write(f"Geraçao: {self.generacao}\n")
        ficheiro.write(f"F:{self.best_indiv.fitness};W:{self.best_indiv.weights};B{self.best_indiv.bias}\n")
        ficheiro.write(f"F:{self.second_best.fitness};W:{self.second_best.weights};B{self.second_best.bias}\n\n")
        ficheiro.close()

    def ler_atributos_individuos(self):
        ficheiro = open("parameters/geracao_atual.txt", "r")
        lines = ficheiro.readlines()
        index = 0
        for line in lines[1:]:
            list_line = line.split(";")
            fit = float(list_line[0][2:])
            wei = list_line[1][3:-1].split(",")
            bia = list_line[2][3:-1].split(",")
            self.lista[index].weights = [float(w) for w in wei]
            self.lista[index].bias = [float(b) for b in bia[:-1]]
            self.lista[index].bias.append(float(bia[-1][:-1]))
            self.lista[index].fitness = fit
            index += 1

        ficheiro.close()
        ficheiro = open("parameters/geracao_atual.txt", "w")
        ficheiro.write(f"Geracao: {self.generacao+1}\n")
        ficheiro.close()

    def select_best(self):
        fit = -1
        for indv in self.lista:
            if indv.fitness >= fit:
                self.second_best = self.best_indiv
                self.best_indiv = indv
                fit = self.best_indiv.fitness

    def criar_familia(self):
        self.generacao += 1
        self.best_indiv.nome = 0
        self.second_best.nome = 1
        self.lista = []
        self.lista.append(self.best_indiv)
        self.lista.append(self.second_best)
        for i in range((self.max_indiv-2)//2):
            self.lista.append(self.best_indiv.breed(self.second_best, i+2))
            self.lista.append(self.second_best.breed(self.best_indiv, i+3))

pygame.init()

# screen
screen = pygame.display.set_mode((1080, 700))
pygame.display.set_caption("Fast and Curious-Beta")
# background
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((0, 255, 0))
keepGoing = True
pop = Populacao(2, 3, 0.2)
w = [-0.024636661554064646, 0.9490338548623168, 0.9490338548623168, 0.17090764398454833, 1.0661495372951384]
b = [0.2670813587084078, -0.6691533200275781, -0.5723370239650385, 0.25406116993577665, -0.486196069971221]
pop.lista[0].get_wb(w, b)
pop.lista[1].get_wb(w, b)
#pop.ler_atributos_individuos()
#pop.select_best()
#pop.criar_familia()
while keepGoing:
    print(f"Geracao: {pop.generacao}")
    for p in pop.lista:
        keepGoing = treino_jogo_autom(screen, background, p)
        if keepGoing is None:
            keepGoing = True
    #pop.ler_atributos_individuos()
    #pop.select_best()
    #pop.gravar_atributos_individuo()
    #pop.criar_familia()
