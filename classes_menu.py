import pygame
import funcoes as f


class Button:
    def __init__(self, x, y, diretorio, efeito, codigo):
        self.x = x
        self.y = y
        self.image = pygame.image.load(diretorio)
        self.efeito = efeito
        self.codigo = codigo

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def change_image(self, diretorio):
        self.image = pygame.image.load(diretorio)


class Button2(Button):
    def __init__(self, x, y, diretorio, efeito, codigo, id_c):
        super().__init__(x, y, diretorio, efeito, codigo)
        self.value = 0
        self.efeito = "manage"
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
        self.best_time_text, self.coo_bt_t = f.writeble_best_time(self.best_time)
        self.best_speed_text, self.coo_bs_t = f.writeble_best_speed(self.best_speed)
        self.parts_text, self.coo_p_t = f.writeble_parts_number(self.parts)
        self.name_text, self.coo_n_t = f.writeble_user_name(self.name)

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
        file.write(f"{self.name} {self.best_speed} {self.best_time} {self.level} {self.parts} {self.password} {self.music_volume} {self.sound_volume}")
        file.close()

    def save_info(self) -> None:
        file = open(f"saves/{self.name}/data.txt", "w")
        data = f"{self.best_speed} {self.best_time} {self.level} {self.parts} {self.password} {self.music_volume} {self.sound_volume}"
        file.write(data)
        file.close()


class Menu_image_sequence:
    def __init__(self, screen, pasta, num_paginas, func_link, name):
        self.screen = screen
        self.name = name
        self.background_image = pygame.image.load("images/menu/interfaces/Main/sequence.png")
        self.images_list = [pygame.image.load(f"images/menu/interfaces/sequences/{pasta}/{i}.png") for i in range(num_paginas)]
        self.num_pages = num_paginas
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
        if self.current_page > self.num_pages:
            self.current_page = self.num_pages
        if self.current_page < 0:
            self.current_page = 0

    def refresh(self):
        self.screen.blit(self.background_image, (0, 0))
        self.screen.blit(self.images_list[self.current_page], (100, 100))
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
                    efeito = self.manage_buttons(pygame.key.get_pressed())
                    if efeito is not None:
                        return efeito
            self.refresh()


