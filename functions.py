# This module contains functions that are used by all the others modules
# -------------------------------------------- IMPORTS -----------------------------------------------------------------
import pygame
from os import walk, mkdir
from sys import platform as system_name
from shutil import rmtree
from gc import collect
from random import choice as random_choice, randint as random_randint, random as random_random
from math import tanh


# ---------------------------------------- GLOBAL VARIABLES ------------------------------------------------------------
pygame.mixer.init()

root_directory = "saves/"
cores_obst = [[196, 15, 23], [239, 10, 9], [191, 15, 23], [245, 71, 20], [252, 130, 18], [255, 17, 11], [255, 18, 11],
              [255, 18, 12], [195, 195, 195], [163, 73, 164], [248, 12, 35], [255, 255, 255]]
cores_part = [[255, 128, 0], [255, 242, 0], [34, 177, 76], [252, 130, 19], [237, 28, 36], [163, 73, 164], [255, 0, 255],
              [120, 0, 120], [0, 255, 255], [0, 0, 255]]
cores_estrada = [[0, 0, 0], [108, 108, 108]]
code_meaning = {3: "unknown", 1: "road", 2: "parts", 0: "lava"}
# AI variables achieved by a genetic algorithm that can be found in the genetic_algorithm module
weights = [-0.024636661554064646, 0.9490338548623168, 0.9490338548623168, 0.17090764398454833, 1.0661495372951384]
bias = [0.2670813587084078, -0.6691533200275781, -0.5723370239650385, 0.25406116993577665, -0.486196069971221]


# ------------------------------------- REIMPLEMENTED FUNCTIONS --------------------------------------------------------
# These functions are just a reimplementation of existing python packages. They are useful because other modules of this
# game don't need to import the module random or time (etc.), just this module functions.

def choice(list_r):
    return random_choice(list_r)


def randint(first_number, last_number):
    return random_randint(first_number, last_number)


def random():
    return random_random()


def wait(seconds):
    pygame.time.wait(seconds*1000)


def os_name():
    return system_name


# uses the pygame module to load a sound to memory and returns it
def load_sound(location):
    return pygame.mixer.Sound(f"sounds/{location}")


# plays a sound passed as argument
def play(sound: pygame.mixer.Sound):
    volume = get_sound_volume()
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
    cor = list(screen.get_at((x, y)))
    cor2 = cor[:-1]
    if cor2 in cores_estrada:
        current_code = 1
    elif cor2 in cores_part:
        current_code = 2
    else:
        current_code = 0
    # sign = code_meaning[current_code] -> turns rgb values into words
    # print(sign)
    return current_code


# Given all seen values, gives back a code value for what to do
def make_a_choice(info):
    soma = sum([weights[i] * info[i] + bias[i] for i in range(len(info))])
    refined_value = tanh(soma)
    if refined_value >= 0.70:
        return 1
    elif refined_value <= -0.70:
        return -1
    else:
        return 0


def prep_cores():
    file = open("parameters/colors.txt", "r")
    lines = file.readlines()
    lines = sorted(lines)
    f = open("parameters/cores.txt", "a")
    [f.write(f"{line}") for line in lines]
    file.close()
    f.close()


# -------------------------------------------- MENU FUNCTIONS ----------------------------------------------------------
def get_sound_volume():
    file = open("saves/active_user.txt", "r")
    line = file.readline().split(" ")
    file.close()
    if len(line) != 1:
        return float(line[7])/10
    else:
        return 1.0


def get_music_volume():
    file = open("saves/active_user.txt", "r")
    line = file.readline().split(" ")
    file.close()
    if len(line) != 1:
        return float(line[6])/20.0
    else:
        return 0.5


def show_error_message(screen, code):
    play(error_sound)
    screen.blit(pygame.image.load(f"images/menu/messages/error{code}.png"), (230, 200))
    pygame.display.update()
    wait(3)


def show_success_message(screen, code) -> None:
    play(success_sound)
    screen.blit(pygame.image.load(f"images/menu/messages/success{code}.png"), (230, 200))
    pygame.display.update()
    wait(3)


def create_folder(nome_user):
    mkdir(root_directory+nome_user)


# returns a list with all the usernames currently existing, but only on windows, linux and Mac OS
def list_users():
    return list(walk("saves"))[0][1]


# returns a list with all the names of the texts that the user will type in the matches
def get_text_names():
    texts = walk("texts")
    texts = [text for text in texts][0][1:][1]
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
    return rendered_text


# writes the name and password typed by a user in the Create User Menu
def write_name_password(screen, name, password, active, hide):
    coordinates1 = [(330, 205), (330, 351)]
    pygame.draw.rect(screen, (0, 0, 255), (coordinates1[active], (422, 57)), 8)
    screen.blit(pygame.image.load("images/menu/interfaces/navigation/pointer.png"), (coordinates1[active][0]+450,
                                                                                     coordinates1[active][1]))
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
    password_text = text_font.render(password, True, (0, 0, 0))
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
def convert_text_to_images(text):
    text = text.strip().split(" ")
    lines, line, length = [], "", 0
    for word in text:
        if length + len(word) < 49:
            length+=len(word)+1
            line += " "+word
        else:
            lines.append(line)
            line = ""+word
            length = 0+len(word)  # create lines with the text requirements
    if line != "":
        lines.append(line)
    text_font = pygame.font.SysFont('Arial Rounded MT Bold', 20)
    text_font.set_bold(True)
    images = [text_font.render(lin, True, (0, 0, 0)) for lin in lines]
    return images


