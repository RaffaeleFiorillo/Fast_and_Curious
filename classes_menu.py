import pygame
import functions as f


class Button:
    def __init__(self, x, y, directory, effect, code):
        self.x = x
        self.y = y
        self.image = pygame.image.load(directory)
        self.effect = effect
        self.code = code

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def change_image(self, directory):
        self.image = pygame.image.load(directory)


class Button2(Button):
    def __init__(self, x, y, directory, effect, code, id_c):
        super().__init__(x, y, directory, effect, code)
        self.value = 0
        self.effect = "manage"
        self.id = id_c
        self.value_image = pygame.image.load("images/menu/buttons/8/7.png")
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
        elif self.value < 0:
            self.value = 0

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        [screen.blit(self.value_image, (self.x+145+20*i, self.y+15)) for i in range(self.value)]


class User:
    def __init__(self, name=""):
        self.name = name
        self.password = ""
        self.best_speed = 0
        self.best_time = 0
        self.level = 1
        self.parts = 0
        self.image = pygame.image.load("images/menu/interfaces/User/user_info/level1.png")
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
        self.image = pygame.image.load(f"images/menu/interfaces/User/user_info/level{self.level}.png")
        file.close()

    def get_texts(self) -> None:
        self.best_time_text, self.coo_bt_t = f.writable_best_time(self.best_time)
        self.best_speed_text, self.coo_bs_t = f.writable_best_speed(self.best_speed)
        self.parts_text, self.coo_p_t = f.writable_parts_number(self.parts)
        self.name_text, self.coo_n_t = f.writable_user_name(self.name)

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
        self.image = pygame.image.load(f"images/menu/interfaces/User/user_info/level{self.level}.png")
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


class Menu_image_sequence:
    def __init__(self, screen, pasta, num_pages, func_link, name):
        self.screen = screen
        self.name = name
        self.background_image = pygame.image.load("images/menu/interfaces/Main/sequence.png")
        self.images_list = [pygame.image.load(f"images/slides/{pasta}/{i+1}.png") for i in range(num_pages)]
        self.slide_name = pygame.image.load(f"images/slides/{pasta}/name.png")
        self.num_pages = num_pages
        self.current_page = 0
        self.origin_link = func_link

    def manage_buttons(self, keys):
        if keys[pygame.K_RIGHT]:
            self.current_page += 1
        elif keys[pygame.K_LEFT]:
            self.current_page -= 1
        elif keys[pygame.K_KP_ENTER] or keys[pygame.K_RETURN]:
            if self.current_page == self.num_pages:
                return self.origin_link
        elif keys[pygame.K_ESCAPE]:
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

    def refresh(self):
        self.screen.blit(self.background_image, (0, 0))
        self.screen.blit(self.images_list[self.current_page], (108, 120))
        self.screen.blit(self.slide_name, (400, 0))
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
                    effect = self.manage_buttons(pygame.key.get_pressed())
                    if effect is not None:
                        return effect
            self.refresh()


