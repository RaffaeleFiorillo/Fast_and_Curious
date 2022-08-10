import pygame
from src.auxiliary_modules import global_variables


class Road:
    def __init__(self):
        self.rect = (0, 0, global_variables.SCREEN_LENGTH, 308)  # characteristics of the road (how it will be drawn)
        self.color = (108, 108, 108)  # color of the road's background
        self.current_frame = 0  # number that varies between 0 and 19 describing the current state of the road
        self.frame_number = 19  # number of frames required for the road cycle to start over

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)  # draw road background
        for i in range(7):  # draw road separations (white rectangles)
            pygame.draw.rect(screen, (255, 255, 255), (i*194-self.current_frame*10, 81, 114, 13))
            pygame.draw.rect(screen, (255, 255, 255), (i*194-self.current_frame*10, 200, 114, 13))
        self.current_frame = (self.current_frame + 1) % self.frame_number  # update frame to create movement effect