class Menu:
    def __init__(self, buttons, diretorio, superficie, user=None):
        self.lista = buttons
        self.diretorio = diretorio
        self.name = self.diretorio.split("/")[-1][:-4]
        self.image_nome = pygame.image.load(diretorio)
        if self.name == "game menu":
            self.efeito = [pygame.image.load(f"images/menu/effects/3/{i+1}.png") for i in range(4)]
        else:
            self.efeito = [pygame.image.load(f"images/menu/effects/1/{i+1}.png") for i in range(4)]
        self.codigo_ativo = 0
        self.screen = superficie
        self.frame_atual = 0
        self.user = user
        self.coord_efeito = (self.lista[0].x-12, self.lista[0].y-12)

    def draw_buttons(self):
        coordenadas = {0: (680, 90), 1: (698, 192), 2: (685, 178)}
        coordenadas2 = {0: (687, 90), 1: (687, 90), 2: (687, 192), 3: (687, 178), 4: (687, 178),  5: (687, 178)}
        coordenadas3 = {0: (680, 90), 1: (680, 90), 2: (698, 192), 3: (685, 178), 4: (685, 178)}
        ch = {"main menu": coordenadas, "game menu": coordenadas2, "tutorial": coordenadas3}
        co_cho = ch[self.name]
        coo = co_cho[self.codigo_ativo]
        self.screen.blit(self.efeito[int(self.frame_atual)], self.coord_efeito)
        self.screen.blit(pygame.image.load(f"images/menu/info/info_{self.name}/{self.codigo_ativo+1}.png"), (coo[0], coo[1]))
        for but in self.lista:
            but.draw(self.screen)
        self.frame_atual += 0.25
        if self.frame_atual > 3:
            self.frame_atual = 0

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
                    efeito = self.manage_buttons(pygame.key.get_pressed())
                    if efeito is not None:
                        return efeito
            self.refresh(background)

    def manage_buttons(self, keys):
        valor = 0
        if keys[pygame.K_UP]:
            valor = -1
        elif keys[pygame.K_DOWN]:
            valor = 1
        elif keys[pygame.K_KP_ENTER] or keys[pygame.K_RETURN]:
            return self.lista[self.codigo_ativo].efeito
        self.codigo_ativo += valor
        if self.codigo_ativo > len(self.lista)-1:
            self.codigo_ativo = 0
        if self.codigo_ativo < 0:
            self.codigo_ativo = len(self.lista)-1
        self.coord_efeito = (self.lista[self.codigo_ativo].x-12, self.lista[self.codigo_ativo].y-12)

    def refresh(self, background):
        self.screen.blit(background, (0, 0))
        self.screen.blit(self.image_nome, ((1080-470)//2, 0))
        self.screen.blit(pygame.image.load("images/menu/interfaces/navigation/navigation.png"), (355, 620))
        if self.user is not None:
            coo = (20, 490)
            self.screen.blit(pygame.image.load(f"images/menu/interfaces/User/user_info/level{self.user.level}.png"), (0, 0))
            self.screen.blit(pygame.image.load(f"images/menu/interfaces/User/car_window.png"), coo)
            self.screen.blit(pygame.image.load(f"images/menu/interfaces/User/records.png"), (coo[0], coo[1]-210))
            self.screen.blit(pygame.image.load(f"images/menu/interfaces/User/parts.png"), (0, coo[1] - 310))
            self.screen.blit(pygame.image.load(f"images/cars/display/{self.user.level}.png"), (coo[0]+15, coo[1]+53))
            self.user.draw_text(self.screen)
        self.draw_buttons()
        pygame.display.update()


class Exit:
    def __init__(self, diretorio, superficie):
        self.image_nome = pygame.image.load(diretorio)
        self.effects = (True, False)
        self.efeito = [pygame.image.load(f"images/menu/effects/1/{i+1}.png") for i in range(4)]
        self.codigo_ativo = 0
        self.screen = superficie
        self.frame_atual = 0

    def draw_buttons(self):
        coordenadas = {0: (240, 410), 1: (570, 410)}
        coo = coordenadas[self.codigo_ativo]
        self.screen.blit(self.efeito[int(self.frame_atual)], coo)
        self.screen.blit(pygame.image.load(f"images/menu/buttons/3/{self.codigo_ativo+1}.png"), (coo[0]+13, coo[1]+10))
        self.frame_atual += 0.25
        if self.frame_atual > 3:
            self.frame_atual = 0

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
                    efeito = self.manage_buttons(pygame.key.get_pressed())
                    if efeito is not None:
                        return efeito
            self.refresh()

    def manage_buttons(self, keys):
        valor = 0
        if keys[pygame.K_RIGHT]:
            valor = 1
        elif keys[pygame.K_LEFT]:
            valor = -1
        elif keys[pygame.K_KP_ENTER] or keys[pygame.K_RETURN]:
            return self.effects[self.codigo_ativo]
        self.codigo_ativo += valor
        if self.codigo_ativo > len(self.effects)-1:
            self.codigo_ativo = 0
        if self.codigo_ativo < 0:
            self.codigo_ativo = 1

    def refresh(self):
        self.screen.blit(self.image_nome, (0, 0))
        self.draw_buttons()
        self.screen.blit(pygame.image.load("images/menu/interfaces/navigation/navigation2.png"), (350, 600))
        pygame.display.update()


class Create_Account:
    def __init__(self, diretorio, superficie):
        self.image_nome = pygame.image.load(diretorio)
        self.effects = (False, True)
        self.efeito = [pygame.image.load(f"images/menu/effects/2/{i+1}.png") for i in range(4)]
        self.codigo_ativo_x = 0
        self.codigo_ativo_y = 0
        self.hide = False
        self.screen = superficie
        self.inputs = [[], []]
        self.frame_atual = 0
        self.user = User()

    def draw_buttons(self) -> None:
        coordenadas = {0: (325, 485), 1: (558, 485)}
        coo = coordenadas[self.codigo_ativo_x]
        self.screen.blit(self.efeito[int(self.frame_atual)], (coo[0]-5, coo[1]-10))
        self.screen.blit(pygame.image.load(f"images/menu/buttons/5/{self.codigo_ativo_x+1}.png"), (coo[0]+13, coo[1]+10))
        self.frame_atual += 0.2
        if self.frame_atual > 3:
            self.frame_atual = 0

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
                    efeito = self.manage_buttons(pygame.key.get_pressed(), event)
                    if efeito is not None:
                        return efeito
            self.refresh()

    def create_account(self) -> None:
        name = "".join(self.inputs[0])
        f.criar_pasta(name)

    def validate_user_information(self) -> bool:
        name, password = "".join(self.inputs[0]), "".join(self.inputs[1])
        if name in f.lista_utilizadores():
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
            self.codigo_ativo_x = 1
        elif keys[pygame.K_LEFT]:
            self.codigo_ativo_x = 0
        elif keys[pygame.K_DOWN]:
            self.codigo_ativo_y = 1
        elif keys[pygame.K_UP]:
            self.codigo_ativo_y = 0
        elif keys[pygame.K_KP_ENTER] or keys[pygame.K_RETURN]:
            if self.effects[self.codigo_ativo_x]:
                if self.validate_user_information():
                    self.user.name = "".join(self.inputs[0])
                    self.user.password = "".join(self.inputs[1])
                    self.create_account()
                    self.user.save_info()
                    self.user.turn_active()
                    f.show_succes_message(self.screen, 1)
                    return True
                else:
                    return "new"
            return False
        elif keys[pygame.K_TAB]:
            self.hide = not self.hide
        elif event.key == pygame.K_BACKSPACE:
            self.inputs[self.codigo_ativo_y] = self.inputs[self.codigo_ativo_y][:-1]
        elif len(self.inputs[self.codigo_ativo_y]) <= 25 and self.codigo_ativo_y == 1:
            self.inputs[self.codigo_ativo_y].append(event.unicode)
        elif len(self.inputs[self.codigo_ativo_y]) <= 20 and self.codigo_ativo_y == 0:
            self.inputs[self.codigo_ativo_y].append(event.unicode)

    def refresh(self) -> None:
        self.screen.blit(self.image_nome, (2, 0))
        self.draw_buttons()
        self.screen.blit(pygame.image.load("images/menu/interfaces/navigation/navigation3.png"), (355, 620))
        f.write_name_passw(self.screen, self.inputs[0], self.inputs[1], self.codigo_ativo_y, self.hide)
        pygame.display.update()


class Choose_Account:
    def __init__(self, screen):
        self.screen = screen
        self.image = pygame.image.load("images/menu/interfaces/Main/choose account.png")
        self.efeito = [pygame.image.load(f"images/menu/effects/2/{i+1}.png") for i in range(4)]
        self.button_coordinates = [(322, 120), (322, 175), (322, 230), (322, 285), (322, 340), (322, 395), (322, 450)]
        self.account_name = None
        self.frame_atual = 0
        self.codigo_ativo_x = 1
        self.codigo_ativo_y = 0
        self.buttons = []
        self.previous_button = 0
        self.users = f.lista_utilizadores()
        self.user_names_images = f.get_users_images(0)
        self.user = User()
        self.create_buttons()

    def display_menu(self):
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        background.fill((0, 0, 0))
        clock = pygame.time.Clock()
        keepGoing = True
        while keepGoing:
            clock.tick(30)
            self.frame_atual += 0.25
            if self.frame_atual > 3:
                self.frame_atual = 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    self.create_buttons()
                    efeito = self.manage_buttons(pygame.key.get_pressed())
                    if efeito is not None:
                        return efeito
            self.refresh()

    def manage_buttons(self, keys):
        if keys[pygame.K_RIGHT]:
            self.codigo_ativo_x = 1
        elif keys[pygame.K_LEFT]:
            self.codigo_ativo_x = 0
        elif keys[pygame.K_DOWN]:
            self.codigo_ativo_y += 1
            self.previous_button = self.codigo_ativo_y-1
        elif keys[pygame.K_UP]:
            self.codigo_ativo_y -= 1
            self.previous_button = self.codigo_ativo_y+1
        self.control_previous_button()
        if self.codigo_ativo_y > len(self.users)-1:
            self.codigo_ativo_y = 0
            self.previous_button = len(self.users)-1
        elif self.codigo_ativo_y < 0:
            self.codigo_ativo_y = len(self.users)-1
            self.previous_button = 0
        self.set_active_button()
        if keys[pygame.K_KP_ENTER] or keys[pygame.K_RETURN]:
            if self.codigo_ativo_x:
                self.user.name = self.users[self.codigo_ativo_y]
                self.user.get_info()
                self.user.turn_active()
                return "enter_password"
            else:
                return "main_menu"

    def control_previous_button(self):
        if self.previous_button == self.codigo_ativo_y:
            if self.codigo_ativo_y == 1:
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
        self.user_names_images = f.get_users_images(self.codigo_ativo_y)
        self.buttons[self.previous_button].image = pygame.image.load("images/menu/buttons/6/2.png")
        self.buttons[self.codigo_ativo_y].image = pygame.image.load("images/menu/buttons/6/1.png")


    def refresh(self):
        coordenadas = {0: (325, 520), 1: (558, 520)}
        coo = coordenadas[self.codigo_ativo_x]
        self.screen.blit(self.image, (0, 0))
        self.screen.blit(self.efeito[int(int(self.frame_atual))], (coo[0]-5, coo[1]-20))
        self.screen.blit(pygame.image.load(f"images/menu/buttons/7/{self.codigo_ativo_x+1}.png"), (coo[0]+13, coo[1]))
        [self.buttons[i].draw(self.screen) for i in range(len(self.users))]
        [self.screen.blit(self.user_names_images[i], (self.button_coordinates[i][0]+10, self.button_coordinates[i][1])) for i in range(len(self.users))]
        self.screen.blit(pygame.image.load("images/menu/interfaces/navigation/navigation3.png"), (355, 620))
        pygame.display.update()


class Enter_Password:
    def __init__(self, screen):
        self.screen = screen
        self.image = pygame.image.load("images/menu/interfaces/Main/insert_password.png")
        self.user = None
        self.password_list = []
        self.create_user()
        self.hide = False

    def create_user(self):
        self.user = User()
        self.user.get_active_user()
        self.user.get_info()

    def show_error_message(self) -> None:
        pygame.image.save(self.screen, "images/menu/interfaces/provisory/provisory.png")
        self.screen.blit(pygame.image.load(f"images/menu/messages/error5.png"), (230, 200))
        pygame.display.update()
        f.wait(3)
        self.screen.blit(pygame.image.load("images/menu/interfaces/provisory/provisory.png"), (0, 0))

    def show_succes_message(self) -> None:
        self.screen.blit(pygame.image.load("images/menu/messages/success2.png"), (230, 200))
        f.write_name(self.screen, self.user.name)
        pygame.display.update()
        f.wait(1)

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
                    efeito = self.manage_buttons(pygame.key.get_pressed(), event)
                    if efeito is not None:
                        return efeito
            self.refresh()

    def manage_buttons(self, keys, event):
        if event.key == pygame.K_BACKSPACE:
            self.password_list = self.password_list[:-1]
        elif keys[pygame.K_ESCAPE]:
            return "choose"
        elif keys[pygame.K_TAB]:
            self.hide = not self.hide
        elif keys[pygame.K_KP_ENTER] or keys[pygame.K_RETURN]:
            self.password = "".join(self.password_list)
            if self.verify_password():
                self.show_succes_message()
                return "continue"
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
    def __init__(self, buttons, diretorio, superficie, user=None):
        self.list = buttons
        self.diretorio = diretorio
        self.image_nome = pygame.image.load(diretorio)
        self.efeito1 = [pygame.image.load(f"images/menu/effects/5/{i+1}.png") for i in range(4)]
        self.efeito2 = [pygame.image.load(f"images/menu/effects/4/{i+1}.png") for i in range(4)]
        self.codigo_ativo = 0
        self.screen = superficie
        self.frame_atual = 0
        self.name = "management"
        self.user = user
        self.coord_efeito = (self.list[0].x-12, self.list[0].y-12)

    def draw_buttons(self):
        if self.codigo_ativo < 2:
            self.screen.blit(self.efeito2[int(self.frame_atual)], self.coord_efeito)
        else:
            self.screen.blit(self.efeito1[int(self.frame_atual)], self.coord_efeito)
        for but in self.list:
            but.draw(self.screen)
        self.frame_atual += 0.25
        if self.frame_atual > 3:
            self.frame_atual = 0

    def display_menu(self):
        clock = pygame.time.Clock()
        keepGoing = True
        while keepGoing:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    efeito = self.manage_buttons(pygame.key.get_pressed())
                    if efeito is not None:
                        return efeito
            self.refresh()

    def update_user(self):
        self.user.music_volume = self.list[0].value
        self.user.sound_volume = self.list[1].value
        self.user.save_info()
        self.user.turn_active()

    def manage_buttons(self, keys):
        if keys[pygame.K_UP]:
            self.codigo_ativo -= 1
        elif keys[pygame.K_DOWN]:
            self.codigo_ativo += 1
        elif self.codigo_ativo == 0 or self.codigo_ativo == 1:
            if keys[pygame.K_LEFT]:
                self.list[self.codigo_ativo].change_value(-1)
            elif keys[pygame.K_RIGHT]:
                self.list[self.codigo_ativo].change_value(1)
            self.update_user()
        elif keys[pygame.K_KP_ENTER] or keys[pygame.K_RETURN]:
            return self.list[self.codigo_ativo].efeito
        if self.codigo_ativo > len(self.list)-1:
            self.codigo_ativo = 0
        if self.codigo_ativo < 0:
            self.codigo_ativo = len(self.list)-1
        self.coord_efeito = (self.list[self.codigo_ativo].x-12, self.list[self.codigo_ativo].y-12)

    def refresh(self):
        self.screen.blit(self.image_nome, ((1080-470)//2, 0))
        self.screen.blit(pygame.image.load("images/menu/interfaces/navigation/navigation.png"), (355, 620))
        coo = (20, 490)
        self.screen.blit(pygame.image.load(f"images/menu/interfaces/User/user_info/level{self.user.level}.png"), (0, 0))
        self.screen.blit(pygame.image.load(f"images/menu/interfaces/User/car_window.png"), coo)
        self.screen.blit(pygame.image.load(f"images/menu/interfaces/User/records.png"), (coo[0], coo[1]-210))
        self.screen.blit(pygame.image.load(f"images/menu/interfaces/User/parts.png"), (0, coo[1] - 310))
        self.screen.blit(pygame.image.load(f"images/cars/display/{self.user.level}.png"), (coo[0]+15, coo[1]+53))
        self.user.draw_text(self.screen)
        coordenadas = {0: (680, 90), 1: (680, 90), 2: (698, 192), 3: (685, 178), 4: (685, 178), 5: (685, 178)}
        coo = coordenadas[self.codigo_ativo]
        self.screen.blit(pygame.image.load(f"images/menu/info/info_{self.name}/{self.codigo_ativo+1}.png"), (coo[0], coo[1]))
        self.draw_buttons()
        pygame.display.update()
