import pygame
from .global_variables import SCREEN_LENGTH, SCREEN_WIDTH


SCREEN = pygame.display.set_mode((SCREEN_LENGTH, SCREEN_WIDTH))


# -------------------------------------     GAME CLASS      ------------------------------------------------------------
# Generic game class that takes some parameters and creates a screen and a dictionary of string keys and
# function values. The keys are a returned value that depends on the link_function in use (see more in the module:
# link_functions). Basically this class just creates the connection between the different menus, functionalities, (...).
class Game:
    link_function_dict: dict

    def __init__(self, screen_label, link_functions):
        self.screen = None
        self.link_function_dict = link_functions
        self.previous_link = None
        self.create_screen(screen_label)

    def create_screen(self, label: str) -> None:
        global SCREEN
        pygame.display.set_caption(label)
        self.screen = SCREEN  # module must be initialized or the "convert_alpha" method won't work

    def start(self, link: str, state=True) -> None:
        keys_list = list(self.link_function_dict.keys())
        while True:
            if state:
                self.previous_link = keys_list[keys_list.index(link)]  # saving current link in case the state is False
                state = self.link_function_dict[link](self.screen)
                if state:
                    link = state
                    state = True
            else:  # In case the User wants to exit the game by clicking on the red crux the state is set to False
                state = self.link_function_dict["exit1"](self.screen)
                link = self.previous_link
