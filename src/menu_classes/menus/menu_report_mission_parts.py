from .basic_input_manager import BasicInputManagement
import pygame
from pygame import Surface
from pygame.event import Event
from src.auxiliary_modules import graphics as grp


# Used every time a "Mission: PARTS" match is over and the game results must be displayed and processed
class ReportMissionParts(BasicInputManagement):
    def __init__(self, screen: Surface, precision: int, avg_speed: int, max_speed: int,
                 parts_collected: int, time: float):
        super().__init__()
        self.screen = screen
        self.is_cheating = False  # value is set to True if,based on the data given to the constructor, player cheated
        self.image = grp.load_image("menu/interfaces/Main/Results_Parts.png")
        self.parts = 0
        self.time = int(time)
        self.coordinates = [(725, 330), (725, 362), (725, 396), (725, 426), (725, 457), (725, 529)]  # screen x,y values
        self.values_images = self.initiate_results(precision, avg_speed, max_speed, parts_collected)
        self.refresh()

    def initiate_results(self, precision: int, avg_speed: int, max_speed: int, parts_collected: int):
        values = []
        # results about parts
        font1 = pygame.font.SysFont('Times New Roman', 16)
        font1.set_bold(True)
        values.append(font1.render(str(int(precision)), True, (255, 255, 255)))
        values.append(font1.render(str(int(avg_speed)), True, (255, 255, 255)))
        values.append(font1.render(str(int(max_speed)), True, (255, 255, 255)))
        values.append(font1.render(str(self.time), True, (255, 255, 255)))
        values.append(font1.render(str(parts_collected), True, (255, 255, 255)))
        self.parts = parts_collected - 300
        values.append(font1.render(str(self.parts), True, (255, 255, 255)))
        if self.parts == -1300:  # player cheated and it shows because he got penalized
            font2 = pygame.font.SysFont('Times New Roman', 23)
            font2.set_bold(True)
            inform_cheating_1 = "You Cheated!!!"
            inform_cheating_2 = "Your Scores Are Now Nullified and You Will Loose 1300parts"
            values.append(font2.render(inform_cheating_1, True, (255, 0, 0)))
            values.append(font1.render(inform_cheating_2, True, (255, 0, 0)))
            self.coordinates.append((460, 200))
            self.coordinates.append((315, 240))
        return values

    def refresh(self):
        self.screen.blit(self.image, (287, 40))
        [self.screen.blit(image, coo) for image, coo in zip(self.values_images, self.coordinates)]
        pygame.display.update()

    def manage_buttons(self, event: Event):
        if event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
            return True
        return False

    def display(self):
        while True:
            self.clock.tick(30)
            effect = self.manage_events()
            if effect is not None:
                return self.parts
            # self.refresh() -> moved to the constructor since the image is static and doesn't need to refresh
