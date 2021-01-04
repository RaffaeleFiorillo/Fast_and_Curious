import pygame
import link_functions as lf


# Generic game class that takes some parameters and creates a screen and a dictionary of string keys and
# function values. The keys are a returned value that depends on the link_function in use (see more in the module:
# link_functions). Basically this class just creates the connection between the different menus,scenes and
# functionalities.
class Game:
    link_function_dict: dict

    def __init__(self, screen_width, screen_length, screen_lable, link_functions):
        self.screen = None
        self.link_function_dict = link_functions
        self.previous_link = None
        self.create_screen(screen_width, screen_length, screen_lable)

    def create_screen(self, width, length, lable):
        self.screen = pygame.display.set_mode((length, width))
        pygame.display.set_caption(lable)

    def start(self, link, state=True):
        if state:
            keys_list = list(self.link_function_dict.keys())
            self.previous_link = keys_list[keys_list.index(link)]  # Current link is saved in case the state turns False
            state = self.link_function_dict[link](self.screen)
            if state:
                link = state
                state = True
        else:  # In case the user wants to exit the game by clicking on the red crux the state is set to False
            state = self.link_function_dict["exit1"](self.screen)
            link = self.previous_link
        self.start(link, state)


pygame.init()
# this dictionary has string keys and the corresponding function values.
links = {"enter_password": lf.enter_password,
         "main_menu": lf.main_menu, "game_menu": lf.game_menu, "tutorial": lf.tutorial, "manage": lf.manage_account,
         "new": lf.create_new_account, "choose": lf.choose_user, "exit1": lf.exit_game,
         "story": lf.display_story, "mai": lf.game_ai, "m_part": lf.game_parts, "exit2": lf.exit_game_menu,
         "change_password": lf.change_password, "eliminate_account": lf.delete_account, "exit3": lf.game_menu,
         "level_up": lf.tutorial_lu, "enemy": lf.tutorial_e, "controls": lf.tutorial_c, "save": lf.tutorial_s,
         }
Fast_and_Curious = Game(700, 1080, "Fast and Curious", links)  # create the game
Fast_and_Curious.start("main_menu")  # start the game
