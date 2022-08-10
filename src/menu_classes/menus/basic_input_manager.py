import pygame
from pygame.event import Event
from src.menu_classes.buttons.button import Button
from src.menu_classes.sounds import button_y_sound
from src.auxiliary_modules import audio


# provides a simple way of managing User input, both keyboard and mouse
class BasicInputManagement:
    def __init__(self, buttons: [Button] = None):
        if buttons is None:
            buttons = []
        self.button_activation_sound = button_y_sound
        self.clock = pygame.time.Clock()
        self.button_list = buttons
        self.active_code = 0
        self.coord_effect = None
        self.already_checked_cursor = False  # True means that actions have already been taken regarding cursor position

    def set_button_to_active(self, new_active_code: int):
        if new_active_code != self.active_code:
            audio.play(self.button_activation_sound)
            self.active_code = new_active_code
            self.coord_effect = self.update_coord_effect()

    def update_coord_effect(self):
        pass

    def manage_events(self):  # returns action to take based on input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                return self.get_effect_by_input(event)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.already_checked_cursor = True
                return self.get_effect_by_input()

    def manage_buttons(self, event: Event):
        if event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
            return self.enter_action()

    def get_effect_by_input(self, event: Event = None):
        if event:  # if input is not None it means a key has been pressed
            effect = self.manage_buttons(event)
        else:
            effect = self.manage_mouse()
        return effect

    def cursor_is_on_button(self):
        mouse_position = pygame.mouse.get_pos()
        for button_index, button in enumerate(self.button_list):
            if button.cursor_is_inside(mouse_position):
                self.set_button_to_active(button_index)
                return True
        return False

    def enter_action(self):
        return self.button_list[self.active_code].effect

    def manage_mouse(self):
        if self.cursor_is_on_button():
            return self.enter_action()
        self.already_checked_cursor = False  # allows the cursor to interact with buttons again after the User clicks
