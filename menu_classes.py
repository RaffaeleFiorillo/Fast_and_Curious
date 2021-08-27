# This module contains all the classes responsible for displaying and managing all the Menus and interfaces available
# In the Game. There are also some classes that makes it easier for all the menu classes to do their job.
# Every menu class has three major methods that are very similar if not the same: - display_menu(); - manage_buttons();
# - refresh(); display_menu is the one called after instantiating a new object of a menu class, it is the only method
# used externally of the class. It is the most important, and his job is to display the events of a menu.
# The manage_buttons method is for transforming input from the keyboard into the correct output. And the refresh method
# just updates the menu after every alteration the user makes.

# -------------------------------------------------- IMPORTS -----------------------------------------------------------
import pygame
import Auxiliary_Functionalities as Af


# --------------------------------------------------- SOUNDS ----------------------------------------------------------
button_y_sound = Af.load_sound("menu/button_activation.WAV")     # sound for changing button on y axis
button_x_sound = Af.load_sound("menu/button_lateral.WAV")        # sound for changing button on x axis
volume_change_sound = Af.load_sound("menu/volume_change.WAV")    # sound for changing volume
erase_letter_sound = Af.load_sound("menu/typing.WAV")            # sound for every time a letter is erased
error_sound = Af.load_sound("menu/error_message2.WAV")           # sound for every time an error occurs
success_sound = Af.load_sound("menu/success.WAV")                # sound for every time a success occurs


# ------------------------------------------------ SUPPORT CLASSES -----------------------------------------------------
# These classes are used by the classes that manage the Menus interfaces

class Button:
    def __init__(self, x, y, directory, effect, code):
        self.x = x
        self.y = y
        self.image = Af.load_image(directory)
        self.effect = effect
        self.code = code

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def change_image(self, directory):
        self.image = Af.load_image(directory)


class Button2(Button):
    def __init__(self, x, y, directory, effect, code, id_c):
        super().__init__(x, y, directory, effect, code)
        self.value = 0
        self.effect = "manage"
        self.id = id_c
        self.value_image = Af.load_image(f"menu/buttons/8/7.png")
        self.get_value()

    def get_value(self):
        file = open("saves/active_user.txt", "r")
        line = file.readline()
        values = line.split(" ")
        values = values[-2:]
        self.value = int(values[self.id])
        file.close()

    def change_value(self, add):
        self.value += add
        if self.value > 10:
            self.value = 10
            return False
        elif self.value < 0:
            self.value = 0
            return False
        return True

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        [screen.blit(self.value_image, (self.x+145+20*i, self.y+15)) for i in range(self.value)]


# Manages the user's information in the Game Menu
class User:
    def __init__(self, name=""):
        self.name = name
        self.password = ""
        self.best_speed = 0
        self.best_time = 0
        self.level = 1
        self.parts = 0
        self.image = Af.load_image(f"menu/interfaces/User/user_info/level1.png")
        self.parts_text, self.coo_p_t = None, (0, 0)
        self.best_speed_text, self.coo_bs_t = None, (0, 0)
        self.best_time_text, self.coo_bt_t = None, (0, 0)
        self.name_text, self.coo_n_t = None, (0, 0)
        self.music_volume = 8
        self.sound_volume = 8

    def get_info(self) -> None:
        file = open(f"saves/{self.name}/data.txt", "r")
        data = file.readline().split(" ")
        self.best_speed, self.best_time, self.level, self.parts, self.password, self.music_volume, self.sound_volume = \
            int(data[0]), int(data[1]), int(data[2]), int(data[3]), data[4], int(data[5]), int(data[6])
        self.image = Af.load_image(f"menu/interfaces/User/user_info/level{self.level}.png")
        file.close()

    def get_texts(self) -> None:
        self.best_time_text, self.coo_bt_t = Af.writable_best_time(self.best_time)
        self.best_speed_text, self.coo_bs_t = Af.writable_best_speed(self.best_speed)
        self.parts_text, self.coo_p_t = Af.writable_parts_number(self.parts)
        self.name_text, self.coo_n_t = Af.writable_user_name(self.name)

    def draw_text(self, screen) -> None:
        screen.blit(self.best_time_text, self.coo_bt_t)
        screen.blit(self.best_speed_text, self.coo_bs_t)
        screen.blit(self.parts_text, self.coo_p_t)
        screen.blit(self.name_text, self.coo_n_t)

    def get_active_user(self) -> None:
        file = open(f"saves/active_user.txt", "r")
        data = file.readline().split(" ")
        self.name, self.best_speed, self.best_time, self.level, self.parts, self.password = \
            data[0], int(data[1]), int(data[2]), int(data[3]), int(data[4]), data[5]
        self.image = Af.load_image(f"menu/interfaces/User/user_info/level{self.level}.png")
        file.close()

    def turn_active(self) -> None:
        file = open(f"saves/active_user.txt", "w")
        file.write(f"{self.name} {self.best_speed} {self.best_time} {self.level} {self.parts} {self.password} "+
                   f"{self.music_volume} {self.sound_volume}")
        file.close()

    def save_info(self) -> None:
        file = open(f"saves/{self.name}/data.txt", "w")
        data = f"{self.best_speed} {self.best_time} {self.level} {self.parts} {self.password} {self.music_volume}" \
               f" {self.sound_volume}"
        file.write(data)
        file.close()


