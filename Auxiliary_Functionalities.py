# This module contains functions that are used by all the others modules
# -------------------------------------------- IMPORTS -----------------------------------------------------------------
import pygame
from os import walk, mkdir
from sys import exit as exit_2
from shutil import rmtree
from random import choice as random_choice, randint as random_randint, random as random_random
import math


# --------------------------------------- GLOBAL VARIABLES -------------------------------------------------------------


root_directory = "saves/"
cores_obst = [[196, 15, 23], [239, 10, 9], [191, 15, 23], [245, 71, 20], [252, 130, 18], [255, 17, 11], [255, 18, 11],
              [255, 18, 12], [195, 195, 195], [163, 73, 164], [248, 12, 35], [255, 255, 255]]
cores_part = [[255, 128, 0], [255, 242, 0], [34, 177, 76], [252, 130, 19], [237, 28, 36], [255, 0, 255],
              [120, 0, 120], [0, 255, 255], [0, 0, 255]]
cores_estrada = [[0, 0, 0], [108, 108, 108]]
code_meaning = {3: "unknown", 0: "road", 1: "parts", -1: "lava"}
# AI variables achieved by a genetic algorithm that can be found in the genetic_algorithm module
WEIGHTS = [-0.024636661554064646, 0.9490338548623168, 0.9490338548623168, 0.17090764398454833, 1.0661495372951384]
BIAS = [0.2670813587084078, -0.6691533200275781, -0.5723370239650385, 0.25406116993577665, -0.486196069971221]
FRAME_RATE = 30
SCREEN_LENGTH, SCREEN_WIDTH = 1080, 700
CAR_MAX_SPEED = 10
CAR_STE_MIN_DAMAGE_DISTANCE = 400  # distance at which the car starts getting damage from the Space-Time-Entity
CAR_MAX_DISTANCE = 470  # maximum distance the car can reach (right)
CAR_MIN_DISTANCE = CAR_STE_MIN_DAMAGE_DISTANCE - 20   # minimum distance the car can reach (left)


# ----------------------------------- MODULES INITIALIZATION -----------------------------------------------------------
pygame.mixer.init()
pygame.init()
SCREEN = pygame.display.set_mode((SCREEN_LENGTH, SCREEN_WIDTH))


# -------------------------------------     GAME CLASS      ------------------------------------------------------------
# Generic game class that takes some parameters and creates a screen and a dictionary of string keys and
# function values. The keys are a returned value that depends on the link_function in use (see more in the module:
# link_functions). Basically this class just creates the connection between the different menus, functionalities, (...).
class Game:
    link_function_dict: dict

    def __init__(self, screen_lable, link_functions):
        self.screen = None
        self.link_function_dict = link_functions
        self.previous_link = None
        self.create_screen(screen_lable)

    def create_screen(self, lable):
        global SCREEN
        pygame.display.set_caption(lable)
        self.screen = SCREEN  # module must be initialized or the "convert_alpha" method wont work

    def start(self, link, state=True):
        while True:
            if state:
                keys_list = list(self.link_function_dict.keys())
                self.previous_link = keys_list[keys_list.index(link)]  # saving current link in case the state is False
                state = self.link_function_dict[link](self.screen)
                if state:
                    link = state
                    state = True
            else:  # In case the user wants to exit the game by clicking on the red crux the state is set to False
                state = self.link_function_dict["exit1"](self.screen)
                link = self.previous_link


# ------------------------------------- REIMPLEMENTED FUNCTIONS --------------------------------------------------------
# These functions are just a reimplementation of existing python packages. They are useful because other modules of this
# game don't need to import the module random or time (etc.), just this module (functions).

def choice(list_r):
    return random_choice(list_r)


def randint(first_number, last_number):
    return random_randint(first_number, last_number)


def random():
    return random_random()


def arc_sin(value):
    return math.degrees(math.asin(value))


def sin(angle):
    return math.sin(math.radians(angle))


