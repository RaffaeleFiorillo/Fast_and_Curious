import pygame
from pygame import Surface
from src.auxiliary_modules import graphics as grp


# The first Interface that shows up when the game is executed. It shows "Fast and Curious"'s logo
class Start:
    def __init__(self, screen: Surface):
        self.screen = screen
        self.image = grp.load_image(f"general/Fast and Curious Logo.png")
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