# returns the number of the last existing text
def get_last_text_number():
    texts = get_text_names()
    last_text_name = texts[-1].split(".")[0]
    return int(last_text_name)


def clean_background(screen):
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))
    screen.blit(background, (0, 0))


def erase_active_user_data():
    file = open("saves/active_user.txt", "w")
    file.close()


def delete_user_account(user_name):
    rmtree(f'saves/{user_name}')


def get_users_images():
    collect()
    users = list_users()
    user_images_active = []
    user_images_passive = []
    image_text1, image_text2 = None, None
    pygame.font.init()
    for user in users:
        for s in range(40)[::-1]:
            text_font = pygame.font.SysFont('Times New Roman', s)
            image_text1 = text_font.render(user, True, (0, 0, 0))
            image_text2 = text_font.render(user, True, (255, 255, 255))
            size = image_text1.get_size()
            if size[0] <= 410:
                break
        user_images_active.append(image_text1)
        user_images_passive.append(image_text2)
    return user_images_active, user_images_passive


def get_requirements():
    user_level = int(open("saves/active_user.txt", "r").readline().split(" ")[3])
    values = open(f"parameters/levels info/{user_level}.txt", "r").readline().split(" ")
    return int(values[0]), int(values[1])


# updates user information after a played match is over, for Mission AI
def save_performance_ai(go_to_next_level, parts, speed):
    # active user format: "Name speed best_time level parts password volume1 volume2"
    file = open("saves/active_user.txt", "r")
    values_p = file.readline().split(" ")
    file.close()
    str_val = [values_p[0], values_p[5]]
    int_val = [int(value) for value in values_p if value.isdigit()]
    if go_to_next_level:
        int_val[2] +=1
    int_val[3] += parts
    if int_val[3] < 0:
        int_val[3] = 0
    if int_val[0] < speed:
        int_val[0] = int(speed)
    line = f"{str_val[0]} {int_val[0]} {int_val[1]} {int_val[2]} {int_val[3]} {str_val[1]} {int_val[4]} {int_val[5]}"
    file = open("saves/active_user.txt", "w")
    file.write(line)
    file.close()
    file = open(f"saves/{str_val[0]}/data.txt", "w")
    line = f"{int_val[0]} {int_val[1]} {int_val[2]} {int_val[3]} {str_val[1]} {int_val[4]} {int_val[5]}"
    file.write(line)
    file.close()


# updates user information after a played match is over, for Mission Parts
def save_performance_parts(parts, speed, time):
    # active user format: "Name speed best_time level parts password volume1 volume2"
    file = open("saves/active_user.txt", "r")
    values_p = file.readline().split(" ")
    file.close()
    str_val = [values_p[0], values_p[5]]
    int_val = [int(value) for value in values_p if value.isdigit()]
    int_val[3] += parts
    if int_val[3] < 0:
        int_val[3] = 0
    if int_val[0] < speed:
        int_val[0] = int(speed)
    if int_val[1] < time:
        int_val[1] = int(time)
    line = f"{str_val[0]} {int_val[0]} {int_val[1]} {int_val[2]} {int_val[3]} {str_val[1]} {int_val[4]} {int_val[5]}"
    file = open("saves/active_user.txt", "w")
    file.write(line)
    file.close()
    file = open(f"saves/{str_val[0]}/data.txt", "w")
    line = f"{int_val[0]} {int_val[1]} {int_val[2]} {int_val[3]} {str_val[1]} {int_val[4]} {int_val[5]}"
    file.write(line)
    file.close()


# --------------------------------------------- HUD FUNCTIONS ----------------------------------------------------------
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
        screen.blit(pygame.image.load("images/HUD/infinite.png"), (529, 665))
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
    screen.blit(pygame.image.load(f"images/HUD/meter/{image_number}.png"), (20, 420))
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
    screen.blit(pygame.image.load(f"images/HUD/meter/{image_number}.png"), (811, 420))
    screen.blit(text_image, (940-adjust, 596))


def display_HUD_energy_bar(screen, energy_level):
    image_number = int(energy_level/3.333)
    if image_number > 30:
        image_number = 30
    elif image_number < 0:
        image_number = 0
    screen.blit(pygame.image.load(f"images/HUD/barr/{image_number}.png"), (296, 640))


def display_HUD_resistance_bar(screen, resistance_level):
    image_number = int(resistance_level/3.333)
    if image_number > 30:
        image_number = 30
    elif image_number < 0:
        image_number = 0
    screen.blit(pygame.image.load(f"images/HUD/barr/{image_number}.png"), (605, 640))


# turns a typed line into an image
def get_text_images(line):
    text_font = pygame.font.SysFont('Times New Roman', 20)
    text_font.set_bold(True)
    return text_font.render(" ".join(line).strip(), True, (0, 0, 0))


# creates a new text's image. those that will be chosen and displayed during a match
def save_text_image(name):
    screen2 = pygame.display.set_mode((519, 135))
    background = pygame.image.load("images/texts/text_background.png")
    file = open(f"texts/{name}.txt", "r")
    lines = file.readlines()
    file.close()
    text_font = pygame.font.SysFont('Times New Roman', 20)
    text_font.set_bold(True)
    coordinates = ((10, 7), (10, 24), (10, 39), (10, 54), (10, 69), (10, 84), (10, 99))
    texts = [text_font.render(lines[i][:-1], True, (0, 0, 0)) for i in range(7)]
    screen2.blit(background, (0, 0))
    [screen2.blit(texts[i], coordinates[i]) for i in range(7)]
    pygame.display.update()
    pygame.image.save(screen2, f"images/texts/{name}.png")
