# This module contains all the functions called by the main module.
# Al the functions take the screen where the images are going to be displayed as a parameter
# For each of the functions there is a correspondent class that manages the functionality of the function
# Each function in this module returns values that correspond to the functionality that the game should open next
# A function's comment in this module has a description and the functions it can lead to when it finishes
# This module is divided in categories like: --- CATEGORY NAME --- ; in order to make it more understandable

# -------------------------------------------- IMPORTS -----------------------------------------------------------------
import menu_classes as mc
import game_classes as gc
import Auxiliary_Functionalities as Af

# -------------------------------------------- SOUNDS ------------------------------------------------------------------
change_menu_sound = Af.load_sound("menu/change_menu.WAV")  # sound for when a user enters a new menu
delete_account_sound = Af.load_sound("menu/delete_account.WAV")  # sound for deleting account
enter_password_sound = Af.load_sound("menu/enter_password.WAV")  # sound for when a password verification is required
exit_sound = Af.load_sound("menu/exit.WAV")  # sound for when the user wants to exit or logout
start_sound = Af.load_sound("menu/ignition.WAV")  # sound for when the game is executed


# ------------------------------------------ GAME START ----------------------------------------------------------------
# this is the first interface the user sees when he opens the game
def start_page(screen: Af.Surface):
    start = mc.Start(screen)
    Af.play(start_sound)
    output = start.display_menu()
    if output:
        return "main_menu"
    return False


# ------------------------------------------- WINNER MENU --------------------------------------------------------------
# the interface that is displayed when a user wins level 12 of the game, and goes to level 13
def winner(screen: Af.Surface):
    w_class = mc.Winner_Menu(screen)
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
    buttons = Af.create_buttons(mc.Button, "menu/buttons/1", ["choose", "new", "exit1"])
    button_coo = {0: (680, 90), 1: (698, 192), 2: (685, 178)}
    effects = [Af.load_image(f"menu/effects/1/{i + 1}.png") for i in range(4)]
    m_m = mc.Basic_Menu(screen, f"menu/interfaces/Main/main menu.png", buttons, button_coo, effects)
    return m_m.display_menu()


# display Choose User Menu, leads to the Game Menu(after password verification), itself or the Main Menu.
def choose_user(screen: Af.Surface):
    Af.play(change_menu_sound)
    m_m = mc.Choose_Account(screen)
    return m_m.display_menu()


# display the Create Account Menu, leads to the Game Menu or to the Main Menu
def create_new_account(screen: Af.Surface):
    Af.play(change_menu_sound)
    if len(Af.list_users()) == 7:
        Af.show_error_message(screen, 6)
        return "main_menu"
    buttons = [mc.Button(335, 210, "/menu/buttons/5/0.png", None),
               mc.Button(335, 356, "/menu/buttons/5/0.png", None),
               mc.Button(335, 495, "/menu/buttons/5/1.png", False),
               mc.Button(573, 495, "/menu/buttons/5/2.png", True)]
    ac = mc.Create_Modify_Account("menu/interfaces/Main/create account.png", screen, buttons)
    effect = ac.display_menu()
    if effect == "new":
        return effect
    elif effect:
        return "game_menu"
    return "main_menu"


# activated when a user wants to exit the Game, leads to finish the game's execution or Main Menu
def exit_game(screen: Af.Surface):
    Af.play(exit_sound)
    buttons = [mc.Button(240, 410, f"menu/buttons/3/1.png", False),
               mc.Button(580, 410, f"menu/buttons/3/2.png", True)]
    if not mc.Exit("menu/exit/exit_game.png", screen, buttons).display_menu():
        Af.terminate_execution()
    return "main_menu"


# -------------------------------------------- GAME MENU ---------------------------------------------------------------
# display and manage the Game Menu, leads to the Manage Menu, Tutorial Menu, display Story, Game AI and Parts
# or Exit Game Menu
def game_menu(screen: Af.Surface):
    Af.play(change_menu_sound)
    y_coo = [y for y in range(107, 600, 80)]
    b_effects = ["story", "m_ai", "missions", "tutorial", "manage", "exit2"]
    buttons = Af.create_buttons(mc.Button, "menu/buttons/2", b_effects, y_coo)
    effects_coo = {0: (687, 90), 1: (687, 90), 2: (687, 192), 3: (687, 178), 4: (687, 178), 5: (687, 178)}
    effects = [Af.load_image(f"menu/effects/3/{i + 1}.png") for i in range(4)]
    user = mc.User()
    user.get_active_user()
    user.get_texts()
    g_menu = mc.Game_Menu(screen, f"menu/interfaces/Main/game menu.png", buttons, effects_coo, effects, user)
    next_link = g_menu.display_menu()
    if next_link == "m_ai":
        mission_is_unlocked = int(Af.read_file_content(f"saves/{user.name}/next_level.txt", 1)[0])
        if not mission_is_unlocked:
            next_link = "nx_l"
    return next_link


# A sequence of slides with the game's story images and texts. Leads to the Game Menu or to the next slide of the story
def display_story(screen: Af.Surface):
    Af.play(change_menu_sound)
    story_slides = mc.Menu_image_sequence(screen, "story", 10, "game_menu", "Story")
    effect = story_slides.display_menu()
    return effect


