import menu_classes as cm
import functions as f
import game_classes as gc
import link_functions as lf
import entity_classes as ce
import os
import pygame

pygame.init()
screen = pygame.display.set_mode((1080, 700))
pygame.display.set_caption("teste")
cla = cm.Add_Text(screen)
cla.display_menu()
