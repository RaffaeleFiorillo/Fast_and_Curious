import classes_entidades as ce
from random import choice
import pygame
import funcoes as f


class Mission_AI:
    def __init__(self, screen):
        self.screen = screen
        # Game objects
        self.car = ce.carro()
        self.estrada = ce.estrada()
        self.obstacles_list = ce.obstaculos()
        self.parts_list = ce.parts()
        self.parts_collected = 0
        # HUD stuff
        self.energy = 100
        self.resistence = 100
        self.hud = ce.HUD(self.screen)
        self.speed = 0
        self.precision = 100
        # text stuff
        self.cursor = pygame.image.load("images/texts/cursor.png")
        self.written_text = [[]]
        self.text_name = None
        self.text_to_write_image = None
        self.line = 0
        self.total_words = 0
        self.correct_letters = 0
        self.text_to_write = None
        self.set_up_texts()
        # loop stuff
        self.clock = pygame.time.Clock()
        self.run = True
        self.time_passed = 0
        self.escolha = 0

    def set_up_texts(self):
        self.text_name = choice(f.get_text_names())[:-4]
        self.text_to_write_image = pygame.image.load(f"images/texts/{self.text_name}.png")
        self.text_to_write = [[line] for line in open(f"texts/{self.text_name}.txt", "r").readlines()]
        self.screen.blit(self.text_to_write_image, (280, 320))
        pygame.display.update()

    def refresh_game(self):
        entidades = [self.estrada, self.parts_list, self.obstacles_list, self.car]
        self.screen.blit(pygame.image.load("images/HUD/HUD_background.png"), (0, 308))
        for entidade in entidades:
            entidade.draw(self.screen)
        time = 60-int(self.time_passed)
        self.hud.draw(self.parts_collected, time, self.speed, self.precision, self.energy, self.resistence)
        self.display_text()
        self.screen.blit(self.text_to_write_image, (280, 320))
        pygame.display.update()

    def car_moviment_y(self):
        if not self.car.keepmoving and self.car.y in self.car.valores_y:
            self.car.visao(self.screen)
            self.escolha = f.make_a_choice(self.car.valores_vistos)
        if self.escolha == 1:
            self.car.movimento("DWN")
            self.car.direction = "DWN"
        elif self.escolha == -1:
            self.car.movimento("UP")
            self.car.direction = "UP"
        self.car.contin_mov()

    def car_moviment_x(self):
        pass

    def manage_buttons(self, keys, event):
        if keys[pygame.K_KP_ENTER] or keys[pygame.K_RETURN]:
            self.written_text.append([])
            self.line += 1
        elif keys[pygame.K_BACKSPACE]:
            if len(self.written_text[self.line]) == 0:
                if len(self.written_text) > 1:
                    self.written_text.pop()
                    self.line -= 1
            else:
                self.correct_letters -= 1
                self.written_text[self.line].pop()
                self.total_words -= 0.2
        elif len(self.written_text[self.line]) >= 48:
            self.written_text.append([])
            self.line += 1
        else:
            if event.unicode != "":
                self.written_text[self.line].append(event.unicode)
                self.total_words += 0.2
                if self.written_text[self.line][-1] == self.text_to_write[self.line][0][len(self.written_text[self.line])-1]:
                    self.correct_letters += 1

    def display_text(self):
        coordinates = [(290, 454), (290, 469), (290, 484), (290, 499), (290, 514), (290, 529), (290, 544), (290, 559)]
        text_images = f.get_text_images(self.written_text)
        for image, coo in zip(text_images, coordinates):
            self.screen.blit(image, coo)
        if int(self.time_passed+self.time_passed*1.5) % 2:
            self.screen.blit(self.cursor, (coordinates[self.line][0]+text_images[self.line].get_size()[0],
                                           coordinates[self.line][1]+3))

    def continue_game(self):
        if not self.resistence:
            return False
        elif not self.energy:
            return False
        elif int(self.time_passed) >= 60:
            return False
        return True

    def update_speed(self):
        self.speed = self.total_words*60/self.time_passed

    def update_precision(self):
        if self.total_words:
            print(self.correct_letters, self.total_words*5)
            self.precision = self.correct_letters/(self.total_words*5) * 100
        else:
            self.precision = 100

    def game_loop(self):
        damage_count = 4
        while self.run:
            self.time_passed += self.clock.tick(30) / (33 * 30)
    # terminate execution
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                if event.type == pygame.KEYDOWN:
                    self.manage_buttons(pygame.key.get_pressed(), event)
    # parts effects
            self.parts_list.remover_parts(self.obstacles_list.lista)
            self.parts_list.criar_parts()
    # car moviment
            self.car_moviment_y()
            self.car_moviment_x()
    # colision
            if self.time_passed >= 4:
                if damage_count >= 0.5:
                    if self.car.colisao_obstaculo(self.obstacles_list.lista):
                        self.resistence -= 4
                        self.car.x -= 10
                        damage_count = 0
                else:
                    damage_count += 0.01
            self.parts_list.lista, value = self.car.colisao_parts(self.parts_list.lista)
            self.parts_collected += value
    # obstacles effects
            self.obstacles_list.remover_obstaculos()
            self.obstacles_list.criar_obstaculos()
    # Refresh screen
            # print(f"words: {self.digited_word_number}; time: {self.time_passed}")
            self.update_speed()
            self.update_precision()
            if self.run:
                self.run = self.continue_game()
            self.refresh_game()
        return self.total_words, int(self.correct_letters/5), self.precision, self.speed, self.parts_collected, \
            self.energy, self.resistence