# Starts and manages the game (for level up). After the game ends, a window with the results is shown and the player
# info is updated.
def game_ai(screen: Af.Surface):
    game = gc.Mission_AI(screen)
    precision, speed, parts_collected, resistance, time, finished = game.game_loop()
    results = mc.Report_Mission_AI(screen, precision, speed, parts_collected, resistance, time, finished)
    go_to_next_level, parts = results.display()
    Af.save_performance_ai(go_to_next_level, parts, speed)
    if Af.get_user_level() == 13 and not Af.user_is_a_winner():
        return "winner"
    return "game_menu"


# display the Missions Menu. Leads to all the available side missions (the ones for practice instead of level up)
def missions(screen: Af.Surface):
    Af.play(change_menu_sound)
    y_coo = [y for y in range(107, 600, 80)]
    effects_game = ["m_endless", "m_aim", "missions", "missions", "missions", "exit3"]
    buttons = Af.create_buttons(mc.Button, "menu/buttons/11", effects_game, y_coo)
    effects_coo = {0: (687, 90), 1: (687, 90), 2: (687, 192), 3: (687, 178), 4: (687, 178), 5: (687, 178)}
    effects = [Af.load_image(f"menu/effects/3/{i + 1}.png") for i in range(4)]
    user = mc.User()
    user.get_active_user()
    user.get_texts()
    missions_menu = mc.User_Menu(screen, f"menu/interfaces/Main/missions menu.png", buttons, effects_coo, effects, user)
    next_link = missions_menu.display_menu()
    return next_link


# display the Tutorial Menu, leads to all the tutorials available or to the Game Menu
def tutorial(screen: Af.Surface):
    Af.play(change_menu_sound)
    position_x_tutorial = (1080 - 260) // 2
    position_y_tutorial = [y for y in range(110, 600, 100)]
    effects_tutorial = ["controls", "save", "enemy", "level_up", "exit3"]
    buttons = [
        mc.Button(position_x_tutorial, y, f"menu/buttons/4/{position_y_tutorial.index(y) + 1}.png",
                  effects_tutorial[position_y_tutorial.index(y)]) for y in
        position_y_tutorial[:len(effects_tutorial)]]
    button_coo = {0: (680, 90), 1: (680, 90), 2: (698, 192), 3: (685, 178), 4: (685, 178)}
    effects = [Af.load_image(f"menu/effects/1/{i + 1}.png") for i in range(4)]
    user = mc.User()
    user.get_active_user()
    user.get_texts()
    tutorial_menu = mc.User_Menu(screen, f"menu/interfaces/Main/tutorial.png", buttons, button_coo, effects, user)
    return tutorial_menu.display_menu()


# display the Management Menu. It leads to the Game Menu, Delete Account Menu, Change Password Menu or Add Text Menu
def manage_account(screen: Af.Surface):
    Af.play(change_menu_sound)
    position_x = (1080 - 260) // 2
    position_y = [y for y in range(155, 600, 70)]
    effects = ["", "", "manage_gp", "manage_ch", "manage_us", "exit3"]
    buttons = [mc.Button(position_x, y + 20, f"menu/buttons/8/{position_y.index(y) + 1}.png",
                         effects[position_y.index(y)])
               for y in position_y[:len(effects)]]
    position_x -= 55
    button1 = mc.Button2(position_x, 130, f"menu/buttons/8/{0 + 1}.png",
                         effects[0], 0)
    button2 = mc.Button2(position_x, 230, f"menu/buttons/8/{1 + 1}.png",
                         effects[1], 1)
    buttons = [button1, button2] + buttons[2:]
    user = mc.User()
    user.get_active_user()
    user.get_texts()
    m = mc.Management(buttons, f"menu/interfaces/Main/management.png", screen, user)
    return m.display_menu()


# activated when a user wants to unlock the ability to go to next level for the current level
def unlock_next_level(screen: Af.Surface):
    nxt_lvl = mc.Unlock_Level(screen)
    nxt_lvl.display_menu()
    return "game_menu"


# activated when a user wants to exit the Game Menu, leads to the Main Menu or Game Menu
def exit_game_menu(screen: Af.Surface):
    Af.play(exit_sound)
    buttons = [mc.Button(240, 410, f"menu/buttons/3/1.png", False),
               mc.Button(580, 410, f"menu/buttons/3/2.png", True)]
    if not mc.Exit("menu/exit/exit_menu.png", screen, buttons).display_menu():
        Af.erase_active_user_data()
        return "main_menu"
    return "game_menu"


# ----------------------------------------------- MISSIONS -------------------------------------------------------------
# Starts and manages the game (Parts collection). After the game ends, a window with the results is shown and the player
# info is updated.
def game_parts(screen: Af.Surface):
    game = gc.Mission_PARTS(screen)
    precision, avg_speed, parts_collected, time, max_speed = game.game_loop()
    results = mc.Report_Mission_Parts(screen, precision, avg_speed, max_speed, parts_collected, time)
    parts = results.display()
    Af.save_performance_parts(parts, max_speed, time)
    return "missions"


