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
from src.menu_classes.sounds import button_x_sound, erase_letter_sound


# Used when the "New Game" option in the Main Menu is selected
class AddText(BasicInputManagement):
    def __init__(self, screen: Surface, buttons: [Button]):
        super().__init__(buttons)
        self.image = grp.load_image(f"menu/interfaces/Main/add text.png")
        self.effect = [grp.load_image(f"menu/effects/2/{i + 1}.png") for i in range(4)]
        self.active_code = 0
        self.text_lines_images = None
        self.screen = screen
        grp.clean_background(self.screen)  # hide previous interface
        self.character_number = 0
        self.written_text = ""
        self.error_code = 0
        self.current_frame = 0
        self.text_lines = []

    def draw_buttons(self) -> None:
        coordinates = {0: (320, 484), 1: (558, 484)}
        coo = coordinates[self.active_code]
        self.screen.blit(self.effect[int(self.current_frame)], (coo[0] - 5, coo[1] - 10))
        [button.draw(self.screen) for button in self.button_list]
        self.current_frame = (self.current_frame + 0.2) % 3

    def show_error_message(self) -> None:
        display.show_error_message(self.screen, self.error_code)
        grp.clean_background(self.screen)

    def show_success_message(self) -> None:
        display.show_success_message(self.screen, 7)

    def display_menu(self):
        while True:
            self.clock.tick(30)
            effect = self.manage_events()
            if effect is not None:
                break
            if not self.already_checked_cursor:  # saves time avoiding iterating over buttons when it was done already
                self.cursor_is_on_button()  # mouse visual interaction with interface
            self.refresh()

    def create_text_content(self) -> [str]:
        text_content = [f"{len(self.text_lines)} \n"]  # first line of these files holds the number of lines in the text
        for line in self.text_lines:
            text_content.append(line + "\n")
        return text_content

    def create_text(self) -> None:
        # creating the image
        self.text_lines, self.text_lines_images = grp.convert_text_to_images(self.written_text, True)
        coordinates = [(15, 5), (15, 25), (15, 45), (15, 65), (15, 85), (15, 105)]
        text_background = pygame.Surface((519, 132))
        text_background.blit(grp.load_image(f"texts/background.png"), (0, 0))
        for img, coo in zip(self.text_lines_images, coordinates):
            text_background.blit(img, coo)
        last_number_text = udm.get_last_text_number()
        pygame.image.save(text_background, f"images/texts/{last_number_text + 1}.png")
        # creating the txt file
        files.write_file_content(f"texts/{last_number_text + 1}.txt", self.create_text_content())

    def validate_text_information(self) -> bool:
        special = [",", ".", "'", " "]
        if self.character_number < 192:
            self.error_code = 10
            return False
        ch_list = set(self.written_text)
        for char in ch_list:  # verify that there are no special characters or numbers
            if char.isalpha() or char in special:
                continue
            self.error_code = 11
            return False
        return True

    def last_word_is_proper(self):
        if self.written_text != "":
            last_word_length = len(self.written_text.split()[-1])
            return last_word_length < 48
        return True

    def manage_buttons(self, event: Event):
        if event.key == pygame.K_RIGHT:
            audio.play(button_x_sound)
            self.active_code = 1
        elif event.key == pygame.K_LEFT:
            audio.play(button_x_sound)
            self.active_code = 0
        elif event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
            return self.enter_action()
        elif event.key == pygame.K_BACKSPACE:
            audio.play(erase_letter_sound)
            self.written_text = self.written_text[:-1]
            self.character_number -= 1
            if self.character_number < 0:
                self.character_number = 0
        elif self.character_number < 288 and self.last_word_is_proper():
            special = [" ", ",", ".", "'"]
            if event.unicode.isalpha() or event.unicode in special:
                self.written_text += event.unicode
                self.character_number = len(self.written_text.strip())

    def enter_action(self):
        if not self.active_code:
            return True
        if self.validate_text_information():
            self.create_text()
            self.show_success_message()
            return True
        self.show_error_message()
        self.already_checked_cursor = False  # make sure cursor gets checked after pressing a button

    def write_potential_text(self):
        coordinates = [(327, 175), (327, 200), (327, 225), (327, 250), (327, 275), (327, 300)]
        self.text_lines, images = grp.convert_text_to_images(self.written_text)
        for img, coo in zip(images, coordinates):
            self.screen.blit(img, coo)
        self.text_lines_images = images

    def refresh(self) -> None:
        self.screen.blit(self.image, (0, 0))
        self.draw_buttons()
        self.write_potential_text()
        pygame.display.update()