class Mission_PARTS:
    def __init__(self, screen):
        self.screen = screen
        # Game objects
        self.car = ce.carro()
        self.estrada = ce.estrada()
        self.obstacles_list = ce.obstaculos()
        self.parts_list = ce.parts()
        self.parts_collected = 0
        # HUD stuff
        self.energy = 100
        self.resistence = 100
        self.hud = ce.HUD(self.screen)
        self.speed = 0
        self.precision = 100
        # text stuff
        self.cursor = pygame.image.load("images/texts/cursor.png")
        self.written_text = [[]]
        self.text_name = None
        self.text_to_write_image = None
        self.line = 0
        self.digited_word_number = 0
        self.text_to_write = [[]]
        self.set_up_texts()
        # loop stuff
        self.clock = pygame.time.Clock()
        self.run = True
        self.time_passed = 0
        self.escolha = 0

    def set_up_texts(self):
        self.text_name = choice(f.get_text_names())[:-4]
        self.text_to_write_image = pygame.image.load(f"images/texts/{self.text_name}.png")
        self.screen.blit(self.text_to_write_image, (280, 320))
        pygame.display.update()

    def refresh_game(self):
        entidades = [self.estrada, self.parts_list, self.obstacles_list, self.car]
        self.screen.blit(pygame.image.load("images/HUD/HUD_background.png"), (0, 308))
        for entidade in entidades:
            entidade.draw(self.screen)
        time = 60 - int(self.time_passed)
        self.hud.draw(self.parts_collected, time, self.speed, self.precision, self.energy, self.resistence)
        self.display_text()
        self.screen.blit(self.text_to_write_image, (280, 320))
        pygame.display.update()

    def car_moviment_y(self):
        if not self.car.keepmoving and self.car.y in self.car.valores_y:
            self.car.visao(self.screen)
            self.escolha = f.make_a_choice(self.car.valores_vistos)
        if self.escolha == 1:
            self.car.movimento("DWN")
            self.car.direction = "DWN"
        elif self.escolha == -1:
            self.car.movimento("UP")
            self.car.direction = "UP"
        self.car.contin_mov()

    def car_moviment_x(self):
        pass

    def manage_buttons(self, keys, event):
        if keys[pygame.K_KP_ENTER] or keys[pygame.K_RETURN]:
            self.written_text.append([])
            self.line += 1
        elif keys[pygame.K_BACKSPACE]:
            if len(self.written_text[self.line]) == 0:
                if len(self.written_text) > 1:
                    self.written_text.pop()
                    self.line -= 1
            else:
                self.written_text[self.line].pop()
                self.digited_word_number -= 0.2
        elif len(self.written_text[self.line]) >= 48:
            self.written_text.append([])
            self.line += 1
        else:
            self.written_text[self.line].append(event.unicode)
            self.digited_word_number += 0.2

    def display_text(self):
        coordinates = [(290, 454), (290, 469), (290, 484), (290, 499), (290, 514), (290, 529), (290, 544), (290, 559)]
        text_images = f.get_text_images(self.written_text)
        for image, coo in zip(text_images, coordinates):
            self.screen.blit(image, coo)
        if int(self.time_passed + self.time_passed * 1.5) % 2:
            self.screen.blit(self.cursor, (coordinates[self.line][0], coordinates[self.line][1]))

    def continue_game(self):
        if not self.resistence:
            return False
        elif not self.energy:
            return False
        elif int(self.time_passed) >= 60:
            return False
        return True

    def game_loop(self):
        damage_count = 4
        while self.run:
            self.time_passed += self.clock.tick(30) / (33 * 30)
            # terminate execution
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    return "continue"
                if event.type == pygame.KEYDOWN:
                    self.manage_buttons(pygame.key.get_pressed(), event)
            # parts effects
            self.parts_list.remover_parts(self.obstacles_list.lista)
            self.parts_list.criar_parts()
            # car moviment
            self.car_moviment_y()
            self.car_moviment_x()
            # colision
            if self.time_passed >= 4:
                if damage_count >= 0.5:
                    if self.car.colisao_obstaculo(self.obstacles_list.lista):
                        self.resistence -= 4
                        self.car.x -= 10
                        damage_count = 0
                else:
                    damage_count += 0.01
            self.parts_list.lista, value = self.car.colisao_parts(self.parts_list.lista)
            self.parts_collected += value
            # obstacles effects
            self.obstacles_list.remover_obstaculos()
            self.obstacles_list.criar_obstaculos()
            # Refresh screen
            # print(f"words: {self.digited_word_number}; time: {self.time_passed}")
            self.speed = self.digited_word_number * 60 // self.time_passed
            self.run = self.continue_game()
            self.refresh_game()
        return "continue"
