import pygame
from src.auxiliary_modules.global_variables import space_between_obstacles
from src.auxiliary_modules import graphics as grp
from src.auxiliary_modules import useful_functions as uf


class _Part:
    def __init__(self, x, type_p, y, cardinality):
        self.type_p = type_p
        self.adjust = 15
        self.y_middle = y + self.adjust
        self.y = self.y_middle + cardinality
        self.x = x
        self.value = self.type_p ** 2
        self.image = grp.load_image(f"parts/part{self.type_p}.png")
        self.hit_box = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.length = 32
        self.movement_module = 10
        self.upwards = True

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def mover(self):
        alternation = {True: -1, False: 1}
        advancement_y = alternation[self.upwards]
        self.x -= 10
        self.y += advancement_y
        if self.y_middle + self.movement_module * advancement_y == self.y and self.upwards:
            self.upwards = not self.upwards
        elif self.y_middle + self.movement_module * advancement_y == self.y and not self.upwards:
            self.upwards = not self.upwards


class Parts:
    def __init__(self):
        self.internal_list = []
        self.first_parts = True
        self.choices = [20, 121, 240]
        self.y = uf.choice(self.choices)
        self.dist_between_parts = 5 + 44
        self.min_dist_between_blocs = 100
        self.max_dist_between_blocs = 200
        self.min_parts = 3
        self.max_parts = 7

    def control_last(self):
        return self.internal_list[-1].x <= space_between_obstacles[-2]

    def create_parts(self):
        dist_between_blocs = uf.randint(self.min_dist_between_blocs, self.max_dist_between_blocs)
        type_p = self.calculate_type_part()
        if self.first_parts:
            for i in range(uf.randint(self.min_parts, self.max_parts)):
                self.internal_list.append(
                    _Part(space_between_obstacles[-1] + dist_between_blocs + i * self.dist_between_parts, type_p,
                          self.y, i % 10))
            self.first_parts = False
            return 0
        if self.control_last():
            for i in range(uf.randint(self.min_parts, self.max_parts)):
                self.internal_list.append(
                    _Part(space_between_obstacles[-1] + dist_between_blocs + i * self.dist_between_parts,
                          type_p, self.y, i % 10))
            self.y = uf.choice(self.choices)
            return 0

    @staticmethod
    def calculate_type_part():
        return uf.choice([1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 4, 4, 5])  # random type (some are rarer than others)

    def remove_parts(self, internal_list_obst):
        for part, obst in zip(self.internal_list, internal_list_obst):
            if part.x < -part.length:  # part is outside the screen
                self.internal_list.remove(part)
            # parts are overlapping with obstacle
            """elif obst.x + obst.length > part.x + part.length and obst.x < part.x:
                print(self.y, obst.y, (self.y - 10)//100 == (obst.y-10)//100, sep=" | ")
                if (self.y - 10)//100 == (obst.y-10)//100:
                    self.internal_list.remove(part)"""

    def draw(self, screen):
        for part in self.internal_list:
            part.draw(screen)
            part.mover()
