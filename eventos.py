import classes_menu as cm
import funcoes as f
import game_classes as gc
import link_functions as lf
import classes_entidades as ce
import pygame

pygame.init()

screen = pygame.display.set_mode((1080, 700))
game = gc.Mission_AI(screen)
game.game_loop()