def cos(angle):
    return math.cos(math.radians(angle))


def wait(seconds):
    pygame.time.wait(seconds*1000)


def terminate_execution():
    erase_active_user_data()
    exit_2()


# uses the pygame module to load a sound to memory and returns it
def load_sound(location):
    return pygame.mixer.Sound(f"sounds/{location}")


# returns an image ready to be displayed on the screen. "convert_alpha" makes it much faster to display
def load_image(directory):
    return pygame.image.load(f"images/{directory}").convert_alpha()


# plays a sound passed as argument
def play(sound: pygame.mixer.Sound, volume=False):
    volume = get_sound_volume() if volume is False else volume/10  # 0->10 must be divided by ten to be in 0->1 range
    sound.set_volume(volume)
    sound.play()


def play_music():
    sound = music_sound
    volume = get_music_volume()
    sound.set_volume(volume)
    sound.play(-1)


def music_fade_out():
    music_sound.fadeout(2)


# stops all currently playing sounds
def stop_all_sounds():
    pygame.mixer.stop()


# ------------------------------------------ SOUNDS --------------------------------------------------------------------
error_sound = load_sound("menu/error_message2.WAV")  # sound for every time an error occurs
success_sound = load_sound("menu/success.WAV")       # sound for every time a success occurs
music_sound = load_sound("game/music.WAV")


# ----------------------------------------- CAR AI/VISION FUNCTIONS ----------------------------------------------------
# These functions are used to make the car see the obstacles in the road and choose what to do

# based on given screen coordinates, gives back what type of object is at that position
def see(screen, coo):
    x, y = coo
    if y <= 0:
        return 0
    elif y > 308:
        return 0
    cor = list(screen.get_at((x, y)))[:-1]
    if cor in cores_estrada:
        current_code = 0
    elif cor in cores_part:
        current_code = 1
    else:
        current_code = -1
    # sign = code_meaning[current_code]  # -> turns rgb values into words
    # print(sign)
    return current_code


# Given all seen values, gives back a code value for what to do
def make_a_choice(info, weights=None, bias=None):
    if weights is None:
        weights, bias = WEIGHTS, BIAS
    soma = sum([weights[i] * info[i] + bias[i] for i in range(len(info))])
    refined_value = math.tanh(soma)
    if refined_value >= 0.70:
        return 1
    elif refined_value <= -0.70:
        return -1
    else:
        return 0


# -------------------------------------      MATH      -----------------------------------------------------------------
def get_vector_distance(init_x, init_y, fin_x, fin_y):
    x = math.pow(fin_x-init_x, 2)
    y = math.pow(fin_y-init_y, 2)
    vector = math.sqrt(x+y)
    return vector


def get_fibonacci(order):
    if order < 3:
        return 1
    first, second, number = 1, 1, None
    for _ in range(2, order):
        second, first = first+second, second
    return second


# ------------------------------------- MENU FUNCTIONS -----------------------------------------------------------------
def get_sound_volume():
    with open("saves/active_user.txt", "r") as file:
        line = file.readline().split(" ")
    if len(line) != 1:
        return float(line[7])/10
    else:
        return 1.0


def get_music_volume():
    with open("saves/active_user.txt", "r") as file:
        line = file.readline().split(" ")
    if len(line) != 1:
        return float(line[6])/20.0
    else:
        return 0.5


# displays on the screen an error message specified by his code
def show_error_message(screen, code, waiting_time=3):
    play(error_sound)
    screen.blit(load_image(f"menu/messages/error{code}.png"), (230, 200))
    pygame.display.update()
    wait(waiting_time)
    pygame.event.clear()  # all pressed buttons are dismissed in this phase


# displays on the screen a success message specified by his code
def show_success_message(screen, code, waiting_time=3) -> None:
    play(success_sound)
    screen.blit(load_image(f"menu/messages/success{code}.png"), (230, 200))
    pygame.display.update()
    wait(waiting_time)
    pygame.event.clear()  # all pressed buttons are dismissed in this phase


