import pygame
import link_functions as lf

pygame.init()

screen = pygame.display.set_mode((1080, 700))
pygame.display.set_caption("Fast and Curious-Beta")

efeitos = {"exit1": lf.exit_game, "main_menu": lf.main_menu, "continue": lf.game_menu, "new": lf.create_new_account,
           "exit2": lf.exit_game_menu, "tutorial": lf.tutorial, "exit3": lf.game_menu, "story": lf.display_story,
           "mai": lf.game_ai, "change_password": lf.change_password, "save": lf.tutorial_s, "level_up": lf.tutorial_lu,
           "enemy": lf.tutorial_e, "controls": lf.tutorial_c, "choose": lf.choose_user, "mpart": lf.game_parts,
           "enter_password": lf.enter_password, "manage": lf.manage_account, "elmnt_account": lf.delete_account
           }

ef = "main_menu"
while True:
    try:
        ef = efeitos[ef](screen)
    except KeyError:
        exit("Game Status: TERMINATED")
