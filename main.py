import Auxiliary_Functionalities as Af
import link_functions as lf


# this dictionary has string keys and the corresponding function values.
links = {"enter_password": lf.enter_password, "initial": lf.start_page,
         "main_menu": lf.main_menu, "game_menu": lf.game_menu, "tutorial": lf.tutorial, "manage": lf.manage_account,
         "new": lf.create_new_account, "choose": lf.choose_user, "exit1": lf.exit_game, "nx_l": lf.unlock_next_level,
         "story": lf.display_story, "m_ai": lf.game_ai, "missions": lf.missions, "exit2": lf.exit_game_menu,
         "m_endless": lf.game_parts, "m_aim": lf.game_mouse,
         "change_password": lf.change_password, "eliminate_account": lf.delete_account, "exit3": lf.game_menu,
         "level_up": lf.tutorial_lu, "enemy": lf.tutorial_e, "controls": lf.tutorial_c, "save": lf.tutorial_s,
         "add": lf.add_text, "winner": lf.winner
         }
Fast_and_Curious = Af.Game("Fast and Curious", links)  # create the game
Fast_and_Curious.start("initial")  # start the game
