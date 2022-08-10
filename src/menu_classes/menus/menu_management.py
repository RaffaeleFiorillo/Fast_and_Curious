from .basic_input_manager import BasicInputManagement
from src.menu_classes.buttons import Button
import pygame
from pygame import Surface
from pygame.event import Event
from src.auxiliary_modules import graphics as grp
from src.menu_classes.user import User


# Used when the "Management" option in the Game Menu is selected
class Management(BasicInputManagement):
    def __init__(self, buttons: [Button], directory: str, screen: Surface, user: User = None):
        super().__init__(buttons)
        self.directory = directory
        self.user = user
        self.name_image = grp.load_image(directory)
        self.level_image = grp.load_image(f"menu/interfaces/User/user_info/level{self.user.level}.png")
        self.records_image = grp.load_image(f"menu/interfaces/User/records.png")
        self.navigation_image = grp.load_image(f"menu/interfaces/navigation/navigation.png")
        self.parts_image = grp.load_image(f"menu/interfaces/User/parts.png")
        self.car_image = grp.load_image(f"cars/display/{self.user.level}.png")
        self.effect1 = [grp.load_image(f"menu/effects/5/{i + 1}.png") for i in range(4)]
        self.effect2 = [grp.load_image(f"menu/effects/4/{i + 1}.png") for i in range(4)]
        self.info_images = [grp.load_image(f"menu/info/info_management/{i + 1}.png") for i in range(6)]
        self.active_code = 0
        self.screen = screen
        self.current_frame = 0
        self.coord_effect = self.update_coord_effect()

    def update_coord_effect(self):
        if self.active_code < 2:
            return self.button_list[self.active_code].x - 10, self.button_list[self.active_code].y - 10
        return self.button_list[self.active_code].x - 12, self.button_list[self.active_code].y - 12

    def draw_buttons(self):
        if self.active_code < 2:
            self.screen.blit(self.effect2[int(self.current_frame)], self.coord_effect)
        else:
            self.screen.blit(self.effect1[int(self.current_frame)], self.coord_effect)
        for but in self.button_list:
            but.draw(self.screen)
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

    def update_user(self):
        self.user.music_volume = self.button_list[0].value
        self.user.sound_volume = self.button_list[1].value
        self.user.save_info()
        self.user.turn_active()

    def manage_buttons(self, event: Event):
        new_active_code = self.active_code  # go up if value is -1 and down if it's 1
        if event.key == pygame.K_UP:
            new_active_code -= 1
        elif event.key == pygame.K_DOWN:
            new_active_code += 1
        elif event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
            return self.enter_action()
        elif self.active_code < 2:  # True means is one of the volume buttons (first two) which is active
            if event.key == pygame.K_LEFT:
                self.button_list[self.active_code].change_value(add=-1)
            elif event.key == pygame.K_RIGHT:
                self.button_list[self.active_code].change_value(add=1)
            self.update_user()
        new_active_code = new_active_code % len(self.button_list)  # make sure active_code doesn't go off-boundaries
        self.set_button_to_active(new_active_code)

    def manage_mouse(self):
        button = self.button_list[self.active_code]
        if self.active_code >= 2:
            return button.effect
        button.change_value(cursor_x=pygame.mouse.get_pos()[0])
        self.already_checked_cursor = False  # allows the cursor to interact with buttons again
        self.update_user()  # save changes in volume

    def refresh(self):
        grp.clean_background(self.screen)
        self.screen.blit(self.name_image, (305, 0))
        self.screen.blit(self.navigation_image, (355, 620))
        self.screen.blit(self.level_image, (0, 0))
        self.screen.blit(self.records_image, (20, 280))
        self.screen.blit(self.parts_image, (0, 180))
        self.screen.blit(self.car_image, (2, 490))
        self.user.draw_text(self.screen)
        self.screen.blit(self.info_images[self.active_code], (786, 195))
        self.button_list[self.active_code].draw_info(self.screen)
        self.draw_buttons()
        pygame.display.update()
