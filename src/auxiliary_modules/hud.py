from pygame import Surface
from .graphics import load_image, create_sized_text
from .user_data_management import get_user_data
from .files import read_file_content

# This section contains functions designed for the proper functioning of the game's HUD interface.
# the job and description of a function can be understood by his name. the last two words of every function refer to
# what they are responsible for displaying on the game screen


def load_text_coordinates():
    layout_coo = {1: ((290, 454), (290, 469), (290, 484), (290, 499), (290, 514), (290, 529), (290, 544), (290, 559)),
                  2: ((290, 454), (290, 469), (290, 484), (290, 499), (290, 514), (290, 529), (290, 544), (290, 559))}
    user_name = get_user_data()[0][0]
    layout_type = int(read_file_content(f"saves/{user_name}/account_config.txt", 1)[0].split("#")[0])
    return layout_coo[layout_type]


def load_hud_background():
    user_name = get_user_data()[0][0]
    layout_type = int(read_file_content(f"saves/{user_name}/account_config.txt", 1)[0].split("#")[0])
    return load_image(f"HUD/backgrounds/HUD_background_{layout_type}.png")


def write_hud_parts_value(screen: Surface, number_parts: int) -> None:
    text = str(number_parts)
    adjust = len(text) * 7
    text_image = create_sized_text(165, 25, text, (0, 0, 0), 7)
    screen.blit(text_image, (540 - adjust, 600))


def write_hud_time_value(screen: Surface, time_value: int) -> None:
    if time_value == "i":
        screen.blit(load_image("HUD/infinite.png"), (529, 665))
    else:
        text = str(time_value)
        adjust = len(text) * 4
        text_image = create_sized_text(100, 16, text, (0, 0, 0), 7)
        screen.blit(text_image, (540 - adjust, 670))


def display_hud_speed_meter(screen: Surface, speed: int) -> None:
    text = str(int(speed))
    image_number = int(speed / 6.7)
    if image_number > 14:
        image_number = 14
    if image_number < 0:
        image_number = 0
    adjust = len(text) * 7
    text_image = create_sized_text(100, 20, text, (0, 0, 0), 7)
    screen.blit(load_image(f"HUD/meter/{image_number}.png"), (20, 420))
    screen.blit(text_image, (148 - adjust, 596))


def display_hud_precision_meter(screen: Surface, precision: int) -> None:
    text = str(int(precision))
    image_number = int(precision / 6.7)
    if precision > 100:
        image_number = 14
    elif precision < 0:
        image_number = 0
    adjust = len(text) * 7
    text_image = create_sized_text(100, 20, text, (0, 0, 0), 7)
    screen.blit(load_image(f"HUD/meter/{image_number}.png"), (811, 420))
    screen.blit(text_image, (940 - adjust, 596))


def display_hud_energy_bar(screen: Surface, energy_level: int) -> None:
    image_number = int(energy_level / 3.333)
    if image_number > 30:
        image_number = 30
    elif image_number < 0:
        image_number = 0
    screen.blit(load_image(f"HUD/barr/{image_number}.png"), (296, 640))


def display_hud_resistance_bar(screen: Surface, resistance_level: int) -> None:
    image_number = int(resistance_level / 3.333)
    if image_number > 30:
        image_number = 30
    elif image_number < 0:
        image_number = 0
    screen.blit(load_image(f"HUD/barr/{image_number}.png"), (605, 640))
