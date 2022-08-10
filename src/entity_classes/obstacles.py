import pygame
from src.auxiliary_modules import graphics as grp
from src.auxiliary_modules.global_variables import space_between_obstacles
from src.auxiliary_modules import useful_functions as uf


class _Obstacle:
    def __init__(self, location, ultimo_y):
        self.x = location
        self.adjust = -10
        self.y = self.calculate_position_y(ultimo_y)
        self.folder = None
        self.image = None
        self.hit_box = None
        self.rect = None
        self.choose_image()
        self.length = 100

    def choose_image(self):
        self.folder = str(uf.randint(1, 4))
        if self.folder == "4":
            self.image = grp.load_image(f"obstacles/4/{uf.randint(1, 11)}.png")
        else:
            self.image = grp.load_image(f"obstacles/{self.folder}/1.png")
        self.hit_box = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

    def calculate_position_y(self, ultimo_y):
        if ultimo_y == 0:
            return uf.choice([20, 130, 240]) + self.adjust
        possibilities = {20: [130, 240], 130: [20, 240], 240: [130, 20]}
        return uf.choice(possibilities[ultimo_y - self.adjust]) + self.adjust

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def mover(self):
        init_m, nxt = 650, 20
        change = {init_m: f"/obstacles/{self.folder}/2.png",
                  init_m - nxt: f"/obstacles/{self.folder}/3.png",
                  init_m - nxt * 2: f"/obstacles/{self.folder}/4.png",
                  init_m - nxt * 3: f"/obstacles/{self.folder}/5.png",
                  init_m - nxt * 4: f"/obstacles/{self.folder}/6.png",
                  init_m - nxt * 5: f"/obstacles/{self.folder}/7.png"
                  }
        self.x -= 10
        if self.x in change and self.folder != "4":
            self.image = grp.load_image(change[self.x])


class Obstacles:
    def __init__(self):
        self.internal_list = []
        self.max = len(space_between_obstacles)
        self.first_born = True
        self.ultimo_y = 0

    def control_last(self):
        if self.internal_list[-1].x <= space_between_obstacles[-2]:
            return True
        else:
            return False

    def create_obstacles(self):
        if self.first_born:
            for i in range(self.max):
                self.first_born = False
                ob = _Obstacle(space_between_obstacles[i], self.ultimo_y)
                if ob.x >= 700:
                    self.internal_list.append(ob)
        elif self.control_last():
            self.internal_list.append(_Obstacle(space_between_obstacles[-1], self.ultimo_y))
        self.ultimo_y = self.internal_list[-1].y

    def remove_obstacles(self):
        for obst in self.internal_list:
            if obst.x < -obst.length:
                self.internal_list.remove(obst)
        if len(self.internal_list) <= self.max:
            self.create_obstacles()

    def draw(self, screen):
        for obst in self.internal_list:
            obst.draw(screen)
            obst.mover()
