import pygame
from pygame.event import Event
import src.entity_classes as ec
from src.auxiliary_modules import *
from src.auxiliary_modules import user_data_management as udm, global_variables as gv, useful_functions as rf
from .sounds import wrong_letter_sound, count_down_sound, start_sound, go_sound, game_over_sound


# Parent Class for managing a Mission-Type World
class Mission:
    def __init__(self, screen):
        self.screen = screen
        # Game objects
        self.sp_ti_entity = ec.SpaceTimeEntity()
        self.car = ec.Car()
        self.road = ec.Road()
        self.obstacles_list = ec.Obstacles()
        self.parts_list = ec.Parts()
        self.parts_collected = 0
        # HUD stuff
        self.background = hud.load_hud_background()  # graphics.load_image("HUD/HUD_background.png")
        self.energy = 100
        self.resistance = 100
        self.hud = ec.HUD(self.screen)
        self.speed = 0
        self.precision = 100
        # text stuff
        self.text_coordinates = hud.load_text_coordinates()
        self.cursor = graphics.load_image("texts/cursor.png")
        self.written_text = [[""]]
        self.text_name = None
        self.text_to_write_image = None
        image = graphics.get_text_images("")
        self.written_text_images = [image, image, image, image, image, image, image, image]
        self.line = 0
        self.max_lines = 8
        self.total_words = 0.0
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
        self.choice = None

    def set_up_texts(self, first=False):
        self.text_name = rf.choice(udm.get_text_names())[:-4]  # chooses random text from existing texts
        self.text_to_write_image = graphics.load_image(f"texts/{self.text_name}.png")  # loads the text's image
        lines = files.read_file_content(f"texts/{self.text_name}.txt")  # loads the text's content
        self.text_to_write = [line.split(" ") for line in lines[1:]]  # sets the text in proper format
        self.screen.blit(self.text_to_write_image, (280, 320))
        image = graphics.get_text_images("")  # turns written text into images to display
        self.written_text_images = [image, image, image, image, image, image, image, image]
        self.written_text = [[""]]
        self.line = 0  # sets current line to 0 (beginning)
        self.max_lines = int(lines[0])  # gets the number of lines that the chosen text has

    def control_resistance_energy(self):
        if self.car.x <= gv.CAR_STE_MIN_DAMAGE_DISTANCE and int(self.time_passed) % 2:
            self.sp_ti_entity.take_action(self.car.x)
            if not self.sp_ti_entity.already_hit_target:
                damage = 0.5*(gv.CAR_STE_MIN_DAMAGE_DISTANCE-self.car.x)  # proportional damage<->distance
                self.resistance -= damage
            self.energy -= 1.6 * (gv.CAR_STE_MIN_DAMAGE_DISTANCE - self.car.x)
            self.sp_ti_entity.already_hit_target = True  # prevents lightning from hitting twice
        else:
            self.sp_ti_entity.already_hit_target = False  # enables lightning again
        self.energy -= 0.5

        if self.energy < 0:
            self.energy = 0

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

    def car_movement_x(self):
        self.car.damage_period += 0.05
        if self.car.damage_period >= 1.0:
            self.car.x -= 10
            self.car.damage_period = 0
        if self.car.x > gv.CAR_MAX_DISTANCE:
            self.car.x = gv.CAR_MAX_DISTANCE
        elif self.car.x < gv.CAR_MIN_DISTANCE:
            self.car.x = gv.CAR_MIN_DISTANCE

    def last_letter_correct(self):  # returns True if last letter is correct, False if not
        last_letter_index = len(self.written_text[-1][-1])-1
        # every last written letter is wrong if the written word is longer than original
        if last_letter_index > len(self.text_to_write[self.line][self.current_word_index])-1:
            self.resistance -= 2  # each wrong letter will make the player loose 2% of the total resistance
            if self.car.speed > 5:
                self.car.speed -= 4
            return False
        elif self.written_text[-1][-1][-1] == self.text_to_write[self.line][self.current_word_index][last_letter_index]:
            if self.car.speed < gv.CAR_MAX_SPEED-1:  # increase car's speed if needed
                self.car.speed += 2
            self.car.x += 6
            self.car.activate_fire(False)  # activates red fire (less powerful-> moves one pixel)
            self.energy += 8
            if self.energy >= 100:
                self.car.activate_fire(True)  # activates blue fire (most powerful-> moves 10 pixels)
                if self.car.x < gv.CAR_MAX_DISTANCE:
                    self.car.x += 10
                self.energy = 75  # reduce energy when reach maximum to simulate blue-fire usage and forward sprint
            return True
        if self.car.speed > 5:  # make sure car's speed is never lower than 0
            self.car.speed -= 4
        self.resistance -= 2  # each wrong letter will make the player loose 2% of the total resistance
        return False

    def manage_buttons(self, event: Event):
        if event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
            if self.line < 7:  # prevents from adding too much lines
                self.written_text.append([""])
                self.line += 1
                self.current_word_index = 0
            else:  # prepare another text to write
                pass
        elif event.key == pygame.K_SPACE:
            # go to next line in case written words are numerically equal to words to write
            if len(self.written_text[self.line]) == len(self.text_to_write[self.line]):
                self.written_text.append([""])
                self.line += 1
                self.current_word_index = 0
            if self.written_text[-1][-1] != "":  # prevents adding new words in case current word is empty
                self.written_text[self.line].append("")
                self.current_word_index += 1
        elif event.key == pygame.K_BACKSPACE:
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
                audio.play(wrong_letter_sound)

    def display_text(self):
        self.written_text_images[self.line] = graphics.get_text_images(self.written_text[-1])
        for image, coo in zip(self.written_text_images, self.text_coordinates):
            self.screen.blit(image, coo)
        if int(self.time_passed+self.time_passed*1.5) % 2:  # make the cursor blink periodically
            if self.written_text[-1][-1] == "" and self.written_text[-1] != [""]:
                self.screen.blit(self.cursor, (self.text_coordinates[self.line][0] +
                                               self.written_text_images[self.line].get_size()[0]+5,
                                               self.text_coordinates[self.line][1]+3))
            else:
                self.screen.blit(self.cursor, (self.text_coordinates[self.line][0] +
                                               self.written_text_images[self.line].get_size()[0],
                                               self.text_coordinates[self.line][1]+3))

    def hud_time(self):
        pass

    def take_exclusive_class_action(self):  # each Mission could do something different for each iteration
        pass

    def refresh_game(self, other_entity: (pygame.Surface, (int, int)) = ()):
        self.screen.blit(self.background, (0, 308))
        for entity in [self.road, self.parts_list, self.obstacles_list, self.car]:
            entity.draw(self.screen)
        if other_entity:
            self.screen.blit(other_entity[0], other_entity[1])
        self.sp_ti_entity.draw(self.screen, self.car.x, self.car.y)
        self.hud.draw(self.parts_collected, self.hud_time(), self.speed, self.precision, self.energy, self.resistance)
        self.display_text()
        self.screen.blit(self.text_to_write_image, (280, 320))
        if self.line == self.max_lines:
            self.set_up_texts()
        self.take_exclusive_class_action()  # if a Mission wants to do something additional
        pygame.display.update()

    def display_countdown(self):
        count_down_images = [graphics.load_image(f"HUD/count_down/{image_index}.png") for image_index in range(4)]
        next_image, time_passed = 1, 0
        coordinates = {0: (440, 150), 1: (440, 150), 2: (450, 160), 3: (400, 150)}
        audio.play(count_down_sound)
        while time_passed < 4.5:
            self.clock.tick(gv.FRAME_RATE)
            time_passed += 0.034
            current_image_index = int(time_passed)
            try:
                self.refresh_game((count_down_images[current_image_index], coordinates[current_image_index]))
            except IndexError:
                self.refresh_game()
                continue
            if current_image_index == next_image:
                if next_image < 3:
                    audio.play(count_down_sound)
                else:
                    audio.play(start_sound)
                next_image += 1
        pygame.event.clear()  # all pressed buttons are dismissed in this phase
        audio.play(go_sound)
        audio.play_music()

    def update_speed(self):
        self.total_words = (sum([len(word) for line in self.written_text for word in line]))/5  # characters_numb/5
        self.speed = self.total_words*60/self.time_passed  # written_words*seconds_per_minute/time_passed

    def update_precision(self):
        total_letters = sum([sum([len(word) for word in line]) for line in self.written_text])
        if total_letters:
            self.precision = self.correct_letters/total_letters * 100
        else:
            self.precision = 100

    def continue_game(self):
        pass

    def manage_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # terminate execution
                self.run = False
            elif event.type == pygame.KEYDOWN:
                self.manage_buttons(event)

    @staticmethod
    def game_over():
        audio.stop_all_sounds()
        audio.play(game_over_sound)

    def game_loop(self):
        damage_count = 4  # waiting time the car has before taking more damage
        self.display_countdown()
        while self.run:
            self.time_passed += self.clock.tick(gv.FRAME_RATE) / 1000
    # input Management
            self.manage_events()
    # parts effects
            self.parts_list.remove_parts(self.obstacles_list.internal_list)
            self.parts_list.create_parts()
    # car movement
            self.car_movement_y()
            self.car_movement_x()
    # collision & damage
            if damage_count >= 50:
                if self.car.obstacle_collision(self.obstacles_list.internal_list):  # damage by obstacle collision
                    self.resistance -= 10
                    self.car.x -= 20
                    damage_count = 0
            else:
                damage_count += 1
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


