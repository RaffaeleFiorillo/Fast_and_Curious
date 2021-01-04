# This module contains all the functions called by the main module.
# Al the functions take the screen where the images are going to be displayed as a parameter
# For each of the functions there is a correspondent class that manages the functionality of the function
# Each function in this module returns values that correspond to the functionality that the game should open next
# A function's comment in this module has a description and the functions it can lead to when it finishes
# This module is divided in categories like: --- CATEGORY NAME --- ; in order to make it more understandable

import classes_menu as cm
import game_classes as gc
import functions as f


# ------------------------------------------- MAIN MENU ----------------------------------------------------------------
# display and manage the Main Menu, leads to the Choose User Menu, New Game Menu or Exit Game Menu
def main_menu(screen):
    position_x_main = (1080 - 260) // 2
    position_y_main = [y for y in range(150, 600, 150)]
    effects_main = ["choose", "new", "exit1"]
    buttons_main = [cm.Button(position_x_main, y, f"images/menu/buttons/1/{position_y_main.index(y) + 1}.png",
                              effects_main[position_y_main.index(y)], position_y_main.index(y)) for y in
                    position_y_main[:len(effects_main)]]
    m_m = cm.Menu(buttons_main, f"images/menu/interfaces/Main/main menu.png", screen)
    return m_m.display_menu()


# display Choose User Menu, leads to the Game Menu(after password verification), itself or the Main Menu.
def choose_user(screen):
    m_m = cm.Choose_Account(screen)
    return m_m.display_menu()


# display the Create Account Menu, leads to the Game Menu or to the Main Menu
def create_new_account(screen):
    if len(f.list_users()) == 7:
        f.show_error_message(screen, 6)
        return "main_menu"
    ac = cm.Create_Account("images/menu/interfaces/Main/create account.png", screen)
    effect = ac.display_menu()
    if effect == "new":
        return effect
    elif effect:
        return "continue"
    return "main_menu"


# activated when a user wants to exit the Game, leads to finish the game's execution or Main Menu
def exit_game(screen):
    if cm.Exit("images/menu/exit/exit_game.png", screen).display_menu():
        f.erase_active_user_data()
        exit("Exit Game")
    return "main_menu"


# -------------------------------------------- GAME MENU ---------------------------------------------------------------
# display and manage the Game Menu, leads to the Manage Menu, Tutorial Menu, display Story, Game AI and Parts
# or Exit Game Menu
def game_menu(screen):
    position_x_game = (1080 - 260) // 2
    position_y_game = [y for y in range(107, 600, 80)]
    effects_game = ["story", "mai", "m_part", "tutorial", "manage", "exit2"]
    buttons_game = [cm.Button(position_x_game, y, f"images/menu/buttons/2/{position_y_game.index(y) + 1}.png",
                              effects_game[position_y_game.index(y)], position_y_game.index(y)) for y in
                    position_y_game[:len(effects_game)]]
    user = cm.User()
    user.get_active_user()
    user.get_texts()
    g_m = cm.Menu(buttons_game, f"images/menu/interfaces/Main/game menu.png", screen, user)
    # f.erase_active_user_data()
    return g_m.display_menu()


# A sequence of slides with the game's story images and texts. Leads to the Game Menu or to the next slide of the story
def display_story(screen):
    story_slides = cm.Menu_image_sequence(screen, "story", 10, "continue", "Story")
    effect = story_slides.display_menu()
    return effect


# Starts and manages the game (for level up). After the game ends, a window with the results is shown and the player
# info is updated.
def game_ai(screen):
    game = gc.Mission_AI(screen)
    precision, speed, parts_collected, resistance, time = game.game_loop()
    results = cm.Results_AI(screen, precision, speed, parts_collected, resistance, time)
    go_to_next_level, parts = results.display()
    f.save_performance_ai(go_to_next_level, parts, speed)
    return "continue"


# Starts and manages the game (Parts collection). After the game ends, a window with the results is shown and the player
# info is updated.
def game_parts(screen):
    game = gc.Mission_PARTS(screen)
    precision, speed, parts_collected, time = game.game_loop()
    results = cm.Results_Parts(screen, precision, speed, parts_collected, time)
    parts = results.display()
    f.save_performance_parts(parts, speed, time)
    return "continue"