# creates a folder inside the root_directory with the name of the user creating the account
def create_folder(nome_user):
    mkdir(root_directory+nome_user)


# returns a list with all the usernames currently existing, but only on windows, linux and Mac OS
def list_users():
    return list(walk("saves"))[0][1]


# returns a list with all the names of the texts that the user will type in the matches
def get_text_names():
    texts = walk("texts")
    texts = [text for text in texts][0][1:][1][:-1]
    return texts


# return a text image that fits into a set size, with some customizations (like color and font size)
def create_sized_text(max_size_image, max_size_letter, text, color, min_size_letter=30):
    pygame.font.init()
    rendered_text = None
    for i in range(min_size_letter, max_size_letter)[::-1]:
        text_font = pygame.font.SysFont('Times New Roman', i)
        text_font.set_bold(True)
        rendered_text = text_font.render(text, True, color)
        if rendered_text.get_size()[0] <= max_size_image:
            break
    return rendered_text.convert_alpha()


# writes the name and password typed by a user in the Create User Menu
def write_name_password(screen, name, password, active, hide):
    coordinates1 = [(330, 205), (330, 351)]
    pygame.draw.rect(screen, (0, 0, 255), (coordinates1[active], (422, 57)), 8)
    screen.blit(load_image("menu/interfaces/navigation/pointer.png"),
                (coordinates1[active][0]+450, coordinates1[active][1]))
    coordinates2 = [(385, 217), (385, 363)]
    if hide:
        password = "".join(["*" for letter in password if str(letter).isalnum()])
    else:
        password = "".join(password)
    name = "".join(name)
    name_text = create_sized_text(330, 32, name, (255, 255, 255), 20)
    password_text = create_sized_text(330, 32, password, (255, 255, 255), 16)
    screen.blit(name_text, coordinates2[0])
    screen.blit(password_text, coordinates2[1])


# Writes the password typed by a user when a Insert Password Menu appears (hides it with "*" if the hide variable is set
# to True
def write_password(screen, password, hide):
    pygame.font.init()
    if hide:
        password = "".join(["*" for letter in password if str(letter).isalnum()])
    else:
        password = "".join(password)
    text_font = pygame.font.SysFont('Times New Roman', 32)
    text_font.set_bold(True)
    password_text = text_font.render(password, True, (0, 0, 0)).convert_alpha()
    screen.blit(password_text, (290, 330))


# Writes the user name into the Welcome interface. Changes the letter size in order to fit into the given space
def write_name(screen, name):
    name_text = create_sized_text(540, 50, name, (0, 255, 0))
    screen.blit(name_text, ((screen.get_width()-name_text.get_size()[0])//2+7, 330))


# Writes the user's "best time" value in the Game Menu. Changes the letter size in order to fit into the given space
def writable_best_time(best_time):
    pygame.font.init()
    coordinates = (135, 357)
    text_font = pygame.font.SysFont('Times New Roman', 19)
    text = ["  " for _ in range(10 - len(str(best_time)))]
    new_text = "".join(text)+str(best_time)
    image_text = text_font.render(new_text, True, (255, 255, 255))
    return [image_text, coordinates]


# Writes the user's "best speed" value in the Game Menu. Changes the letter size in order to fit into the given space
def writable_best_speed(best_speed):
    pygame.font.init()
    coordinates = (185, 427)
    text_font = pygame.font.SysFont('Times New Roman', 20)
    text = ["  " for _ in range(4 - len(str(best_speed)))]
    new_text = "".join(text)+str(best_speed)
    image_text = text_font.render(new_text, True, (255, 255, 255))
    return [image_text, coordinates]


# Writes the user's username in the Game Menu. Changes the letter size in order to fit into the given space
def writable_user_name(name):
    pygame.font.init()
    image_text = create_sized_text(253, 65, name, (0, 0, 0), 15)
    size = image_text.get_size()
    coordinates = (107, 85-size[1]/2)
    return [image_text, coordinates]


# Writes the user's collected Parts number in the Game Menu.Changes the letter size in order to fit into the given space
def writable_parts_number(number):
    image_text = create_sized_text(170, 65, str(number), (255, 255, 0))
    size = image_text.get_size()
    coordinates = (132, 226-size[1]/2)
    return [image_text, coordinates]


# converts the written text in the Add Text Menu, to images.Changes the letter size in order to fit into the given space
def convert_text_to_images(text, real_application=False):
    text = text.strip().split(" ")
    lines, line, length = [], "", 0
    for word in text:  # create lines with the text requirements
        if length + len(word) < 49:
            length += len(word)+1
            line += " "+word
        else:
            lines.append(line)
            line = ""+word
            length = 0+len(word)
    if line != "":
        lines.append(line)
    lines[0] = lines[0][1:]  # to remove the additional space (" ") at the beginning
    if real_application:
        text_font = pygame.font.SysFont("Arial", 23)
    else:
        text_font = pygame.font.SysFont("Arial", 19)
        text_font.set_bold(True)
    images = [text_font.render(lin, True, (0, 0, 0)).convert_alpha() for lin in lines]
    return lines, images


# returns the number of the last existing text
def get_last_text_number():
    texts = get_text_names()
    last_text_name = texts[-1].split(".")[0]
    return int(last_text_name)


# cleans the background of the screen in order for it to take images correctly
def clean_background(screen):
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))
    screen.blit(background, (0, 0))


