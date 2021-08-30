# import menu_classes as cm
import Auxiliary_Functionalities as Af
import game_classes as gc
# import link_functions as lf
import entity_classes as ce
# import math
# import time
import pygame


# Creates a world where Car-movement-data can be extracted
class Data_World:
    def __init__(self, screen_i):
        self.screen = screen_i
        # Game objects
        self.car = ce.Car()
        self.road = ce.Road()
        self.STE = ce.Space_Time_Entity()
        self.obstacles_list = ce.Obstacles()
        self.parts_list = ce.parts()
        self.parts_collected = 0
        self.hud_image = Af.load_image("HUD/HUD_background.png")
        # loop stuff
        self.clock = pygame.time.Clock()
        self.frame_rate = 1  # must not be multiple of 10
        self.run = True
        self.choice = None
        self.time_passed = 0
        self.total_time = 0.0
        self.resistance = True
        self.seen_values = []
        self.choices_made = []

    def refresh_game(self):
        self.screen.blit(self.hud_image, (0, 308))
        for entity in [self.road, self.parts_list, self.obstacles_list, self.car]:
            entity.draw(self.screen)
        self.STE.draw(self.screen, self.car.x, self.car.y)
        pygame.display.update()

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

    def manage_buttons(self, button):
        # self.car.vision(self.screen)
        # self.seen_values.append(self.car.seen_values)
        if button == pygame.K_UP:
            # self.choices_made.append("UP")
            self.car.movement("UP")
        elif button == pygame.K_DOWN:
            # self.choices_made.append("DWN")
            self.car.movement("DWN")
        elif button == pygame.K_RIGHT:
            # self.choices_made.append("UP")
            self.car.x += 10
        elif button == pygame.K_LEFT:
            # self.choices_made.append("DWN")
            self.car.x -= 10
        elif button == pygame.K_PLUS:
            if self.frame_rate < 90:
                self.frame_rate += 10
                print(self.frame_rate)
        elif button == pygame.K_MINUS:
            if self.frame_rate > 10:
                self.frame_rate -= 10
                print(self.frame_rate)

    def save_data(self):
        file = open("training data.txt", "a")
        for line in self.seen_values:
            file.write(str(line))
            file.write("\n")
        file.write(str(self.choices_made))

    def continue_game(self):
        return self.resistance

    def initiate_test(self):
        while self.run:
            # terminate execution
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                if event.type == pygame.KEYDOWN:
                    self.manage_buttons(event.key)
    # parts effects
            self.parts_list.remover_parts(self.obstacles_list.internal_list)
            self.parts_list.create_parts()
    # car movement
            self.car_movement_y()
    # collision & damage
            self.parts_list.internal_list, value = self.car.parts_collision(self.parts_list.internal_list)
            self.parts_collected += value
            self.STE.take_action(self.car.x)
            # print(f"Lightning should be shown: {self.STE.draw_lightning}")
    # obstacles effects
            self.obstacles_list.remove_obstacles()
            self.obstacles_list.create_obstacles()
    # Refresh screen
            if self.run:
                self.run = self.continue_game()
            self.refresh_game()
            self.time_passed += self.clock.tick(self.frame_rate) / 990
        # self.save_data()
        Af.stop_all_sounds()
        Af.play(gc.game_over_sound)
        return False  # if it gets here, it means it not good enough


SCREEN = pygame.display.set_mode((Af.SCREEN_LENGTH, Af.SCREEN_WIDTH))
World = Data_World(SCREEN)
World.initiate_test()

