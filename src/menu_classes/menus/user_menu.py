from .basic_menu import BasicMenu
from src.menu_classes.buttons import Button
import pygame
from pygame import Surface
from src.auxiliary_modules import graphics as grp
from src.menu_classes.user import User


# provides some changes to the Basic_Menu in order to include a display of User information. Tutorial Menu uses it
class UserMenu(BasicMenu):
    def __init__(self, screen: Surface, direct: str, buttons: [Button], b_coo: {int: (int, int, int)}, eff: [Surface],
                 user: User):
        super().__init__(screen, direct, buttons, b_coo, eff)
        self.user = user
        self.user_related_images = []
        self.user_related_images.append(grp.load_image(f"menu/interfaces/User/user_info/level{self.user.level}.png"))
        self.user_related_images.append(grp.load_image(f"menu/interfaces/User/records.png"))
        self.user_related_images.append(grp.load_image(f"menu/interfaces/User/parts.png"))
        self.user_related_images.append(grp.load_image(f"cars/display/{self.user.level}.png"))

    def draw_user_related_images(self):
        for coo, image in zip([(0, 0), (20, 280), (0, 180), (2, 490)], self.user_related_images):
            self.screen.blit(image, coo)
        self.user.draw_text(self.screen)

    def refresh(self, background: Surface):
        self.screen.blit(background, (0, 0))
        self.screen.blit(self.menu_image, (305, 0))
        self.screen.blit(self.navigation_image, (355, 620))
        self.draw_user_related_images()
        self.screen.blit(self.info_images[self.active_code], (786, 195))
        self.draw_buttons()
        pygame.display.update()