# erases the data inside the file: "active user data.txt" when the user logs out or exits the game
def erase_active_user_data():
    file = open("saves/active_user.txt", "w")
    file.close()


# deletes the folder that has the data of the users that is requesting it to be deleted
def delete_user_account(user_name):
    rmtree(f'saves/{user_name}')


# assembles text with user name on a background
def user_name_button_image(background, background_size, text):
    image = pygame.Surface(background_size)
    image.blit(background, (0, 0))
    image.blit(text, (10, 0))
    return image


# creates buttons images for the "Choose Account" menu. For both cases when the button is on and of
def get_users_images():
    users = list_users()
    user_images_active, user_images_passive = [], []
    text_active, text_passive = None, None
    pygame.font.init()
    active_background = load_image("menu/buttons/6/1.png")
    passive_background = load_image("menu/buttons/6/2.png")
    background_size = passive_background.get_size()
    for user in users:
        for text_size in range(40)[::-1]:
            text_font = pygame.font.SysFont('Times New Roman', text_size)
            text_active = text_font.render(user, True, (0, 0, 0))
            text_passive = text_font.render(user, True, (255, 255, 255))
            size = text_active.get_size()
            if size[0] <= 410:
                break
        active = user_name_button_image(active_background, background_size, text_active)  # create active user image
        passive = user_name_button_image(passive_background, background_size, text_passive)  # create passive user image
        user_images_active.append(active)
        user_images_passive.append(passive)
    return user_images_active, user_images_passive


# gets the requirement values in order to verify if user has leveled up from the parameters file and returns them
def get_requirements():
    with open("saves/active_user.txt", "r") as f:
        str_level = f.readline().split(" ")[3]
    user_level = int(str_level)
    with open(f"parameters/levels info/{user_level}.txt", "r") as f:
        values = f.readline().split(" ")
    return int(values[0]), int(values[1])


# updates the data in the next_level.txt file
def save_next_level_data(user_name, m_ai_data, winner_data):
    with open(f"saves/{user_name}/next_level.txt", "w") as file:
        file.write(f"{m_ai_data} \n{winner_data}")


# returns current user's information
def get_user_data():
    # active user format: "Name speed best_time level parts password volume1 volume2"
    with open("saves/active_user.txt", "r") as file:
        values_p = file.readline().split(" ")
    str_val = [values_p[0], values_p[5]]
    int_val = [int(value) for value in values_p if value.isdigit()]
    return str_val, int_val


