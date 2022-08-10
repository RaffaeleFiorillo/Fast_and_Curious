from src.auxiliary_modules import graphics as grp
from src.auxiliary_modules import files
from src.auxiliary_modules import audio
from src.menu_classes import sounds
from .button import Button
from pygame import Surface
import pygame


class Button2(Button):
    def __init__(self, x: int, y: int, directory: str, effect: str, id_c: int):
        super().__init__(x, y, directory, effect)
        self.value = 0
        self.effect = "manage"
        self.id = id_c
        self.value_image = grp.load_image(f"menu/buttons/8/7.png")
        self.get_value()

    def get_value(self):
        values = files.read_file_content("saves/active_user.txt", 1)[0].split(" ")[-2:]
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
            audio.play(sounds.error_sound)
        elif self.value < 0:
            self.value = 0
            audio.play(sounds.error_sound)
        else:
            audio.play(sounds.volume_change_sound, volume=self.value)

    def draw_info(self, screen):
        screen.blit(self.pointer_image, (710, self.y + self.size[1] // 2 - 19))  # draw the head of the arrow (pointer)
        # line from pointer to center line (vertical)
        pygame.draw.line(screen, (0, 255, 255), (755, self.y + self.size[1] // 2 + 3), (755, 343), 5)
        # center line (horizontal)
        pygame.draw.rect(screen, (0, 255, 255), (753, 342, 5, 5))

    def draw(self, screen: Surface):
        screen.blit(self.image, (self.x, self.y))
        [screen.blit(self.value_image, (self.x + 145 + 20 * i, self.y + 15)) for i in range(self.value)]
