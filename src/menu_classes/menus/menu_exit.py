from .basic_input_manager import BasicInputManagement
from src.menu_classes.buttons import Button
import pygame
from pygame import Surface
from pygame.event import Event
from src.auxiliary_modules import graphics as grp


# Used whenever the User wants to leave the game
class Exit(BasicInputManagement):
    def __init__(self, directory: str, screen: Surface, buttons: [Button]):
        super().__init__(buttons)
        self.name_image = grp.load_image(directory)
        self.effect = [grp.load_image(f"menu/effects/1/{i + 1}.png") for i in range(4)]
        self.active_code = 0
        self.screen = screen
        self.current_frame = 0

    def draw_buttons(self):
        coordinates = {0: (240, 410), 1: (567, 410)}
        coo = coordinates[self.active_code]
        self.screen.blit(self.effect[int(self.current_frame)], coo)
        self.current_frame += 0.25
        if self.current_frame > 3:
            self.current_frame = 0

    def display_menu(self):
        while True:
            self.clock.tick(30)
            effect = self.manage_events()
            if effect is not None:
                return effect
            if not self.already_checked_cursor:  # saves time avoiding iterating over buttons when it was done already
                self.cursor_is_on_button()  # mouse visual interaction with interface
            self.refresh()

    def manage_buttons(self, event: Event):
        new_active_code = self.active_code  # go up if value is -1 and down if it's 1
        if event.key == pygame.K_RIGHT:
            new_active_code += 1
        elif event.key == pygame.K_LEFT:
            new_active_code -= 1
        elif event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
            return self.button_list[self.active_code].effect
        new_active_code = new_active_code % len(self.button_list)  # make sure active_code doesn't go off-boundaries
        self.set_button_to_active(new_active_code)

    def refresh(self):
        self.screen.blit(self.name_image, (0, 0))
        self.draw_buttons()
        self.screen.blit(grp.load_image(f"menu/interfaces/navigation/navigation2.png"), (350, 600))
        pygame.display.update()