# saves current user's new information
def save_user_data(name, b_speed, b_time, level, parts, password, volume1, volume2):
    line = f"{name} {b_speed} {b_time} {level} {parts} {password} {volume1} {volume2}"
    with open("saves/active_user.txt", "w") as file:
        file.write(line)

    line = f"{b_speed} {b_time} {level} {parts} {password} {volume1} {volume2}"
    with open(f"saves/{name}/data.txt", "w") as file:
        file.write(line)


# updates user information after a played match is over, for Mission AI
def save_performance_ai(go_to_next_level, parts, speed):
    str_val, int_val = get_user_data()
    if go_to_next_level:  # change user data in case he levels up
        if get_user_level() < 13:  # level 13 is the highest in the game
            int_val[2] +=1
            save_next_level_data(str_val[0], 0, 0)
        else:
            save_next_level_data(str_val[0], 0, 1)
    int_val[3] += parts
    if int_val[3] < 0:
        int_val[3] = 0
    if int_val[0] < speed:
        int_val[0] = int(speed)
    save_user_data(str_val[0], int_val[0], int_val[1], int_val[2], int_val[3], str_val[1], int_val[5], int_val[6])


# updates user information after a played match is over, for Mission Parts
def save_performance_parts(parts, speed, time):
    str_val, int_val = get_user_data()
    int_val[3] += parts
    if int_val[3] < 0:
        int_val[3] = 0
    if int_val[0] < speed:
        int_val[0] = int(speed)
    if int_val[1] < time:
        int_val[1] = int(time)
    # name best-speed best-time level parts password music-volume sound-volume
    save_user_data(str_val[0], int_val[0], int_val[1], int_val[2], int_val[3], str_val[1], int_val[5], int_val[6])


# returns the current user's level
def get_user_level():
    with open("saves/active_user.txt", "r") as file:
        user_level = int(file.readline().split(" ")[3])
    return user_level


# returns True if the user has already won the game before, and False in the opposite case
def user_is_a_winner():
    with open("saves/active_user.txt", "r") as file:
        user_name = file.readline().split(" ")[0]
    with open(f"saves/{user_name}/next_level.txt", "r") as file:
        file.readline()  # ignore the first line
        is_a_winner = int(file.readline())
    return is_a_winner


# ------------------------------------ HUD FUNCTIONS -------------------------------------------------------------------
# This section contains functions designed for the proper functioning of the game's HUD interface.
# the job and description of a function can be understood by his name. the last two words of every functions refer to
# what they are responsible for displaying on the game screen

def write_HUD_parts_value(screen, number_parts):
    text = str(number_parts)
    adjust = len(text)*7
    text_image = create_sized_text(165, 25, text, (0, 0, 0), 7)
    screen.blit(text_image, (540-adjust, 600))


def write_HUD_time_value(screen, time_value):
    if time_value == "i":
        screen.blit(load_image("HUD/infinite.png"), (529, 665))
    else:
        text = str(time_value)
        adjust = len(text)*4
        text_image = create_sized_text(100, 16, text, (0, 0, 0), 7)
        screen.blit(text_image, (540-adjust, 670))


def display_HUD_speed_meter(screen, speed):
    text = str(int(speed))
    image_number = int(speed/6.7)
    if image_number > 14:
        image_number = 14
    if image_number < 0:
        image_number = 0
    adjust = len(text)*7
    text_image = create_sized_text(100, 20, text, (0, 0, 0), 7)
    screen.blit(load_image(f"HUD/meter/{image_number}.png"), (20, 420))
    screen.blit(text_image, (148-adjust, 596))


def display_HUD_precision_meter(screen, precision):
    text = str(int(precision))
    image_number = int(precision/6.7)
    if precision > 100:
        image_number = 14
    elif precision < 0:
        image_number = 0
    adjust = len(text)*7
    text_image = create_sized_text(100, 20, text, (0, 0, 0), 7)
    screen.blit(load_image(f"HUD/meter/{image_number}.png"), (811, 420))
    screen.blit(text_image, (940-adjust, 596))


