# This module contains all the functions called by the main module.
# All the functions take the screen where the images are going to be displayed as a parameter
# For each of the functions there is a correspondent class that manages the functionality of the function
# Each function in this module returns values that correspond to the functionality that the game should open next
# A function's comment in this module has a description and the functions it can lead to when it finishes
# This module is divided in categories like: --- CATEGORY NAME --- ; in order to make it more understandable

# -------------------------------------------- IMPORTS -----------------------------------------------------------------
from src.menu_classes import menus as mc, buttons as btn
from src.menu_classes import User
import game_classes as gc
import pygame
from src.auxiliary_modules import audio, display, menu_aux, files
from src.auxiliary_modules import graphics as grp, user_data_management as um

# -------------------------------------------- SOUNDS ------------------------------------------------------------------
change_menu_sound = audio.load_sound("menu/change_menu.WAV")  # sound for when a User enters a new menu
delete_account_sound = audio.load_sound("menu/delete_account.WAV")  # sound for deleting account
enter_password_sound = audio.load_sound("menu/enter_password.WAV")  # sound for when a password verification is required
exit_sound = audio.load_sound("menu/exit.WAV")  # sound for when the User wants to exit or logout
start_sound = audio.load_sound("menu/ignition.WAV")  # sound for when the game is executed


def create_buttons(button, button_dir: str, effects: [str], y_coo=None):
    position_x = (1080 - 260) // 2
    position_y = y_coo if y_coo is not None else [y for y in range(150, 600, 150)]
    buttons = []
    for i, y in enumerate(position_y[:len(effects)]):
        directory = f"{button_dir}/{i + 1}.png"
        buttons.append(button(position_x, y, directory, effects[i]))
    return buttons


# ------------------------------------------ GAME START ----------------------------------------------------------------
# this is the first interface the User sees when he opens the game
def start_page(screen: pygame.Surface):
    start = mc.Start(screen)
    audio.play(start_sound)
    output = start.display_menu()
    if output:
        return "MainMenu"
    return False


# ------------------------------------------- WINNER MENU --------------------------------------------------------------
# the interface that is displayed when a User wins level 12 of the game, and goes to level 13
def winner(screen: pygame.Surface):
    w_class = mc.WinnerMenu(screen)
    # f.play(start_sound)
    output = w_class.display_menu()
    if output:
        return "GameMenu"
    return False


# ------------------------------------------- MAIN MENU ----------------------------------------------------------------
# display and manage the Main Menu, leads to the Choose User Menu, New Game Menu or Exit Game Menu
def main_menu(screen: pygame.Surface):
    audio.stop_all_sounds()
    audio.play(change_menu_sound)
    buttons = create_buttons(btn.Button, "menu/buttons/1", ["choose", "new", "exit1"])
    button_coo = {0: (680, 90), 1: (698, 192), 2: (685, 178)}
    effects = [grp.load_image(f"menu/effects/1/{i + 1}.png") for i in range(4)]
    m_m = mc.BasicMenu(screen, f"menu/interfaces/Main/main menu.png", buttons, button_coo, effects)
    return m_m.display_menu()


# display Choose User Menu, leads to the Game Menu(after password verification), itself or the Main Menu.
def choose_user(screen: pygame.Surface):
    audio.play(change_menu_sound)
    m_m = mc.ChooseAccount(screen)
    return m_m.display_menu()


# display the Create Account Menu, leads to the Game Menu or to the Main Menu
def create_new_account(screen: pygame.Surface):
    audio.play(change_menu_sound)
    if len(um.list_users()) == 7:
        display.show_error_message(screen, 6)
        return "MainMenu"
    buttons = [btn.Button(335, 210, "/menu/buttons/5/0.png", None),
               btn.Button(335, 356, "/menu/buttons/5/0.png", None),
               btn.Button(335, 495, "/menu/buttons/5/1.png", False),
               btn.Button(573, 495, "/menu/buttons/5/2.png", True)]
    ac = mc.CreateModifyAccount("menu/interfaces/Main/create account.png", screen, buttons)
    effect = ac.display_menu()
    if effect == "new":
        return effect
    elif effect:
        return "GameMenu"
    return "MainMenu"


# activated when a User wants to exit the Game, leads to finish the game's execution or Main Menu
def exit_game(screen: pygame.Surface):
    audio.play(exit_sound)
    buttons = [btn.Button(240, 410, f"menu/buttons/3/1.png", False),
               btn.Button(580, 410, f"menu/buttons/3/2.png", True)]
    if not mc.Exit("menu/exit/exit_game.png", screen, buttons).display_menu():
        menu_aux.terminate_execution()
    return "MainMenu"


