import pygame
from pygame import Surface
from pygame.event import Event
from src.auxiliary_modules import graphics as grp
from .basic_input_manager import BasicInputManagement
from src.menu_classes.buttons import Button
from src.auxiliary_modules import audio
from src.menu_classes.sounds import error_sound, button_y_sound


# Used for "Story", and every Tutorial option
class MenuImageSequence(BasicInputManagement):
    def __init__(self, screen: Surface, directory: str, num_pages: int, func_link: str, name: str):
        buttons = [Button(110, 640, "menu/buttons/10/1.png", False), Button(745, 640, "menu/buttons/10/2.png", True)]
        super().__init__(buttons)
        self.screen = screen
        self.name = name
        self.background_image = grp.load_image(f"menu/interfaces/Main/sequence.png")
        self.directory = directory
        self.slide_name = grp.load_image(f"slides/{self.directory}/name.png")
        self.num_pages = num_pages
        self.update_screen = True  # variable that prevents updating screen without need
        self.current_page = 0
        self.origin_link = func_link

    def go_to_next_page(self):
        if self.current_page + 1 == self.num_pages:
            audio.play(error_sound)
        else:
            audio.play(button_y_sound)
            self.current_page += 1
            self.update_screen = True

    def go_to_previous_page(self):
        if self.current_page == 0:
            audio.play(error_sound)
        else:
            audio.play(button_y_sound)
            self.current_page -= 1
            self.update_screen = True

    def manage_buttons(self, event: Event):
        if event.key == pygame.K_RIGHT:
            self.go_to_next_page()
        elif event.key == pygame.K_LEFT:
            self.go_to_previous_page()
        elif event.key == pygame.K_ESCAPE:
            return self.origin_link
        if self.current_page > self.num_pages - 1:
            self.current_page = self.num_pages - 1
        if self.current_page < 0:
            self.current_page = 0

    def hide_unwanted_button(self):
        if self.current_page == self.num_pages - 1:
            pygame.draw.rect(self.screen, (0, 0, 0), (745, 640, 240, 40))
        elif self.current_page == 0:
            pygame.draw.rect(self.screen, (0, 0, 0), (110, 640, 240, 40))

    def write_page_number(self):
        page_image = grp.create_sized_text(20, 50, str(self.current_page + 1), (255, 255, 255))
        self.screen.blit(page_image, (530, 640))

    def enter_action(self):
        if self.button_list[self.active_code].effect:
            self.go_to_next_page()
        else:
            self.go_to_previous_page()

    def refresh(self):
        if not self.update_screen:  # if screen has not been changed menu shouldn't refresh anything
            return None
        self.screen.blit(self.background_image, (0, 0))
        self.screen.blit(grp.load_image(f"slides/{self.directory}/{self.current_page + 1}.png"), (108, 120))
        self.screen.blit(self.slide_name, (400, 0))
        self.write_page_number()
        [button.draw(self.screen) for button in self.button_list]
        self.hide_unwanted_button()  # if at the beginning/end of slides, it won't show the button to go further
        self.update_screen = False
        pygame.display.update()

    def display_menu(self):
        while True:
            self.clock.tick(30)
            effect = self.manage_events()
            if effect is not None:
                return effect
            self.refresh()
