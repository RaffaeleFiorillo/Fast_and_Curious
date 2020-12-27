import time
import pygame
import os
import shutil
# import classes_menu as cm
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


def wait(seconds):
    time.sleep(seconds)

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


def show_error_message(screen, code):
    screen.blit(pygame.image.load(f"images/menu/messages/error{code}.png"), (230, 200))
    pygame.display.update()
    wait(3)


def show_succes_message(screen, code) -> None:
    screen.blit(pygame.image.load(f"images/menu/messages/success{code}.png"), (230, 200))
    pygame.display.update()
    wait(3)


def refresh_game(screen, background, entidades):
    screen.blit(background, (0, 0))
    for entidade in entidades:
        entidade.draw(screen)
    pygame.display.update()


def criar_pasta(nome_utilizador):
    os.mkdir(diretorio_raiz+nome_utilizador)


def eliminar_pasta(nome_utilizador):
    pass


def lista_utilizadores():
    utilizadores = [x[0].split("\\") for x in os.walk("saves")][1:]
    return [u[1] for u in utilizadores]


def numero_textos():
    texts = os.walk("texts")
    texts = [text for text in texts][0][1:][1]
    print(texts)
    #return [u[1] for u in utilizadores]


def create_sized_text(max_size_image, max_size_letter, text, color, min_size_letter=30):
    pygame.font.init()
    text_font = None
    rendered_text = None
    for i in range(min_size_letter, max_size_letter)[::-1]:
        text_font = pygame.font.SysFont('Times New Roman', i)
        text_font.set_bold(True)
        rendered_text = text_font.render(text, True, color)
        if rendered_text.get_size()[0] <= max_size_image:
            break
    return rendered_text


def write_name_passw(screen, name, password, ativo, hide):
    coordenadas1 = [(333, 203), (335, 349)]
    pygame.draw.rect(screen, (0, 0, 255),(coordenadas1[ativo], (420, 57)), 8)
    screen.blit(pygame.image.load("images/menu/interfaces/navigation/pointer.png"), (coordenadas1[ativo][0]+450, coordenadas1[ativo][1]))
    coordenadas2 = [(385, 217), (385, 363)]
    if hide:
        password = "".join(["*" for letter in password if str(letter).isalnum()])
    else:
        password = "".join(password)
    name = "".join(name)
    name_text = create_sized_text(330, 32, name, (255, 255, 255), 20)
    password_text = create_sized_text(330, 32, password, (255, 255, 255), 16)
    screen.blit(name_text, coordenadas2[0])
    screen.blit(password_text, coordenadas2[1])


def write_password(screen, password, hide):
    pygame.font.init()
    if hide:
        password = "".join(["*" for letter in password if str(letter).isalnum()])
    else:
        password = "".join(password)
    text_font = pygame.font.SysFont('Times New Roman', 32)
    text_font.set_bold(True)
    password_text = text_font.render(password, True, (0, 0, 0))
    screen.blit(password_text, (290, 330))


def write_name(screen, name):
    pygame.font.init()
    password = "".join(name)
    text_font, name_text = None, None
    for i in range(30, 50)[::-1]:
        text_font = pygame.font.SysFont('Times New Roman', i)
        text_font.set_bold(True)
        name_text = text_font.render(password, True, (0, 255, 0))
        if name_text.get_size()[0] <= 540:
            break
    screen.blit(name_text, ((screen.get_width()-name_text.get_size()[0])//2+7, 330))


def writeble_best_time(best_time):
    pygame.font.init()
    coordenadas = (135, 357)
    text_font = pygame.font.SysFont('Times New Roman', 19)
    text = ["  " for y in range(10 - len(str(best_time)))]
    new_text = "".join(text)+str(best_time)
    image_text = text_font.render(new_text, True, (255, 255, 255))
    return [image_text, coordenadas]


def writeble_best_speed(best_speed):
    pygame.font.init()
    coordenadas = (185, 427)
    text_font = pygame.font.SysFont('Times New Roman', 20)
    text = ["  " for y in range(4 - len(str(best_speed)))]
    new_text = "".join(text)+str(best_speed)
    image_text = text_font.render(new_text, True, (255, 255, 255))
    return [image_text, coordenadas]


def writeble_user_name(name):
    pygame.font.init()
    for s in range(65)[::-1]:
        text_font = pygame.font.SysFont('Times New Roman', s)
        text_font.set_bold(True)
        image_text = text_font.render(name, True, (0, 0, 0))
        size = image_text.get_size()
        if size[0] <= 253:
            break
    coordenadas = (107, 85-size[1]/2)
    return [image_text, coordenadas]


def writeble_parts_number(number):
    pygame.font.init()
    text_font = pygame.font.SysFont('Times New Roman', 12)
    new_text = str(number)
    #image_text = create_sized_text(170, 65, new_text, (0, 0, 0))
    for s in range(65)[::-1]:
            text_font = pygame.font.SysFont('Times New Roman', s)
            image_text = text_font.render(str(number), True, (0, 0, 0))
            size = image_text.get_size()
            if size[0] <= 170:
                break
    size = image_text.get_size()
    coordenadas = (132, 226-size[1]/2)
    image_text = text_font.render(new_text, True, (255, 255, 255))
    return [image_text, coordenadas]


def clean_background(screen):
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))
    screen.blit(background, (0, 0))


def erase_active_user_data():
    ficheiro = open("saves/active_user.txt", "w")
    ficheiro.close()


def delete_user_account(user_name):
    shutil.rmtree(f'saves/{user_name}')


def get_users_images(codigo):
    users = lista_utilizadores()
    users_images = []
    pygame.font.init()
    for user in users:
        for s in range(40)[::-1]:
            text_font = pygame.font.SysFont('Times New Roman', s)
            if users.index(user) == codigo:
                image_text = text_font.render(user, True, (0, 0, 0))
            else:
                image_text = text_font.render(user, True, (255, 255, 255))
            size = image_text.get_size()
            if size[0] <= 410:
                break
        users_images.append(image_text)
    return users_images
