import classes_entidades as ce
from random import choice
import pygame
import functions as f


class Mission_AI:
    def __init__(self, screen):
        self.screen = screen
        # Game objects
        self.sp_ti_entity = ce.space_time_entity()
        self.car = ce.carro()
        self.estrada = ce.estrada()
        self.obstacles_list = ce.obstaculos()
        self.parts_list = ce.parts()
        self.parts_collected = 0
        # HUD stuff
        self.energy = 100
        self.resistance = 100
        self.hud = ce.HUD(self.screen)
        self.speed = 0
        self.precision = 100
        # text stuff
        self.cursor = pygame.image.load("images/texts/cursor.png")
        self.written_text = [[""]]
        self.text_name = None
        self.text_to_write_image = None
        image = f.get_text_images("")
        self.written_text_images = [image, image, image, image, image, image, image, image]
        self.line = 0
        self.total_words = 0.0
        self.correct_letters = 0
        self.current_word_index = 0
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
        self.text_to_write = [line.split(" ") for line in open(f"texts/{self.text_name}.txt", "r").readlines()]
        self.screen.blit(self.text_to_write_image, (280, 320))
        pygame.display.update()

    def control_resistance_energy(self):
        if self.car.x <= 290 and int(self.time_passed) % 2:
            self.resistance -= 0.08*((300-self.car.x) // 8)
            self.energy -= 0.2 * ((300 - self.car.x) // 8)
        if self.energy > 0:
            self.energy -= 0.5

    def refresh_game(self):
        entidades = [self.estrada, self.parts_list, self.obstacles_list, self.car, self.sp_ti_entity]
        self.screen.blit(pygame.image.load("images/HUD/HUD_background.png"), (0, 308))
        for entidade in entidades:
            entidade.draw(self.screen)
        time = 60-int(self.time_passed)
        self.hud.draw(self.parts_collected, time, self.speed, self.precision, self.energy, self.resistance)
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
        self.car.damage_period += 0.05
        if self.car.damage_period >= 1.0:
            self.car.x -= 1
            self.car.damage_period = 0
        if self.car.x > 350:
            self.car.x = 350

    def last_letter_correct(self):
        last_letter_index = len(self.written_text[-1][-1])-1
        if last_letter_index > len(self.text_to_write[self.line][self.current_word_index])-1:  #every last written letter is wrong if the written word is longer than original
            if self.car.speed > 3:
                self.car.speed -= 1
            return False
        elif self.written_text[-1][-1][-1] == self.text_to_write[self.line][self.current_word_index][last_letter_index]:
            if self.car.speed < 7:
                self.car.speed += 1
            self.car.x += 1
            self.car.activate_fire(False)
            self.energy += 8
            if self.energy > 100:
                self.car.activate_fire(True)
                if self.car.x < 350:
                    self.car.x += 10
                self.energy = 78
            return True
        if self.car.speed > 3:
            self.car.speed -= 1
        return False

    def manage_buttons(self, keys, event):
        if keys[pygame.K_KP_ENTER] or keys[pygame.K_RETURN]:
            if self.line < 7:  # prevents from adding too much lines
                self.written_text.append([""])
                self.line += 1
                self.current_word_index = 0
            else:  # prepare another text to write
                pass
        elif keys[pygame.K_SPACE]:
            if len(self.written_text[self.line]) == len(self.text_to_write[self.line]):  # go to next line in case written words are numericaly equal to words to wrtite
                self.written_text.append([""])
                self.line += 1
                self.current_word_index = 0
            if self.written_text[-1][-1] != "":  # prevents adding new words in case current word is empty
                self.written_text[self.line].append("")
                self.current_word_index += 1
        elif keys[pygame.K_BACKSPACE]:
            if self.written_text[-1] == [""] and len(self.written_text) != 1:  # if line is empty go to previous
                self.written_text.pop()
                self.line -= 1
                self.current_word_index = len(self.written_text[-1]) - 1
            elif self.written_text[-1] == [""] and len(self.written_text) == 1:  # prevents from going beyond deleting last word
                pass
            elif self.written_text[-1][-1] != "":  # checks if a word is not empty to make sure letter can be deleted
                if self.last_letter_correct():
                    self.correct_letters -= 1
                self.written_text[-1][-1] = self.written_text[-1][-1][:-1]
            elif self.written_text[-1][-1] == "":  # pass to previous word if current is empty
                self.written_text[-1].pop()
                self.current_word_index = len(self.written_text[-1]) - 1
                self.total_words -= 1
        elif event.unicode != "":  # verify that a character is a symbol, letter or number before writing it
            if self.written_text_images[self.line].get_size()[0] > 490:  # checks if line is too long to fit
                self.written_text.append([""])
                self.line += 1
                self.current_word_index = 0
            self.written_text[self.line][self.current_word_index] += event.unicode
            if self.last_letter_correct():
                self.correct_letters += 1

    def display_text(self):
        coordinates = [(290, 454), (290, 469), (290, 484), (290, 499), (290, 514), (290, 529), (290, 544), (290, 559)]
        self.written_text_images[self.line] = f.get_text_images(self.written_text[-1])
        for image, coo in zip(self.written_text_images, coordinates):
            self.screen.blit(image, coo)
        if int(self.time_passed+self.time_passed*1.5) % 2:  # make the cursor blink periodicaly
            if self.written_text[-1][-1] == "" and self.written_text[-1] != [""]:
                self.screen.blit(self.cursor, (coordinates[self.line][0]+self.written_text_images[self.line].get_size()[0]+5,
                                               coordinates[self.line][1]+3))
            else:
                self.screen.blit(self.cursor, (coordinates[self.line][0]+self.written_text_images[self.line].get_size()[0],
                                               coordinates[self.line][1]+3))

    def continue_game(self):
        if not int(self.resistance):
            return False
        elif int(self.time_passed) >= 60:
            return False
        return True

    def update_speed(self):
        self.total_words = sum([len(line) for line in self.written_text]) - 1
        self.speed = self.total_words*60/self.time_passed

    def update_precision(self):
        total_letters = sum([sum([len(word) for word in line]) for line in self.written_text])
        if total_letters:
            self.precision = self.correct_letters/total_letters * 100
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
    # colision & damage
            if self.time_passed >= 4:
                if damage_count >= 0.5:
                    if self.car.colisao_obstaculo(self.obstacles_list.lista):
                        self.resistance -= 4
                        self.car.x -= 10
                        damage_count = 0
                else:
                    damage_count += 0.01
            self.control_resistance_energy()
            self.parts_list.lista, value = self.car.colisao_parts(self.parts_list.lista)
            self.parts_collected += value
    # obstacles effects
            self.obstacles_list.remover_obstaculos()
            self.obstacles_list.criar_obstaculos()
    # Refresh screen
            self.update_speed()
            self.update_precision()
            if self.run:
                self.run = self.continue_game()
            self.refresh_game()
        return self.precision, self.speed, self.parts_collected, self.resistance, self.time_passed


class Mission_PARTS:
    def __init__(self, screen):
        self.screen = screen
        # Game objects
        self.sp_ti_entity = ce.space_time_entity()
        self.car = ce.carro()
        self.estrada = ce.estrada()
        self.obstacles_list = ce.obstaculos()
        self.parts_list = ce.parts()
        self.parts_collected = 0
        # HUD stuff
        self.energy = 100
        self.resistance = 100
        self.hud = ce.HUD(self.screen)
        self.speed = 0
        self.precision = 100
        # text stuff
        self.cursor = pygame.image.load("images/texts/cursor.png")
        self.written_text = [[""]]
        self.text_name = None
        self.text_to_write_image = None
        image = f.get_text_images("")
        self.written_text_images = [image, image, image, image, image, image, image, image]
        self.line = 0
        self.total_words = 0.0
        self.correct_letters = 0
        self.current_word_index = 0
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
        self.text_to_write = [line.split(" ") for line in open(f"texts/{self.text_name}.txt", "r").readlines()]
        self.screen.blit(self.text_to_write_image, (280, 320))
        pygame.display.update()

    def control_resistance_energy(self):
        if self.car.x <= 290 and int(self.time_passed) % 2:
            self.resistance -= 0.08*((300-self.car.x) // 8)
            self.energy -= 0.2 * ((300 - self.car.x) // 8)
        if self.energy > 0:
            self.energy -= 0.5

    def refresh_game(self):
        entidades = [self.estrada, self.parts_list, self.obstacles_list, self.car, self.sp_ti_entity]
        self.screen.blit(pygame.image.load("images/HUD/HUD_background.png"), (0, 308))
        for entidade in entidades:
            entidade.draw(self.screen)
        time = 60-int(self.time_passed)
        self.hud.draw(self.parts_collected, "i", self.speed, self.precision, self.energy, self.resistance)
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
        self.car.damage_period += 0.05
        if self.car.damage_period >= 1.0:
            self.car.x -= 1
            self.car.damage_period = 0
        if self.car.x > 350:
            self.car.x = 350

    def last_letter_correct(self):
        last_letter_index = len(self.written_text[-1][-1])-1
        if last_letter_index > len(self.text_to_write[self.line][self.current_word_index])-1:  #every last written letter is wrong if the written word is longer than original
            if self.car.speed > 3:
                self.car.speed -= 1
            return False
        elif self.written_text[-1][-1][-1] == self.text_to_write[self.line][self.current_word_index][last_letter_index]:
            if self.car.speed < 7:
                self.car.speed += 1
            self.car.x += 1
            self.car.activate_fire(False)
            self.energy += 8
            if self.energy > 100:
                self.car.activate_fire(True)
                if self.car.x < 350:
                    self.car.x += 10
                self.energy = 78
            return True
        if self.car.speed > 3:
            self.car.speed -= 1
        return False

    def manage_buttons(self, keys, event):
        if keys[pygame.K_KP_ENTER] or keys[pygame.K_RETURN]:
            if self.line < 7:  # prevents from adding too much lines
                self.written_text.append([""])
                self.line += 1
                self.current_word_index = 0
            else:  # prepare another text to write
                pass
        elif keys[pygame.K_SPACE]:
            if len(self.written_text[self.line]) == len(self.text_to_write[self.line]):  # go to next line in case written words are numericaly equal to words to wrtite
                self.written_text.append([""])
                self.line += 1
                self.current_word_index = 0
            if self.written_text[-1][-1] != "":  # prevents adding new words in case current word is empty
                self.written_text[self.line].append("")
                self.current_word_index += 1
        elif keys[pygame.K_BACKSPACE]:
            if self.written_text[-1] == [""] and len(self.written_text) != 1:  # if line is empty go to previous
                self.written_text.pop()
                self.line -= 1
                self.current_word_index = len(self.written_text[-1]) - 1
            elif self.written_text[-1] == [""] and len(self.written_text) == 1:  # prevents from going beyond deleting last word
                pass
            elif self.written_text[-1][-1] != "":  # checks if a word is not empty to make sure letter can be deleted
                if self.last_letter_correct():
                    self.correct_letters -= 1
                self.written_text[-1][-1] = self.written_text[-1][-1][:-1]
            elif self.written_text[-1][-1] == "":  # pass to previous word if current is empty
                self.written_text[-1].pop()
                self.current_word_index = len(self.written_text[-1]) - 1
                self.total_words -= 1
        elif event.unicode != "":  # verify that a character is a symbol, letter or number before writing it
            if self.written_text_images[self.line].get_size()[0] > 490:  # checks if line is too long to fit
                self.written_text.append([""])
                self.line += 1
                self.current_word_index = 0
            self.written_text[self.line][self.current_word_index] += event.unicode
            if self.last_letter_correct():
                self.correct_letters += 1

    def display_text(self):
        coordinates = [(290, 454), (290, 469), (290, 484), (290, 499), (290, 514), (290, 529), (290, 544), (290, 559)]
        self.written_text_images[self.line] = f.get_text_images(self.written_text[-1])
        for image, coo in zip(self.written_text_images, coordinates):
            self.screen.blit(image, coo)
        if int(self.time_passed+self.time_passed*1.5) % 2:  # make the cursor blink periodicaly
            if self.written_text[-1][-1] == "" and self.written_text[-1] != [""]:
                self.screen.blit(self.cursor, (coordinates[self.line][0]+self.written_text_images[self.line].get_size()[0]+5,
                                               coordinates[self.line][1]+3))
            else:
                self.screen.blit(self.cursor, (coordinates[self.line][0]+self.written_text_images[self.line].get_size()[0],
                                               coordinates[self.line][1]+3))

    def continue_game(self):
        if not int(self.resistance):
            return False
        return True

    def update_speed(self):
        self.total_words = sum([len(line) for line in self.written_text]) - 1
        self.speed = self.total_words*60/self.time_passed

    def update_precision(self):
        total_letters = sum([sum([len(word) for word in line]) for line in self.written_text])
        if total_letters:
            self.precision = self.correct_letters/total_letters * 100
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
    # colision & damage
            if self.time_passed >= 4:
                if damage_count >= 0.5:
                    if self.car.colisao_obstaculo(self.obstacles_list.lista):
                        self.resistance -= 4
                        self.car.x -= 10
                        damage_count = 0
                else:
                    damage_count += 0.01
            self.control_resistance_energy()
            self.parts_list.lista, value = self.car.colisao_parts(self.parts_list.lista)
            self.parts_collected += value
    # obstacles effects
            self.obstacles_list.remover_obstaculos()
            self.obstacles_list.criar_obstaculos()
    # Refresh screen
            self.update_speed()
            self.update_precision()
            if self.run:
                self.run = self.continue_game()
            self.refresh_game()
        return self.precision, self.speed, self.parts_collected, self.time_passed
