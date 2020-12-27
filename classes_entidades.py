import pygame
import random
import funcoes as f
# import time

distancia_obstaculos = 290
distancia_parts = 5
espacamento_obst = [o for o in range(300, 1290, distancia_obstaculos)]
# print(espacamento_obst)


class carro:
    def __init__(self):
        self.valores_y = [20, 130, 240]
        self.imagem = pygame.image.load("images/cars/1.png")
        self.speed = 7
        self.x = 400
        self.y = 130
        self.hitbox = pygame.mask.from_surface(self.imagem.convert_alpha())
        self.keepmoving = False
        self.destino = 1
        self.direction = None
        self.rect = (self.x, self.y, self.imagem.get_size()[0], self.imagem.get_size()[1])
        self.vision_coo = [[self.x+150, self.y-90], [self.x+150, self.y+27], [self.x+150, self.y+130],
                           [self.x+70, self.y - 90], [self.x+70, self.y+130]]
        self.valores_vistos = []
        self.po = 0

    def colisao_obstaculo(self, l_obstaculos):
        for obst in l_obstaculos:
            if self.hitbox.overlap(obst.hitbox, (self.x-obst.x+obst.ajuste, self.y-obst.y+obst.ajuste)):
                return False
        return True

    def visao(self, screen):
        self.valores_vistos = []
        for i in self.vision_coo:
            self.valores_vistos.append(f.ver(screen, i))
        # time.sleep(0.5)

    def colisao_parts(self, l_parts):
        value = 0
        new_parts = []
        for part in l_parts:
            if part.x+44 >= self.rect[0] and part.x <= self.rect[0]+self.rect[2]:
                if part.y + 24 >= self.rect[1] and part.y <= self.rect[1] + self.rect[3]:
                    value += part.value
                    continue
                else:
                    new_parts.append(part)
            else:
                new_parts.append(part)
        return new_parts, value

    def draw(self, screen):
        screen.blit(self.imagem, (self.x, self.y))
        # pygame.draw.rect(screen, (255, 255, 0), self.rect, 5)
        """for i in self.vision_coo:
            pygame.draw.circle(screen, (255, 242, 0), i, 2, 1)"""

    def movimento(self, evento):
        movimentos = {"UP": -self.speed, "DWN": self.speed}
        self.y += movimentos[evento]
        if self.destino == 1:
            if self.direction == "UP":
                self.destino = 2
            elif self.direction == "DWN":
                self.destino = 0
        elif self.destino == 2:
            if self.direction == "UP":
                self.destino = 2
            elif self.direction == "DWN":
                self.destino = 1
        elif self.destino == 0:
            if self.direction == "UP":
                self.destino = 1
            elif self.direction == "DWN":
                self.destino = 0
        self.keepmoving = True
        if self.y > self.valores_y[2]:
            self.y = self.valores_y[2]
        elif self.valores_y[0] > self.y:
            self.y = self.valores_y[0]
        self.vision_coo = [[self.x + 150, self.y - 90], [self.x + 150, self.y + 27], [self.x + 150, self.y + 130], [self.x+70, self.y - 90], [self.x+70, self.y+130]]
        self.rect = (self.x, self.y, self.imagem.get_size()[0], self.imagem.get_size()[1])

    def contin_mov(self):
        if self.keepmoving:
            self.movimento(self.direction)
        if self.y in self.valores_y:
            self.keepmoving = False


class estrada:
    def __init__(self):
        self.frame_atual = 0
        self.images_estrada = [pygame.image.load("images/estrada/frame"+str(num+1)+".png") for num in range(19)]
        self.frames = len(self.images_estrada)

    def draw(self, screen):
        screen.blit(self.images_estrada[self.frame_atual], self.images_estrada[self.frame_atual].get_rect())
        self.frame_atual += 1
        if self.frame_atual == self.frames:
            self.frame_atual = 0


class _obstaculo:
    def __init__(self, onde, ultimo_y):
        self.x = onde
        self.ajuste = -23
        self.y = self.calcular_posicao_y(ultimo_y)
        self.pasta = None
        self.imagem = None
        self.escolher_imagem()
        self.hitbox = pygame.mask.from_surface(self.imagem.convert_alpha())
        self.rect = self.imagem.get_rect()
        self.comprimento = 100

    def escolher_imagem(self):
        self.pasta = str(random.randint(1, 4))
        if self.pasta == "4":
            self.imagem = pygame.image.load(f"images/obstacles/4/{random.randint(1,12)}.png")
        else:
            self.imagem = pygame.image.load("images/obstacles/" + self.pasta + "/1.png")

    def calcular_posicao_y(self, ultimo_y):
        if ultimo_y == 0:
            return random.choice([20, 130, 240])+self.ajuste
        possibilidades = {20: [130, 240], 130: [20, 240], 240: [130, 20]}
        return random.choice(possibilidades[ultimo_y-self.ajuste])+self.ajuste

    def draw(self, screen):
        screen.blit(self.imagem, (self.x, self.y))

    def mover(self):
        init_m, nxt = 650, 30
        mudanca = {init_m: f"images/obstacles/{self.pasta}/2.png", init_m-nxt: f"images/obstacles/{self.pasta}/3.png",
                   init_m-nxt*2: f"images/obstacles/{self.pasta}/4.png", init_m-nxt*3: f"images/obstacles/{self.pasta}/5.png",
                   init_m - nxt * 4: f"images/obstacles/{self.pasta}/6.png",  init_m-nxt*5: f"images/obstacles/{self.pasta}/7.png"
                   }
        self.x -= 10
        if self.x in mudanca and self.pasta != "4":
            self.imagem = pygame.image.load(mudanca[self.x])