def display_HUD_energy_bar(screen, energy_level):
    image_number = int(energy_level/3.333)
    if image_number > 30:
        image_number = 30
    elif image_number < 0:
        image_number = 0
    screen.blit(load_image(f"HUD/barr/{image_number}.png"), (296, 640))


def display_HUD_resistance_bar(screen, resistance_level):
    image_number = int(resistance_level/3.333)
    if image_number > 30:
        image_number = 30
    elif image_number < 0:
        image_number = 0
    screen.blit(load_image(f"HUD/barr/{image_number}.png"), (605, 640))


# turns a typed line into an image
def get_text_images(line):
    text_font = pygame.font.SysFont('Arial', 22)
    return text_font.render(" ".join(line).strip(), True, (0, 0, 0)).convert_alpha()


# creates a new text's image. those that will be chosen and displayed during a match
def modify_color(color: tuple):
    new_color = []
    for i in range(3):
        while True:
            new_tone = color[i]+randint(0, 50)*choice([-1, 1])
            if 0 <= new_tone < 256:
                break
        new_color.append(new_tone)
    return tuple(new_color)


# modifies a specific color turning it slightly different from the original
def create_firework_colors(color_number):
    base_colors = [(255, 0, 0), (34, 177, 76), (0, 0, 255), (0, 255, 0), (255, 255, 0), (0, 255, 255), (255, 0, 255),
                   (255, 90, 0), (130, 0, 255)]
    return [modify_color(choice(base_colors)) for _ in range(color_number)]


# creates a sample of colors, which are slightly modifications of pre-existing colors
def calculate_rs_rhomb(x, y, radius):
    if random() > 0.5:
        additional = randint(0, int(radius)) * choice([-1, 1])
        r_x = x + additional
        max_y_size = int(radius-abs(additional))
        r_y = y + randint(0, max_y_size) * choice([-1, 1])
    else:
        additional = randint(0, int(radius)) * choice([-1, 1])
        r_y = y + additional
        max_x_size = int(radius-abs(additional))
        r_x = x + randint(0, max_x_size) * choice([-1, 1])
    return r_x, r_y


# returns x and y values for a rhomb like firework
def calculate_rs_square(x, y, radius):
    r_x = x + randint(0, int(radius-radius*0.3)) * choice([-1, 1])
    r_y = y + randint(0, int(radius-radius*0.3)) * choice([-1, 1])
    return r_x, r_y


def save_text_image(name):
    screen2 = pygame.display.set_mode((519, 135))
    background = load_image("texts/text_background.png")
    with open(f"texts/{name}.txt", "r") as file:
        lines = file.readlines()
    text_font = pygame.font.SysFont('Times New Roman', 20)
    text_font.set_bold(True)
    coordinates = ((12, 6), (12, 22), (12, 38), (12, 53), (12, 68), (12, 83), (12, 98))
    texts = [text_font.render(lines[i][:-1], True, (0, 0, 0)) for i in range(7)]
    screen2.blit(background, (0, 0))
    [screen2.blit(texts[i], coordinates[i]) for i in range(7)]
    pygame.display.update()
    pygame.image.save(screen2, f"images/texts/{name}.png")
# returns x and y values for a squared like firework


def calculate_rs_circle(x, y, radius):
    # condition for a point to be inside a circle: (x - center_x)**2 + (y - center_y)**2 < radius**2
    if random() > 0.5:
        r_x = x + randint(0, int(radius))*choice([-1, 1])
        r_y = y + randint(0, int(abs(((r_x-x)**2 - radius**2)**(1/2)))) * choice([-1, 1])
    else:
        r_y = y + randint(0, int(radius))*choice([-1, 1])
        r_x = x + randint(0, int(abs(((r_y-y)**2 - radius**2)**(1/2)))) * choice([-1, 1])
    return r_x, r_y
# returns x and y values for a circle like firework
