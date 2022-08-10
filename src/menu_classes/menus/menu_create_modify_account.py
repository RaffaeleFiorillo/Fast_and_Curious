from .basic_input_manager import BasicInputManagement
from src.menu_classes.buttons import Button
import pygame
from pygame import Surface
from pygame.event import Event
from src.auxiliary_modules import graphics as grp
from src.auxiliary_modules import user_data_management as udm
from src.auxiliary_modules import display
from src.auxiliary_modules import audio
from src.auxiliary_modules import files
from src.menu_classes.sounds import button_y_sound, button_x_sound, erase_letter_sound
from src.menu_classes.menus.user_menu import User


# Used when the "New Game" option in the Main Menu is selected or when, to change some info, credentials are required
class CreateModifyAccount(BasicInputManagement):
    def __init__(self, directory: str, screen: Surface, buttons: [Button], change: bool = False):
        super().__init__(buttons)
        self.name_image = grp.load_image(directory)
        self.effect = [grp.load_image(f"menu/effects/2/{i + 1}.png") for i in range(4)]
        self.active_code_y = 0
        self.button_activation_sound = button_x_sound
        self.hide = False
        self.screen = screen
        self.inputs = [[], []]
        self.current_frame = 0
        self.user = User()
        self.change = change
        if change:
            self.user.get_active_user()

    def activate_y_button(self, active_code: int):
        self.active_code_y = active_code
        audio.play(button_y_sound)

    def cursor_is_on_button(self):
        mouse_position = pygame.mouse.get_pos()
        if self.button_list[0].cursor_is_inside(mouse_position) and self.active_code_y != 0:
            self.activate_y_button(0)
        elif self.button_list[1].cursor_is_inside(mouse_position) and self.active_code_y != 1:
            self.activate_y_button(1)
        else:
            for button_index, button in enumerate(self.button_list[2:]):
                if button.cursor_is_inside(mouse_position):
                    self.set_button_to_active(button_index)
                    return True
        return False

    def draw_buttons(self) -> None:
        coordinates = {0: (322, 485), 1: (558, 485)}
        coo = coordinates[self.active_code]
        self.screen.blit(self.effect[int(self.current_frame)], (coo[0] - 5, coo[1] - 10))
        [button.draw(self.screen) for button in self.button_list]
        self.current_frame = (self.current_frame + 0.2) % 3

    def display_menu(self):
        while True:
            self.clock.tick(30)
            effect = self.manage_events()
            if effect is not None:  # if meaningful input is given take respective action
                return effect
            if not self.already_checked_cursor:  # saves time avoiding iterating over buttons when it was done already
                self.cursor_is_on_button()  # mouse visual interaction with interface
            self.refresh()

    def create_account(self) -> None:
        name = "".join(self.inputs[0])
        udm.create_folder(name)  # create the User's folder
        content = ["1 \n", "0"]  # User is initiated with Mission AI available and that he didn't win the game
        # create a file in the User's folder named next_level
        files.write_file_content(f"saves/{name}/next_level.txt", content)

    def validate_user_information(self) -> bool:
        password = "".join(self.inputs[0])
        if self.change:
            if password != self.user.password:
                display.show_error_message(self.screen, 7)
                return False
            elif len(self.inputs[1]) == 0:
                display.show_error_message(self.screen, 3)
                return False
            elif " " in self.inputs[1]:
                display.show_error_message(self.screen, 4)
                return False
        else:
            if password in udm.list_users():
                display.show_error_message(self.screen, 1)
                return False
            elif len(self.inputs[0]) == 0:
                display.show_error_message(self.screen, 2)
                return False
            elif len(self.inputs[1]) == 0:
                display.show_error_message(self.screen, 3)
                return False
            elif " " in self.inputs[0] or " " in self.inputs[1]:
                display.show_error_message(self.screen, 4)
                return False
        return True

    def enter_action(self):
        if self.button_list[self.active_code + 2].effect:
            if self.validate_user_information():
                if self.change:
                    display.show_success_message(self.screen, 4)
                else:
                    self.user.name = "".join(self.inputs[0])
                    self.create_account()
                    display.show_success_message(self.screen, 1)
                self.user.password = "".join(self.inputs[1])
                self.user.save_info()
                self.user.turn_active()
                return True
            elif self.change:
                return "change_password"
            return "new"
        return False

    def manage_buttons(self, event: Event):
        if event.key == pygame.K_RIGHT:
            audio.play(button_x_sound)
            self.active_code = 1
        elif event.key == pygame.K_LEFT:
            audio.play(button_x_sound)
            self.active_code = 0
        elif event.key == pygame.K_DOWN:
            self.activate_y_button(1)
        elif event.key == pygame.K_UP:
            self.activate_y_button(0)
        elif event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
            return self.enter_action()
        elif event.key == pygame.K_TAB:
            self.hide = not self.hide
        elif event.key == pygame.K_BACKSPACE:
            audio.play(erase_letter_sound)
            self.inputs[self.active_code_y] = self.inputs[self.active_code_y][:-1]
        elif len(self.inputs[self.active_code_y]) <= 25 and self.active_code_y == 1:
            self.inputs[self.active_code_y].append(event.unicode)
        elif len(self.inputs[self.active_code_y]) <= 20 and self.active_code_y == 0:
            self.inputs[self.active_code_y].append(event.unicode)

    def refresh(self) -> None:
        self.screen.blit(self.name_image, (0, 0))
        self.draw_buttons()
        self.screen.blit(grp.load_image(f"menu/interfaces/navigation/navigation3.png"), (355, 620))
        grp.write_name_password(self.screen, self.inputs[0], self.inputs[1], self.active_code_y, self.hide)
        pygame.display.update()
