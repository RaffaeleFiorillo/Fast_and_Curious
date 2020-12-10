import time
import pygame
import os
# import random
import math

diretorio_raiz = "saves/"
cores_obst = [[196, 15, 23], [239, 10, 9], [191, 15, 23], [245, 71, 20], [252, 130, 18], [255, 17, 11], [255, 18, 11],
              [255, 18, 12], [195, 195, 195], [163, 73, 164], [248, 12, 35]]
cores_part = [[255, 128, 0], [255, 242, 0], [34, 177, 76], [252, 130, 19], [237, 28, 36], [163, 73, 164], [255, 0, 255],
              [120, 0, 120], [0, 255, 255], [0, 0, 255]]
cores_estrada = [[0, 0, 0], [108, 108, 108]]
codigos_significados = {3: "desconhecido", 1: "estrada", 2: "parts", 0: "lava"}

weights = [-0.024636661554064646, 0.9490338548623168, 0.9490338548623168, 0.17090764398454833, 1.0661495372951384]
bias = [0.2670813587084078, -0.6691533200275781, -0.5723370239650385, 0.25406116993577665, -0.486196069971221]


def ver(screen, coo):
    x, y = coo
    # print(y)
    if y <= 0:
        return 0
    elif y > 700:
        return 0
    cor = list(screen.get_at((x, y)))
    cor2 = cor[:-1]
    # print(f"X: {x}; Y: {y}; Cor: {cor2}")
    if cor2 in cores_obst:
        codigo_atual = 0
    elif cor2 in cores_estrada:
        codigo_atual = 1
    elif cor2 in cores_part:
        codigo_atual = 2
    else:
        codigo_atual = 0
    # sign = codigos_significados[codigo_atual]
    # print(sign)
    return codigo_atual


def make_a_choice(info):
    soma = 0
    for i in range(len(info)):
        soma += weights[i] * info[i] + bias[i]
    refined_value = math.tanh(soma)
    if refined_value >= 0.70:
        return 1
    elif refined_value <= -0.70:
        return -1
    else:
        return 0


def prep_cores():
    ficheiro = open("parameters/cors.txt", "r")
    lines = ficheiro.readlines()
    lines = sorted(lines)
    f = open("parameters/cores.txt", "a")
    for line in lines:
        f.write(f"{line}")
    ficheiro.close()
    f.close()


def refresh_game(screen, background, entidades):
    screen.blit(background, (0, 0))
    for entidade in entidades:
        entidade.draw(screen)
    pygame.display.update()


def criar_pasta(nome_utilizador):
    os.mkdir(diretorio_raiz+nome_utilizador)


def lista_utilizadores():
    utilizadores = [x[0].split("\\") for x in os.walk("saves")][1:]
    return [u[1] for u in utilizadores]


def write_best_time(screen, best_time):
    pygame.font.init()
    text_font = pygame.font.SysFont('Times New Roman', 12)
    text = ["0" for y in range(10 - len(str(best_time)))]
    new_text = str(best_time)
    for y in text:
        new_text = y+new_text
    image_text = text_font.render(new_text, True, (255, 255, 255))
    while True:
        screen.blit(image_text, (20, 20))
        pygame.display.update()


def write_name_passw(screen, name, password, ativo):
    pygame.font.init()
    coordenadas1 = [(333, 203), (335, 349)]
    pygame.draw.rect(screen, (0, 0, 255),(coordenadas1[ativo], (420, 57)), 8)
    screen.blit(pygame.image.load("imagens/menu/interfaces/navigation/pointer.png"), (coordenadas1[ativo][0]+450, coordenadas1[ativo][1]))
    coordenadas2 = [(385, 217), (385, 363)]
    name, password = "".join(name), "".join(password)
    text_font = pygame.font.SysFont('Times New Roman', 32)
    name_text = text_font.render(name, True, (255, 255, 255))
    password_text = text_font.render(password, True, (255, 255, 255))
    screen.blit(name_text, coordenadas2[0])
    screen.blit(password_text, coordenadas2[1])


def write_best_speed(screen, best_speed):
    pygame.font.init()
    text_font = pygame.font.SysFont('Times New Roman', 12)
    text = ["0" for y in range(10 - len(str(best_speed)))]
    new_text = str(best_speed)
    for y in text:
        new_text = y+new_text
    image_text = text_font.render(new_text, True, (255, 255, 255))
    while True:
        screen.blit(image_text, (20, 20))
        pygame.display.update()


def write_user_name(screen, best_time):
    pygame.font.init()
    text_font = pygame.font.SysFont('Times New Roman', 12)
    text = ["0" for y in range(10 - len(str(best_time)))]
    new_text = str(best_time)
    for y in text:
        new_text = y+new_text
    image_text = text_font.render(new_text, True, (255, 255, 255))
    while True:
        screen.blit(image_text, (20, 20))
        pygame.display.update()


def write_parts_number(screen, best_time):
    pygame.font.init()
    text_font = pygame.font.SysFont('Times New Roman', 12)
    text = ["0" for y in range(10 - len(str(best_time)))]
    new_text = str(best_time)
    for y in text:
        new_text = y+new_text
    image_text = text_font.render(new_text, True, (255, 255, 255))
    while True:
        screen.blit(image_text, (20, 20))
        pygame.display.update()

