import classes_menu as cm
import funcoes as f
import loops as lp
import link_functions as lf
import classes_entidades as ce
import pygame

pygame.init()

screen = pygame.display.set_mode((1080, 700))
game = lp.Mission_AI(screen)
game.game_loop()




