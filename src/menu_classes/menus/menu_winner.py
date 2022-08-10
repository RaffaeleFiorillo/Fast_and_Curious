import pygame
from pygame import Surface
from src.auxiliary_modules import graphics as grp
from src.entity_classes.fireworks import Fireworks


# Winner_Winner_Chicken_Dinner!!! This Class is used when the User finishes the game (passes at level 13)
class WinnerMenu:
    time = 0
    image = grp.load_image(f"menu/interfaces/Main/winner.png")
    fireworks = Fireworks()

    def __init__(self, screen: Surface):
        self.screen = screen
        text_font = pygame.font.SysFont('Times New Roman', 20)
        text_font.set_bold(True)
        self.directives_image = text_font.render("Press any key to continue", True, (255, 255, 255))
        self.time = 0

    def show_directives(self):
        if int(self.time) % 2 == 0:
            self.screen.blit(self.directives_image, (440, 670))

    def display_menu(self):
        clock = pygame.time.Clock()
        keep_going = True
        while keep_going:
            self.time += clock.tick(30) / 990
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.KEYDOWN:
                    return True
            self.refresh()

    def refresh(self):
        self.screen.blit(self.image, (0, 0))
        self.fireworks.display(self.screen)
        self.show_directives()
        pygame.display.update()
