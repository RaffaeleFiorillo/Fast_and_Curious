import pygame
from src.auxiliary_modules import hud
from src.auxiliary_modules import graphics as grp


class HUD:
    def __init__(self, screen, mode=False):
        self.screen = screen
        self.speed_meter_image = grp.load_image("HUD/meter/7.png")
        self.precision_meter_image = grp.load_image("HUD/meter/7.png")
        self.background = grp.load_image("HUD/HUD_background.png")
        self.speed = 0
        self.precision = 0
        self.energy = 0
        self.resistance = 0
        self.parts = 0
        self.mode = mode
        if mode:
            self.time = "infinite"
        else:
            self.time = 60
        self.set_up_hud()

    def set_up_hud(self):
        self.screen.blit(self.background, (0, 308))
        pygame.display.update()

    def draw(self, number_parts, time, speed, precision, energy, resistance):
        hud.write_hud_parts_value(self.screen, number_parts)
        hud.write_hud_time_value(self.screen, time)
        hud.display_hud_speed_meter(self.screen, speed)
        hud.display_hud_precision_meter(self.screen, precision)
        hud.display_hud_energy_bar(self.screen, energy)
        hud.display_hud_resistance_bar(self.screen, resistance)
