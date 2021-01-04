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
            self.previous_link = keys_list[keys_list.index(link)]
            state = self.link_function_dict[link](self.screen)
            if state:
                link = state
                state = True
        else:
            state = self.link_function_dict["exit1"](self.screen)
            link = self.previous_link
        self.start(link, state)


pygame.init()
# this dictionary has string keys and corresponding function values.
links = {"exit1": lf.exit_game, "main_menu": lf.main_menu, "continue": lf.game_menu,
         "new": lf.create_new_account, "exit2": lf.exit_game_menu, "tutorial": lf.tutorial, "exit3": lf.game_menu,
         "story": lf.display_story, "mai": lf.game_ai, "change_password": lf.change_password, "save": lf.tutorial_s,
         "level_up": lf.tutorial_lu, "enemy": lf.tutorial_e, "controls": lf.tutorial_c, "choose": lf.choose_user,
         "m_part": lf.game_parts, "enter_password": lf.enter_password, "manage": lf.manage_account,
         "eliminate_account": lf.delete_account
         }
Fast_and_Curious = Game(700, 1080, "Fast and Curious", links)  # create the game
Fast_and_Curious.start("main_menu")  # start the game
