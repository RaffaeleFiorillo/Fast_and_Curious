# This module contains all the functions called by the main module.
# Al the functions take the screen where the images are going to be displayed as a parameter
# For each of the functions there is a correspondent class that manages the functionality of the function
# Each function in this module returns values that correspond to the functionality that the game should open next
# A function's comment in this module has a description and the functions it can lead to when it finishes
# This module is divided in categories like: --- CATEGORY NAME --- ; in order to make it more understandable

# -------------------------------------------- IMPORTS -----------------------------------------------------------------
import menu_classes as cm
import game_classes as gc
import Auxiliary_Functionalities as Af

# -------------------------------------------- SOUNDS ------------------------------------------------------------------
change_menu_sound = Af.load_sound("menu/change_menu.WAV")        # sound for when a user enters a new menu
delete_account_sound = Af.load_sound("menu/delete_account.WAV")  # sound for deleting account
enter_password_sound = Af.load_sound("menu/enter_password.WAV")  # sound for when a password verification is required
exit_sound = Af.load_sound("menu/exit.WAV")                      # sound for when the user wants to exit or logout
start_sound = Af.load_sound("menu/ignition.WAV")                 # sound for when the game is executed


# ------------------------------------------ GAME START ----------------------------------------------------------------
# this is the first interface the user sees when he opens the game
def start_page(screen: Af.Surface):
    start = cm.Start(screen)
    Af.play(start_sound)
    output = start.display_menu()
    if output:
        return "main_menu"
    return False


# ------------------------------------------- WINNER MENU --------------------------------------------------------------
# the interface that is displayed when a user wins level 12 of the game, and goes to level 13
def winner(screen: Af.Surface):
    w_class = cm.Winner_Menu(screen)
    # f.play(start_sound)
    output = w_class.display_menu()
    if output:
        return "game_menu"
    return False


# ------------------------------------------- MAIN MENU ----------------------------------------------------------------
# display and manage the Main Menu, leads to the Choose User Menu, New Game Menu or Exit Game Menu
def main_menu(screen: Af.Surface):
    Af.stop_all_sounds()
    Af.play(change_menu_sound)
    position_x_main = (1080 - 260) // 2
    position_y_main = [y for y in range(150, 600, 150)]
    effects_main = ["choose", "new", "exit1"]
    buttons_main = [cm.Button(position_x_main, y, f"menu/buttons/1/{position_y_main.index(y) + 1}.png",
                              effects_main[position_y_main.index(y)]) for y in
                    position_y_main[:len(effects_main)]]
    m_m = cm.Menu(buttons_main, f"menu/interfaces/Main/main menu.png", screen)
    return m_m.display_menu()


# display Choose User Menu, leads to the Game Menu(after password verification), itself or the Main Menu.
def choose_user(screen: Af.Surface):
    Af.play(change_menu_sound)
    m_m = cm.Choose_Account(screen)
    return m_m.display_menu()


# display the Create Account Menu, leads to the Game Menu or to the Main Menu
def create_new_account(screen: Af.Surface):
    Af.play(change_menu_sound)
    if len(Af.list_users()) == 7:
        Af.show_error_message(screen, 6)
        return "main_menu"
    buttons = [cm.Button(335, 210, "/menu/buttons/5/0.png", None),
               cm.Button(335, 356, "/menu/buttons/5/0.png", None),
               cm.Button(335, 495, "/menu/buttons/5/1.png", False),
               cm.Button(573, 495, "/menu/buttons/5/2.png", True)]
    ac = cm.Create_Modify_Account("menu/interfaces/Main/create account.png", screen, buttons)
    effect = ac.display_menu()
    if effect == "new":
        return effect
    elif effect:
        return "game_menu"
    return "main_menu"


# activated when a user wants to exit the Game, leads to finish the game's execution or Main Menu
def exit_game(screen: Af.Surface):
    Af.play(exit_sound)
    buttons = [cm.Button(240, 410, f"menu/buttons/3/1.png", False),
               cm.Button(580, 410, f"menu/buttons/3/2.png", True)]
    if not cm.Exit("menu/exit/exit_game.png", screen, buttons).display_menu():
        Af.terminate_execution()
    return "main_menu"


