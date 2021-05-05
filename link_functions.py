# This module contains all the functions called by the main module.
# Al the functions take the screen where the images are going to be displayed as a parameter
# For each of the functions there is a correspondent class that manages the functionality of the function
# Each function in this module returns values that correspond to the functionality that the game should open next
# A function's comment in this module has a description and the functions it can lead to when it finishes
# This module is divided in categories like: --- CATEGORY NAME --- ; in order to make it more understandable

# -------------------------------------------- IMPORTS -----------------------------------------------------------------
import menu_classes as cm
import game_classes as gc
import functions as f

# -------------------------------------------- SOUNDS ------------------------------------------------------------------
change_menu_sound = f.load_sound("menu/change_menu.WAV")        # sound for when a user enters a new menu
delete_account_sound = f.load_sound("menu/delete_account.WAV")  # sound for deleting account
enter_password_sound = f.load_sound("menu/enter_password.WAV")  # sound for when a password verification is required
exit_sound = f.load_sound("menu/exit.WAV")                      # sound for when the user wants to exit or logout
start_sound = f.load_sound("menu/ignition.WAV")                 # sound for when the game is executed


# ------------------------------------------ GAME START ----------------------------------------------------------------
# this is the first interface the user sees when he opens the game
def start_page(screen):
    start = cm.Start(screen)
    f.play(start_sound)
    output = start.display_menu()
    if output:
        return "main_menu"
    return False


# ------------------------------------------- WINNER MENU --------------------------------------------------------------
def winner(screen):
    w_class = cm.Winner_Menu(screen)
    # f.play(start_sound)
    output = w_class.display_menu()
    if output:
        return "game_menu"
    return False


# ------------------------------------------- MAIN MENU ----------------------------------------------------------------
# display and manage the Main Menu, leads to the Choose User Menu, New Game Menu or Exit Game Menu
def main_menu(screen):
    f.stop_all_sounds()
    f.play(change_menu_sound)
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
    f.play(change_menu_sound)
    m_m = cm.Choose_Account(screen)
    return m_m.display_menu()


# display the Create Account Menu, leads to the Game Menu or to the Main Menu
def create_new_account(screen):
    f.play(change_menu_sound)
    if len(f.list_users()) == 7:
        f.show_error_message(screen, 6)
        return "main_menu"
    ac = cm.Create_Account("images/menu/interfaces/Main/create account.png", screen)
    effect = ac.display_menu()
    if effect == "new":
        return effect
    elif effect:
        return "game_menu"
    return "main_menu"


# activated when a user wants to exit the Game, leads to finish the game's execution or Main Menu
def exit_game(screen):
    f.play(exit_sound)
    if cm.Exit("images/menu/exit/exit_game.png", screen).display_menu():
        f.erase_active_user_data()
        f.terminate_execution()
    return "main_menu"


# -------------------------------------------- GAME MENU ---------------------------------------------------------------
# display and manage the Game Menu, leads to the Manage Menu, Tutorial Menu, display Story, Game AI and Parts
# or Exit Game Menu
def game_menu(screen):
    f.play(change_menu_sound)
    position_x_game = (1080 - 260) // 2
    position_y_game = [y for y in range(107, 600, 80)]
    effects_game = ["story", "m_ai", "m_part", "tutorial", "manage", "exit2"]
    buttons_game = [cm.Button(position_x_game, y, f"images/menu/buttons/2/{position_y_game.index(y) + 1}.png",
                              effects_game[position_y_game.index(y)], position_y_game.index(y)) for y in
                    position_y_game[:len(effects_game)]]
    user = cm.User()
    user.get_active_user()
    user.get_texts()
    g_m = cm.Menu(buttons_game, f"images/menu/interfaces/Main/game menu.png", screen, user)
    next_link = g_m.display_menu()
    if next_link == "m_ai":
        if not int(open(f"saves/{user.name}/next_level.txt").readline()):
            next_link = "nx_l"
    return next_link


# A sequence of slides with the game's story images and texts. Leads to the Game Menu or to the next slide of the story
def display_story(screen):
    f.play(change_menu_sound)
    story_slides = cm.Menu_image_sequence(screen, "story", 10, "game_menu", "Story")
    effect = story_slides.display_menu()
    return effect