# simulates a single firework
class Firework:
    def __init__(self, y):
        self.type = Af.choice(["circle", "star"])
        self.x = Af.randint(520, 560)
        self.y = y + Af.randint(0, 50) * Af.choice([-1, 1])
        self.max_height = Af.randint(130, 320)
        self.colors = Af.create_firework_colors(Af.randint(3, 6))
        self.x_speed = Af.randint(0, 8) * Af.choice([-1, 1])
        self.y_speed = -Af.randint(10, 15)
        self.alive = True
        self.time_alive = Af.randint(100, 200)
        self.radius = 10

    def draw_ascending(self, screen):
        for i in range(Af.randint(7, 10)):
            r_x, r_y = self.x + Af.randint(2, 5) * Af.choice([-1, 1]), self.y + Af.randint(2, 5) * Af.choice([-1, 1])
            pygame.draw.circle(screen, Af.choice(self.colors), (r_x, r_y), 1, 1)
        pygame.draw.circle(screen, Af.choice(self.colors), (self.x, self.y), 3, 1)
        self.x += self.x_speed
        self.y += self.y_speed

    def draw_star(self, screen, min_sparkle_number, max_sparkle_number):
        for i in range(Af.randint(min_sparkle_number, max_sparkle_number)):
            calculate_rs = Af.choice([Af.calculate_rs_rhomb, Af.calculate_rs_square])  # randomly chooses shape
            r_x, r_y = calculate_rs(self.x, self.y, self.radius)
            pygame.draw.circle(screen, Af.choice(self.colors), (r_x, r_y), 1, 1)

    def draw_circle(self, screen, min_sparkle_number, max_sparkle_number):
        for i in range(Af.randint(min_sparkle_number, max_sparkle_number)):
            r_x, r_y = Af.calculate_rs_circle(self.x, self.y, self.radius)
            pygame.draw.circle(screen, Af.choice(self.colors), (r_x, r_y), 1, 1)

    def draw_explosion(self, screen):
        min_sparkle_number = (200-self.time_alive)*200//100 - 30
        max_sparkle_number = (200 - self.time_alive) * 2 + 30
        types_of_firework = {"star": self.draw_star, "circle": self.draw_circle}
        # noinspection PyArgumentList
        types_of_firework[self.type](screen, min_sparkle_number, max_sparkle_number)
        self.time_alive -= 1
        self.radius += self.radius*0.1
        if self.radius > 100:
            self.alive = False

    def draw(self, screen):
        if self.y >= self.max_height:
            self.draw_ascending(screen)
        else:
            self.draw_explosion(screen)


# simulates a group of fireworks by managing single fireworks (Firework class)
class Fireworks:
    y_values = list(range(720, 2000, 40))[:15]

    def __init__(self):
        self.firework_stock = [Firework(self.y_values[i]) for i in range(len(self.y_values))]

    def update(self):
        self.firework_stock = [firework if firework.alive else Firework(720) for firework in self.firework_stock]
        if len(self.y_values) != len(self.firework_stock):
            for y in self.y_values[:len(self.y_values)-len(self.firework_stock)]:
                self.firework_stock.append(Firework(y))

    def display(self, screen):
        for firework in self.firework_stock:
            firework.draw(screen)
        self.update()


# ------------------------------------------------- MENU CLASSES -------------------------------------------------------
# Used for "Story", and every Tutorial option
class Menu_image_sequence:
    def __init__(self, screen, pasta, num_pages, func_link, name):
        self.screen = screen
        self.name = name
        self.background_image = Af.load_image(f"menu/interfaces/Main/sequence.png")
        self.images_list = [Af.load_image(f"slides/{pasta}/{i + 1}.png") for i in range(num_pages)]
        self.slide_name = Af.load_image(f"slides/{pasta}/name.png")
        self.num_pages = num_pages
        self.current_page = 0
        self.origin_link = func_link

    def manage_buttons(self, key):
        if key == pygame.K_RIGHT:
            if self.current_page+1 == self.num_pages:
                Af.play(error_sound)
            else:
                Af.play(button_y_sound)
            self.current_page += 1
        elif key == pygame.K_LEFT:
            if self.current_page == 0:
                Af.play(error_sound)
            else:
                Af.play(button_y_sound)
            self.current_page -= 1
        elif key == pygame.K_KP_ENTER or key == pygame.K_RETURN:
            if self.current_page == self.num_pages:
                return self.origin_link
        elif key == pygame.K_ESCAPE:
            return self.origin_link
        if self.current_page > self.num_pages-1:
            self.current_page = self.num_pages-1
        if self.current_page < 0:
            self.current_page = 0

    def get_rectangle(self):
        if self.current_page == self.num_pages-1:
            return 700, 633, 300, 40
        elif self.current_page == 0:
            return 85, 633, 300, 40
        else:
            return 200, 640, 1, 1

    def write_page_number(self):
        page_image = Af.create_sized_text(20, 50, str(self.current_page + 1), (255, 255, 255))
        self.screen.blit(page_image, (515, 640))

    def refresh(self):
        self.screen.blit(self.background_image, (0, 0))
        self.screen.blit(self.images_list[self.current_page], (108, 120))
        self.screen.blit(self.slide_name, (400, 0))
        self.write_page_number()
        pygame.draw.rect(self.screen, (0, 0, 0), self.get_rectangle())
        pygame.display.update()

    def display_menu(self):
        clock = pygame.time.Clock()
        keepGoing = True
        while keepGoing:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    effect = self.manage_buttons(event.key)
                    if effect is not None:
                        return effect
            self.refresh()