class obstaculos:
    def __init__(self):
        self.lista = []
        self.max = len(espacamento_obst)
        self.first_borns = True
        self.ultimo_y = 0

    def controlar_o_ultimo(self):
        if self.lista[-1].x <= espacamento_obst[-2]:
            return True
        else:
            return False

    def criar_obstaculos(self):
        if self.first_borns:
            for i in range(self.max):
                self.first_borns = False
                ob = _obstaculo(espacamento_obst[i], self.ultimo_y)
                if ob.x >= 700:
                    self.lista.append(ob)
        elif self.controlar_o_ultimo():
            self.lista.append(_obstaculo(espacamento_obst[-1], self.ultimo_y))
        self.ultimo_y = self.lista[-1].y

    def remover_obstaculos(self):
        for obst in self.lista:
            if obst.x < -obst.comprimento:
                self.lista.remove(obst)
        if len(self.lista) <= self.max:
            self.criar_obstaculos()

    def draw(self, screen):
        for obst in self.lista:
            obst.draw(screen)
            obst.mover()


class _part:
    def __init__(self, x, type_p, y, numero):
        self.type_p = type_p
        self.ajuste = 15
        self.y_medio = y + self.ajuste
        self.y = self.y_medio+numero
        self.x = x
        self.value = self.type_p**2
        self.imagem = pygame.image.load("images/parts/part"+str(self.type_p)+".png")
        self.hitbox = pygame.mask.from_surface(self.imagem.convert_alpha())
        self.rect = self.imagem.get_rect()
        self.comprimento = 32
        self.modulo_movimento = 10
        self.subir = True

    def draw(self, screen):
        screen.blit(self.imagem, (self.x, self.y))

    def mover(self):
        altern = {True: -1, False: 1}
        avanco_y = altern[self.subir]
        self.x -= 10
        self.y += avanco_y
        if self.y_medio + self.modulo_movimento*avanco_y == self.y and self.subir:
            self.subir = not self.subir
        elif self.y_medio + self.modulo_movimento*avanco_y == self.y and not self.subir:
            self.subir = not self.subir


class parts:
    def __init__(self):
        self.lista = []
        self.first_parts = True
        self.choices = [20, 130, 240]
        self.y = random.choice(self.choices)
        self.dist_entre_parts = 5 + 44
        self.dist_min_entre_blocos = 100
        self.dist_max_entre_blocos = 200
        self.min_parts = 3
        self.max_parts = 7

    def controlar_o_ultimo(self):
        if self.lista[-1].x <= espacamento_obst[-2]:
            return True
        else:
            return False

    def criar_parts(self):
        dist_entre_blocos = random.randint(self.dist_min_entre_blocos, self.dist_max_entre_blocos)
        type_p = self.calcular_type_part()
        if self.first_parts:
            for i in range(random.randint(self.min_parts, self.max_parts)):
                self.lista.append(_part(espacamento_obst[-1] + dist_entre_blocos + i * self.dist_entre_parts, type_p, self.y, i % 10))
            self.first_parts = False
            return 0
        if self.controlar_o_ultimo():
            for i in range(random.randint(self.min_parts, self.max_parts)):
                self.lista.append(_part(espacamento_obst[-1]+dist_entre_blocos+i*self.dist_entre_parts, type_p, self.y, i % 10))
            self.y = random.choice(self.choices)
            return 0

    @staticmethod
    def calcular_type_part():
        probabilidade = random.random()
        if probabilidade <= 0.3:
            return 1
        elif 0.3 < probabilidade <= 0.55:
            return 2
        elif 0.55 < probabilidade <= 0.75:
            return 3
        elif 0.75 < probabilidade <= 0.9:
            return 4
        else:
            return 5

    def remover_parts(self, lista_obst):
        for part, obst in zip(self.lista, lista_obst):
            if part.x < -part.comprimento:  # or (obst.x >= part.x and obst.x <= part.x+44 and obst.y <= part.y and obst.y+obst.comprimento>= part.y):
                self.lista.remove(part)

    def draw(self, screen):
        for part in self.lista:
            part.draw(screen)
            part.mover()


class HUD:
    def __init__(self, screen, mode=False):
        self.screen = screen
        self.speed_meter_image = pygame.image.load("images/HUD/meter/7.png")
        self.precision_meter_image = pygame.image.load("images/HUD/meter/7.png")
        self.speed = 0
        self.precision = 0
        self.energy = 0
        self.resistence = 0
        self.parts = 0
        self.modo = mode
        if mode:
            self.time = "infinit"
        else:
            self.time = 60
        self.written_text = []
        self.texts = []
        self.line = 0
        self.text_to_write = []
        self.get_text()
        self.set_up_HUD()

    def set_up_HUD(self):
        self.screen.blit(pygame.image.load("images/HUD/HUD_background.png"), (0, 308))
        pygame.display.update()

    def get_text(self):
        self.texts = f.get_text_names()
        self.text_to_write = random.choice(self.texts)

    def manage_buttons(self, keys, event):
        if keys[pygame.K_KP_ENTER] or keys[pygame.K_RETURN]:
            self.line += 1
            self.written_text.append([])
        elif event.key == pygame.K_BACKSPACE:
            if len(self.written_text[self.line]) == 0:
                self.written_text = self.written_text[:-1]
            else:
                self.written_text[self.line] = self.written_text[self.line][:-1]
        elif len(self.written_text[self.line]) >= 25:
            self.line += 1
            self.written_text.append([])
        self.written_text[self.line].append(event.unicode)

    def draw(self, number_parts, time, speed, precision):
        f.write_HUD_parts_value(self.screen, number_parts)
        f.write_HUD_time_value(self.screen, time)
        f.display_HUD_speed_meter(self.screen, speed)
        f.display_HUD_precision_meter(self.screen, precision)