# -------------------------------------------- GAME MENU ---------------------------------------------------------------
# display and manage the Game Menu, leads to the Manage Menu, Tutorial Menu, display Story, Game AI and Parts
# or Exit Game Menu
def game_menu(screen: pygame.Surface):
    audio.play(change_menu_sound)
    y_coo = [y for y in range(107, 600, 80)]
    b_effects = ["story", "m_ai", "Missions", "tutorial", "manage", "exit2"]
    buttons = create_buttons(btn.Button, "menu/buttons/2", b_effects, y_coo)
    effects_coo = {0: (687, 90), 1: (687, 90), 2: (687, 192), 3: (687, 178), 4: (687, 178), 5: (687, 178)}
    effects = [grp.load_image(f"menu/effects/3/{i + 1}.png") for i in range(4)]
    user = User()
    user.get_active_user()
    user.get_texts()
    g_menu = mc.GameMenu(screen, f"menu/interfaces/Main/game menu.png", buttons, effects_coo, effects, user)
    next_link = g_menu.display_menu()
    if next_link == "m_ai":
        mission_is_unlocked = int(files.read_file_content(f"saves/{user.name}/next_level.txt", 1)[0])
        if not mission_is_unlocked:
            next_link = "nx_l"
    files.write_file_content("../../parameters/prev_men.txt", "GameMenu")  # make sure any submenu returns to Game Menu after
    return next_link


# A sequence of slides with the game's story images and texts. Leads to the Game Menu or to the next slide of the story
def display_story(screen: pygame.Surface):
    audio.play(change_menu_sound)
    story_slides = mc.MenuImageSequence(screen, "story", 10, "GameMenu", "Story")
    effect = story_slides.display_menu()
    return effect


# Starts and manages the game (for level up). After the game ends, a window with the results is shown and the player
# info is updated.
def mission_ai(screen: pygame.Surface):
    game_mode = gc.MissionAI(screen)
    precision, speed, parts_collected, resistance, time, finished = game_mode.game_loop()
    results = mc.ReportMissionAI(screen, precision, speed, parts_collected, resistance, time, finished)
    go_to_next_level, parts = results.display()
    um.save_performance_ai(go_to_next_level, parts, speed)
    if um.get_user_level() == 13 and not um.user_is_a_winner():
        return "winner"
    return "GameMenu"


# display the Missions Menu. Leads to all the available side Missions (the ones for practice instead of level up)
def missions(screen: pygame.Surface):
    audio.play(change_menu_sound)
    y_coo = [y for y in range(107, 600, 80)]
    effects_game = ["m_endless", "m_aim", "Missions", "Missions", "Missions", "GameMenu"]
    buttons = create_buttons(btn.Button, "menu/buttons/11", effects_game, y_coo)
    effects_coo = {0: (687, 90), 1: (687, 90), 2: (687, 192), 3: (687, 178), 4: (687, 178), 5: (687, 178)}
    effects = [grp.load_image(f"menu/effects/3/{i + 1}.png") for i in range(4)]
    user = User()
    user.get_active_user()
    user.get_texts()
    missions_menu = mc.UserMenu(screen, f"menu/interfaces/Main/Missions menu.png", buttons, effects_coo, effects, user)
    next_link = missions_menu.display_menu()
    files.write_file_content("../../parameters/prev_men.txt", "GameMenu")  # make sure any submenu returns to Game Menu after
    return next_link


# display the Tutorial Menu, leads to all the Tutorials available or to the Game Menu
def tutorial(screen: pygame.Surface):
    audio.play(change_menu_sound)
    position_x_tutorial = (1080 - 260) // 2
    position_y_tutorial = [y for y in range(110, 600, 100)]
    effects_tutorial = ["controls", "save", "enemy", "level_up", "GameMenu"]
    buttons = [
        btn.Button(position_x_tutorial, y, f"menu/buttons/4/{position_y_tutorial.index(y) + 1}.png",
                   effects_tutorial[position_y_tutorial.index(y)])
        for y in position_y_tutorial[:len(effects_tutorial)]]
    button_coo = {0: (680, 90), 1: (680, 90), 2: (698, 192), 3: (685, 178), 4: (685, 178)}
    effects = [grp.load_image(f"menu/effects/1/{i + 1}.png") for i in range(4)]
    user = User()
    user.get_active_user()
    user.get_texts()
    tutorial_menu = mc.UserMenu(screen, f"menu/interfaces/Main/tutorial.png", buttons, button_coo, effects, user)
    files.write_file_content("../../parameters/prev_men.txt", "GameMenu")  # make sure any submenu returns to Game Menu after
    return tutorial_menu.display_menu()