# -------------------------------------------- GAME MENU ---------------------------------------------------------------
# display and manage the Game Menu, leads to the Manage Menu, Tutorial Menu, display Story, Game AI and Parts
# or Exit Game Menu
def game_menu(screen: Af.Surface):
    Af.play(change_menu_sound)
    position_x_game = (1080 - 260) // 2
    position_y_game = [y for y in range(107, 600, 80)]
    effects_game = ["story", "m_ai", "m_part", "tutorial", "manage", "exit2"]
    buttons_game = [cm.Button(position_x_game, y, f"menu/buttons/2/{position_y_game.index(y) + 1}.png",
                              effects_game[position_y_game.index(y)]) for y in
                    position_y_game[:len(effects_game)]]
    user = cm.User()
    user.get_active_user()
    user.get_texts()
    g_m = cm.Menu(buttons_game, f"menu/interfaces/Main/game menu.png", screen, user)
    next_link = g_m.display_menu()
    if next_link == "m_ai":
        if not int(open(f"saves/{user.name}/next_level.txt").readline()):
            next_link = "nx_l"
    return next_link


# A sequence of slides with the game's story images and texts. Leads to the Game Menu or to the next slide of the story
def display_story(screen: Af.Surface):
    Af.play(change_menu_sound)
    story_slides = cm.Menu_image_sequence(screen, "story", 10, "game_menu", "Story")
    effect = story_slides.display_menu()
    return effect


# Starts and manages the game (for level up). After the game ends, a window with the results is shown and the player
# info is updated.
def game_ai(screen: Af.Surface):
    game = gc.Mission_AI(screen)
    precision, speed, parts_collected, resistance, time, finished = game.game_loop()
    results = cm.Results_AI(screen, precision, speed, parts_collected, resistance, time, finished)
    go_to_next_level, parts = results.display()
    Af.save_performance_ai(go_to_next_level, parts, speed)
    if Af.get_user_level() == 13 and not Af.user_is_a_winner():
        return "winner"
    return "game_menu"


# Starts and manages the game (Parts collection). After the game ends, a window with the results is shown and the player
# info is updated.
def game_parts(screen: Af.Surface):
    game = gc.Mission_PARTS(screen)
    precision, avg_speed, parts_collected, time, max_speed = game.game_loop()
    results = cm.Results_Parts(screen, precision, avg_speed, max_speed, parts_collected, time)
    parts = results.display()
    Af.save_performance_parts(parts, max_speed, time)
    return "game_menu"


# display the Tutorial Menu, leads to all the tutorials available or to the Game Menu
def tutorial(screen: Af.Surface):
    Af.play(change_menu_sound)
    position_x_tutorial = (1080 - 260) // 2
    position_y_tutorial = [y for y in range(110, 600, 100)]
    effects_tutorial = ["controls", "save", "enemy", "level_up", "exit3"]
    buttons_tutorial = [
        cm.Button(position_x_tutorial, y, f"menu/buttons/4/{position_y_tutorial.index(y) + 1}.png",
                  effects_tutorial[position_y_tutorial.index(y)]) for y in
        position_y_tutorial[:len(effects_tutorial)]]
    user = cm.User()
    user.get_active_user()
    user.get_texts()
    t = cm.Menu(buttons_tutorial, f"menu/interfaces/Main/tutorial.png", screen, user)
    return t.display_menu()


# display the Management Menu. It leads to the Game Menu, Delete Account Menu, Change Password Menu or Add Text Menu
def manage_account(screen: Af.Surface):
    Af.play(change_menu_sound)
    position_x = (1080 - 260) // 2
    position_y = [y for y in range(155, 600, 70)]
    effects = ["", "", "add", "change_password", "eliminate_account", "exit3"]
    buttons = [cm.Button(position_x, y + 20, f"menu/buttons/8/{position_y.index(y) + 1}.png",
                         effects[position_y.index(y)])
               for y in position_y[:len(effects)]]
    position_x -= 55
    button1 = cm.Button2(position_x, 130, f"menu/buttons/8/{0 + 1}.png",
                         effects[0], 0)
    button2 = cm.Button2(position_x, 230, f"menu/buttons/8/{1 + 1}.png",
                         effects[1], 1)
    buttons = [button1, button2] + buttons[2:]
    user = cm.User()
    user.get_active_user()
    user.get_texts()
    m = cm.Management(buttons, f"menu/interfaces/Main/management.png", screen, user)
    return m.display_menu()


