import classes_entidades as ce
import pygame
import funcoes


class Mission_AI:
    def __init__(self, screen):
        # Entities
        self.screen = screen
        self.car = ce.carro()
        self.estrada = ce.estrada()
        self.obstacles_list = ce.obstaculos()
        self.parts_list = ce.parts()
        self.parts_collected = 0
        self.energy = 100
        self.resistence = 100
        self.hud = ce.HUD(self.screen)
        # loop stuff
        self.clock = pygame.time.Clock()
        self.run = True
        self.time_passed = 0
        self.escolha = 0

    def refresh_game(self):
        entidades = [self.estrada, self.parts_list, self.obstacles_list, self.car]
        self.screen.blit(pygame.image.load("images/HUD/HUD_background.png"), (0, 308))
        for entidade in entidades:
            entidade.draw(self.screen)
        self.hud.draw(self.parts_collected)
        pygame.display.update()

    def car_moviment_y(self):
        if not self.car.keepmoving and self.car.y in self.car.valores_y:
            self.car.visao(self.screen)
            self.escolha = funcoes.make_a_choice(self.car.valores_vistos)
        if self.escolha == 1:
            self.car.movimento("DWN")
            self.car.direction = "DWN"
        elif self.escolha == -1:
            self.car.movimento("UP")
            self.car.direction = "UP"
        self.car.contin_mov()

    def car_moviment_x(self):
        pass

    # Loop
    def game_loop(self):
        while self.run:
            self.time_passed += self.clock.tick(30) / (33 * 30)
            # terminate execution
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
    # parts effects
            self.parts_list.remover_parts(self.obstacles_list.lista)
            self.parts_list.criar_parts()
    # car moviment
            self.car_moviment_y()
            self.car_moviment_x()
    # colision
            self.run = self.car.colisao_obstaculo(self.obstacles_list.lista)
            self.parts_list.lista, value = self.car.colisao_parts(self.parts_list.lista)
            self.parts_collected += value
    # obstacles effects
            self.obstacles_list.remover_obstaculos()
            self.obstacles_list.criar_obstaculos()
    # Refresh screen
            self.refresh_game()
