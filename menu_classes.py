# This module contains all the classes responsible for displaying and managing all the Menus and interfaces available
# In the Game. There are also some classes that makes it easier for all the menu classes to do their job.
# Every menu class has three major methods that are very similar if not the same: - display_menu(); - manage_buttons();
# - refresh(); display_menu is the one called after instantiating a new object of a menu class, it is the only method
# used externally of the class. It is the most important, and his job is to display the events of a menu.
# The manage_buttons method is for transforming input from the keyboard into the correct output. And the refresh method
# just updates the menu after every alteration the user makes.

# -------------------------------------------------- IMPORTS -----------------------------------------------------------
import pygame
from pygame import Surface
from pygame.event import Event
import Auxiliary_Functionalities as Af


# --------------------------------------------------- SOUNDS ----------------------------------------------------------
button_y_sound = Af.load_sound("menu/button_activation.WAV")     # sound for changing button on y-axis
button_x_sound = Af.load_sound("menu/button_lateral.WAV")        # sound for changing button on x-axis
volume_change_sound = Af.load_sound("menu/volume_change.WAV")    # sound for changing volume
erase_letter_sound = Af.load_sound("menu/typing.WAV")            # sound for every time a letter is erased
error_sound = Af.load_sound("menu/error_message2.WAV")           # sound for every time an error occurs
success_sound = Af.load_sound("menu/success.WAV")                # sound for every time a success occurs


# ------------------------------------------------ SUPPORT CLASSES -----------------------------------------------------
# These classes are used by the classes that manage the Menus interfaces

