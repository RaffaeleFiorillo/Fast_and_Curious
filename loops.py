import classes_entidades
import pygame
import funcoes


def Mission_Parts (screen, background):
# Entidades
    car = classes_entidades.carro()
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
        time_passed += clock.tick(30) / (33 * 30)
        # terminate execution
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
# player effects
        if not car.keepmoving and car.y in car.valores_y:
            car.visao(screen)
            escolha = funcoes.make_a_choice(car.valores_vistos)
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
        funcoes.refresh_game(screen, background, [estrada, lista_parts, lista_obstaculos, car])

def Mission_AI (screen, background):
# Entidades
    car = classes_entidades.carro()
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
        time_passed += clock.tick(30) / (33 * 30)
        # terminate execution
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
# player effects
        if not car.keepmoving and car.y in car.valores_y:
            car.visao(screen)
            escolha = funcoes.make_a_choice(car.valores_vistos)
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
        funcoes.refresh_game(screen, background, [estrada, lista_parts, lista_obstaculos, car])
