from src.menu_classes import menus as mc
import pygame
from src.auxiliary_modules import audio
from src.link_functions.sounds import change_menu_sound


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
