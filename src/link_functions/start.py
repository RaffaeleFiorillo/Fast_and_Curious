from pygame import Surface
from src.auxiliary_modules import audio
from .sounds import start_sound
from src.menu_classes import menus as mc


# this is the first interface the User sees when he opens the game
def start_page(screen: Surface):
    start = mc.Start(screen)
    audio.play(start_sound)
    output = start.display_menu()
    if output:
        return "MainMenu"
    return False
