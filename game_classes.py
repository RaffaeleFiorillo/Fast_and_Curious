# This module contains two classes. This classes are responsible for managing the game's graphics,input and output (HUD)
# They are both similar and most of the things they do are the same. They only differ in duration and returned values.
# They utilize classes of the "entity_classes" module. This way we can think about both of them like an interaction
# management system for the game's entities (dictating rules, changing attributes based on certain events, etc.)
# ----------------------------------------------- IMPORTS --------------------------------------------------------------
import entity_classes as ce
import pygame
import functions as f

# ----------------------------------------------- SOUNDS ---------------------------------------------------------------
go_sound = f.load_sound("game/car_ignition.WAV")                # sound of after the final count down alert (GO)
count_down_sound = f.load_sound("game/count_down.WAV")          # sound of the usual count down (3, 2, 1)
space_time_hit_sound = f.load_sound("game/space_time_hit.WAV")  # sound of the space-time entity hitting
tic_toc_sound = f.load_sound("game/tic_toc.WAV")                # sound of the final clock ticking
game_over_sound = f.load_sound("game/game_over.WAV")            # sound of the match ending
start_sound = f.load_sound("game/go.WAV")                       # sound of the GO image
wrong_letter_sound = f.load_sound("game/letter_wrong.WAV")      # sound of the user typing a character wrong


