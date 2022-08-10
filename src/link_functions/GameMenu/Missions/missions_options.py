from src.menu_classes import menus as mc
from src.deprecated import game_classes as gc
import pygame
from src.auxiliary_modules import user_data_management as um


# Starts and manages the game (Parts collection). After the game ends, a window with the results is shown and the player
# info is updated.
def mission_parts(screen: pygame.Surface):
    game_mode = gc.MissionPARTS(screen)
    precision, avg_speed, parts_collected, time, max_speed = game_mode.game_loop()
    results = mc.ReportMissionParts(screen, precision, avg_speed, max_speed, parts_collected, time)
    parts = results.display()
    um.save_performance_parts(parts, max_speed, time)
    return "Missions"


# Starts and manages the game: Mouse improvement. After the game ends, a window with the results is shown and the player
# info is updated. NOT IMPLEMENTED YET!!!
def mission_mouse(screen: pygame.Surface):
    """game = gc.Mission_PARTS(screen)
    precision, avg_speed, parts_collected, time, max_speed = game.game_loop()
    results = mc.Report_Mission_Parts(screen, precision, avg_speed, max_speed, parts_collected, time)
    parts = results.display()
    Af.save_performance_parts(parts, max_speed, time)"""
    return "Missions"