# Starts and manages the game: Mouse improvement. After the game ends, a window with the results is shown and the player
# info is updated. NOT IMPLEMENTED YET!!!
def game_mouse(screen: Af.Surface):
    """game = gc.Mission_PARTS(screen)
    precision, avg_speed, parts_collected, time, max_speed = game.game_loop()
    results = mc.Report_Mission_Parts(screen, precision, avg_speed, max_speed, parts_collected, time)
    parts = results.display()
    Af.save_performance_parts(parts, max_speed, time)"""
    return "missions_menu"


# ----------------------------------------------- TUTORIAL -------------------------------------------------------------
def tutorial_s(screen: Af.Surface):
    Af.play(change_menu_sound)
    tut_s_slides = mc.Menu_image_sequence(screen, "tutorial_save", 2, "tutorial", "Save")
    effect = tut_s_slides.display_menu()
    return effect


def tutorial_c(screen: Af.Surface):
    Af.play(change_menu_sound)
    tut_c_slides = mc.Menu_image_sequence(screen, "tutorial_controls", 5, "tutorial", "Controls")
    effect = tut_c_slides.display_menu()
    return effect


def tutorial_e(screen: Af.Surface):
    Af.play(change_menu_sound)
    tut_e_slides = mc.Menu_image_sequence(screen, "tutorial_enemies", 2, "tutorial", "Enemies")
    effect = tut_e_slides.display_menu()
    return effect


def tutorial_lu(screen: Af.Surface):
    Af.play(change_menu_sound)
    tut_lu_slides = mc.Menu_image_sequence(screen, "tutorial_level_up", 3, "tutorial", "Level Up")
    effect = tut_lu_slides.display_menu()
    return effect


# ----------------------------------------- MANAGEMENT USER ------------------------------------------------------------
# display the Change Password Menu. It leads to the Management Menu (after password verification)
def change_password(screen: Af.Surface):
    Af.play(change_menu_sound)
    buttons = [mc.Button(335, 210, "/menu/buttons/5/0.png", None),
               mc.Button(335, 356, "/menu/buttons/5/0.png", None),
               mc.Button(335, 495, "/menu/buttons/9/1.png", False),
               mc.Button(573, 495, "/menu/buttons/9/2.png", True)]
    cma = mc.Create_Modify_Account("menu/interfaces/Main/change password.png", screen, buttons, True)
    effect = cma.display_menu()
    if effect == "change_password":
        return effect
    return "manage"


# display the Delete Account Menu. It leads to the Main Menu (after password verification) or Management User Menu
def delete_account(screen: Af.Surface):
    Af.play(change_menu_sound)
    buttons = [mc.Button(240, 410, f"menu/buttons/3/1.png", True),
               mc.Button(580, 410, f"menu/buttons/3/2.png", False)]
    if mc.Exit("menu/exit/delete_account.png", screen, buttons).display_menu():
        user_name = Af.read_file_content("saves/active_user.txt", 1)[0].split(" ")[0]
        verification_password = mc.Enter_Password(screen, True).display_menu()
        if verification_password == "main_menu":
            Af.play(delete_account_sound)
            Af.delete_user_account(user_name)
        return verification_password
    return "manage"


# display the Delete Statistics Menu. It leads to the Management User Menu
def delete_statistics(screen: Af.Surface):
    Af.play(change_menu_sound)
    buttons = [mc.Button(240, 410, f"menu/buttons/3/1.png", True),
               mc.Button(580, 410, f"menu/buttons/3/2.png", False)]
    if mc.Exit("menu/exit/delete_account.png", screen, buttons).display_menu():
        user_name = Af.read_file_content("saves/active_user.txt", 1)[0].split(" ")[0]
        verification_password = mc.Enter_Password(screen, True).display_menu()
        if verification_password == "main_menu":
            Af.play(delete_account_sound)
            Af.delete_user_account(user_name)
        return verification_password
    return "manage"


# ---------------------------------------- MANAGEMENT GAMEPLAY ---------------------------------------------------------
# display the Add Text Menu. It leads to the Management Gameplay Menu for both successful and Unsuccessful outcome
def add_text(screen: Af.Surface):
    Af.play(change_menu_sound)
    buttons = [mc.Button(335, 495, "/menu/buttons/5/1.png", False),
               mc.Button(573, 495, "/menu/buttons/5/2.png", True)]
    at = mc.Add_Text(screen, buttons)
    at.display_menu()
    return "manage"


# ----------------------------------------- MANAGEMENT CHEATS ----------------------------------------------------------


# ----------------------------------------------- GLOBAL ---------------------------------------------------------------
# display the Enter_Password_Menu which is needed whenever a validation needs to be done, where it leads depends on who
# called him. Every time it is said "after password verification" in a commentary, this menu is used
def enter_password(screen: Af.Surface):
    e_m = mc.Enter_Password(screen)
    Af.play(enter_password_sound)
    effect = e_m.display_menu()
    Af.remove_prov_image()  # remove a background image with compromising info
    return effect