class Menu:
    def __init__(self, buttons, directory, screen, user=None):
        self.internal_list = buttons
        self.directory = directory
        self.name = self.directory.split("/")[-1][:-4]
        self.image_nome = pygame.image.load(directory)
        if self.name == "game menu":
            self.effect = [pygame.image.load(f"images/menu/effects/3/{i+1}.png") for i in range(4)]
        else:
            self.effect = [pygame.image.load(f"images/menu/effects/1/{i+1}.png") for i in range(4)]
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
        self.screen.blit(pygame.image.load(f"images/menu/info/info_{self.name}/{self.active_code+1}.png"),
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
                    effect = self.manage_buttons(pygame.key.get_pressed())
                    if effect is not None:
                        return effect
            self.refresh(background)

    def manage_buttons(self, keys):
        valor = 0
        if keys[pygame.K_UP]:
            valor = -1
        elif keys[pygame.K_DOWN]:
            valor = 1
        elif keys[pygame.K_KP_ENTER] or keys[pygame.K_RETURN]:
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
        self.screen.blit(pygame.image.load("images/menu/interfaces/navigation/navigation.png"), (355, 620))
        if self.user is not None:
            coo = (20, 490)
            self.screen.blit(pygame.image.load(f"images/menu/interfaces/User/user_info/level{self.user.level}.png"),
                             (0, 0))
            self.screen.blit(pygame.image.load(f"images/menu/interfaces/User/records.png"), (coo[0], coo[1]-210))
            self.screen.blit(pygame.image.load(f"images/menu/interfaces/User/parts.png"), (0, coo[1] - 310))
            self.screen.blit(pygame.image.load(f"images/cars/display/{self.user.level}.png"), (coo[0] - 18, coo[1]))
            self.user.draw_text(self.screen)
        self.draw_buttons()
        pygame.display.update()


class Exit:
    def __init__(self, directory, screen):
        self.image_nome = pygame.image.load(directory)
        self.effects = (True, False)
        self.effect = [pygame.image.load(f"images/menu/effects/1/{i+1}.png") for i in range(4)]
        self.active_code = 0
        self.screen = screen
        self.current_frame = 0

    def draw_buttons(self):
        coordinates = {0: (240, 410), 1: (570, 410)}
        coo = coordinates[self.active_code]
        self.screen.blit(self.effect[int(self.current_frame)], coo)
        self.screen.blit(pygame.image.load(f"images/menu/buttons/3/{self.active_code+1}.png"), (coo[0]+13, coo[1]+10))
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
                    effect = self.manage_buttons(pygame.key.get_pressed())
                    if effect is not None:
                        return effect
            self.refresh()

    def manage_buttons(self, keys):
        valor = 0
        if keys[pygame.K_RIGHT]:
            valor = 1
        elif keys[pygame.K_LEFT]:
            valor = -1
        elif keys[pygame.K_KP_ENTER] or keys[pygame.K_RETURN]:
            return self.effects[self.active_code]
        self.active_code += valor
        if self.active_code > len(self.effects)-1:
            self.active_code = 0
        if self.active_code < 0:
            self.active_code = 1

    def refresh(self):
        self.screen.blit(self.image_nome, (0, 0))
        self.draw_buttons()
        self.screen.blit(pygame.image.load("images/menu/interfaces/navigation/navigation2.png"), (350, 600))
        pygame.display.update()


class Create_Account:
    def __init__(self, directory, screen, change=False):
        self.image_nome = pygame.image.load(directory)
        self.effects = (False, True)
        self.effect = [pygame.image.load(f"images/menu/effects/2/{i+1}.png") for i in range(4)]
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
            self.screen.blit(pygame.image.load(f"images/menu/buttons/9/{self.active_code_x + 1}.png"),
                             (coo[0] + 13, coo[1] + 10))
        else:
            self.screen.blit(pygame.image.load(f"images/menu/buttons/5/{self.active_code_x+1}.png"),
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
                    effect = self.manage_buttons(pygame.key.get_pressed(), event)
                    if effect is not None:
                        return effect
            self.refresh()

    def create_account(self) -> None:
        name = "".join(self.inputs[0])
        f.create_folder(name)

    def validate_user_information(self) -> bool:
        first, second = "".join(self.inputs[0]), "".join(self.inputs[1])
        if self.change:
            if first != self.user.password:
                f.show_error_message(self.screen, 7)
                return False
            elif len(self.inputs[1]) == 0:
                f.show_error_message(self.screen, 3)
                return False
            elif " " in self.inputs[1]:
                f.show_error_message(self.screen, 4)
                return False
        else:
            if first in f.list_users():
                f.show_error_message(self.screen, 1)
                return False
            elif len(self.inputs[0]) == 0:
                f.show_error_message(self.screen, 2)
                return False
            elif len(self.inputs[1]) == 0:
                f.show_error_message(self.screen, 3)
                return False
            elif " " in self.inputs[0] or " " in self.inputs[1]:
                f.show_error_message(self.screen, 4)
                return False
        return True

    def manage_buttons(self, keys, event):
        if keys[pygame.K_RIGHT]:
            self.active_code_x = 1
        elif keys[pygame.K_LEFT]:
            self.active_code_x = 0
        elif keys[pygame.K_DOWN]:
            self.active_code_y = 1
        elif keys[pygame.K_UP]:
            self.active_code_y = 0
        elif keys[pygame.K_KP_ENTER] or keys[pygame.K_RETURN]:
            if self.effects[self.active_code_x]:
                if self.validate_user_information():
                    if self.change:
                        self.user.password = "".join(self.inputs[1])
                        self.user.save_info()
                        self.user.turn_active()
                        f.show_success_message(self.screen, 4)
                    else:
                        self.user.name = "".join(self.inputs[0])
                        self.user.password = "".join(self.inputs[1])
                        self.create_account()
                        self.user.save_info()
                        self.user.turn_active()
                        f.show_success_message(self.screen, 1)
                    return True
                else:
                    if self.change:
                        return "change_password"
                    return "new"
            return False
        elif keys[pygame.K_TAB]:
            self.hide = not self.hide
        elif event.key == pygame.K_BACKSPACE:
            self.inputs[self.active_code_y] = self.inputs[self.active_code_y][:-1]
        elif len(self.inputs[self.active_code_y]) <= 25 and self.active_code_y == 1:
            self.inputs[self.active_code_y].append(event.unicode)
        elif len(self.inputs[self.active_code_y]) <= 20 and self.active_code_y == 0:
            self.inputs[self.active_code_y].append(event.unicode)

    def refresh(self) -> None:
        self.screen.blit(self.image_nome, (0, 0))
        self.draw_buttons()
        self.screen.blit(pygame.image.load("images/menu/interfaces/navigation/navigation3.png"), (355, 620))
        f.write_name_password(self.screen, self.inputs[0], self.inputs[1], self.active_code_y, self.hide)
        pygame.display.update()


class Choose_Account:
    def __init__(self, screen):
        self.screen = screen
        self.image = pygame.image.load("images/menu/interfaces/Main/choose account.png")
        self.effect = [pygame.image.load(f"images/menu/effects/2/{i+1}.png") for i in range(4)]
        self.passive_button_image = pygame.image.load("images/menu/buttons/6/2.png")
        self.active_button_image = pygame.image.load("images/menu/buttons/6/1.png")
        self.button_coordinates = [(322, 120), (322, 175), (322, 230), (322, 285), (322, 340), (322, 395), (322, 450)]
        self.account_name = None
        self.current_frame = 0
        self.active_code_x = 1
        self.active_code_y = 0
        self.buttons = []
        self.previous_button = 0
        self.users = f.list_users()
        self.user_names_images_active, self.user_names_images_passive = f.get_users_images()
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
                    effect = self.manage_buttons(pygame.key.get_pressed())
                    if effect is not None:
                        return effect
            self.refresh()

    def manage_buttons(self, keys):
        if keys[pygame.K_RIGHT]:
            self.active_code_x = 1
        elif keys[pygame.K_LEFT]:
            self.active_code_x = 0
        elif keys[pygame.K_DOWN]:
            self.active_code_y += 1
            self.previous_button = self.active_code_y-1
        elif keys[pygame.K_UP]:
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
        if keys[pygame.K_KP_ENTER] or keys[pygame.K_RETURN]:
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
                                       "images/menu/buttons/6/2.png", None, self.users.index(user)))
        self.set_active_button()

    def set_active_button(self):
        self.adjust_user_name_images()
        self.buttons[self.previous_button].image = self.passive_button_image
        self.buttons[self.active_code_y].image = self.active_button_image

    def refresh(self):
        coordinates = {0: (325, 520), 1: (558, 520)}
        coo = coordinates[self.active_code_x]
        self.screen.blit(self.image, (0, 0))
        self.screen.blit(self.effect[int(int(self.current_frame))], (coo[0]-5, coo[1]-20))
        self.screen.blit(pygame.image.load(f"images/menu/buttons/7/{self.active_code_x+1}.png"), (coo[0]+13, coo[1]))
        [self.buttons[i].draw(self.screen) for i in range(len(self.users))]
        [self.screen.blit(self.user_names_images[i], (self.button_coordinates[i][0]+10, self.button_coordinates[i][1]))
         for i in range(len(self.users))]
        self.screen.blit(pygame.image.load("images/menu/interfaces/navigation/navigation3.png"), (355, 620))
        pygame.display.update()