class Button:
    pointer_image = Af.load_image("menu/info/pointer.png")

    def __init__(self, x: int, y: int, directory: str, effect: str):
        self.x = x
        self.y = y
        if directory is not None:
            self.image = Af.load_image(directory)
            self.size = self.image.get_size()
        self.effect = effect

    def cursor_is_inside(self, cursor_coo: (int, int)):
        cursor_x, cursor_y = cursor_coo[0], cursor_coo[1]
        button_width, button_height = self.image.get_size()[0], self.image.get_size()[1]
        if self.x <= cursor_x <= self.x + button_width and self.y <= cursor_y <= self.y + button_height:
            return True
        return False

    def draw(self, screen: Surface):
        screen.blit(self.image, (self.x, self.y))

    def draw_info(self, screen):
        screen.blit(self.pointer_image, (685, self.y+self.size[1]//2-19))  # draw the head of the arrow (pointer)
        # line from pointer to center line (vertical)
        pygame.draw.line(screen, (0, 255, 255), (730, self.y+self.size[1]//2+3), (730, 343), 5)
        # center line (horizontal)
        pygame.draw.rect(screen, (0, 255, 255), (728, 342, 30, 5))

    def change_image(self, directory: str):
        self.image = Af.load_image(directory)


class Button2(Button):
    def __init__(self, x: int, y: int, directory: str, effect: str, id_c: int):
        super().__init__(x, y, directory, effect)
        self.value = 0
        self.effect = "manage"
        self.id = id_c
        self.value_image = Af.load_image(f"menu/buttons/8/7.png")
        self.get_value()

    def get_value(self):
        values = Af.read_file_content("saves/active_user.txt", 1)[0].split(" ")[-2:]
        self.value = int(values[self.id])

    def change_value(self, add=0, cursor_x=0):
        if cursor_x:  # cursor_x is the x coordinate of the cursor
            total_size = 2 * self.image.get_size()[0] / 3 - 33  # (2/3) * total image size - adjust
            relative_size = cursor_x - (self.x + self.image.get_size()[0] / 3 + 25)
            self.value = round(10 * relative_size / total_size)
        else:
            self.value += add
        if self.value > 10:
            self.value = 10
            Af.play(error_sound)
        elif self.value < 0:
            self.value = 0
            Af.play(error_sound)
        else:
            Af.play(volume_change_sound, volume=self.value)

    def draw_info(self, screen):
        screen.blit(self.pointer_image, (710, self.y+self.size[1]//2-19))  # draw the head of the arrow (pointer)
        # line from pointer to center line (vertical)
        pygame.draw.line(screen, (0, 255, 255), (755, self.y+self.size[1]//2+3), (755, 343), 5)
        # center line (horizontal)
        pygame.draw.rect(screen, (0, 255, 255), (753, 342, 5, 5))

    def draw(self, screen: Surface):
        screen.blit(self.image, (self.x, self.y))
        [screen.blit(self.value_image, (self.x+145+20*i, self.y+15)) for i in range(self.value)]


class Name_Button(Button):
    def __init__(self, x: int, y: int, active_image: Surface, passive_image: Surface, name: str):
        super().__init__(x, y, None, None)
        self.name = name
        self.active_image = active_image
        self.passive_image = passive_image
        self.image = passive_image

    def activate(self):
        self.image = self.active_image

    def deactivate(self):
        self.image = self.passive_image


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
        data = Af.read_file_content(f"saves/{self.name}/data.txt", 1)[0].split(" ")
        self.best_speed, self.best_time, self.level, self.parts, self.password, self.music_volume, self.sound_volume = \
            int(data[0]), int(data[1]), int(data[2]), int(data[3]), data[4], int(data[5]), int(data[6])
        self.image = Af.load_image(f"menu/interfaces/User/user_info/level{self.level}.png")

    def get_texts(self) -> None:
        self.best_time_text, self.coo_bt_t = Af.writable_best_time(self.best_time)
        self.best_speed_text, self.coo_bs_t = Af.writable_best_speed(self.best_speed)
        self.parts_text, self.coo_p_t = Af.writable_parts_number(self.parts)
        self.name_text, self.coo_n_t = Af.writable_user_name(self.name)

    def draw_text(self, screen: Surface) -> None:
        screen.blit(self.best_time_text, self.coo_bt_t)
        screen.blit(self.best_speed_text, self.coo_bs_t)
        screen.blit(self.parts_text, self.coo_p_t)
        screen.blit(self.name_text, self.coo_n_t)

    def get_active_user(self) -> None:
        data = Af.read_file_content("saves/active_user.txt", 1)[0].split(" ")
        self.name, self.best_speed, self.best_time = data[0], int(data[1]), int(data[2])
        self.level, self.parts, self.password = int(data[3]), int(data[4]), data[5]
        self.music_volume, self.sound_volume = data[6], data[7]
        self.image = Af.load_image(f"menu/interfaces/User/user_info/level{self.level}.png")

    def get_string_attributes(self):
        return f"{self.best_speed} {self.best_time} {self.level} {self.parts} {self.password} {self.music_volume}" \
               f" {self.sound_volume}"

    def turn_active(self) -> None:
        Af.write_file_content("saves/active_user.txt",  f"{self.name} {self.get_string_attributes()}")

    def save_info(self) -> None:
        Af.write_file_content(f"saves/{self.name}/data.txt", self.get_string_attributes())


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

    def draw_ascending(self, screen: Surface):
        for i in range(Af.randint(7, 10)):
            r_x, r_y = self.x + Af.randint(2, 5) * Af.choice([-1, 1]), self.y + Af.randint(2, 5) * Af.choice([-1, 1])
            pygame.draw.circle(screen, Af.choice(self.colors), (r_x, r_y), 1, 1)
        pygame.draw.circle(screen, Af.choice(self.colors), (self.x, self.y), 3, 1)
        self.x += self.x_speed
        self.y += self.y_speed

    def draw_star(self, screen: Surface, min_sparkle_number: int, max_sparkle_number: int):
        for i in range(Af.randint(min_sparkle_number, max_sparkle_number)):
            calculate_rs = Af.choice([Af.calculate_rs_rhomb, Af.calculate_rs_square])  # randomly chooses shape
            r_x, r_y = calculate_rs(self.x, self.y, self.radius)
            pygame.draw.circle(screen, Af.choice(self.colors), (r_x, r_y), 1, 1)

    def draw_circle(self, screen: Surface, min_sparkle_number: int, max_sparkle_number: int):
        for i in range(Af.randint(min_sparkle_number, max_sparkle_number)):
            r_x, r_y = Af.calculate_rs_circle(self.x, self.y, self.radius)
            pygame.draw.circle(screen, Af.choice(self.colors), (r_x, r_y), 1, 1)

    def draw_explosion(self, screen: Surface):
        min_sparkle_number = (200-self.time_alive)*200//100 - 30
        max_sparkle_number = (200 - self.time_alive) * 2 + 30
        types_of_firework = {"star": self.draw_star, "circle": self.draw_circle}
        # noinspection PyArgumentList
        types_of_firework[self.type](screen, min_sparkle_number, max_sparkle_number)
        self.time_alive -= 1
        self.radius += self.radius*0.1
        if self.radius > 100:
            self.alive = False

    def draw(self, screen: Surface):
        if self.y >= self.max_height:
            self.draw_ascending(screen)
        else:
            self.draw_explosion(screen)
        return self.alive


# simulates a group of fireworks by managing single fireworks (Firework class)
class Fireworks:
    y_values = list(range(720, 2000, 40))[:15]

    def __init__(self):
        self.firework_stock = [Firework(self.y_values[i]) for i in range(len(self.y_values))]

    def update(self):
        self.firework_stock = [firework if firework.alive else Firework(720) for firework in self.firework_stock]

    def display(self, screen: Surface):
        update_needed = False  # update should be made only if a firework is dead
        for firework in self.firework_stock:
            if firework.draw(screen):  # draw function returns True if firework is "dead" (which means update is needed)
                update_needed = True
        if update_needed:
            self.update()


# provides a simple way of managing user input, both keyboard and mouse
class Basic_Input_Management:
    def __init__(self, buttons: [Button] = None):
        if buttons is None:
            buttons = []
        self.button_activation_sound = button_y_sound
        self.clock = pygame.time.Clock()
        self.button_list = buttons
        self.active_code = 0
        self.coord_effect = None
        self.already_checked_cursor = False  # True means that actions have already been taken regarding cursor position

    def set_button_to_active(self, new_active_code: int):
        if new_active_code != self.active_code:
            Af.play(self.button_activation_sound)
            self.active_code = new_active_code
            self.coord_effect = self.update_coord_effect()

    def update_coord_effect(self):
        pass

    def manage_events(self):  # returns action to take based on input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                return self.get_effect_by_input(event)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.already_checked_cursor = True
                return self.get_effect_by_input()

    def manage_buttons(self, event: Event):
        if event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
            return self.enter_action()

    def get_effect_by_input(self, event: Event = None):
        if event:  # if input is not None it means a key has been pressed
            effect = self.manage_buttons(event)
        else:
            effect = self.manage_mouse()
        return effect

    def cursor_is_on_button(self):
        mouse_position = pygame.mouse.get_pos()
        for button_index, button in enumerate(self.button_list):
            if button.cursor_is_inside(mouse_position):
                self.set_button_to_active(button_index)
                return True
        return False

    def enter_action(self):
        return self.button_list[self.active_code].effect

    def manage_mouse(self):
        if self.cursor_is_on_button():
            return self.enter_action()
        self.already_checked_cursor = False   # allows the cursor to interact with buttons again after the user clicks


# provides a simple structure for a menu. The Main Menu directly uses it
class Basic_Menu(Basic_Input_Management):
    def __init__(self, screen: Surface, direct: str, buttons: [Button], e_coo: {int: (int, int, int)}, eff: [Surface]):
        super().__init__(buttons)
        self.screen = screen  # screen surface
        self.name = direct.split("/")[-1][:-4]  # the name of the menu (extracted from its directory)
        self.menu_image = Af.load_image(direct)  # image of the menu's background (loaded based on its name)
        self.navigation_image = Af.load_image(f"menu/interfaces/navigation/navigation.png")  # img with info about menu
        self.info_images = [Af.load_image(f"menu/info/info_{self.name}/{i + 1}.png") for i, _ in enumerate(buttons)]
        self.effect = eff  # list of effects to be used for evidencing the buttons
        self.active_code = 0  # index of the active button
        self.current_frame = 0  # frame representing the current state of the button's evidencing effect
        self.effect_coo = e_coo  # coordinates where the effects will be displayed
        self.coord_effect = self.update_coord_effect()  # actual coordinate of the effect currently at use

    def draw_buttons(self):
        self.screen.blit(self.effect[int(self.current_frame)], self.coord_effect)  # draw button's evidencing effect
        [but.draw(self.screen) for but in self.button_list]  # draw each button
        self.button_list[self.active_code].draw_info(self.screen)  # displays information about current active button
        self.current_frame = (self.current_frame + 0.25) % 3  # update frame in a way that it restarts at a value of 3

    def update_coord_effect(self):
        return self.button_list[self.active_code].x-12, self.button_list[self.active_code].y-12

    def get_effect_by_input(self, event: Event = None):
        effect = super().get_effect_by_input(event)
        if effect == "m_ai":
            if Af.get_user_level() < 13:
                return effect
            else:
                Af.show_error_message(self.screen, 12)
        else:
            return effect

    def display_menu(self):
        background = pygame.Surface(self.screen.get_size())
        background.convert().fill((0, 0, 0))
        while True:
            self.clock.tick(30)
            # effect carries information about what to do based on input. None is base case and means "do nothing"
            effect = self.manage_events()  # taking and evaluating input
            if effect is not None:  # if meaningful input is given take respective action
                return effect
            if not self.already_checked_cursor:  # saves time avoiding iterating over buttons when it was done already
                self.cursor_is_on_button()  # mouse visual interaction with interface
            self.refresh(background)

    def manage_buttons(self, event: Event):
        new_active_code = self.active_code  # go up if value is -1 and down if it's 1
        if event.key == pygame.K_UP:
            new_active_code -= 1
        elif event.key == pygame.K_DOWN:
            new_active_code += 1
        elif event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
            return self.enter_action()
        new_active_code = new_active_code % len(self.button_list)  # make sure active_code doesn't go off-boundaries
        self.set_button_to_active(new_active_code)

    def refresh(self, background: Surface):
        self.screen.blit(background, (0, 0))
        self.screen.blit(self.menu_image, (305, 0))
        self.screen.blit(self.navigation_image, (355, 620))
        self.draw_buttons()
        self.screen.blit(self.info_images[self.active_code], (786, 195))
        pygame.display.update()


# provides some changes to the Basic_Menu in order to include a display of user information. Tutorial Menu uses it
class User_Menu(Basic_Menu):
    def __init__(self, screen: Surface, direct: str, buttons: [Button], b_coo: {int: (int, int, int)}, eff: [Surface],
                 user: User):
        super().__init__(screen, direct, buttons, b_coo, eff)
        self.user = user
        self.user_related_images = []
        self.user_related_images.append(Af.load_image(f"menu/interfaces/User/user_info/level{self.user.level}.png"))
        self.user_related_images.append(Af.load_image(f"menu/interfaces/User/records.png"))
        self.user_related_images.append(Af.load_image(f"menu/interfaces/User/parts.png"))
        self.user_related_images.append(Af.load_image(f"cars/display/{self.user.level}.png"))

    def draw_user_related_images(self):
        for coo, image in zip([(0, 0), (20, 280), (0, 180), (2, 490)], self.user_related_images):
            self.screen.blit(image, coo)
        self.user.draw_text(self.screen)

    def refresh(self, background: Surface):
        self.screen.blit(background, (0, 0))
        self.screen.blit(self.menu_image, (305, 0))
        self.screen.blit(self.navigation_image, (355, 620))
        self.draw_user_related_images()
        self.screen.blit(self.info_images[self.active_code], (786, 195))
        self.draw_buttons()
        pygame.display.update()


# ------------------------------------------------- MENU CLASSES -------------------------------------------------------
# Used for "Story", and every Tutorial option
class Menu_image_sequence(Basic_Input_Management):
    def __init__(self, screen: Surface, directory: str, num_pages: int, func_link: str, name: str):
        buttons = [Button(110, 640, "menu/buttons/10/1.png", False), Button(745, 640, "menu/buttons/10/2.png", True)]
        super().__init__(buttons)
        self.screen = screen
        self.name = name
        self.background_image = Af.load_image(f"menu/interfaces/Main/sequence.png")
        self.directory = directory
        self.slide_name = Af.load_image(f"slides/{self.directory}/name.png")
        self.num_pages = num_pages
        self.update_screen = True  # variable that prevents updating screen without need
        self.current_page = 0
        self.origin_link = func_link

    def go_to_next_page(self):
        if self.current_page + 1 == self.num_pages:
            Af.play(error_sound)
        else:
            Af.play(button_y_sound)
            self.current_page += 1
            self.update_screen = True

    def go_to_previous_page(self):
        if self.current_page == 0:
            Af.play(error_sound)
        else:
            Af.play(button_y_sound)
            self.current_page -= 1
            self.update_screen = True

    def manage_buttons(self, event: Event):
        if event.key == pygame.K_RIGHT:
            self.go_to_next_page()
        elif event.key == pygame.K_LEFT:
            self.go_to_previous_page()
        elif event.key == pygame.K_ESCAPE:
            return self.origin_link
        if self.current_page > self.num_pages-1:
            self.current_page = self.num_pages-1
        if self.current_page < 0:
            self.current_page = 0

    def hide_unwanted_button(self):
        if self.current_page == self.num_pages-1:
            pygame.draw.rect(self.screen, (0, 0, 0), (745, 640, 240, 40))
        elif self.current_page == 0:
            pygame.draw.rect(self.screen, (0, 0, 0), (110, 640, 240, 40))

    def write_page_number(self):
        page_image = Af.create_sized_text(20, 50, str(self.current_page + 1), (255, 255, 255))
        self.screen.blit(page_image, (530, 640))

    def enter_action(self):
        if self.button_list[self.active_code].effect:
            self.go_to_next_page()
        else:
            self.go_to_previous_page()

    def refresh(self):
        if not self.update_screen:  # if screen has not been changed menu shouldn't refresh anything
            return None
        self.screen.blit(self.background_image, (0, 0))
        self.screen.blit(Af.load_image(f"slides/{self.directory}/{self.current_page + 1}.png"), (108, 120))
        self.screen.blit(self.slide_name, (400, 0))
        self.write_page_number()
        [button.draw(self.screen) for button in self.button_list]
        self.hide_unwanted_button()  # if at the beginning/end of slides, it won't show the button to go further
        self.update_screen = False
        pygame.display.update()

    def display_menu(self):
        while True:
            self.clock.tick(30)
            effect = self.manage_events()
            if effect is not None:
                return effect
            self.refresh()

# Used for the Game Menu. Just implements some changes in the way some buttons work
class Game_Menu(User_Menu):
    def get_effect_by_input(self, event: Event = None):
        effect = super().get_effect_by_input(event)
        if effect == "m_ai":
            if Af.get_user_level() < 13:
                return effect
            else:
                Af.show_error_message(self.screen, 12)
        else:
            return effect


# Used whenever the user wants to leave the game
class Exit(Basic_Input_Management):
    def __init__(self, directory: str, screen: Surface, buttons: [Button]):
        super().__init__(buttons)
        self.name_image = Af.load_image(directory)
        self.effect = [Af.load_image(f"menu/effects/1/{i + 1}.png") for i in range(4)]
        self.active_code = 0
        self.screen = screen
        self.current_frame = 0

    def draw_buttons(self):
        coordinates = {0: (240, 410), 1: (567, 410)}
        coo = coordinates[self.active_code]
        self.screen.blit(self.effect[int(self.current_frame)], coo)
        self.current_frame += 0.25
        if self.current_frame > 3:
            self.current_frame = 0

    def display_menu(self):
        while True:
            self.clock.tick(30)
            effect = self.manage_events()
            if effect is not None:
                return effect
            if not self.already_checked_cursor:  # saves time avoiding iterating over buttons when it was done already
                self.cursor_is_on_button()  # mouse visual interaction with interface
            self.refresh()

    def manage_buttons(self, event: Event):
        new_active_code = self.active_code  # go up if value is -1 and down if it's 1
        if event.key == pygame.K_RIGHT:
            new_active_code += 1
        elif event.key == pygame.K_LEFT:
            new_active_code -= 1
        elif event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
            return self.button_list[self.active_code].effect
        new_active_code = new_active_code % len(self.button_list)  # make sure active_code doesn't go off-boundaries
        self.set_button_to_active(new_active_code)

    def refresh(self):
        self.screen.blit(self.name_image, (0, 0))
        self.draw_buttons()
        self.screen.blit(Af.load_image(f"menu/interfaces/navigation/navigation2.png"), (350, 600))
        pygame.display.update()


# Used when the "New Game" option in the Main Menu is selected or when, to change some info, credentials are required
class Create_Modify_Account(Basic_Input_Management):
    def __init__(self, directory: str, screen: Surface, buttons: [Button], change: bool = False):
        super().__init__(buttons)
        self.name_image = Af.load_image(directory)
        self.effect = [Af.load_image(f"menu/effects/2/{i + 1}.png") for i in range(4)]
        self.active_code_y = 0
        self.button_activation_sound = button_x_sound
        self.hide = False
        self.screen = screen
        self.inputs = [[], []]
        self.current_frame = 0
        self.user = User()
        self.change = change
        if change:
            self.user.get_active_user()

    def activate_y_button(self, active_code: int):
        self.active_code_y = active_code
        Af.play(button_y_sound)

    def cursor_is_on_button(self):
        mouse_position = pygame.mouse.get_pos()
        if self.button_list[0].cursor_is_inside(mouse_position) and self.active_code_y != 0:
            self.activate_y_button(0)
        elif self.button_list[1].cursor_is_inside(mouse_position) and self.active_code_y != 1:
            self.activate_y_button(1)
        else:
            for button_index, button in enumerate(self.button_list[2:]):
                if button.cursor_is_inside(mouse_position):
                    self.set_button_to_active(button_index)
                    return True
        return False

    def draw_buttons(self) -> None:
        coordinates = {0: (322, 485), 1: (558, 485)}
        coo = coordinates[self.active_code]
        self.screen.blit(self.effect[int(self.current_frame)], (coo[0]-5, coo[1]-10))
        [button.draw(self.screen) for button in self.button_list]
        self.current_frame = (self.current_frame+0.2) % 3

    def display_menu(self):
        while True:
            self.clock.tick(30)
            effect = self.manage_events()
            if effect is not None:  # if meaningful input is given take respective action
                return effect
            if not self.already_checked_cursor:  # saves time avoiding iterating over buttons when it was done already
                self.cursor_is_on_button()  # mouse visual interaction with interface
            self.refresh()

    def create_account(self) -> None:
        name = "".join(self.inputs[0])
        Af.create_folder(name)  # create the user's folder
        content = ["1 \n", "0"]  # user is initiated with Mission AI available and that he didn't win the game
        # create a file in the user's folder named next_level
        Af.write_file_content(f"saves/{name}/next_level.txt", content)

    def validate_user_information(self) -> bool:
        password = "".join(self.inputs[0])
        if self.change:
            if password != self.user.password:
                Af.show_error_message(self.screen, 7)
                return False
            elif len(self.inputs[1]) == 0:
                Af.show_error_message(self.screen, 3)
                return False
            elif " " in self.inputs[1]:
                Af.show_error_message(self.screen, 4)
                return False
        else:
            if password in Af.list_users():
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

    def enter_action(self):
        if self.button_list[self.active_code+2].effect:
            if self.validate_user_information():
                if self.change:
                    Af.show_success_message(self.screen, 4)
                else:
                    self.user.name = "".join(self.inputs[0])
                    self.create_account()
                    Af.show_success_message(self.screen, 1)
                self.user.password = "".join(self.inputs[1])
                self.user.save_info()
                self.user.turn_active()
                return True
            elif self.change:
                return "change_password"
            return "new"
        return False

    def manage_buttons(self, event: Event):
        if event.key == pygame.K_RIGHT:
            Af.play(button_x_sound)
            self.active_code = 1
        elif event.key == pygame.K_LEFT:
            Af.play(button_x_sound)
            self.active_code = 0
        elif event.key == pygame.K_DOWN:
            self.activate_y_button(1)
        elif event.key == pygame.K_UP:
            self.activate_y_button(0)
        elif event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
            return self.enter_action()
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
        self.screen.blit(self.name_image, (0, 0))
        self.draw_buttons()
        self.screen.blit(Af.load_image(f"menu/interfaces/navigation/navigation3.png"), (355, 620))
        Af.write_name_password(self.screen, self.inputs[0], self.inputs[1], self.active_code_y, self.hide)
        pygame.display.update()


# Used when the "Continue" option in the Main Menu is selected
class Choose_Account(Basic_Input_Management):
    def __init__(self, screen: Surface):
        super().__init__()
        self.screen = screen
        self.image = Af.load_image(f"menu/interfaces/Main/choose account.png")
        self.active_code = 0
        self.user = User()
        self.create_buttons()

    def display_menu(self):
        while True:
            self.clock.tick(30)
            effect = self.manage_events()
            if effect is not None:
                return effect
            if not self.already_checked_cursor:  # saves time avoiding iterating over buttons when it was done already
                self.cursor_is_on_button()  # mouse visual interaction with interface
            self.refresh()

    def set_button_to_active(self, new_active_code: int):
        self.button_list[self.active_code].deactivate()  # deactivate previous active button
        super().set_button_to_active(new_active_code)
        self.button_list[self.active_code].activate()  # activate current active button

    def manage_buttons(self, event: Event):
        new_active_code = self.active_code
        if event.key == pygame.K_DOWN:
            new_active_code += 1
        elif event.key == pygame.K_UP:
            new_active_code -= 1
        elif event.key == pygame.K_ESCAPE:
            return "main_menu"
        elif event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
            return self.enter_action()
        new_active_code = new_active_code % len(self.button_list)  # make sure active_code doesn't go off-boundaries
        self.set_button_to_active(new_active_code)

    def enter_action(self):
        if self.button_list:
            self.user.name = self.button_list[self.active_code].name
            self.user.get_info()
            self.user.turn_active()
            return "enter_password"

    def create_buttons(self):
        users = Af.list_users()  # list of usernames in alphabetical order
        if not users:  # if there are no accounts available, user should know therefore menu image is changed
            self.image = Af.load_image(f"menu/interfaces/Main/choose account- no users.png")
            return None
        active, passive = Af.get_users_images()  # lists of button images for both cases of being active or passive
        button_coordinates = [(322, 115 + 55 * i) for i in range(len(users) % 9)]  # max users is 9
        self.button_list = []
        for user_index, coordinates in enumerate(button_coordinates):
            x, y, active_image, passive_image = coordinates[0], coordinates[1], active[user_index], passive[user_index]
            self.button_list.append(Name_Button(x, y, active_image, passive_image, users[user_index]))
        self.button_list[self.active_code].activate()  # first button is set to active

    def refresh(self):
        self.screen.blit(self.image, (0, 0))
        [button.draw(self.screen) for button in self.button_list]
        self.screen.blit(Af.load_image(f"menu/interfaces/navigation/navigation3.png"), (355, 620))
        pygame.display.update()


# Used whenever is required the introduction of a password in order to complete a task
class Enter_Password(Basic_Input_Management):
    def __init__(self, screen: Surface, change: bool = False):
        super().__init__(None)
        self.screen = screen
        self.image = Af.load_image(f"menu/interfaces/Main/insert_password.png")
        self.user = None
        self.password_list = []
        self.create_user()
        self.hide = False
        self.change = change

    def create_user(self):
        self.user = User()
        self.user.get_active_user()  # makes user get his name
        self.user.get_info()  # now that it has his name it can access his folder
        Af.erase_active_user_data()  # user should not be active YET

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
        while True:
            self.clock.tick(30)
            effect = self.manage_events()
            if effect is not None:
                self.user.turn_active()  # NOW user should be active (check method "create_user" for context)
                return effect
            self.refresh()

    def manage_buttons(self, event: Event):
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

    def manage_mouse(self):
        pass

    def refresh(self):
        self.screen.blit(self.image, (210, 250))
        Af.write_password(self.screen, self.password_list, self.hide)
        pygame.display.update()


# Used when the "Management" option in the Game Menu is selected
class Management(Basic_Input_Management):
    def __init__(self, buttons: [Button], directory: str, screen: Surface, user: User = None):
        super().__init__(buttons)
        self.directory = directory
        self.user = user
        self.name_image = Af.load_image(directory)
        self.level_image = Af.load_image(f"menu/interfaces/User/user_info/level{self.user.level}.png")
        self.records_image = Af.load_image(f"menu/interfaces/User/records.png")
        self.navigation_image = Af.load_image(f"menu/interfaces/navigation/navigation.png")
        self.parts_image = Af.load_image(f"menu/interfaces/User/parts.png")
        self.car_image = Af.load_image(f"cars/display/{self.user.level}.png")
        self.effect1 = [Af.load_image(f"menu/effects/5/{i + 1}.png") for i in range(4)]
        self.effect2 = [Af.load_image(f"menu/effects/4/{i + 1}.png") for i in range(4)]
        self.info_images = [Af.load_image(f"menu/info/info_management/{i + 1}.png") for i in range(6)]
        self.active_code = 0
        self.screen = screen
        self.current_frame = 0
        self.coord_effect = self.update_coord_effect()
        
    def update_coord_effect(self):
        if self.active_code < 2:
            return self.button_list[self.active_code].x-10, self.button_list[self.active_code].y-10
        return self.button_list[self.active_code].x-12, self.button_list[self.active_code].y-12

    def draw_buttons(self):
        if self.active_code < 2:
            self.screen.blit(self.effect2[int(self.current_frame)], self.coord_effect)
        else:
            self.screen.blit(self.effect1[int(self.current_frame)], self.coord_effect)
        for but in self.button_list:
            but.draw(self.screen)
        self.current_frame += 0.25
        if self.current_frame > 3:
            self.current_frame = 0

    def display_menu(self):
        while True:
            self.clock.tick(30)
            effect = self.manage_events()
            if effect is not None:
                return effect
            if not self.already_checked_cursor:  # saves time avoiding iterating over buttons when it was done already
                self.cursor_is_on_button()  # mouse visual interaction with interface
            self.refresh()

    def update_user(self):
        self.user.music_volume = self.button_list[0].value
        self.user.sound_volume = self.button_list[1].value
        self.user.save_info()
        self.user.turn_active()

    def manage_buttons(self, event: Event):
        new_active_code = self.active_code  # go up if value is -1 and down if it's 1
        if event.key == pygame.K_UP:
            new_active_code -= 1
        elif event.key == pygame.K_DOWN:
            new_active_code += 1
        elif event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
            return self.enter_action()
        elif self.active_code < 2:  # True means is one of the volume buttons (first two) which is active
            if event.key == pygame.K_LEFT:
                self.button_list[self.active_code].change_value(add=-1)
            elif event.key == pygame.K_RIGHT:
                self.button_list[self.active_code].change_value(add=1)
            self.update_user()
        new_active_code = new_active_code % len(self.button_list)  # make sure active_code doesn't go off-boundaries
        self.set_button_to_active(new_active_code)

    def manage_mouse(self):
        button = self.button_list[self.active_code]
        if self.active_code >= 2:
            return button.effect
        button.change_value(cursor_x=pygame.mouse.get_pos()[0])
        self.already_checked_cursor = False   # allows the cursor to interact with buttons again
        self.update_user()  # save changes in volume

    def refresh(self):
        Af.clean_background(self.screen)
        self.screen.blit(self.name_image, (305, 0))
        self.screen.blit(self.navigation_image, (355, 620))
        self.screen.blit(self.level_image, (0, 0))
        self.screen.blit(self.records_image, (20, 280))
        self.screen.blit(self.parts_image, (0, 180))
        self.screen.blit(self.car_image, (2, 490))
        self.user.draw_text(self.screen)
        self.screen.blit(self.info_images[self.active_code], (786, 195))
        self.button_list[self.active_code].draw_info(self.screen)
        self.draw_buttons()
        pygame.display.update()


# Used every time a "Mission: AI" match is over and the game results must be displayed and processed
class Report_Mission_AI(Basic_Input_Management):
    def __init__(self, screen: Surface, precision: int, speed: int, parts_collected: int,
                 resistance: int, time: int, finished: bool):
        super().__init__()
        self.screen = screen
        self.image = Af.load_image(f"menu/interfaces/Main/Results_AI.png")
        self.requirements_satisfied = False
        self.parts = 0
        self.coordinates = ((635, 360), (635, 300), (622, 397),
                            (515, 360), (515, 300),
                            (713, 275), (713, 336), (713, 397),
                            (725, 503), (725, 471), (725, 540), (725, 576))
        self.values_images = self.initiate_results(precision, speed, parts_collected, resistance, time, finished)
        self.refresh()

    def initiate_results(self, precision: int, speed: int, parts_collected: int,
                         resistance: int, time: int, finished: bool):
        values = []
        # results about level requirements
        c_w = {True: "correct", False: "wrong"}
        font1 = pygame.font.SysFont('Times New Roman', 20)
        font1.set_bold(True)
        values.append(font1.render(str(int(precision)), True, (255, 255, 255)))  # player's achieved precision
        values.append(font1.render(str(int(speed)), True, (255, 255, 255)))  # player's achieved speed
        values.append(Af.load_image(f"menu/interfaces/navigation/{c_w[finished]}.png"))   # player typed all the text
        required_speed, required_precision = Af.get_requirements()  # get required speed and precision to pass level
        values.append(font1.render(str(required_precision), True, (255, 255, 255)))  # player's required precision
        values.append(font1.render(str(required_speed), True, (255, 255, 255)))  # player's required speed
        values.append(Af.load_image(f"menu/interfaces/navigation/{c_w[speed >= required_speed]}.png"))  # speed status
        values.append(Af.load_image(f"menu/interfaces/navigation/{c_w[precision >= required_precision]}.png"))
        values.append(Af.load_image(f"menu/interfaces/navigation/{c_w[finished]}.png"))  # text completed status
        # results about parts
        font1 = pygame.font.SysFont('Times New Roman', 16)
        font1.set_bold(True)
        values.append(font1.render(str(parts_collected), True, (255, 255, 255)))
        values.append(font1.render(str(int(resistance)), True, (255, 255, 255)))
        values.append(font1.render(str((100-int(resistance))*3), True, (255, 255, 255)))
        self.parts = parts_collected-(100-int(resistance))*3
        values.append(font1.render(str(self.parts), True, (255, 255, 255)))
        # verify if requirements were satisfied in order to proceed to next level
        if speed>=required_speed and precision>= required_precision and (int(time)>= 60 or finished):
            self.requirements_satisfied = True
        return values

    def refresh(self):
        self.screen.blit(self.image, (287, 40))
        [self.screen.blit(image, coo) for image, coo in zip(self.values_images, self.coordinates)]
        pygame.display.update()

    def manage_buttons(self, event: Event):
        if event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
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
        while True:
            self.clock.tick(30)
            effect = self.manage_events()
            if effect is not None:
                self.display_level_info_message()
                return self.requirements_satisfied, self.parts
            # self.refresh() -> moved to the constructor since the image is static and doesn't need to refresh


# Used every time a "Mission: PARTS" match is over and the game results must be displayed and processed
class Report_Mission_Parts(Basic_Input_Management):
    def __init__(self, screen: Surface, precision: int, avg_speed: int, max_speed: int,
                 parts_collected: int, time: float):
        super().__init__()
        self.screen = screen
        self.is_cheating = False  # value is set to True if,based on the data given to the constructor, player cheated
        self.image = Af.load_image("menu/interfaces/Main/Results_Parts.png")
        self.parts = 0
        self.time = int(time)
        self.coordinates = [(725, 330), (725, 362), (725, 396), (725, 426), (725, 457), (725, 529)]  # screen x,y values
        self.values_images = self.initiate_results(precision, avg_speed, max_speed, parts_collected)
        self.refresh()

    def initiate_results(self, precision: int, avg_speed: int, max_speed: int, parts_collected: int):
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
        if self.parts == -1300:  # player cheated and it shows because he got penalized
            font2 = pygame.font.SysFont('Times New Roman', 23)
            font2.set_bold(True)
            inform_cheating_1 = "You Cheated!!!"
            inform_cheating_2 = "Your Scores Are Now Nullified and You Will Loose 1300parts"
            values.append(font2.render(inform_cheating_1, True, (255, 0, 0)))
            values.append(font1.render(inform_cheating_2, True, (255, 0, 0)))
            self.coordinates.append((460, 200))
            self.coordinates.append((315, 240))
        return values

    def refresh(self):
        self.screen.blit(self.image, (287, 40))
        [self.screen.blit(image, coo) for image, coo in zip(self.values_images, self.coordinates)]
        pygame.display.update()

    def manage_buttons(self, event: Event):
        if event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
            return True
        return False

    def display(self):
        while True:
            self.clock.tick(30)
            effect = self.manage_events()
            if effect is not None:
                return self.parts
            # self.refresh() -> moved to the constructor since the image is static and doesn't need to refresh


# Used every time a user manages to level up, and he must unlock the "Mission: AI" option in the Game Menu
class Unlock_Level(Basic_Input_Management):
    def __init__(self, screen: Surface):
        super().__init__()
        self.screen = screen
        self.image = Af.load_image("menu/interfaces/Main/unlock level.png")
        self.user = None
        self.parts_needed = None
        self.create_user()

    def create_user(self):
        self.user = User()
        self.user.get_active_user()
        self.user.get_info()
        content = Af.read_file_content(f"parameters/levels info/{self.user.level}.txt", 1)[0].split(" ")[2]
        self.parts_needed = int(content)

    def show_error_message(self) -> None:
        Af.show_error_message(self.screen, 9)

    def show_success_message(self) -> None:
        Af.show_success_message(self.screen, 6)

    def verify_parts_number(self):
        return self.parts_needed <= self.user.parts

    def save_state(self):
        Af.write_file_content(f"saves/{self.user.name}/next_level.txt", "1")
        self.user.parts = self.user.parts - self.parts_needed
        self.user.save_info()
        self.user.turn_active()

    def parts_image(self):
        return Af.create_sized_text(190, 50, str(self.parts_needed), (255, 180, 0))

    def display_menu(self):
        while True:
            self.clock.tick(30)
            effect = self.manage_events()
            if effect is not None:
                return effect
            self.refresh()

    def manage_buttons(self, event: Event):
        if event.key == pygame.K_ESCAPE:
            return True
        elif event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
            if self.verify_parts_number():
                self.show_success_message()
                self.save_state()
                return True
            self.show_error_message()
            return True

    def refresh(self):
        self.screen.blit(self.image, (210, 250))
        self.screen.blit(self.parts_image(), (635, 310))
        pygame.display.update()


# The first Interface that shows up when the game is executed. It shows "Fast and Curious"'s logo
class Start:
    def __init__(self, screen: Surface):
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
        while True:
            self.time += clock.tick(30) / 990
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONUP:
                    return True
            self.refresh()

    def refresh(self):
        self.screen.blit(self.image, (0, 0))
        self.show_directives()
        pygame.display.update()


# Used when the "New Game" option in the Main Menu is selected
class Add_Text(Basic_Input_Management):
    def __init__(self, screen: Surface, buttons: [Button]):
        super().__init__(buttons)
        self.image = Af.load_image(f"menu/interfaces/Main/add text.png")
        self.effect = [Af.load_image(f"menu/effects/2/{i + 1}.png") for i in range(4)]
        self.active_code = 0
        self.text_lines_images = None
        self.screen = screen
        Af.clean_background(self.screen)  # hide previous interface
        self.character_number = 0
        self.written_text = ""
        self.error_code = 0
        self.current_frame = 0
        self.text_lines = []

    def draw_buttons(self) -> None:
        coordinates = {0: (320, 484), 1: (558, 484)}
        coo = coordinates[self.active_code]
        self.screen.blit(self.effect[int(self.current_frame)], (coo[0]-5, coo[1]-10))
        [button.draw(self.screen) for button in self.button_list]
        self.current_frame = (self.current_frame+0.2) % 3

    def show_error_message(self) -> None:
        Af.show_error_message(self.screen, self.error_code)
        Af.clean_background(self.screen)

    def show_success_message(self) -> None:
        Af.show_success_message(self.screen, 7)

    def display_menu(self):
        while True:
            self.clock.tick(30)
            effect = self.manage_events()
            if effect is not None:
                break
            if not self.already_checked_cursor:  # saves time avoiding iterating over buttons when it was done already
                self.cursor_is_on_button()  # mouse visual interaction with interface
            self.refresh()

    def create_text_content(self) -> [str]:
        text_content = [f"{len(self.text_lines)} \n"]  # first line of these files holds the number of lines in the text
        for line in self.text_lines:
            text_content.append(line + "\n")
        return text_content

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
        Af.write_file_content(f"texts/{last_number_text+1}.txt", self.create_text_content())

    def validate_text_information(self) -> bool:
        special = [",", ".", "'", " "]
        if self.character_number < 192:
            self.error_code = 10
            return False
        ch_list = set(self.written_text)
        for char in ch_list:  # verify that there are no special characters or numbers
            if char.isalpha() or char in special:
                continue
            self.error_code = 11
            return False
        return True

    def last_word_is_proper(self):
        if self.written_text != "":
            last_word_length = len(self.written_text.split()[-1])
            return last_word_length < 48
        return True

    def manage_buttons(self, event: Event):
        if event.key == pygame.K_RIGHT:
            Af.play(button_x_sound)
            self.active_code = 1
        elif event.key == pygame.K_LEFT:
            Af.play(button_x_sound)
            self.active_code = 0
        elif event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
            return self.enter_action()
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

    def enter_action(self):
        if not self.active_code:
            return True
        if self.validate_text_information():
            self.create_text()
            self.show_success_message()
            return True
        self.show_error_message()
        self.already_checked_cursor = False  # make sure cursor gets checked after pressing a button

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

    def __init__(self, screen: Surface):
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