# ----------------------------------------------- CLASSES --------------------------------------------------------------
# Creates a game where there is a time limit of 60 seconds
class Mission_AI:
    def __init__(self, screen):
        self.screen = screen
        # Game objects
        self.sp_ti_entity = ce.Space_Time_Entity()
        self.car = ce.Car()
        self.road = ce.Road()
        self.obstacles_list = ce.Obstacles()
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
        self.max_lines = 8
        self.total_words = 0.0
        self.total_words_all = 0.0
        self.correct_letters = 0
        self.current_word_index = 0
        self.text_to_write = None
        self.set_up_texts(True)
        # sound stuff
        self.play_tic_toc = True
        # loop stuff
        self.terminate = False
        self.clock = pygame.time.Clock()
        self.run = True
        self.time_passed = 0
        self.choice = 0

    def set_up_texts(self, first=False):
        if not first:
            self.terminate = True
            return None
        self.text_name = f.choice(f.get_text_names())[:-4]
        self.text_to_write_image = pygame.image.load(f"images/texts/{self.text_name}.png")
        lines = open(f"texts/{self.text_name}.txt", "r").readlines()
        self.text_to_write = [line.split(" ") for line in lines[1:]]
        self.screen.blit(self.text_to_write_image, (280, 320))
        image = f.get_text_images("")
        self.written_text_images = [image, image, image, image, image, image, image, image]
        self.written_text = [[""]]
        self.line = 0
        self.max_lines = int(lines[0])
        pygame.display.update()

    def control_resistance_energy(self):
        if self.car.x <= 290 and int(self.time_passed) % 2:
            f.play(space_time_hit_sound)
            self.resistance -= 0.08*((300-self.car.x) // 8)
            self.energy -= 0.2 * ((300 - self.car.x) // 8)
        if self.energy > 0:
            self.energy -= 0.5

    def refresh_game(self):
        entities = [self.road, self.parts_list, self.obstacles_list, self.car, self.sp_ti_entity]
        self.screen.blit(pygame.image.load("images/HUD/HUD_background.png"), (0, 308))
        for entity in entities:
            entity.draw(self.screen)
        time = 60-int(self.time_passed)
        self.hud.draw(self.parts_collected, time, self.speed, self.precision, self.energy, self.resistance)
        self.display_text()
        self.screen.blit(self.text_to_write_image, (280, 320))
        if self.line == self.max_lines:
            self.set_up_texts()
        pygame.display.update()

    def car_movement_y(self):
        if not self.car.keep_moving and self.car.y in self.car.y_values:
            self.car.vision(self.screen)
            self.choice = f.make_a_choice(self.car.seen_values)
        if self.choice == 1:
            self.car.movement("DWN")
            self.car.direction = "DWN"
        elif self.choice == -1:
            self.car.movement("UP")
            self.car.direction = "UP"
        self.car.continue_mov()

    def car_movement_x(self):
        self.car.damage_period += 0.05
        if self.car.damage_period >= 1.0:
            self.car.x -= 1
            self.car.damage_period = 0
        if self.car.x > 350:
            self.car.x = 350

    def last_letter_correct(self):
        last_letter_index = len(self.written_text[-1][-1])-1
        # every last written letter is wrong if the written word is longer than original
        if last_letter_index > len(self.text_to_write[self.line][self.current_word_index])-1:
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
            # go to next line in case written words are numerically equal to words to write
            if len(self.written_text[self.line]) == len(self.text_to_write[self.line]):
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
            # prevents from going beyond deleting last word
            elif self.written_text[-1] == [""] and len(self.written_text) == 1:
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
            else:
                f.play(wrong_letter_sound)

    def display_text(self):
        coordinates = [(290, 454), (290, 469), (290, 484), (290, 499), (290, 514), (290, 529), (290, 544), (290, 559)]
        self.written_text_images[self.line] = f.get_text_images(self.written_text[-1])
        for image, coo in zip(self.written_text_images, coordinates):
            self.screen.blit(image, coo)
        if int(self.time_passed+self.time_passed*1.5) % 2:  # make the cursor blink periodically
            if self.written_text[-1][-1] == "" and self.written_text[-1] != [""]:
                self.screen.blit(self.cursor, (coordinates[self.line][0]+
                                               self.written_text_images[self.line].get_size()[0]+5,
                                               coordinates[self.line][1]+3))
            else:
                self.screen.blit(self.cursor, (coordinates[self.line][0]+
                                               self.written_text_images[self.line].get_size()[0],
                                               coordinates[self.line][1]+3))

    def continue_game(self):
        if int(self.resistance) <= 0:
            return False
        elif int(self.time_passed) >= 60:
            return False
        elif self.terminate:
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
        next_image = 1
        current = 0
        f.play(count_down_sound)
        while self.time_passed < 4.5:
            self.time_passed += self.clock.tick(30) / 990
            if self.time_passed <= 4:
                current = int(self.time_passed) % 4
            self.refresh_game()
            self.screen.blit(pygame.image.load(f"images/HUD/count_down/{current}.png"), (420, 150))
            pygame.display.update()
            if current == next_image:
                if next_image< 3:
                    f.play(count_down_sound)
                else:
                    f.play(start_sound)
                next_image += 1
        f.play(go_sound)
        f.play_music()
        self.time_passed = 0
        while self.run:
            self.time_passed += self.clock.tick(30) / 990
    # terminate execution
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
    # controls
                if event.type == pygame.KEYDOWN:
                    self.manage_buttons(pygame.key.get_pressed(), event)
    # parts effects
            self.parts_list.remover_parts(self.obstacles_list.internal_list)
            self.parts_list.create_parts()
    # car movement
            self.car_movement_y()
            self.car_movement_x()
    # collision & damage
            if self.time_passed >= 4:
                if damage_count >= 0.5:
                    if self.car.obstacle_collision(self.obstacles_list.internal_list):
                        self.resistance -= 4
                        self.car.x -= 10
                        damage_count = 0
                else:
                    damage_count += 0.01
            self.control_resistance_energy()
            self.parts_list.internal_list, value = self.car.parts_collision(self.parts_list.internal_list)
            self.parts_collected += value
    # obstacles effects
            self.obstacles_list.remove_obstacles()
            self.obstacles_list.create_obstacles()
    # Refresh screen
            self.update_speed()
            self.update_precision()
            if self.run:
                self.run = self.continue_game()
            if int(self.time_passed) == 51 and self.play_tic_toc:
                f.play(tic_toc_sound)
                self.play_tic_toc = False
            self.refresh_game()
        f.stop_all_sounds()
        f.play(game_over_sound)
        return self.precision, self.speed, self.parts_collected, self.resistance, self.time_passed


# Creates a game where the time limit is only imposed by the user's skills
class Mission_PARTS:
    def __init__(self, screen):
        self.screen = screen
        # Game objects
        self.sp_ti_entity = ce.Space_Time_Entity()
        self.car = ce.Car()
        self.road = ce.Road()
        self.obstacles_list = ce.Obstacles()
        self.parts_list = ce.parts()
        self.parts_collected = 0
        # HUD stuff
        self.energy = 100
        self.resistance = 100
        self.hud = ce.HUD(self.screen)
        self.speed = 0
        self.precision = 100
        self.speed_list = []
        self.precision_list = []
        # text stuff
        self.cursor = pygame.image.load("images/texts/cursor.png")
        self.written_text = [[""]]
        self.text_name = None
        self.text_to_write_image = None
        image = f.get_text_images("")
        self.written_text_images = [image, image, image, image, image, image, image, image]
        self.line = 0
        self.max_lines = 8
        self.total_words = 0.0
        self.correct_letters = 0
        self.current_word_index = 0
        self.text_to_write = None
        self.set_up_texts(True)
        # loop stuff
        self.clock = pygame.time.Clock()
        self.run = True
        self.time_passed = 0
        self.total_time = 0.0
        self.choice = 0

    def set_up_texts(self, first=False):
        self.text_name = f.choice(f.get_text_names())[:-4]
        self.text_to_write_image = pygame.image.load(f"images/texts/{self.text_name}.png")
        lines = open(f"texts/{self.text_name}.txt", "r").readlines()
        self.text_to_write = [line.split(" ") for line in lines[1:]]
        self.screen.blit(self.text_to_write_image, (280, 320))
        image = f.get_text_images("")
        self.written_text_images = [image, image, image, image, image, image, image, image]
        self.written_text = [[""]]
        self.line = 0
        self.max_lines = int(lines[0])
        if not first:
            self.speed_list.append(self.speed)
            self.precision_list.append(self.precision)
            self.total_time += self.time_passed
        self.total_words = 0.0
        self.time_passed = 0.0
        self.correct_letters = 0
        self.current_word_index = 0
        pygame.display.update()

    def control_resistance_energy(self):
        if self.car.x <= 290 and int(self.time_passed) % 2:
            f.play(space_time_hit_sound)
            self.resistance -= 0.08*((300-self.car.x) // 8)
            self.energy -= 0.2 * ((300 - self.car.x) // 8)
        if self.energy > 0:
            self.energy -= 0.5

    def refresh_game(self):
        entities = [self.road, self.parts_list, self.obstacles_list, self.car, self.sp_ti_entity]
        self.screen.blit(pygame.image.load("images/HUD/HUD_background.png"), (0, 308))
        for entity in entities:
            entity.draw(self.screen)
        self.hud.draw(self.parts_collected, "i", self.speed, self.precision, self.energy, self.resistance)
        self.display_text()
        self.screen.blit(self.text_to_write_image, (280, 320))
        if self.line == self.max_lines:
            self.set_up_texts()
        pygame.display.update()

    def car_movement_y(self):
        if not self.car.keep_moving and self.car.y in self.car.y_values:
            self.car.vision(self.screen)
            self.choice = f.make_a_choice(self.car.seen_values)
        if self.choice == 1:
            self.car.movement("DWN")
            self.car.direction = "DWN"
        elif self.choice == -1:
            self.car.movement("UP")
            self.car.direction = "UP"
        self.car.continue_mov()

    def car_movement_x(self):
        self.car.damage_period += 0.05
        if self.car.damage_period >= 1.0:
            self.car.x -= 1
            self.car.damage_period = 0
        if self.car.x > 350:
            self.car.x = 350

    def last_letter_correct(self):
        last_letter_index = len(self.written_text[-1][-1])-1
        # every last written letter is wrong if the written word is longer than original
        if last_letter_index > len(self.text_to_write[self.line][self.current_word_index])-1:
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
            # go to next line in case written words are numerically equal to words to write
            if len(self.written_text[self.line]) == len(self.text_to_write[self.line]):
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
            # prevents from going beyond deleting last word
            elif self.written_text[-1] == [""] and len(self.written_text) == 1:
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
            else:
                f.play(wrong_letter_sound)

    def display_text(self):
        coordinates = [(290, 454), (290, 469), (290, 484), (290, 499), (290, 514), (290, 529), (290, 544), (290, 559)]
        self.written_text_images[self.line] = f.get_text_images(self.written_text[-1])
        for image, coo in zip(self.written_text_images, coordinates):
            self.screen.blit(image, coo)
        if int(self.time_passed+self.time_passed*1.5) % 2:  # make the cursor blink periodically
            if self.written_text[-1][-1] == "" and self.written_text[-1] != [""]:
                self.screen.blit(self.cursor, (coordinates[self.line][0]+
                                               self.written_text_images[self.line].get_size()[0]+5,
                                               coordinates[self.line][1]+3))
            else:
                self.screen.blit(self.cursor, (coordinates[self.line][0]+
                                               self.written_text_images[self.line].get_size()[0],
                                               coordinates[self.line][1]+3))

    def continue_game(self):
        if int(self.resistance) <= 0:
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
        next_image = 1
        current = 0
        f.play(count_down_sound)
        while self.time_passed < 4.5:
            self.time_passed += self.clock.tick(30) / 990
            if self.time_passed <= 4:
                current = int(self.time_passed) % 4
            self.refresh_game()
            self.screen.blit(pygame.image.load(f"images/HUD/count_down/{current}.png"), (420, 150))
            pygame.display.update()
            if current == next_image:
                if next_image< 3:
                    f.play(count_down_sound)
                else:
                    f.play(start_sound)
                next_image += 1
        f.play_music()
        f.play(go_sound)
        self.time_passed = 0
        while self.run:
            self.time_passed += self.clock.tick(30) / 990
    # terminate execution
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                if event.type == pygame.KEYDOWN:
                    self.manage_buttons(pygame.key.get_pressed(), event)
    # parts effects
            self.parts_list.remover_parts(self.obstacles_list.internal_list)
            self.parts_list.create_parts()
    # car movement
            self.car_movement_y()
            self.car_movement_x()
    # collision & damage
            if self.time_passed >= 4:
                if damage_count >= 0.5:
                    if self.car.obstacle_collision(self.obstacles_list.internal_list):
                        self.resistance -= 4
                        self.car.x -= 10
                        damage_count = 0
                else:
                    damage_count += 0.01
            self.control_resistance_energy()
            self.parts_list.internal_list, value = self.car.parts_collision(self.parts_list.internal_list)
            self.parts_collected += value
    # obstacles effects
            self.obstacles_list.remove_obstacles()
            self.obstacles_list.create_obstacles()
    # Refresh screen
            self.update_speed()
            self.update_precision()
            if self.run:
                self.run = self.continue_game()
            self.refresh_game()
        f.stop_all_sounds()
        f.play(game_over_sound)
        self.set_up_texts()
        pre = sum(self.precision_list) // len(self.precision_list)
        speed = sum(self.speed_list) // len(self.speed_list)
        return pre, speed, self.parts_collected, self.total_time