# display the Management Menu. It leads to the Game Menu, Delete Account Menu, Change Password Menu or Add Text Menu
def management(screen: pygame.Surface):
    audio.play(change_menu_sound)
    position_x = (1080 - 260) // 2
    position_y = [y for y in range(155, 600, 70)]
    effects = ["", "", "manage_gp", "manage_ch", "manage_us", "GameMenu"]
    buttons = [btn.Button(position_x, y + 20, f"menu/buttons/8/{position_y.index(y) + 1}.png",
                          effects[position_y.index(y)])
               for y in position_y[:len(effects)]]
    position_x -= 55
    button1 = btn.Button2(position_x, 130, f"menu/buttons/8/{0 + 1}.png", effects[0], 0)
    button2 = btn.Button2(position_x, 230, f"menu/buttons/8/{1 + 1}.png", effects[1], 1)
    buttons = [button1, button2] + buttons[2:]
    user = User()
    user.get_active_user()
    user.get_texts()
    m = mc.Management(buttons, f"menu/interfaces/Main/management.png", screen, user)
    return m.display_menu()


# activated when a User wants to unlock the ability to go to next level for the current level
def unlock_next_level(screen: pygame.Surface):
    nxt_lvl = mc.UnlockLevel(screen)
    nxt_lvl.display_menu()
    return "GameMenu"


# activated when a User wants to exit the Game Menu, leads to the Main Menu or Game Menu
def exit_game_menu(screen: pygame.Surface):
    audio.play(exit_sound)
    buttons = [btn.Button(240, 410, f"menu/buttons/3/1.png", False),
               btn.Button(580, 410, f"menu/buttons/3/2.png", True)]
    if not mc.Exit("menu/exit/exit_menu.png", screen, buttons).display_menu():
        um.erase_active_user_data()
        return "MainMenu"
    return "GameMenu"


# ----------------------------------------------- MISSIONS -------------------------------------------------------------
# Starts and manages the game (Parts collection). After the game ends, a window with the results is shown and the player
# info is updated.
def game_parts(screen: pygame.Surface):
    game_mode = gc.MissionPARTS(screen)
    precision, avg_speed, parts_collected, time, max_speed = game_mode.game_loop()
    results = mc.ReportMissionParts(screen, precision, avg_speed, max_speed, parts_collected, time)
    parts = results.display()
    um.save_performance_parts(parts, max_speed, time)
    return "Missions"


# Starts and manages the game: Mouse improvement. After the game ends, a window with the results is shown and the player
# info is updated. NOT IMPLEMENTED YET!!!
def game_mouse(screen: pygame.Surface):
    """game = gc.Mission_PARTS(screen)
    precision, avg_speed, parts_collected, time, max_speed = game.game_loop()
    results = mc.Report_Mission_Parts(screen, precision, avg_speed, max_speed, parts_collected, time)
    parts = results.display()
    Af.save_performance_parts(parts, max_speed, time)"""
    return "Missions"


# ----------------------------------------------- TUTORIAL -------------------------------------------------------------
def tutorial_s(screen: pygame.Surface):
    audio.play(change_menu_sound)
    tut_s_slides = mc.MenuImageSequence(screen, "tutorial_save", 2, "tutorial", "Save")
    effect = tut_s_slides.display_menu()
    return effect


def tutorial_c(screen: pygame.Surface):
    audio.play(change_menu_sound)
    tut_c_slides = mc.MenuImageSequence(screen, "tutorial_controls", 5, "tutorial", "Controls")
    effect = tut_c_slides.display_menu()
    return effect


def tutorial_e(screen: pygame.Surface):
    audio.play(change_menu_sound)
    tut_e_slides = mc.MenuImageSequence(screen, "tutorial_enemies", 2, "tutorial", "Enemies")
    effect = tut_e_slides.display_menu()
    return effect


def tutorial_lu(screen: pygame.Surface):
    audio.play(change_menu_sound)
    tut_lu_slides = mc.MenuImageSequence(screen, "tutorial_level_up", 3, "tutorial", "Level Up")
    effect = tut_lu_slides.display_menu()
    return effect


# ----------------------------------------- MANAGEMENT USER ------------------------------------------------------------
# Display Account Management Menu. It leads to its sub-menus (listed in this section) or to the Management Menu
def management_user(screen: pygame.Surface):
    files.write_file_content("../../parameters/prev_men.txt", "manage")  # make sure any submenu returns to Management after
    audio.play(change_menu_sound)
    y_coo = [110, 190, 270, 510]
    effects = ["change_password", "delete_account", "manage_us", "manage"]
    buttons = create_buttons(btn.Button, "menu/buttons/12", effects, y_coo)
    effects_coo = {0: (687, 90), 1: (687, 90), 2: (687, 192), 3: (687, 178), 4: (687, 178)}
    effects = [grp.load_image(f"menu/effects/3/{i + 1}.png") for i in range(4)]
    user = User()
    user.get_active_user()
    user.get_texts()
    directory = "menu/interfaces/Main/management_account.png"  # directory for the background image of the menu
    m_user_menu = mc.UserMenu(screen, directory, buttons, effects_coo, effects, user)
    next_link = m_user_menu.display_menu()
    return next_link