# activated when a user wants to unlock the ability to go to next level for the current level
def unlock_next_level(screen: Af.Surface):
    nxt_lvl = cm.Unlock_Level(screen)
    nxt_lvl.display_menu()
    return "game_menu"


# activated when a user wants to exit the Game Menu, leads to the Main Menu or Game Menu
def exit_game_menu(screen: Af.Surface):
    Af.play(exit_sound)
    buttons = [cm.Button(240, 410, f"menu/buttons/3/1.png", False),
               cm.Button(580, 410, f"menu/buttons/3/2.png", True)]
    if not cm.Exit("menu/exit/exit_menu.png", screen, buttons).display_menu():
        Af.erase_active_user_data()
        return "main_menu"
    return "game_menu"


# ----------------------------------------------- TUTORIAL -------------------------------------------------------------
def tutorial_s(screen: Af.Surface):
    Af.play(change_menu_sound)
    tut_s_slides = cm.Menu_image_sequence(screen, "tutorial_save", 2, "tutorial", "Save")
    effect = tut_s_slides.display_menu()
    return effect


def tutorial_c(screen: Af.Surface):
    Af.play(change_menu_sound)
    tut_c_slides = cm.Menu_image_sequence(screen, "tutorial_controls", 5, "tutorial", "Controls")
    effect = tut_c_slides.display_menu()
    return effect


def tutorial_e(screen: Af.Surface):
    Af.play(change_menu_sound)
    tut_e_slides = cm.Menu_image_sequence(screen, "tutorial_enemies", 2, "tutorial", "Enemies")
    effect = tut_e_slides.display_menu()
    return effect


def tutorial_lu(screen: Af.Surface):
    Af.play(change_menu_sound)
    tut_lu_slides = cm.Menu_image_sequence(screen, "tutorial_level_up", 3, "tutorial", "Level Up")
    effect = tut_lu_slides.display_menu()
    return effect


# --------------------------------------------- MANAGEMENT -------------------------------------------------------------
# display the Change Password Menu. It leads to the Management Menu (after password verification)
def change_password(screen: Af.Surface):
    Af.play(change_menu_sound)
    buttons = [cm.Button(335, 210, "/menu/buttons/5/0.png", None),
               cm.Button(335, 356, "/menu/buttons/5/0.png", None),
               cm.Button(335, 495, "/menu/buttons/9/1.png", False),
               cm.Button(573, 495, "/menu/buttons/9/2.png", True)]
    cma = cm.Create_Modify_Account("menu/interfaces/Main/change password.png", screen, buttons, True)
    effect = cma.display_menu()
    if effect == "change_password":
        return effect
    return "manage"


# display the Delete Account Menu. It leads to the Main Menu (after password verification) or Management Menu
def delete_account(screen: Af.Surface):
    Af.play(change_menu_sound)
    buttons = [cm.Button(240, 410, f"menu/buttons/3/1.png", True),
               cm.Button(580, 410, f"menu/buttons/3/2.png", False)]
    if cm.Exit("menu/exit/delete_account.png", screen, buttons).display_menu():
        file = open("saves/active_user.txt", "r")
        line = file.readline().split(" ")
        verification_password = cm.Enter_Password(screen, True).display_menu()
        file.close()
        if verification_password == "main_menu":
            Af.play(delete_account_sound)
            Af.delete_user_account(line[0])
        return verification_password
    return "manage"


# display the Add Text Menu. It leads to the Management Menu for both successful and Unsuccessful outcome
def add_text(screen: Af.Surface):
    Af.play(change_menu_sound)
    buttons = [cm.Button(335, 495, "/menu/buttons/5/1.png", False),
               cm.Button(573, 495, "/menu/buttons/5/2.png", True)]
    at = cm.Add_Text(screen, buttons)
    at.display_menu()
    return "manage"


# ----------------------------------------------- GLOBAL ---------------------------------------------------------------
# display the Enter_Password_Menu which is needed whenever a validation needs to be done, where it leads depends on who
# called him. Every time it is said "after password verification" in a commentary, this menu is used
def enter_password(screen: Af.Surface):
    e_m = cm.Enter_Password(screen)
    Af.play(enter_password_sound)
    return e_m.display_menu()
