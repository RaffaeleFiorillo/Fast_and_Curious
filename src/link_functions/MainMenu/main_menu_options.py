from src.menu_classes import buttons as btn
import pygame
from src.auxiliary_modules import display, menu_aux
from src.auxiliary_modules import graphics as grp, user_data_management as um
from src.auxiliary_modules.useful_functions import create_buttons
from src.auxiliary_modules import audio
from src.menu_classes import menus as mc
from src.link_functions.sounds import change_menu_sound, exit_sound


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