class Enter_Password:
    def __init__(self, screen, change=False):
        self.screen = screen
        self.image = pygame.image.load("images/menu/interfaces/Main/insert_password.png")
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
        self.screen.blit(pygame.image.load(f"images/menu/messages/error5.png"), (230, 200))
        pygame.display.update()
        f.wait(3)
        self.screen.blit(pygame.image.load("images/menu/interfaces/prov_image/prov_image.png"), (0, 0))

    def show_success_message(self) -> None:
        if self.change:
            self.screen.blit(pygame.image.load("images/menu/messages/success3.png"), (230, 200))
            time = 3
        else:
            self.screen.blit(pygame.image.load("images/menu/messages/success2.png"), (230, 200))
            f.write_name(self.screen, self.user.name)
            time = 1
        pygame.display.update()
        f.wait(time)

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
                    effect = self.manage_buttons(pygame.key.get_pressed(), event)
                    if effect is not None:
                        return effect
            self.refresh()

    def manage_buttons(self, keys, event):
        if event.key == pygame.K_BACKSPACE:
            self.password_list = self.password_list[:-1]
        elif keys[pygame.K_ESCAPE]:
            if self.change:
                return "manage"
            return "choose"
        elif keys[pygame.K_TAB]:
            self.hide = not self.hide
        elif keys[pygame.K_KP_ENTER] or keys[pygame.K_RETURN]:
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
        pygame.draw.rect(self.screen, (0, 0, 0), (550, 500, 213, 105), 20, True)
        f.write_password(self.screen, self.password_list, self.hide)
        pygame.display.update()