# display the Tutorial Menu, leads to all the tutorials available or to the Game Menu
def tutorial(screen):
    position_x_tutorial = (1080 - 260) // 2
    position_y_tutorial = [y for y in range(110, 600, 100)]
    effects_tutorial = ["commands", "t_save", "enemies", "level_up", "exit3"]
    buttons_tutorial = [
        cm.Button(position_x_tutorial, y, f"images/menu/buttons/4/{position_y_tutorial.index(y) + 1}.png",
                  effects_tutorial[position_y_tutorial.index(y)], position_y_tutorial.index(y)) for y in
        position_y_tutorial[:len(effects_tutorial)]]
    user = cm.User()
    user.get_active_user()
    user.get_texts()
    t = cm.Menu(buttons_tutorial, f"images/menu/interfaces/Main/tutorial.png", screen, user)
    return t.display_menu()


# display the Management Menu. It leads to the Game Menu, Delete Account Menu, Change Password Menu or Add Text Menu
def manage_account(screen):
    position_x = (1080 - 260) // 2
    position_y = [y for y in range(155, 600, 70)]
    effects = ["", "", "add_text", "change_password", "eliminate_account", "exit3"]
    buttons = [cm.Button(position_x, y + 20, f"images/menu/buttons/8/{position_y.index(y) + 1}.png",
                         effects[position_y.index(y)], position_y.index(y))
               for y in position_y[:len(effects)]]
    position_x -= 55
    button1 = cm.Button2(position_x, 130, f"images/menu/buttons/8/{0 + 1}.png",
                         effects[0], 0, 0)
    button2 = cm.Button2(position_x, 230, f"images/menu/buttons/8/{1 + 1}.png",
                         effects[1], 1, 1)
    buttons = [button1, button2] + buttons[2:]
    user = cm.User()
    user.get_active_user()
    user.get_texts()
    m = cm.Management(buttons, f"images/menu/interfaces/Main/management.png", screen, user)
    return m.display_menu()


# activated when a user wants to exit the Game Menu, leads to the Main Menu or Game Menu
def exit_game_menu(screen):
    if cm.Exit("images/menu/exit/exit_menu.png", screen).display_menu():
        f.erase_active_user_data()
        return "main_menu"
    return "continue"


# ----------------------------------------------- TUTORIAL -------------------------------------------------------------
def tutorial_s(screen):
    pass


def tutorial_c(screen):
    pass


def tutorial_e(screen):
    pass


def tutorial_lu(screen):
    pass


# activated when a user wants to exit the Tutorial Menu, leads to the Game Menu or Tutorial Menu
def exit_tutorial(screen):
    if cm.Exit("images/menu/exit/exit_menu.png", screen).display_menu():
        return "continue"
    return "tutorial"


# --------------------------------------------- MANAGEMENT -------------------------------------------------------------
# display the Change Password Menu. It leads to the Management Menu (after password verification)
def change_password(screen):
    if len(f.list_users()) == 7:
        f.show_error_message(screen, 6)
        return "main_menu"
    cp = cm.Create_Account("images/menu/interfaces/Main/change password.png", screen, True)
    effect = cp.display_menu()
    if effect == "change_password":
        return effect
    elif effect:
        return "manage"
    return "manage"


# display the Delete Account Menu. It leads to the Main Menu (after password verification) or Management Menu
def delete_account(screen):
    if cm.Exit("images/menu/exit/delete_account.png", screen).display_menu():
        file = open("saves/active_user.txt", "r")
        line = file.readline().split(" ")
        verification_password = cm.Enter_Password(screen, True).display_menu()
        file.close()
        if verification_password == "main_menu":
            f.delete_user_account(line[0])
        return verification_password
    return "manage"


# ----------------------------------------------- GLOBAL ---------------------------------------------------------------
# display the Enter_Password_Menu which is needed whenever a validation needs to be done, where it leads depends on who
# called him. Every time it is said "after password verification" in a commentary, this menu is used
def enter_password(screen):
    e_m = cm.Enter_Password(screen)
    return e_m.display_menu()