# Starts and manages the game (for level up). After the game ends, a window with the results is shown and the player
# info is updated.
def game_ai(screen):
    game = gc.Mission_AI(screen)
    precision, speed, parts_collected, resistance, time, finished = game.game_loop()
    results = cm.Results_AI(screen, precision, speed, parts_collected, resistance, time, finished)
    go_to_next_level, parts = results.display()
    f.save_performance_ai(go_to_next_level, parts, speed)
    if f.get_user_level() == 13 and not f.user_is_a_winner():
        return "winner"
    return "game_menu"


# Starts and manages the game (Parts collection). After the game ends, a window with the results is shown and the player
# info is updated.
def game_parts(screen):
    game = gc.Mission_PARTS(screen)
    precision, speed, parts_collected, time = game.game_loop()
    results = cm.Results_Parts(screen, precision, speed, parts_collected, time)
    parts = results.display()
    f.save_performance_parts(parts, speed, time)
    return "game_menu"


# display the Tutorial Menu, leads to all the tutorials available or to the Game Menu
def tutorial(screen):
    f.play(change_menu_sound)
    position_x_tutorial = (1080 - 260) // 2
    position_y_tutorial = [y for y in range(110, 600, 100)]
    effects_tutorial = ["controls", "save", "enemy", "level_up", "exit3"]
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
    f.play(change_menu_sound)
    position_x = (1080 - 260) // 2
    position_y = [y for y in range(155, 600, 70)]
    effects = ["", "", "add", "change_password", "eliminate_account", "exit3"]
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


def unlock_next_level(screen):
    nxt_lvl = cm.Unlock_Level(screen)
    nxt_lvl.display_menu()
    return "game_menu"


# activated when a user wants to exit the Game Menu, leads to the Main Menu or Game Menu
def exit_game_menu(screen):
    f.play(exit_sound)
    if cm.Exit("images/menu/exit/exit_menu.png", screen).display_menu():
        f.erase_active_user_data()
        return "main_menu"
    return "game_menu"


# ----------------------------------------------- TUTORIAL -------------------------------------------------------------
def tutorial_s(screen):
    f.play(change_menu_sound)
    tut_s_slides = cm.Menu_image_sequence(screen, "tutorial_save", 2, "tutorial", "Save")
    effect = tut_s_slides.display_menu()
    return effect


def tutorial_c(screen):
    f.play(change_menu_sound)
    tut_c_slides = cm.Menu_image_sequence(screen, "tutorial_controls", 5, "tutorial", "Controls")
    effect = tut_c_slides.display_menu()
    return effect


def tutorial_e(screen):
    f.play(change_menu_sound)
    tut_e_slides = cm.Menu_image_sequence(screen, "tutorial_enemies", 2, "tutorial", "Enemies")
    effect = tut_e_slides.display_menu()
    return effect


def tutorial_lu(screen):
    f.play(change_menu_sound)
    tut_lu_slides = cm.Menu_image_sequence(screen, "tutorial_level_up", 3, "tutorial", "Level Up")
    effect = tut_lu_slides.display_menu()
    return effect


# --------------------------------------------- MANAGEMENT -------------------------------------------------------------
# display the Change Password Menu. It leads to the Management Menu (after password verification)
def change_password(screen):
    f.play(change_menu_sound)
    cp = cm.Create_Account("images/menu/interfaces/Main/change password.png", screen, True)
    effect = cp.display_menu()
    if effect == "change_password":
        return effect
    elif effect:
        return "manage"
    return "manage"


# display the Delete Account Menu. It leads to the Main Menu (after password verification) or Management Menu
def delete_account(screen):
    f.play(change_menu_sound)
    if cm.Exit("images/menu/exit/delete_account.png", screen).display_menu():
        file = open("saves/active_user.txt", "r")
        line = file.readline().split(" ")
        verification_password = cm.Enter_Password(screen, True).display_menu()
        file.close()
        if verification_password == "main_menu":
            f.play(delete_account_sound)
            f.delete_user_account(line[0])
        return verification_password
    return "manage"


# display the Add Text Menu. It leads to the Management Menu for both successful and Unsuccessful outcome
def add_text(screen):
    f.play(change_menu_sound)
    at = cm.Add_Text(screen)
    at.display_menu()
    return "manage"


# ----------------------------------------------- GLOBAL ---------------------------------------------------------------
# display the Enter_Password_Menu which is needed whenever a validation needs to be done, where it leads depends on who
# called him. Every time it is said "after password verification" in a commentary, this menu is used
def enter_password(screen):
    e_m = cm.Enter_Password(screen)
    f.play(enter_password_sound)
    return e_m.display_menu()
