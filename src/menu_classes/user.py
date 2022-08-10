from pygame import Surface
from src.auxiliary_modules import *
from src.auxiliary_modules import graphics as grp


# Manages the User's information in the Game Menu
class User:
    def __init__(self, name=""):
        self.name = name
        self.password = ""
        self.best_speed = 0
        self.best_time = 0
        self.level = 1
        self.parts = 0
        self.image = grp.load_image(f"menu/interfaces/User/user_info/level1.png")
        self.parts_text, self.coo_p_t = None, (0, 0)
        self.best_speed_text, self.coo_bs_t = None, (0, 0)
        self.best_time_text, self.coo_bt_t = None, (0, 0)
        self.name_text, self.coo_n_t = None, (0, 0)
        self.music_volume = 8
        self.sound_volume = 8

    def get_info(self) -> None:
        data = files.read_file_content(f"saves/{self.name}/data.txt", 1)[0].split(" ")
        self.best_speed, self.best_time, self.level, self.parts, self.password, self.music_volume, self.sound_volume = \
            int(data[0]), int(data[1]), int(data[2]), int(data[3]), data[4], int(data[5]), int(data[6])
        self.image = grp.load_image(f"menu/interfaces/User/user_info/level{self.level}.png")

    def get_texts(self) -> None:
        self.best_time_text, self.coo_bt_t = grp.writable_best_time(self.best_time)
        self.best_speed_text, self.coo_bs_t = grp.writable_best_speed(self.best_speed)
        self.parts_text, self.coo_p_t = grp.writable_parts_number(self.parts)
        self.name_text, self.coo_n_t = grp.writable_user_name(self.name)

    def draw_text(self, screen: Surface) -> None:
        screen.blit(self.best_time_text, self.coo_bt_t)
        screen.blit(self.best_speed_text, self.coo_bs_t)
        screen.blit(self.parts_text, self.coo_p_t)
        screen.blit(self.name_text, self.coo_n_t)

    def get_active_user(self) -> None:
        data = files.read_file_content("saves/active_user.txt", 1)[0].split(" ")
        self.name, self.best_speed, self.best_time = data[0], int(data[1]), int(data[2])
        self.level, self.parts, self.password = int(data[3]), int(data[4]), data[5]
        self.music_volume, self.sound_volume = data[6], data[7]
        self.image = grp.load_image(f"menu/interfaces/User/user_info/level{self.level}.png")

    def get_string_attributes(self):
        return f"{self.best_speed} {self.best_time} {self.level} {self.parts} {self.password} {self.music_volume}" \
               f" {self.sound_volume}"

    def turn_active(self) -> None:
        files.write_file_content("saves/active_user.txt", f"{self.name} {self.get_string_attributes()}")

    def save_info(self) -> None:
        files.write_file_content(f"saves/{self.name}/data.txt", self.get_string_attributes())
