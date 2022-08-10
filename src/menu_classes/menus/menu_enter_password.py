from .basic_input_manager import BasicInputManagement
import pygame
from pygame import Surface
from pygame.event import Event
from src.auxiliary_modules import graphics as grp
from src.auxiliary_modules import user_data_management as udm
from src.auxiliary_modules import useful_functions as uf
from src.auxiliary_modules import display
from src.auxiliary_modules import audio
from src.menu_classes.sounds import success_sound, erase_letter_sound
from src.menu_classes.menus.user_menu import User


# Used whenever is required the introduction of a password in order to complete a task
class EnterPassword(BasicInputManagement):
    def __init__(self, screen: Surface, change: bool = False):
        super().__init__(None)
        self.screen = screen
        self.image = grp.load_image(f"menu/interfaces/Main/insert_password.png")
        self.user = None
        self.password_list = []
        self.create_user()
        self.hide = False
        self.change = change

    def create_user(self):
        self.user = User()
        self.user.get_active_user()  # makes User get his name
        self.user.get_info()  # now that it has his name it can access his folder
        udm.erase_active_user_data()  # User should not be active YET

    def show_error_message(self) -> None:
        pygame.image.save(self.screen, "images/menu/interfaces/prov_image/prov_image.png")
        display.show_error_message(self.screen, 5)
        self.screen.blit(grp.load_image(f"menu/interfaces/prov_image/prov_image.png"), (0, 0))

    def show_success_message(self) -> None:
        audio.play(success_sound)
        if self.change:
            self.screen.blit(grp.load_image(f"menu/messages/success3.png"), (230, 200))
            time = 3
        else:
            self.screen.blit(grp.load_image(f"menu/messages/success2.png"), (230, 200))
            grp.write_name(self.screen, self.user.name)
            time = 1
        pygame.display.update()
        uf.wait(time)
        pygame.event.clear()  # all pressed buttons are dismissed in this phase

    def verify_password(self):
        return "".join(self.password_list) == self.user.password

    def display_menu(self):
        while True:
            self.clock.tick(30)
            effect = self.manage_events()
            if effect is not None:
                self.user.turn_active()  # NOW User should be active (check method "create_user" for context)
                return effect
            self.refresh()

    def manage_buttons(self, event: Event):
        if event.key == pygame.K_BACKSPACE:
            audio.play(erase_letter_sound)
            self.password_list = self.password_list[:-1]
        elif event.key == pygame.K_ESCAPE:
            if self.change:
                return "manage"
            return "choose"
        elif event.key == pygame.K_TAB:
            self.hide = not self.hide
        elif event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
            if self.verify_password():
                self.show_success_message()
                if self.change:
                    return "MainMenu"
                return "GameMenu"
            else:
                self.show_error_message()
                return "enter_password"
        elif len(self.password_list) < 25:
            self.password_list.append(event.unicode)

    def manage_mouse(self):
        pass

    def refresh(self):
        self.screen.blit(self.image, (210, 250))
        grp.write_password(self.screen, self.password_list, self.hide)
        pygame.display.update()
