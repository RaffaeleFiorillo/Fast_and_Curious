from .basic_input_manager import BasicInputManagement
import pygame
from pygame import Surface
from pygame.event import Event
from src.auxiliary_modules import graphics as grp
from src.auxiliary_modules import display
from src.auxiliary_modules import files
from src.menu_classes.user import User


# Used every time a User manages to level up, and he must unlock the "Mission: AI" option in the Game Menu
class UnlockLevel(BasicInputManagement):
    def __init__(self, screen: Surface):
        super().__init__()
        self.screen = screen
        self.image = grp.load_image("menu/interfaces/Main/unlock level.png")
        self.user = None
        self.parts_needed = None
        self.create_user()

    def create_user(self):
        self.user = User()
        self.user.get_active_user()
        self.user.get_info()
        content = files.read_file_content(f"parameters/levels info/{self.user.level}.txt", 1)[0].split(" ")[2]
        self.parts_needed = int(content)

    def show_error_message(self) -> None:
        display.show_error_message(self.screen, 9)

    def show_success_message(self) -> None:
        display.show_success_message(self.screen, 6)

    def verify_parts_number(self):
        return self.parts_needed <= self.user.parts

    def save_state(self):
        files.write_file_content(f"saves/{self.user.name}/next_level.txt", "1")
        self.user.parts = self.user.parts - self.parts_needed
        self.user.save_info()
        self.user.turn_active()

    def parts_image(self):
        return grp.create_sized_text(190, 50, str(self.parts_needed), (255, 180, 0))

    def display_menu(self):
        while True:
            self.clock.tick(30)
            effect = self.manage_events()
            if effect is not None:
                return effect
            self.refresh()

    def manage_buttons(self, event: Event):
        if event.key == pygame.K_ESCAPE:
            return True
        elif event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
            if self.verify_parts_number():
                self.show_success_message()
                self.save_state()
                return True
            self.show_error_message()
            return True

    def refresh(self):
        self.screen.blit(self.image, (210, 250))
        self.screen.blit(self.parts_image(), (635, 310))
        pygame.display.update()
