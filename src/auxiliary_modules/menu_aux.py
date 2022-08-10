from os import remove, path
from sys import exit as exit_2
from .user_data_management import erase_active_user_data


def remove_prov_image():
    if path.isfile("images/menu/interfaces/prov_image/prov_image.png"):
        remove("images/menu/interfaces/prov_image/prov_image.png")


def terminate_execution() -> None:
    erase_active_user_data()
    remove_prov_image()
    exit_2()
