from pygame import Surface
from src.auxiliary_modules import graphics as grp
import pygame


class Button:
    pointer_image = grp.load_image("menu/info/pointer.png")

    def __init__(self, x: int, y: int, directory: str, effect):
        self.x = x
        self.y = y
        if directory != "":
            self.image = grp.load_image(directory)
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
        screen.blit(self.pointer_image, (685, self.y + self.size[1] // 2 - 19))  # draw the head of the arrow (pointer)
        # line from pointer to center line (vertical)
        pygame.draw.line(screen, (0, 255, 255), (730, self.y + self.size[1] // 2 + 3), (730, 343), 5)
        # center line (horizontal)
        pygame.draw.rect(screen, (0, 255, 255), (728, 342, 30, 5))

    def change_image(self, directory: str):
        self.image = grp.load_image(directory)