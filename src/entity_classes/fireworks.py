import pygame
from pygame import Surface
from src.auxiliary_modules import graphics as grp
from src.auxiliary_modules import useful_functions as uf


# simulates a single firework
class Firework:
    def __init__(self, y):
        self.type = uf.choice(["circle", "star"])
        self.x = uf.randint(520, 560)
        self.y = y + uf.randint(0, 50) * uf.choice([-1, 1])
        self.max_height = uf.randint(130, 320)
        self.colors = grp.create_firework_colors(uf.randint(3, 6))
        self.x_speed = uf.randint(0, 8) * uf.choice([-1, 1])
        self.y_speed = -uf.randint(10, 15)
        self.alive = True
        self.time_alive = uf.randint(100, 200)
        self.radius = 10

    def draw_ascending(self, screen: Surface):
        for i in range(uf.randint(7, 10)):
            r_x, r_y = self.x + uf.randint(2, 5) * uf.choice([-1, 1]), self.y + uf.randint(2, 5) * uf.choice([-1, 1])
            pygame.draw.circle(screen, uf.choice(self.colors), (r_x, r_y), 1, 1)
        pygame.draw.circle(screen, uf.choice(self.colors), (self.x, self.y), 3, 1)
        self.x += self.x_speed
        self.y += self.y_speed

    def draw_star(self, screen: Surface, min_sparkle_number: int, max_sparkle_number: int):
        for i in range(uf.randint(min_sparkle_number, max_sparkle_number)):
            calculate_rs = uf.choice([grp.calculate_rs_rhomb, grp.calculate_rs_square])  # randomly chooses shape
            r_x, r_y = calculate_rs(self.x, self.y, self.radius)
            pygame.draw.circle(screen, uf.choice(self.colors), (r_x, r_y), 1, 1)

    def draw_circle(self, screen: Surface, min_sparkle_number: int, max_sparkle_number: int):
        for i in range(uf.randint(min_sparkle_number, max_sparkle_number)):
            r_x, r_y = grp.calculate_rs_circle(self.x, self.y, self.radius)
            pygame.draw.circle(screen, uf.choice(self.colors), (r_x, r_y), 1, 1)

    def draw_explosion(self, screen: Surface):
        min_sparkle_number = (200 - self.time_alive) * 200 // 100 - 30
        max_sparkle_number = (200 - self.time_alive) * 2 + 30
        types_of_firework = {"star": self.draw_star, "circle": self.draw_circle}
        # noinspection PyArgumentList
        types_of_firework[self.type](screen, min_sparkle_number, max_sparkle_number)
        self.time_alive -= 1
        self.radius += self.radius * 0.1
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