# Used for the Main Menu, Game Menu and Tutorial
class Menu:
    def __init__(self, buttons, directory, screen, user=None):
        self.internal_list = buttons
        self.directory = directory
        self.name = self.directory.split("/")[-1][:-4]
        self.image_nome = Af.load_image(directory)
        if self.name == "game menu":
            self.effect = [Af.load_image(f"menu/effects/3/{i + 1}.png") for i in range(4)]
        else:
            self.effect = [Af.load_image(f"menu/effects/1/{i + 1}.png") for i in range(4)]
        self.active_code = 0
        self.screen = screen
        self.current_frame = 0
        self.user = user
        self.coord_effect = (self.internal_list[0].x-12, self.internal_list[0].y-12)

    def draw_buttons(self):
        coordinates = {0: (680, 90), 1: (698, 192), 2: (685, 178)}
        coordinates2 = {0: (687, 90), 1: (687, 90), 2: (687, 192), 3: (687, 178), 4: (687, 178),  5: (687, 178)}
        coordinates3 = {0: (680, 90), 1: (680, 90), 2: (698, 192), 3: (685, 178), 4: (685, 178)}
        ch = {"main menu": coordinates, "game menu": coordinates2, "tutorial": coordinates3}
        co_cho = ch[self.name]
        coo = co_cho[self.active_code]
        self.screen.blit(self.effect[int(self.current_frame)], self.coord_effect)
        self.screen.blit(Af.load_image(f"menu/info/info_{self.name}/{self.active_code + 1}.png"),
                         (coo[0], coo[1]))
        for but in self.internal_list:
            but.draw(self.screen)
        self.current_frame += 0.25
        if self.current_frame > 3:
            self.current_frame = 0

    def display_menu(self):
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        background.fill((0, 0, 0))
        clock = pygame.time.Clock()
        keepGoing = True
        while keepGoing:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    effect = self.manage_buttons(event.key)
                    if effect is not None:
                        if effect == "m_ai":
                            if Af.get_user_level() < 13:
                                return effect
                            else:
                                Af.show_error_message(self.screen, 12)
                        else:
                            return effect
            self.refresh(background)

    def manage_buttons(self, key):
        valor = 0
        if key == pygame.K_UP:
            Af.play(button_y_sound)
            valor = -1
        elif key == pygame.K_DOWN:
            Af.play(button_y_sound)
            valor = 1
        elif key == pygame.K_KP_ENTER or key == pygame.K_RETURN:
            return self.internal_list[self.active_code].effect
        self.active_code += valor
        if self.active_code > len(self.internal_list)-1:
            self.active_code = 0
        if self.active_code < 0:
            self.active_code = len(self.internal_list)-1
        self.coord_effect = (self.internal_list[self.active_code].x-12, self.internal_list[self.active_code].y-12)

    def refresh(self, background):
        self.screen.blit(background, (0, 0))
        self.screen.blit(self.image_nome, ((1080-470)//2, 0))
        self.screen.blit(Af.load_image(f"menu/interfaces/navigation/navigation.png"), (355, 620))
        if self.user is not None:
            coo = (20, 490)
            self.screen.blit(Af.load_image(f"menu/interfaces/User/user_info/level{self.user.level}.png"),
                             (0, 0))
            self.screen.blit(Af.load_image(f"menu/interfaces/User/records.png"), (coo[0], coo[1] - 210))
            self.screen.blit(Af.load_image(f"menu/interfaces/User/parts.png"), (0, coo[1] - 310))
            self.screen.blit(Af.load_image(f"cars/display/{self.user.level}.png"), (coo[0] - 18, coo[1]))
            self.user.draw_text(self.screen)
        self.draw_buttons()
        pygame.display.update()


# Used whenever the user wants to leave the game
class Exit:
    def __init__(self, directory, screen):
        self.image_nome = Af.load_image(directory)
        self.effects = (True, False)
        self.effect = [Af.load_image(f"menu/effects/1/{i + 1}.png") for i in range(4)]
        self.active_code = 0
        self.screen = screen
        self.current_frame = 0

    def draw_buttons(self):
        coordinates = {0: (240, 410), 1: (570, 410)}
        coo = coordinates[self.active_code]
        self.screen.blit(self.effect[int(self.current_frame)], coo)
        self.screen.blit(Af.load_image(f"menu/buttons/3/{self.active_code + 1}.png"), (coo[0] + 13, coo[1] + 10))
        self.current_frame += 0.25
        if self.current_frame > 3:
            self.current_frame = 0

    def display_menu(self):
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        background.fill((0, 0, 0))
        clock = pygame.time.Clock()
        keepGoing = True
        while keepGoing:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Af.terminate_execution()
                if event.type == pygame.KEYDOWN:
                    effect = self.manage_buttons(event.key)
                    if effect is not None:
                        return effect
            self.refresh()

    def manage_buttons(self, key):
        valor = 0
        if key == pygame.K_RIGHT:
            Af.play(button_x_sound)
            valor = 1
        elif key == pygame.K_LEFT:
            Af.play(button_x_sound)
            valor = -1
        elif key == pygame.K_KP_ENTER or key == pygame.K_RETURN:
            return self.effects[self.active_code]
        self.active_code += valor
        if self.active_code > len(self.effects)-1:
            self.active_code = 0
        if self.active_code < 0:
            self.active_code = 1

    def refresh(self):
        self.screen.blit(self.image_nome, (0, 0))
        self.draw_buttons()
        self.screen.blit(Af.load_image(f"menu/interfaces/navigation/navigation2.png"), (350, 600))
        pygame.display.update()


# Used when the "New Game" option in the Main Menu is selected
class Create_Account:
    def __init__(self, directory, screen, change=False):
        self.image_nome = Af.load_image(directory)
        self.effects = (False, True)
        self.effect = [Af.load_image(f"menu/effects/2/{i + 1}.png") for i in range(4)]
        self.active_code_x = 0
        self.active_code_y = 0
        self.hide = False
        self.screen = screen
        self.inputs = [[], []]
        self.current_frame = 0
        self.user = User()
        self.change = change
        if change:
            self.user.get_active_user()

    def draw_buttons(self) -> None:
        coordinates = {0: (325, 485), 1: (558, 485)}
        coo = coordinates[self.active_code_x]
        self.screen.blit(self.effect[int(self.current_frame)], (coo[0]-5, coo[1]-10))
        if self.change:
            self.screen.blit(Af.load_image(f"menu/buttons/9/{self.active_code_x + 1}.png"),
                             (coo[0] + 13, coo[1] + 10))
        else:
            self.screen.blit(Af.load_image(f"menu/buttons/5/{self.active_code_x + 1}.png"),
                             (coo[0]+13, coo[1]+10))
        self.current_frame += 0.2
        if self.current_frame > 3:
            self.current_frame = 0

    def display_menu(self):
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        background.fill((0, 0, 0))
        clock = pygame.time.Clock()
        keepGoing = True
        while keepGoing:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    effect = self.manage_buttons(event)
                    if effect is not None:
                        return effect
            self.refresh()

    def create_account(self) -> None:
        name = "".join(self.inputs[0])
        Af.create_folder(name)  # create the user's folder
        file = open(f"saves/{name}/next_level.txt", "w")  # create a file in the user's folder named next_level
        file.write("1 \n")  # this value means that the MISSION AI is available
        file.write("0")  # this value means that the user has not yet won the game
        file.close()

    def validate_user_information(self) -> bool:
        first, second = "".join(self.inputs[0]), "".join(self.inputs[1])
        if self.change:
            if first != self.user.password:
                Af.show_error_message(self.screen, 7)
                return False
            elif len(self.inputs[1]) == 0:
                Af.show_error_message(self.screen, 3)
                return False
            elif " " in self.inputs[1]:
                Af.show_error_message(self.screen, 4)
                return False
        else:
            if first in Af.list_users():
                Af.show_error_message(self.screen, 1)
                return False
            elif len(self.inputs[0]) == 0:
                Af.show_error_message(self.screen, 2)
                return False
            elif len(self.inputs[1]) == 0:
                Af.show_error_message(self.screen, 3)
                return False
            elif " " in self.inputs[0] or " " in self.inputs[1]:
                Af.show_error_message(self.screen, 4)
                return False
        return True

    def manage_buttons(self, event):
        if event.key == pygame.K_RIGHT:
            Af.play(button_x_sound)
            self.active_code_x = 1
        elif event.key == pygame.K_LEFT:
            Af.play(button_x_sound)
            self.active_code_x = 0
        elif event.key == pygame.K_DOWN:
            Af.play(button_y_sound)
            self.active_code_y = 1
        elif event.key == pygame.K_UP:
            Af.play(button_y_sound)
            self.active_code_y = 0
        elif event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
            if self.effects[self.active_code_x]:
                if self.validate_user_information():
                    if self.change:
                        self.user.password = "".join(self.inputs[1])
                        self.user.save_info()
                        self.user.turn_active()
                        Af.show_success_message(self.screen, 4)
                    else:
                        self.user.name = "".join(self.inputs[0])
                        self.user.password = "".join(self.inputs[1])
                        self.create_account()
                        self.user.save_info()
                        self.user.turn_active()
                        Af.show_success_message(self.screen, 1)
                    return True
                else:
                    if self.change:
                        return "change_password"
                    return "new"
            return False
        elif event.key == pygame.K_TAB:
            self.hide = not self.hide
        elif event.key == pygame.K_BACKSPACE:
            Af.play(erase_letter_sound)
            self.inputs[self.active_code_y] = self.inputs[self.active_code_y][:-1]
        elif len(self.inputs[self.active_code_y]) <= 25 and self.active_code_y == 1:
            self.inputs[self.active_code_y].append(event.unicode)
        elif len(self.inputs[self.active_code_y]) <= 20 and self.active_code_y == 0:
            self.inputs[self.active_code_y].append(event.unicode)

    def refresh(self) -> None:
        self.screen.blit(self.image_nome, (0, 0))
        self.draw_buttons()
        self.screen.blit(Af.load_image(f"menu/interfaces/navigation/navigation3.png"), (355, 620))
        Af.write_name_password(self.screen, self.inputs[0], self.inputs[1], self.active_code_y, self.hide)
        pygame.display.update()


# Used when the "Continue" option in the Main Menu is selected
class Choose_Account:
    def __init__(self, screen):
        self.screen = screen
        self.image = Af.load_image(f"menu/interfaces/Main/choose account.png")
        self.effect = [Af.load_image(f"menu/effects/2/{i + 1}.png") for i in range(4)]
        self.passive_button_image = Af.load_image(f"menu/buttons/6/2.png")
        self.active_button_image = Af.load_image(f"menu/buttons/6/1.png")
        self.button_coordinates = [(322, 120), (322, 175), (322, 230), (322, 285), (322, 340), (322, 395), (322, 450)]
        self.account_name = None
        self.current_frame = 0
        self.active_code_x = 1
        self.active_code_y = 0
        self.buttons = []
        self.previous_button = 0
        self.users = Af.list_users()
        self.user_names_images_active, self.user_names_images_passive = Af.get_users_images()
        self.user_names_images = None
        self.adjust_user_name_images()
        self.user = User()
        self.create_buttons()

    def adjust_user_name_images(self):
        self.user_names_images = self.user_names_images_passive[:]
        self.user_names_images[self.active_code_y] = self.user_names_images_active[self.active_code_y]
        if self.previous_button != self.active_code_y:  # prevents getting wrong image in the initiation
            self.user_names_images[self.previous_button] = self.user_names_images_passive[self.previous_button]

    def display_menu(self):
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        background.fill((0, 0, 0))
        clock = pygame.time.Clock()
        keepGoing = True
        while keepGoing:
            clock.tick(30)
            self.current_frame += 0.25
            if self.current_frame > 3:
                self.current_frame = 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    self.create_buttons()
                    effect = self.manage_buttons(event.key)
                    if effect is not None:
                        return effect
            self.refresh()

    def manage_buttons(self, key):
        if key == pygame.K_RIGHT:
            Af.play(button_x_sound)
            self.active_code_x = 1
        elif key == pygame.K_LEFT:
            Af.play(button_x_sound)
            self.active_code_x = 0
        elif key == pygame.K_DOWN:
            if len(self.buttons) > 1:
                Af.play(button_y_sound)
                self.active_code_y += 1
                self.previous_button = self.active_code_y-1
        elif key == pygame.K_UP:
            if len(self.buttons) > 1:
                Af.play(button_y_sound)
                self.active_code_y -= 1
                self.previous_button = self.active_code_y+1
        self.control_previous_button()
        if self.active_code_y > len(self.users)-1:
            self.active_code_y = 0
            self.previous_button = len(self.users)-1
        elif self.active_code_y < 0:
            self.active_code_y = len(self.users)-1
            self.previous_button = 0
        self.set_active_button()
        if key == pygame.K_KP_ENTER or key == pygame.K_RETURN:
            if self.active_code_x:
                self.user.name = self.users[self.active_code_y]
                self.user.get_info()
                self.user.turn_active()
                return "enter_password"
            else:
                return "main_menu"

    def control_previous_button(self):
        if self.previous_button == self.active_code_y:
            if self.active_code_y == 1:
                self.previous_button = 0
            else:
                self.previous_button = 1

    def create_buttons(self):
        for user in self.users:
            self.buttons.append(Button(self.button_coordinates[self.users.index(user)][0],
                                       self.button_coordinates[self.users.index(user)][1],
                                       "menu/buttons/6/2.png", None, self.users.index(user)))
        self.set_active_button()

    def set_active_button(self):
        if len(self.users) > 1:
            self.adjust_user_name_images()
            self.buttons[self.previous_button].image = self.passive_button_image
            self.buttons[self.active_code_y].image = self.active_button_image
        else:
            self.buttons[self.previous_button].image = self.active_button_image

    def refresh(self):
        coordinates = {0: (325, 520), 1: (558, 520)}
        coo = coordinates[self.active_code_x]
        self.screen.blit(self.image, (0, 0))
        self.screen.blit(self.effect[int(int(self.current_frame))], (coo[0]-5, coo[1]-20))
        self.screen.blit(Af.load_image(f"menu/buttons/7/{self.active_code_x + 1}.png"), (coo[0] + 13, coo[1]))
        [self.buttons[i].draw(self.screen) for i in range(len(self.users))]
        [self.screen.blit(self.user_names_images[i], (self.button_coordinates[i][0]+10, self.button_coordinates[i][1]))
         for i in range(len(self.users))]
        self.screen.blit(Af.load_image(f"menu/interfaces/navigation/navigation3.png"), (355, 620))
        pygame.display.update()


# Used whenever is required the introduction of a password in order to complete a task
class Enter_Password:
    def __init__(self, screen, change=False):
        self.screen = screen
        self.image = Af.load_image(f"menu/interfaces/Main/insert_password.png")
        self.user = None
        self.password_list = []
        self.create_user()
        self.hide = False
        self.change = change

    def create_user(self):
        self.user = User()
        self.user.get_active_user()
        self.user.get_info()

    def show_error_message(self) -> None:
        pygame.image.save(self.screen, "images/menu/interfaces/prov_image/prov_image.png")
        Af.show_error_message(self.screen, 5)
        self.screen.blit(Af.load_image(f"menu/interfaces/prov_image/prov_image.png"), (0, 0))

    def show_success_message(self) -> None:
        Af.play(success_sound)
        if self.change:
            self.screen.blit(Af.load_image(f"menu/messages/success3.png"), (230, 200))
            time = 3
        else:
            self.screen.blit(Af.load_image(f"menu/messages/success2.png"), (230, 200))
            Af.write_name(self.screen, self.user.name)
            time = 1
        pygame.display.update()
        Af.wait(time)
        pygame.event.clear()  # all pressed buttons are dismissed in this phase

    def verify_password(self):
        return "".join(self.password_list) == self.user.password

    def display_menu(self):
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        background.fill((0, 0, 0))
        clock = pygame.time.Clock()
        keepGoing = True
        while keepGoing:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    effect = self.manage_buttons(event)
                    if effect is not None:
                        return effect
            self.refresh()

    def manage_buttons(self, event):
        if event.key == pygame.K_BACKSPACE:
            Af.play(erase_letter_sound)
            self.password_list = self.password_list[:-1]
        elif event.key == pygame.K_ESCAPE:
            if self.change:
                return "manage"
            return "choose"
        elif event.key == pygame.K_TAB:
            self.hide = not self.hide
        elif event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
            # self.password = "".join(self.password_list)
            if self.verify_password():
                self.show_success_message()
                if self.change:
                    return "main_menu"
                return "game_menu"
            else:
                self.show_error_message()
                return "enter_password"
        elif len(self.password_list) < 25:
            self.password_list.append(event.unicode)

    def refresh(self):
        self.screen.blit(self.image, (210, 250))
        if not self.change:  # verifies if this class was called for login purposes. In this case it deletes extra stuff
            self.screen.blit(Af.load_image(f"menu/interfaces/prov_image/button.png"), (550, 500))
        Af.write_password(self.screen, self.password_list, self.hide)
        pygame.display.update()


# Used when the "Management" option in the Game Menu is selected
class Management:
    def __init__(self, buttons, directory, screen, user=None):
        self.list = buttons
        self.directory = directory
        self.image_nome = Af.load_image(directory)
        self.effect1 = [Af.load_image(f"menu/effects/5/{i + 1}.png") for i in range(4)]
        self.effect2 = [Af.load_image(f"menu/effects/4/{i + 1}.png") for i in range(4)]
        self.active_code = 0
        self.screen = screen
        self.current_frame = 0
        self.name = "management"
        self.user = user
        self.coord_effect = (self.list[0].x-8, self.list[0].y-8)

    def draw_buttons(self):
        if self.active_code < 2:
            self.screen.blit(self.effect2[int(self.current_frame)], self.coord_effect)
        else:
            self.screen.blit(self.effect1[int(self.current_frame)], self.coord_effect)
        for but in self.list:
            but.draw(self.screen)
        self.current_frame += 0.25
        if self.current_frame > 3:
            self.current_frame = 0

    def display_menu(self):
        clock = pygame.time.Clock()
        keepGoing = True
        while keepGoing:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    effect = self.manage_buttons(event.key)
                    if effect is not None:
                        return effect
            self.refresh()

    def update_user(self):
        self.user.music_volume = self.list[0].value
        self.user.sound_volume = self.list[1].value
        self.user.save_info()
        self.user.turn_active()

    def manage_buttons(self, key):
        if key == pygame.K_UP:
            Af.play(button_y_sound)
            self.active_code -= 1
        elif key == pygame.K_DOWN:
            Af.play(button_y_sound)
            self.active_code += 1
        elif self.active_code == 0 or self.active_code == 1:
            if key == pygame.K_LEFT:
                play_sound = self.list[self.active_code].change_value(-1)  # change_value returns True if max is reached
                if play_sound:  # if volume is max or min, then the sound is played
                    Af.play(volume_change_sound)
            elif key == pygame.K_RIGHT:
                play_sound = self.list[self.active_code].change_value(1)  # change_value returns True if max is reached
                if play_sound is True:  # if volume is max or min, then the sound is not played
                    Af.play(volume_change_sound)
                else:
                    Af.play(error_sound)
            self.update_user()
        elif key == pygame.K_KP_ENTER or key == pygame.K_RETURN:
            return self.list[self.active_code].effect
        if self.active_code > len(self.list)-1:
            self.active_code = 0
        if self.active_code < 0:
            self.active_code = len(self.list)-1
        self.coord_effect = (self.list[self.active_code].x-12, self.list[self.active_code].y-12)

    def refresh(self):
        Af.clean_background(self.screen)
        self.screen.blit(self.image_nome, ((1080-470)//2, 0))
        self.screen.blit(Af.load_image(f"menu/interfaces/navigation/navigation.png"), (355, 620))
        coo = (20, 490)
        self.screen.blit(Af.load_image(f"menu/interfaces/User/user_info/level{self.user.level}.png"), (0, 0))
        self.screen.blit(Af.load_image(f"menu/interfaces/User/records.png"), (coo[0], coo[1] - 210))
        self.screen.blit(Af.load_image(f"menu/interfaces/User/parts.png"), (0, coo[1] - 310))
        self.screen.blit(Af.load_image(f"cars/display/{self.user.level}.png"), (coo[0] - 18, coo[1]))
        self.user.draw_text(self.screen)
        coordinates = {0: (680, 90), 1: (680, 90), 2: (698, 192), 3: (685, 178), 4: (685, 178), 5: (685, 178)}
        coo = coordinates[self.active_code]
        self.screen.blit(Af.load_image(f"menu/info/info_{self.name}/{self.active_code + 1}.png"),
                         (coo[0], coo[1]))
        self.draw_buttons()
        pygame.display.update()


# Used every time a "Mission: AI" match is over and the game results must be displayed and processed
class Results_AI:
    def __init__(self, screen, precision, speed, parts_collected, resistance, time, finished):
        self.screen = screen
        self.image = Af.load_image(f"menu/interfaces/Main/Results_AI.png")
        self.requirements_satisfied = False
        self.parts = 0
        self.values_images = self.initiate_results(precision, speed, parts_collected, resistance, time, finished)

    def initiate_results(self, precision, speed, parts_collected, resistance, time, finished):
        values = []
        # results about level requirements
        c_w = {True: "correct", False: "wrong"}
        font1 = pygame.font.SysFont('Times New Roman', 20)
        font1.set_bold(True)
        values.append(font1.render(str(int(precision)), True, (255, 255, 255)))
        values.append(font1.render(str(int(speed)), True, (255, 255, 255)))
        speed2, precision2 = Af.get_requirements()
        values.append(font1.render(str(precision2), True, (255, 255, 255)))
        values.append(font1.render(str(speed2), True, (255, 255, 255)))
        values.append(Af.load_image(f"menu/interfaces/navigation/{c_w[speed >= speed2]}.png"))
        values.append(Af.load_image(f"menu/interfaces/navigation/{c_w[precision >= precision2]}.png"))
        # results about parts
        font1 = pygame.font.SysFont('Times New Roman', 16)
        font1.set_bold(True)
        values.append(font1.render(str(parts_collected), True, (255, 255, 255)))
        values.append(font1.render(str(int(resistance)), True, (255, 255, 255)))
        values.append(font1.render(str((100-int(resistance))*3), True, (255, 255, 255)))
        self.parts = parts_collected-(100-int(resistance))*3
        values.append(font1.render(str(self.parts), True, (255, 255, 255)))
        # verify if requirements were satisfied in order to proceed to next level
        if speed>=speed2 and precision>=precision2 and (int(time)>= 60 or finished):
            self.requirements_satisfied = True
        return values

    def refresh(self):
        coordinates = ((635, 360), (635, 300), (515, 360), (515, 300), (713, 275), (713, 336), (725, 457), (725, 425),
                       (725, 494), (725, 530))
        self.screen.blit(self.image, (287, 40))
        [self.screen.blit(image, coo) for image, coo in zip(self.values_images, coordinates)]
        pygame.display.update()

    @staticmethod
    def manage_buttons(key):
        if key == pygame.K_KP_ENTER or key == pygame.K_RETURN:
            return True
        return False

    def display_level_info_message(self):
        message_dict = {True: "success5", False: "error8"}
        time_dict = {True: 3, False: 3}
        sound_dict = {True: success_sound, False: error_sound}
        message = message_dict[self.requirements_satisfied]
        time = time_dict[self.requirements_satisfied]
        Af.play(sound_dict[self.requirements_satisfied])
        self.screen.blit(Af.load_image(f"menu/messages/{message}.png"), (230, 200))
        pygame.display.update()
        Af.wait(time)
        pygame.event.clear()  # all pressed buttons are dismissed in this phase

    def display(self):
        clock = pygame.time.Clock()
        keepGoing = True
        while keepGoing:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return self.requirements_satisfied, self.parts
                if event.type == pygame.KEYDOWN:
                    if self.manage_buttons(event.key):
                        self.display_level_info_message()
                        return self.requirements_satisfied, self.parts
            self.refresh()


# Used every time a "Mission: PARTS" match is over and the game results must be displayed and processed
class Results_Parts:
    def __init__(self, screen, precision, avg_speed, max_speed, parts_collected, time):
        self.screen = screen
        self.image = Af.load_image("menu/interfaces/Main/Results_Parts.png")
        self.parts = 0
        self.time = int(time)
        self.values_images = self.initiate_results(precision, avg_speed, max_speed, parts_collected)

    def initiate_results(self, precision, avg_speed, max_speed, parts_collected):
        values = []
        # results about parts
        font1 = pygame.font.SysFont('Times New Roman', 16)
        font1.set_bold(True)
        values.append(font1.render(str(int(precision)), True, (255, 255, 255)))
        values.append(font1.render(str(int(avg_speed)), True, (255, 255, 255)))
        values.append(font1.render(str(int(max_speed)), True, (255, 255, 255)))
        values.append(font1.render(str(self.time), True, (255, 255, 255)))
        values.append(font1.render(str(parts_collected), True, (255, 255, 255)))
        self.parts = parts_collected-300
        values.append(font1.render(str(self.parts), True, (255, 255, 255)))
        return values

    def refresh(self):
        coordinates = ((725, 330), (725, 362), (725, 396),  (725, 426), (725, 457), (725, 529))
        self.screen.blit(self.image, (287, 40))
        [self.screen.blit(image, coo) for image, coo in zip(self.values_images, coordinates)]
        pygame.display.update()

    @staticmethod
    def manage_buttons(key):
        if key == pygame.K_KP_ENTER or key == pygame.K_RETURN:
            return True
        return False

    def display(self):
        clock = pygame.time.Clock()
        keepGoing = True
        while keepGoing:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return self.parts
                if event.type == pygame.KEYDOWN:
                    if self.manage_buttons(event.key):
                        return self.parts
            self.refresh()


# Used every time a user manages to level up and he must unlock the "Mission: AI" option in the Game Menu
class Unlock_Level:
    def __init__(self, screen):
        self.screen = screen
        self.image = Af.load_image("menu/interfaces/Main/unlock level.png")
        self.user = None
        self.parts_needed = None
        self.create_user()

    def create_user(self):
        self.user = User()
        self.user.get_active_user()
        self.user.get_info()
        file = open(f"parameters/levels info/{self.user.level}.txt", "r")
        self.parts_needed = int(file.readline().split(" ")[2])
        file.close()

    def show_error_message(self) -> None:
        Af.show_error_message(self.screen, 9)

    def show_success_message(self) -> None:
        Af.show_success_message(self.screen, 6)

    def verify_parts_number(self):
        return self.parts_needed <= self.user.parts

    def save_state(self):
        file = open(f"saves/{self.user.name}/next_level.txt", "w")
        file.write("1")
        file.close()
        self.user.parts = self.user.parts - self.parts_needed
        self.user.save_info()
        self.user.turn_active()

    def parts_image(self):
        return Af.create_sized_text(190, 50, str(self.parts_needed), (255, 180, 0))

    def display_menu(self):
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        background.fill((0, 0, 0))
        clock = pygame.time.Clock()
        keepGoing = True
        while keepGoing:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    effect = self.manage_buttons(event.key)
                    if effect is not None:
                        return effect
            self.refresh()

    def manage_buttons(self, key):
        if key == pygame.K_ESCAPE:
            return True
        elif key == pygame.K_KP_ENTER or key == pygame.K_RETURN:
            if self.verify_parts_number():
                self.show_success_message()
                self.save_state()
                return True
            else:
                self.show_error_message()
                return True

    def refresh(self):
        self.screen.blit(self.image, (210, 250))
        self.screen.blit(self.parts_image(), (635, 310))
        pygame.display.update()


# The first Interface that shows up when the game is executed. It shows "Fast and Curious"'s logo
class Start:
    def __init__(self, screen):
        self.screen = screen
        self.image = Af.load_image(f"general/Fast and Curious Logo.png")
        text_font = pygame.font.SysFont('Times New Roman', 20)
        text_font.set_bold(True)
        self.directives_image = text_font.render("Press any key to continue", True, (255, 255, 255))
        self.time = 0

    def show_directives(self):
        if int(self.time) % 2 == 0:
            self.screen.blit(self.directives_image, (440, 670))

    def display_menu(self):
        clock = pygame.time.Clock()
        keepGoing = True
        while keepGoing:
            self.time += clock.tick(30) / 990
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.KEYDOWN:
                    return True
            self.refresh()

    def refresh(self):
        self.screen.blit(self.image, (0, 0))
        self.show_directives()
        pygame.display.update()


# Used when the "New Game" option in the Main Menu is selected
class Add_Text:
    def __init__(self, screen):
        self.image = Af.load_image(f"menu/interfaces/Main/add text.png")
        self.effects = (False, True)
        self.effect = [Af.load_image(f"menu/effects/2/{i + 1}.png") for i in range(4)]
        self.active_code_x = 0
        self.text_lines_images = None
        self.screen = screen
        self.character_number = 0
        self.written_text = ""
        self.error_code = 0
        self.current_frame = 0
        self.text_lines = []

    def draw_buttons(self) -> None:
        coordinates = {0: (325, 485), 1: (558, 485)}
        coo = coordinates[self.active_code_x]
        self.screen.blit(self.effect[int(self.current_frame)], (coo[0]-5, coo[1]-10))
        self.current_frame += 0.2
        if self.current_frame > 3:
            self.current_frame = 0

    def show_error_message(self) -> None:
        Af.show_error_message(self.screen, self.error_code)

    def show_success_message(self) -> None:
        Af.show_success_message(self.screen, 7)

    def display_menu(self):
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        background.fill((0, 0, 0))
        clock = pygame.time.Clock()
        keepGoing = True
        while keepGoing:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    effect = self.manage_buttons(event)
                    if effect is not None:
                        if effect:
                            if self.validate_text_information():
                                self.create_text()
                                self.show_success_message()
                                return True
                            else:
                                self.show_error_message()
                        else:
                            return True

            self.refresh()

    def create_text(self) -> None:
        # creating the image
        self.text_lines, self.text_lines_images = Af.convert_text_to_images(self.written_text, True)
        coordinates = [(15, 5), (15, 25), (15, 45), (15, 65), (15, 85), (15, 105)]
        text_background = pygame.Surface((519, 132))
        text_background.blit(Af.load_image(f"texts/background.png"), (0, 0))
        for img, coo in zip(self.text_lines_images, coordinates):
            text_background.blit(img, coo)
        last_number_text = Af.get_last_text_number()
        pygame.image.save(text_background, f"images/texts/{last_number_text+1}.png")
        # creating the txt file
        with open(f"texts/{last_number_text+1}.txt", "w") as file:
            file.write(f"{len(self.text_lines)} \n")  # first line of these files holds the number of lines in the text
            for line in self.text_lines:
                file.write(line+"\n")

    def validate_text_information(self) -> bool:
        special = [",", ".", "'", " "]
        if self.character_number < 192:
            self.error_code = 10
            return False
        ch_list = set(self.written_text)
        for char in ch_list:  # verify that there are no special characters or numbers
            if char.isalpha():
                continue
            elif char in special:
                continue
            else:
                self.error_code = 11
                return False
        return True

    def last_word_is_proper(self):
        if self.written_text != "":
            last_word_length = len(self.written_text.split()[-1])
            return last_word_length < 48
        return True

    def manage_buttons(self, event):
        if event.key == pygame.K_RIGHT:
            Af.play(button_x_sound)
            self.active_code_x = 1
        elif event.key == pygame.K_LEFT:
            Af.play(button_x_sound)
            self.active_code_x = 0
        elif event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
            if self.active_code_x:
                return True
            else:
                return False
        elif event.key == pygame.K_BACKSPACE:
            Af.play(erase_letter_sound)
            self.written_text = self.written_text[:-1]
            self.character_number-=1
            if self.character_number < 0:
                self.character_number = 0
        elif self.character_number < 288 and self.last_word_is_proper():
            special = [" ", ",", ".", "'"]
            if event.unicode.isalpha() or event.unicode in special:
                self.written_text+=event.unicode
                self.character_number = len(self.written_text.strip())

    def write_potential_text(self):
        coordinates = [(327, 175), (327, 200), (327, 225), (327, 250), (327, 275), (327, 300)]
        self.text_lines, images = Af.convert_text_to_images(self.written_text)
        for img, coo in zip(images, coordinates):
            self.screen.blit(img, coo)
        self.text_lines_images = images

    def refresh(self) -> None:
        self.screen.blit(self.image, (0, 0))
        self.draw_buttons()
        self.write_potential_text()
        pygame.display.update()


# Winner_Winner_Chicken_Dinner!!! This Class is used when the user finishes the game (passes at level 13)
class Winner_Menu:
    time = 0
    image = Af.load_image(f"menu/interfaces/Main/winner.png")
    fireworks = Fireworks()

    def __init__(self, screen):
        self.screen = screen
        text_font = pygame.font.SysFont('Times New Roman', 20)
        text_font.set_bold(True)
        self.directives_image = text_font.render("Press any key to continue", True, (255, 255, 255))
        self.time = 0

    def show_directives(self):
        if int(self.time) % 2 == 0:
            self.screen.blit(self.directives_image, (440, 670))

    def display_menu(self):
        clock = pygame.time.Clock()
        keepGoing = True
        while keepGoing:
            self.time += clock.tick(30) / 990
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.KEYDOWN:
                    return True
            self.refresh()

    def refresh(self):
        self.screen.blit(self.image, (0, 0))
        self.fireworks.display(self.screen)
        self.show_directives()
        pygame.display.update()
