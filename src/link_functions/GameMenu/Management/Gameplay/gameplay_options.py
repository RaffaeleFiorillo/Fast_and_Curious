from src.menu_classes import menus as mc, buttons as btn
import pygame
from src.auxiliary_modules import audio
from src.link_functions.sounds import change_menu_sound


# display the Add Text Menu. It leads to the Gameplay Management Menu for both successful and Unsuccessful outcome
def add_text(screen: pygame.Surface):
    audio.play(change_menu_sound)
    buttons = [btn.Button(335, 495, "/menu/buttons/5/1.png", False),
               btn.Button(573, 495, "/menu/buttons/5/2.png", True)]
    at = mc.AddText(screen, buttons)
    at.display_menu()
    return "manage_gp"
