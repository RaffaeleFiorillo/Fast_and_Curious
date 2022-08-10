from src.menu_classes import menus as mc, buttons as btn
from src.menu_classes import User
import pygame
from src.auxiliary_modules import audio, files
from src.auxiliary_modules import graphics as grp
from src.link_functions.sounds import change_menu_sound
from src.auxiliary_modules.useful_functions import create_buttons


# Display Account Management Menu. It leads to its sub-menus (listed in this section) or to the Management Menu
def management_user(screen: pygame.Surface):
    files.write_file_content("parameters/prev_men.txt", "manage")  # make sure any submenu returns to Management after
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


# Display Gameplay Management Menu. It leads to its sub-menus (listed in this section) or to the Management Menu
def management_gameplay(screen: pygame.Surface):
    files.write_file_content("parameters/prev_men.txt", "manage")  # make sure any submenu returns to Management after
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


# Display Cheats Management Menu. It leads to its sub-menus (listed in this section) or to the Management Menu
def management_cheats(screen: pygame.Surface):
    # effects = ["", "", "", "manage"]
    return "manage"