class Management:
    def __init__(self, buttons, directory, screen, user=None):
        self.list = buttons
        self.directory = directory
        self.image_nome = pygame.image.load(directory)
        self.effect1 = [pygame.image.load(f"images/menu/effects/5/{i+1}.png") for i in range(4)]
        self.effect2 = [pygame.image.load(f"images/menu/effects/4/{i+1}.png") for i in range(4)]
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
                    effect = self.manage_buttons(pygame.key.get_pressed())
                    if effect is not None:
                        return effect
            self.refresh()

    def update_user(self):
        self.user.music_volume = self.list[0].value
        self.user.sound_volume = self.list[1].value
        self.user.save_info()
        self.user.turn_active()

    def manage_buttons(self, keys):
        if keys[pygame.K_UP]:
            self.active_code -= 1
        elif keys[pygame.K_DOWN]:
            self.active_code += 1
        elif self.active_code == 0 or self.active_code == 1:
            if keys[pygame.K_LEFT]:
                self.list[self.active_code].change_value(-1)
            elif keys[pygame.K_RIGHT]:
                self.list[self.active_code].change_value(1)
            self.update_user()
        elif keys[pygame.K_KP_ENTER] or keys[pygame.K_RETURN]:
            return self.list[self.active_code].effect
        if self.active_code > len(self.list)-1:
            self.active_code = 0
        if self.active_code < 0:
            self.active_code = len(self.list)-1
        self.coord_effect = (self.list[self.active_code].x-12, self.list[self.active_code].y-12)

    def refresh(self):
        f.clean_background(self.screen)
        self.screen.blit(self.image_nome, ((1080-470)//2, 0))
        self.screen.blit(pygame.image.load("images/menu/interfaces/navigation/navigation.png"), (355, 620))
        coo = (20, 490)
        self.screen.blit(pygame.image.load(f"images/menu/interfaces/User/user_info/level{self.user.level}.png"), (0, 0))
        self.screen.blit(pygame.image.load(f"images/menu/interfaces/User/records.png"), (coo[0], coo[1]-210))
        self.screen.blit(pygame.image.load(f"images/menu/interfaces/User/parts.png"), (0, coo[1] - 310))
        self.screen.blit(pygame.image.load(f"images/cars/display/{self.user.level}.png"), (coo[0]-18, coo[1]))
        self.user.draw_text(self.screen)
        coordinates = {0: (680, 90), 1: (680, 90), 2: (698, 192), 3: (685, 178), 4: (685, 178), 5: (685, 178)}
        coo = coordinates[self.active_code]
        self.screen.blit(pygame.image.load(f"images/menu/info/info_{self.name}/{self.active_code+1}.png"),
                         (coo[0], coo[1]))
        self.draw_buttons()
        pygame.display.update()


class Results_AI:
    def __init__(self, screen, precision, speed, parts_collected, resistance, time):
        self.screen = screen
        self.image = pygame.image.load("images/menu/interfaces/Main/Results_AI.png")
        self.requirements_satisfied = False
        self.parts = 0
        self.values_images = self.initiate_results(precision, speed, parts_collected, resistance, time)

    def initiate_results(self, precision, speed, parts_collected, resistance, time):
        values = []
        # results about level requirements
        c_w = {True: "correct", False: "wrong"}
        font1 = pygame.font.SysFont('Times New Roman', 20)
        font1.set_bold(True)
        values.append(font1.render(str(int(precision)), True, (255, 255, 255)))
        values.append(font1.render(str(int(speed)), True, (255, 255, 255)))
        speed2, precision2 = f.get_requirements()
        values.append(font1.render(str(precision2), True, (255, 255, 255)))
        values.append(font1.render(str(speed2), True, (255, 255, 255)))
        values.append(pygame.image.load(f"images/menu/interfaces/navigation/{c_w[speed>=speed2]}.png"))
        values.append(pygame.image.load(f"images/menu/interfaces/navigation/{c_w[precision>=precision2]}.png"))
        # results about parts
        font1 = pygame.font.SysFont('Times New Roman', 16)
        font1.set_bold(True)
        values.append(font1.render(str(parts_collected), True, (255, 255, 255)))
        values.append(font1.render(str(int(resistance)), True, (255, 255, 255)))
        values.append(font1.render(str((100-int(resistance))*3), True, (255, 255, 255)))
        self.parts = parts_collected-(100-int(resistance))*3
        values.append(font1.render(str(self.parts), True, (255, 255, 255)))
        # verify if requirements were satisfied in order to proceed to next level
        if speed>=speed2 and precision>=precision2 and int(time)>= 60:
            self.requirements_satisfied = True
        return values

    def refresh(self):
        coordinates = ((635, 360), (635, 300), (515, 360), (515, 300), (713, 275), (713, 336), (725, 457), (725, 425),
                       (725, 494), (725, 530))
        self.screen.blit(self.image, (287, 40))
        [self.screen.blit(image, coo) for image, coo in zip(self.values_images, coordinates)]
        pygame.display.update()

    @staticmethod
    def manage_buttons(keys):
        if keys[pygame.K_KP_ENTER] or keys[pygame.K_RETURN]:
            return True
        return False

    def display_level_info_message(self):
        message_dict = {True: "success5", False: "error8"}
        time_dict = {True: 3, False: 6}
        message = message_dict[self.requirements_satisfied]
        time = time_dict[self.requirements_satisfied]
        self.screen.blit(pygame.image.load(f"images/menu/messages/{message}.png"), (230, 200))
        pygame.display.update()
        f.wait(time)

    def display(self):
        clock = pygame.time.Clock()
        keepGoing = True
        while keepGoing:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return self.requirements_satisfied, self.parts
                if event.type == pygame.KEYDOWN:
                    if self.manage_buttons(pygame.key.get_pressed()):
                        self.display_level_info_message()
                        return self.requirements_satisfied, self.parts
            self.refresh()


class Results_Parts:
    def __init__(self, screen, precision, speed, parts_collected, time):
        self.screen = screen
        self.image = pygame.image.load("images/menu/interfaces/Main/Results_Parts.png")
        self.parts = 0
        self.time = int(time)
        self.values_images = self.initiate_results(precision, speed, parts_collected)

    def initiate_results(self, precision, speed, parts_collected):
        values = []
        # results about parts
        font1 = pygame.font.SysFont('Times New Roman', 16)
        font1.set_bold(True)
        values.append(font1.render(str(int(precision)), True, (255, 255, 255)))
        values.append(font1.render(str(int(speed)), True, (255, 255, 255)))
        values.append(font1.render(str(self.time), True, (255, 255, 255)))
        values.append(font1.render(str(parts_collected), True, (255, 255, 255)))
        self.parts = parts_collected-300
        values.append(font1.render(str(self.parts), True, (255, 255, 255)))
        return values

    def refresh(self):
        coordinates = ((725, 357), (725, 390),  (725, 426), (725, 457), (725, 529))
        self.screen.blit(self.image, (287, 40))
        [self.screen.blit(image, coo) for image, coo in zip(self.values_images, coordinates)]
        pygame.display.update()

    @staticmethod
    def manage_buttons(keys):
        if keys[pygame.K_KP_ENTER] or keys[pygame.K_RETURN]:
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
                    if self.manage_buttons(pygame.key.get_pressed()):
                        return self.parts
            self.refresh()
