# import menu_classes as cm
# import Auxiliary_Functionalities as Af
# import game_classes as gc
# import link_functions as lf
# import entity_classes as ce
import shutil as shut
from pathlib import Path
import os

# import math
# import time
# import pygame


# Creates a world where Car-movement-data can be extracted
"""class Data_World:
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

    def car_movement_x(self):
        if self.car.x > Af.CAR_MAX_DISTANCE:
            self.car.x = Af.CAR_MAX_DISTANCE
        elif self.car.x < Af.CAR_MIN_DISTANCE:
            self.car.x = Af.CAR_MIN_DISTANCE

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
            print(self.car.x)
        elif button == pygame.K_LEFT:
            # self.choices_made.append("DWN")
            self.car.x -= 10
            print(self.car.x)
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
            self.car_movement_x()
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
"""

# SCREEN = pygame.display.set_mode((Af.SCREEN_LENGTH, Af.SCREEN_WIDTH))
"""World = Data_World(SCREEN)
World.initiate_test()"""

"""menu = cm.Winner_Menu(SCREEN)
menu.display_menu()"""

"""file = open("my name encrypted.txt", "w")
file.write(Af.encrypt_line("Raffaele Fiorillo"))
file.close()"""

directories = ["saves/R.F.J.8/data.txt", "saves/Raffaele/data.txt", "saves/teste/data.txt",
               "saves/R.F.J.8/next_level.txt", "saves/Raffaele/next_level.txt", "saves/teste/next_level.txt",
               "parameters/levels info/1.txt", "parameters/levels info/2.txt", "parameters/levels info/3.txt",
               "parameters/levels info/4.txt", "parameters/levels info/5.txt", "parameters/levels info/6.txt",
               "parameters/levels info/7.txt", "parameters/levels info/8.txt", "parameters/levels info/9.txt",
               "parameters/levels info/10.txt", "parameters/levels info/11.txt", "parameters/levels info/12.txt",
               "parameters/levels info/13.txt", "texts/1.txt", "texts/2.txt", "texts/3.txt", "texts/4.txt",
               "texts/5.txt", "texts/6.txt", "texts/7.txt", "texts/8.txt", ]


# Af.encrypt_all_files(directories)

# [print(f'"{directory}",') for directory in directories]


def create_executable():
    print("\n ############### Creating File ###############\n")
    ico_directory = "images\general\\fire.ICO"  # location of the Icon that will be set to the .exe
    options = "--onefile --noconsole --windowed --name Game"  # options for the creation of the .exe
    command = f"pyinstaller {options} --icon={ico_directory} main.py"
    os.system(f'cmd /c "{command}"')  # create Game.exe with *pyinstaller* set with the options defined before
    print("\n ############### Moving file ###############\n")
    shut.move("dist/Game.exe", Path.cwd())  # Move Game.exe from source to destination (Destination is the current path)
    print("\n ############### File Moved ###############\n")
    print("\n ############### File Created ###############\n")


def create_game_executable():
    print("\n ############### Building Game ###############\n")
    print("\n ############## Authentication ###############\n")
    if input("Password: ") != "Raffaele8":
        print("Error: Wrong Password")
        print("\n ######### Authentication Failed #############\n")
        return None
    print("\n ######## Authentication Successful ##########\n")
    os.remove('Game.exe')  # delete the old version of the game
    create_executable()  # create the new version of the game
    # delete the unnecessary files created in the previous step
    print("\n ############### Deleting Trash ###############\n")
    shut.rmtree("dist")
    shut.rmtree("build")
    os.remove("Game.spec")
    print("\n ############### Trash Deleted ###############\n")
    print("\n ############### Game Built ###############\n")


if __name__ == "__main__":
    create_game_executable()
