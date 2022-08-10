from .basic_input_manager import BasicInputManagement
import pygame
from pygame import Surface
from pygame.event import Event
from src.auxiliary_modules import graphics as grp
from src.auxiliary_modules import user_data_management as udm
from src.auxiliary_modules import useful_functions as uf
from src.auxiliary_modules import audio
from src.menu_classes.sounds import success_sound, error_sound


# Used every time a "Mission: AI" match is over and the game results must be displayed and processed
class ReportMissionAI(BasicInputManagement):
    def __init__(self, screen: Surface, precision: int, speed: int, parts_collected: int,
                 resistance: int, time: int, finished: bool):
        super().__init__()
        self.screen = screen
        self.image = grp.load_image(f"menu/interfaces/Main/Results_AI.png")
        self.requirements_satisfied = False
        self.parts = 0
        self.coordinates = ((635, 360), (635, 300), (622, 397),
                            (515, 360), (515, 300),
                            (713, 275), (713, 336), (713, 397),
                            (725, 503), (725, 471), (725, 540), (725, 576))
        self.values_images = self.initiate_results(precision, speed, parts_collected, resistance, time, finished)
        self.refresh()

    def initiate_results(self, precision: int, speed: int, parts_collected: int,
                         resistance: int, time: int, finished: bool):
        values = []
        # results about level requirements
        c_w = {True: "correct", False: "wrong"}
        font1 = pygame.font.SysFont('Times New Roman', 20)
        font1.set_bold(True)
        values.append(font1.render(str(int(precision)), True, (255, 255, 255)))  # player's achieved precision
        values.append(font1.render(str(int(speed)), True, (255, 255, 255)))  # player's achieved speed
        values.append(grp.load_image(f"menu/interfaces/navigation/{c_w[finished]}.png"))  # player typed all the text
        required_speed, required_precision = udm.get_requirements()  # get required speed and precision to pass level
        values.append(font1.render(str(required_precision), True, (255, 255, 255)))  # player's required precision
        values.append(font1.render(str(required_speed), True, (255, 255, 255)))  # player's required speed
        values.append(grp.load_image(f"menu/interfaces/navigation/{c_w[speed >= required_speed]}.png"))  # speed status
        values.append(grp.load_image(f"menu/interfaces/navigation/{c_w[precision >= required_precision]}.png"))
        values.append(grp.load_image(f"menu/interfaces/navigation/{c_w[finished]}.png"))  # text completed status
        # results about parts
        font1 = pygame.font.SysFont('Times New Roman', 16)
        font1.set_bold(True)
        values.append(font1.render(str(parts_collected), True, (255, 255, 255)))
        values.append(font1.render(str(int(resistance)), True, (255, 255, 255)))
        values.append(font1.render(str((100 - int(resistance)) * 3), True, (255, 255, 255)))
        self.parts = parts_collected - (100 - int(resistance)) * 3
        values.append(font1.render(str(self.parts), True, (255, 255, 255)))
        # verify if requirements were satisfied in order to proceed to next level
        if speed >= required_speed and precision >= required_precision and (int(time) >= 60 or finished):
            self.requirements_satisfied = True
        return values

    def refresh(self):
        self.screen.blit(self.image, (287, 40))
        [self.screen.blit(image, coo) for image, coo in zip(self.values_images, self.coordinates)]
        pygame.display.update()

    def manage_buttons(self, event: Event):
        if event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
            return True
        return False

    def display_level_info_message(self):
        message_dict = {True: "success5", False: "error8"}
        time_dict = {True: 3, False: 3}
        sound_dict = {True: success_sound, False: error_sound}
        message = message_dict[self.requirements_satisfied]
        time = time_dict[self.requirements_satisfied]
        audio.play(sound_dict[self.requirements_satisfied])
        self.screen.blit(grp.load_image(f"menu/messages/{message}.png"), (230, 200))
        pygame.display.update()
        uf.wait(time)
        pygame.event.clear()  # all pressed buttons are dismissed in this phase

    def display(self):
        while True:
            self.clock.tick(30)
            effect = self.manage_events()
            if effect is not None:
                self.display_level_info_message()
                return self.requirements_satisfied, self.parts
            # self.refresh() -> moved to the constructor since the image is static and doesn't need to refresh