# Creates a game where there is a time limit of 60 seconds to type a given text
class MissionAI(Mission):
    def __init__(self, screen):
        super().__init__(screen)
        self.total_words_all = 0.0

    def set_up_texts(self, first=False):
        if not first:
            self.terminate = True
            return None
        super(MissionAI, self).set_up_texts()
        pygame.display.update()

    def hud_time(self):  # returns what to display on the clock of the HUD interface.
        return 60-round(self.time_passed)

    def continue_game(self):
        if int(self.resistance) <= 0:
            return False
        elif int(self.time_passed) >= 60:
            return False
        elif self.terminate:
            return False
        return True

    def game_loop(self):
        super(MissionAI, self).game_loop()
        self.game_over()
        return self.precision, self.speed, self.parts_collected, self.resistance, self.time_passed, self.terminate


# Creates a game where the time limit is only imposed by the User's typing skills
class MissionPARTS(Mission):
    def __init__(self, screen):
        super().__init__(screen)
        # performance stuff
        self.speed_list = []
        self.precision_list = []
        # loop stuff
        self.total_time = 0.0

    def set_up_texts(self, first=False):
        super(MissionPARTS, self).set_up_texts()  # sets up next text to be displayed
        if not first:  # if it's not the first text to be loaded:
            self.speed_list.append(self.speed)
            self.precision_list.append(self.precision)
            self.total_time += self.time_passed
        self.total_words = 0.0
        self.time_passed = 0.0
        self.correct_letters = 0
        self.current_word_index = 0
        pygame.display.update()

    def hud_time(self):  # returns what to display on the clock of the HUD interface. "i" makes it "infinite"
        return "i"

    def continue_game(self):
        if int(self.resistance) <= 0:
            return False
        return True

    def player_is_cheating(self):
        # makes sure there is not a DivisionByZero error
        # player quit the game without ending any text
        if not len(self.precision_list):
            return True
        # player just pretended writing/only pressed Enter
        if sum(self.speed_list)/len(self.speed_list) <= 10 and len(self.speed_list) >= 5:
            return True
        return False

    def game_loop(self):
        super(MissionPARTS, self).game_loop()
        self.game_over()  # takes actions relative to the game being over
        if self.player_is_cheating():  # apply a cheating detection system
            return 0, 0, -1000, 0, 0  # The results of a match are nullified and player looses 1000 parts
        precision = sum(self.precision_list) // len(self.precision_list)
        speed = sum(self.speed_list) // len(self.speed_list)
        max_speed = max(self.speed_list)
        return precision, speed, self.parts_collected, self.total_time, max_speed