# display the Change Password Menu. It leads to the Account Management Menu (after password verification)
def change_password(screen: pygame.Surface):
    audio.play(change_menu_sound)
    buttons = [btn.Button(335, 210, "/menu/buttons/5/0.png", None),
               btn.Button(335, 356, "/menu/buttons/5/0.png", None),
               btn.Button(335, 495, "/menu/buttons/9/1.png", False),
               btn.Button(573, 495, "/menu/buttons/9/2.png", True)]
    cma = mc.CreateModifyAccount("menu/interfaces/Main/change password.png", screen, buttons, True)
    effect = cma.display_menu()
    if effect == "change_password":
        return effect
    return "manage_us"


# display Delete Account Menu. It leads to the Main Menu (after password verification) or Management User Menu
def delete_account(screen: pygame.Surface):
    audio.play(change_menu_sound)
    buttons = [btn.Button(240, 410, f"menu/buttons/3/1.png", True),
               btn.Button(580, 410, f"menu/buttons/3/2.png", False)]
    if mc.Exit("menu/exit/delete_account.png", screen, buttons).display_menu():
        user_name = files.read_file_content("../../saves/active_user.txt", 1)[0].split(" ")[0]
        verification_password = mc.EnterPassword(screen, True).display_menu()
        if verification_password == "MainMenu":
            audio.play(delete_account_sound)
            um.delete_user_account(user_name)
        return verification_password
    return "manage_us"


# display Delete Statistics Menu. It leads to the Account Management User Menu
def delete_statistics(screen: pygame.Surface):
    audio.play(change_menu_sound)
    buttons = [btn.Button(240, 410, f"menu/buttons/3/1.png", True),
               btn.Button(580, 410, f"menu/buttons/3/2.png", False)]
    if mc.Exit("menu/exit/delete_account.png", screen, buttons).display_menu():
        user_name = files.read_file_content("../../saves/active_user.txt", 1)[0].split(" ")[0]
        verification_password = mc.EnterPassword(screen, True).display_menu()
        if verification_password == "MainMenu":
            audio.play(delete_account_sound)
            um.delete_user_account(user_name)
        return verification_password
    return "manage_us"


# ---------------------------------------- MANAGEMENT GAMEPLAY ---------------------------------------------------------
# Display Gameplay Management Menu. It leads to its sub-menus (listed in this section) or to the Management Menu
def management_gameplay(screen: pygame.Surface):
    files.write_file_content("../../parameters/prev_men.txt", "manage")  # make sure any submenu returns to Management after
    audio.play(change_menu_sound)
    y_coo = [110, 190, 270, 510]
    effects = ["add", "txt_display", "", "manage"]
    buttons = create_buttons(btn.Button, "menu/buttons/13", effects, y_coo)
    effects_coo = {0: (687, 90), 1: (687, 90), 2: (687, 192), 3: (687, 178), 4: (687, 178)}
    effects = [grp.load_image(f"menu/effects/3/{i + 1}.png") for i in range(4)]
    user = User()
    user.get_active_user()
    user.get_texts()
    directory = "menu/interfaces/Main/management_gameplay.png"  # directory for the background image of the menu
    m_user_menu = mc.UserMenu(screen, directory, buttons, effects_coo, effects, user)
    next_link = m_user_menu.display_menu()
    return next_link


# display the Add Text Menu. It leads to the Gameplay Management Menu for both successful and Unsuccessful outcome
def add_text(screen: pygame.Surface):
    audio.play(change_menu_sound)
    buttons = [btn.Button(335, 495, "/menu/buttons/5/1.png", False),
               btn.Button(573, 495, "/menu/buttons/5/2.png", True)]
    at = mc.AddText(screen, buttons)
    at.display_menu()
    return "manage_gp"


# ----------------------------------------- MANAGEMENT CHEATS ----------------------------------------------------------
# Display Cheats Management Menu. It leads to its sub-menus (listed in this section) or to the Management Menu
def management_cheats(screen: pygame.Surface):
    # effects = ["", "", "", "manage"]
    return "manage"


# ----------------------------------------------- GLOBAL ---------------------------------------------------------------
# display the Enter_Password_Menu which is needed whenever a validation needs to be done, where it leads depends on who
# called him. Every time it is said "after password verification" in a commentary, this menu is used
def enter_password(screen: pygame.Surface):
    e_m = mc.EnterPassword(screen)
    audio.play(enter_password_sound)
    effect = e_m.display_menu()
    menu_aux.remove_prov_image()  # remove a background image with compromising info
    return effect
