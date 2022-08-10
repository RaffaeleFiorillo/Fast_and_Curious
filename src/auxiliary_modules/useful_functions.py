from random import choice as random_choice, randint as random_randint, random as random_random
import math
from pygame import time

# These functions are just a reimplementation of existing python packages. They are useful because other modules of this
# game don't need to import the module random or time (etc.), just this module (functions).


def choice(list_r: list):
    return random_choice(list_r)


def randint(first_number: int, last_number: int) -> int:
    return random_randint(first_number, last_number)


def random() -> float:
    return random_random()


def arc_sin(value: int) -> float:
    return math.degrees(math.asin(value))


def sin(angle: int) -> float:
    return math.sin(math.radians(angle))


def cos(angle: int) -> float:
    return math.cos(math.radians(angle))


def wait(milliseconds: int) -> None:
    time.wait(milliseconds * 1000)


def get_vector_distance(init_x: int, init_y: int, fin_x: int, fin_y: int):
    x = math.pow(fin_x - init_x, 2)
    y = math.pow(fin_y - init_y, 2)
    vector = math.sqrt(x + y)
    return vector


def get_fibonacci(order: int) -> int:
    if order < 3:
        return 1
    first, second, number = 1, 1, None
    for _ in range(2, order):
        second, first = first + second, second
    return second


def create_buttons(button, button_dir: str, effects: [str], y_coo=None):
    position_x = (1080 - 260) // 2
    position_y = y_coo if y_coo is not None else [y for y in range(150, 600, 150)]
    buttons = []
    for i, y in enumerate(position_y[:len(effects)]):
        directory = f"{button_dir}/{i + 1}.png"
        buttons.append(button(position_x, y, directory, effects[i]))
    return buttons
