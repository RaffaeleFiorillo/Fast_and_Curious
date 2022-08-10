from .basic_input_manager import BasicInputManagement
from src.menu_classes.buttons import NameButton
import pygame
from pygame import Surface
from pygame.event import Event
from src.auxiliary_modules import graphics as grp
from src.auxiliary_modules import user_data_management as udm
from src.menu_classes.menus.user_menu import User


# Used when the "Continue" option in the Main Menu is selected
class ChooseAccount(BasicInputManagement):
    def __init__(self, screen: Surface):
        super().__init__()
        self.screen = screen
        self.image = grp.load_image(f"menu/interfaces/Main/choose account.png")
        self.active_code = 0
        self.user = User()
        self.create_buttons()

    def display_menu(self):
        while True:
            self.clock.tick(30)
            effect = self.manage_events()
            if effect is not None:
                return effect
            if not self.already_checked_cursor:  # saves time avoiding iterating over buttons when it was done already
                self.cursor_is_on_button()  # mouse visual interaction with interface
            self.refresh()

    def set_button_to_active(self, new_active_code: int):
        self.button_list[self.active_code].deactivate()  # deactivate previous active button
        super().set_button_to_active(new_active_code)
        self.button_list[self.active_code].activate()  # activate current active button

    def manage_buttons(self, event: Event):
        new_active_code = self.active_code
        if event.key == pygame.K_DOWN:
            new_active_code += 1
        elif event.key == pygame.K_UP:
            new_active_code -= 1
        elif event.key == pygame.K_ESCAPE:
            return "MainMenu"
        elif event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
            return self.enter_action()
        new_active_code = new_active_code % len(self.button_list)  # make sure active_code doesn't go off-boundaries
        self.set_button_to_active(new_active_code)

    def enter_action(self):
        if self.button_list:
            self.user.name = self.button_list[self.active_code].name
            self.user.get_info()
            self.user.turn_active()
            return "enter_password"

    def create_buttons(self):
        users = udm.list_users()  # list of usernames in alphabetical order
        if not users:  # if there are no accounts available, User should know therefore menu image is changed
            self.image = grp.load_image(f"menu/interfaces/Main/choose account- no users.png")
            return None
        active, passive = grp.get_users_images()  # lists of button images for both cases of being active or passive
        button_coordinates = [(322, 115 + 55 * i) for i in range(len(users) % 9)]  # max users is 9
        self.button_list = []
        for user_index, coordinates in enumerate(button_coordinates):
            x, y, active_image, passive_image = coordinates[0], coordinates[1], active[user_index], passive[user_index]
            self.button_list.append(NameButton(x, y, active_image, passive_image, users[user_index]))
        self.button_list[self.active_code].activate()  # first button is set to active

    def refresh(self):
        self.screen.blit(self.image, (0, 0))
        [button.draw(self.screen) for button in self.button_list]
        self.screen.blit(grp.load_image(f"menu/interfaces/navigation/navigation3.png"), (355, 620))
        pygame.display.update()
