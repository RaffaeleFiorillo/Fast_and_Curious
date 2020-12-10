import pygame
import funcoes as f


class Button:
    def __init__(self, x, y, diretorio, efeito, codigo):
        self.x = x
        self.y = y
        self.imagem = pygame.image.load(diretorio)
        self.efeito = efeito
        self.codigo = codigo

    def draw(self, screen):
        screen.blit(self.imagem, (self.x, self.y))


class Menu:
    def __init__(self, buttons, diretorio, superficie, user=None):
        self.lista = buttons
        self.diretorio = diretorio
        self.name = self.diretorio.split("/")[-1][:-4]
        self.imagem_nome = pygame.image.load(diretorio)
        self.efeito = [pygame.image.load(f"imagens/menu/efeitos/1/{i+1}.png") for i in range(4)]
        self.codigo_ativo = 0
        self.screen = superficie
        self.frame_atual = 0
        self.user = user
        self.coord_efeito = (self.lista[0].x-12, self.lista[0].y-12)

    def draw_buttons(self):
        coordenadas = {0: (680, 90), 1: (698, 192), 2: (685, 178)}
        coordenadas2 = {0: (680, 90), 1: (680, 90), 2: (698, 192), 3: (685, 178), 4: (685, 178)}
        ch = {"main menu": coordenadas, "game menu": coordenadas2, "tutorial": coordenadas2}
        co_cho = ch[self.name]
        coo = co_cho[self.codigo_ativo]
        self.screen.blit(self.efeito[int(self.frame_atual)], self.coord_efeito)
        self.screen.blit(pygame.image.load(f"imagens/menu/interfaces/info_{self.name}/{self.codigo_ativo+1}.png"), (coo[0], coo[1]))
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
        elif keys[pygame.K_KP_ENTER] or keys.index(1) == 40:
            return self.lista[self.codigo_ativo].efeito
        self.codigo_ativo += valor
        if self.codigo_ativo > len(self.lista)-1:
            self.codigo_ativo = 0
        if self.codigo_ativo < 0:
            self.codigo_ativo = len(self.lista)-1
        self.coord_efeito = (self.lista[self.codigo_ativo].x-12, self.lista[self.codigo_ativo].y-12)

    def refresh(self, background):
        self.screen.blit(background, (0, 0))
        self.screen.blit(self.imagem_nome, ((1080-470)//2, 0))
        self.screen.blit(pygame.image.load("imagens/menu/interfaces/navigation/navigation.png"), (355, 620))
        if self.user is not None:
            coo = (20, 490)
            self.screen.blit(pygame.image.load(f"imagens/menu/interfaces/User/user_info/level{self.user.level}.png"), (0, 0))
            self.screen.blit(pygame.image.load(f"imagens/menu/interfaces/User/car_window.png"), coo)
            self.screen.blit(pygame.image.load(f"imagens/menu/interfaces/User/records.png"), (coo[0], coo[1]-210))
            self.screen.blit(pygame.image.load(f"imagens/menu/interfaces/User/parts.png"), (0, coo[1] - 310))
            self.screen.blit(pygame.image.load(f"imagens/carros/display/{self.user.level}.png"), (coo[0]+15, coo[1]+53))
            f.write_best_time(self.screen, self.user.best_time)
            f.write_best_speed(self.screen, self.user.best_speed)
            f.write_parts_number(self.screen, self.user.parts)
            f.write_user_name(self.screen, self.user.name)
        self.draw_buttons()
        pygame.display.update()


class Exit:
    def __init__(self, diretorio, superficie):
        self.imagem_nome = pygame.image.load(diretorio)
        self.efeitos = (True, False)
        self.efeito = [pygame.image.load(f"imagens/menu/efeitos/1/{i+1}.png") for i in range(4)]
        self.codigo_ativo = 0
        self.screen = superficie
        self.frame_atual = 0

    def draw_buttons(self):
        coordenadas = {0: (240, 410), 1: (570, 410)}
        coo = coordenadas[self.codigo_ativo]
        self.screen.blit(self.efeito[int(self.frame_atual)], coo)
        self.screen.blit(pygame.image.load(f"imagens/menu/buttons/3/{self.codigo_ativo+1}.png"), (coo[0]+13, coo[1]+10))
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
        if keys[pygame.K_RIGHT]:
            valor = 1
        elif keys[pygame.K_LEFT]:
            valor = -1
        elif keys[pygame.K_KP_ENTER] or keys.index(1) == 40:
            return self.efeitos[self.codigo_ativo]
        self.codigo_ativo += valor
        if self.codigo_ativo > len(self.efeitos)-1:
            self.codigo_ativo = 0
        if self.codigo_ativo < 0:
            self.codigo_ativo = 1

    def refresh(self, background):
        self.screen.blit(self.imagem_nome, (0, 0))
        self.draw_buttons()
        self.screen.blit(pygame.image.load("imagens/menu/interfaces/navigation/navigation2.png"), (350, 600))
        pygame.display.update()


class Create_Account:
    def __init__(self, diretorio, superficie):
        self.imagem_nome = pygame.image.load(diretorio)
        self.efeitos = (True, False)
        self.efeito = [pygame.image.load(f"imagens/menu/efeitos/2/{i+1}.png") for i in range(4)]
        self.codigo_ativo_x = 0
        self.codigo_ativo_y = 0
        self.screen = superficie
        self.inputs = [[], []]
        self.frame_atual = 0
        self.user = None

    def draw_buttons(self):
        coordenadas = {0: (325, 485), 1: (558, 485)}
        coo = coordenadas[self.codigo_ativo_x]
        self.screen.blit(self.efeito[int(self.frame_atual)], (coo[0]-5, coo[1]-10))
        self.screen.blit(pygame.image.load(f"imagens/menu/buttons/5/{self.codigo_ativo_x+1}.png"), (coo[0]+13, coo[1]+10))
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
                        if not efeito:
                            self.create_account()
                        return efeito
            self.refresh(background)

    def create_account(self):
        f.criar_pasta(self.name)

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
            return self.efeitos[self.codigo_ativo_x]
        elif event.key == pygame.K_BACKSPACE:
            self.inputs[self.codigo_ativo_y] = self.inputs[self.codigo_ativo_y][:-1]
        elif len(self.inputs[self.codigo_ativo_y]) <= 25:
            self.inputs[self.codigo_ativo_y].append(event.unicode)

    def refresh(self, background):
        self.screen.blit(self.imagem_nome, (2, 0))
        self.draw_buttons()
        self.screen.blit(pygame.image.load("imagens/menu/interfaces/navigation/navigation3.png"), (355, 620))
        f.write_name_passw(self.screen, self.inputs[0], self.inputs[1], self.codigo_ativo_y)
        pygame.display.update()


class Choose_Account:
    def __init__(self, screen):
        self.screen = screen
        self.button_coordinates = [(20,20)]
        self.account_name = None
        self.buttons = []
        self.users = f.lista_utilizadores()

    def create_buttons(self):
        pass

class User:
    def __init__(self, name):
        self.name = name
        self.password = None
        self.best_speed = None
        self.best_time = None
        self.level = None
        self.parts = None
        self.imagem = None
        self.get_info()

    def draw(self, screen):
        screen.blit(self.imagem, (0, 0))

    def get_info(self):
        file = open(f"saves/{self.name}/data.txt", "r")
        data = file.readline().split(" ")
        self.best_speed, self.best_time, self.level, self.parts, self.password = int(data[0]), int(data[1]), int(data[2]), int(data[3]), data[4]
        self.imagem = pygame.image.load(f"imagens/menu/interfaces/user_info/level{self.level}.png")
        file.close()

    def save_info(self):
        file = open(f"saves/{self.name}/data.txt", "w")
        data = f"{self.best_speed} {self.best_time} {self.level} {self.parts} {self.password}"
        file.write(data)
        file.close()

