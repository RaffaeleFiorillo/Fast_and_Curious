from pygame import Surface
from .sounds import enter_password_sound
from src.menu_classes import menus as mc
from src.auxiliary_modules import audio, menu_aux


# display the Enter_Password_Menu which is needed whenever a validation needs to be done, where it leads depends on who
# called him. Every time it is said "after password verification" in a commentary, this menu is used
def enter_password(screen: Surface):
    e_m = mc.EnterPassword(screen)
    audio.play(enter_password_sound)
    effect = e_m.display_menu()
    menu_aux.remove_prov_image()  # remove a background image with compromising info
    return effect
