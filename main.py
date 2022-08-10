import src.auxiliary_modules as am
import src.link_functions as lf
import pygame

pygame.init()


# this dictionary has string keys and the corresponding function values.
links = {"enter_password": lf.enter_password, "initial": lf.start_page,
         "MainMenu": lf.main_menu, "GameMenu": lf.game_menu, "tutorial": lf.tutorials, "manage": lf.management,
         "new": lf.create_new_account, "choose": lf.choose_user, "exit1": lf.exit_game, "nx_l": lf.unl_nxt_l,
         "manage_gp": lf.management_gameplay, "manage_ch": lf.management_cheats, "manage_us": lf.management_user,
         "story": lf.display_story, "m_ai": lf.mission_lu, "Missions": lf.missions, "exit2": lf.exit_game_menu,
         "m_endless": lf.mission_parts, "m_aim": lf.mission_mouse,
         "change_password": lf.change_password, "delete_account": lf.delete_account,
         "level_up": lf.tutorial_lu, "enemy": lf.tutorial_e, "controls": lf.tutorial_c, "save": lf.tutorial_s,
         "add": lf.add_text, "winner": lf.winner
         }
Fast_and_Curious = am.game.Game("Fast and Curious", links)  # create the game
Fast_and_Curious.start("initial")  # start the game
