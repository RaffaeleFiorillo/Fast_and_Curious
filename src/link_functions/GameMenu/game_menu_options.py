from src.menu_classes import menus as mc, buttons as btn
from src.menu_classes import User
import pygame
from src.auxiliary_modules import audio, files, user_data_management as um, graphics as grp
from src.auxiliary_modules.useful_functions import create_buttons
from src.missions import MissionAI
from src.link_functions.sounds import change_menu_sound, exit_sound


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
    files.write_file_content("parameters/prev_men.txt", "GameMenu")  # make sure any submenu returns to Game Menu after
    return next_link


# A sequence of slides with the game's story images and texts. Leads to the Game Menu or to the next slide of the story
def display_story(screen: pygame.Surface):
    audio.play(change_menu_sound)
    story_slides = mc.MenuImageSequence(screen, "story", 10, "GameMenu", "Story")
    effect = story_slides.display_menu()
    return effect


# Starts and manages the game (for level up). After the game ends, a window with the results is shown and the player
# info is updated.
def mission_level_up(screen: pygame.Surface):
    game_mode = MissionAI(screen)
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
    files.write_file_content("parameters/prev_men.txt", "GameMenu")  # make sure any submenu returns to Game Menu after
    return next_link


# display the Tutorial Menu, leads to all the Tutorials available or to the Game Menu
def tutorials(screen: pygame.Surface):
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
    files.write_file_content("parameters/prev_men.txt", "GameMenu")  # make sure any submenu returns to Game Menu after
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


# activated when a User wants to exit the Game Menu, leads to the Main Menu or Game Menu
def exit_game_menu(screen: pygame.Surface):
    audio.play(exit_sound)
    buttons = [btn.Button(240, 410, f"menu/buttons/3/1.png", False),
               btn.Button(580, 410, f"menu/buttons/3/2.png", True)]
    if not mc.Exit("menu/exit/exit_menu.png", screen, buttons).display_menu():
        um.erase_active_user_data()
        return "MainMenu"
    return "GameMenu"


# activated when a User wants to unlock the ability to go to next level for the current level
def unlock_next_level(screen: pygame.Surface):
    nxt_lvl = mc.UnlockLevel(screen)
    nxt_lvl.display_menu()
    return "GameMenu"


# the interface that is displayed when a User wins level 12 of the game, and goes to level 13
def winner(screen: pygame.Surface):
    w_class = mc.WinnerMenu(screen)
    # f.play(start_sound)
    output = w_class.display_menu()
    if output:
        return "GameMenu"
    return False
