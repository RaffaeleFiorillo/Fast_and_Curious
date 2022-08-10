from pygame import Surface
from .user_data_management import *
from .files import *
from .useful_functions import *
import pygame


# returns an image ready to be displayed on the screen. "convert_alpha" makes it much faster to display
def load_image(directory: str) -> Surface:
    try:
        return pygame.image.load(f"assets/images/{directory}").convert_alpha()
    except FileNotFoundError:
        exit(f"Error: Directory *{directory}* Not Found")


# return a text image that fits into a set size, with some customizations (like color and font size)
def create_sized_text(max_size_image: int, max_size_letter: int, text: str,
                      color: (int, int, int), min_size_letter=30) -> Surface:
    pygame.font.init()
    rendered_text = None
    for i in range(min_size_letter, max_size_letter)[::-1]:
        text_font = pygame.font.SysFont('Times New Roman', i)
        text_font.set_bold(True)
        rendered_text = text_font.render(text, True, color)
        if rendered_text.get_size()[0] <= max_size_image:
            break
    return rendered_text.convert_alpha()


# writes the name and password typed by a User in the Create User Menu
def write_name_password(screen: Surface, name: [str], password: [str], active: int, hide: bool) -> None:
    coordinates1 = [(330, 205), (330, 351)]
    pygame.draw.rect(screen, (0, 0, 255), (coordinates1[active], (422, 57)), 8)
    screen.blit(load_image("menu/interfaces/navigation/pointer.png"),
                (coordinates1[active][0] + 450, coordinates1[active][1]))
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


# Writes the password typed by a User when Insert Password Menu appears (hides it with "*" if the hide variable is True)
def write_password(screen: Surface, password: [str], hide: bool) -> None:
    pygame.font.init()
    if hide:
        password = "".join(["*" for letter in password if str(letter).isalnum()])
    else:
        password = "".join(password)
    text_font = pygame.font.SysFont('Times New Roman', 32)
    text_font.set_bold(True)
    password_text = text_font.render(password, True, (0, 0, 0)).convert_alpha()
    screen.blit(password_text, (290, 330))


# Writes the username into the Welcome interface. Changes the letter size in order to fit into the given space
def write_name(screen: Surface, name: str) -> None:
    name_text_image = create_sized_text(540, 50, name, (0, 255, 0))
    screen.blit(name_text_image, ((screen.get_width() - name_text_image.get_size()[0]) // 2 + 7, 330))


# Writes the User's "best time" value in the Game Menu. Changes the letter size in order to fit into the given space
def writable_best_time(best_time: int) -> [Surface, (int, int)]:
    pygame.font.init()
    coordinates = (135, 357)
    text_font = pygame.font.SysFont('Times New Roman', 19)
    text = ["  " for _ in range(10 - len(str(best_time)))]
    new_text = "".join(text) + str(best_time)
    image_text = text_font.render(new_text, True, (255, 255, 255))
    return [image_text, coordinates]


# Writes the User's "best speed" value in the Game Menu. Changes the letter size in order to fit into the given space
def writable_best_speed(best_speed: int) -> [Surface, (int, int)]:
    pygame.font.init()
    coordinates = (185, 427)
    text_font = pygame.font.SysFont('Times New Roman', 20)
    text = ["  " for _ in range(4 - len(str(best_speed)))]
    new_text = "".join(text) + str(best_speed)
    image_text = text_font.render(new_text, True, (255, 255, 255))
    return [image_text, coordinates]


# Writes the User's username in the Game Menu. Changes the letter size in order to fit into the given space
def writable_user_name(name: str) -> [Surface, (int, int)]:
    pygame.font.init()
    image_text = create_sized_text(253, 65, name, (0, 0, 0), 15)
    size = image_text.get_size()
    coordinates = (107, 85 - size[1] / 2)
    return [image_text, coordinates]


# Writes the User's collected Parts number in the Game Menu.Changes the letter size in order to fit into the given space
def writable_parts_number(number: int) -> [Surface, (int, int)]:
    image_text = create_sized_text(170, 65, str(number), (255, 255, 0))
    size = image_text.get_size()
    coordinates = (132, 226 - size[1] / 2)
    return [image_text, coordinates]


# converts the written text in the Add Text Menu, to images.Changes the letter size in order to fit into the given space
def convert_text_to_images(text: str, real_application=False) -> ([str], [Surface]):
    text = text.strip().split(" ")
    lines, line, length = [], "", 0
    for word in text:  # create lines with the text requirements
        if length + len(word) < 49:
            length += len(word) + 1
            line += " " + word
        else:
            lines.append(line)
            line = "" + word
            length = 0 + len(word)
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


# cleans the background of the screen in order for it to take images correctly
def clean_background(screen: Surface) -> None:
    background = Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))
    screen.blit(background, (0, 0))


# assembles text with username on a background
def user_name_button_image(background: Surface, background_size: (int, int), text: Surface) -> Surface:
    image = Surface(background_size)
    image.blit(background, (0, 0))
    image.blit(text, (10, 0))
    return image


# creates button images for the "Choose Account" menu. For both cases when the button is on and off
def get_users_images() -> ([Surface], [Surface]):
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
        active = user_name_button_image(active_background, background_size, text_active)  # create active User image
        passive = user_name_button_image(passive_background, background_size, text_passive)  # create passive User image
        user_images_active.append(active)
        user_images_passive.append(passive)
    return user_images_active, user_images_passive


# turns a typed line (text/string) into an image
def get_text_images(line: [str]) -> Surface:
    text_font = pygame.font.SysFont('Arial', 22)
    return text_font.render(" ".join(line).strip(), True, (0, 0, 0)).convert_alpha()


# creates a new text's image (those that will be chosen and displayed during a match) and saves it
def save_text_image(name: str) -> None:
    screen2 = pygame.display.set_mode((519, 135))
    background = load_image("texts/text_background.png")
    lines = read_file_content(f"texts/{name}.txt")
    text_font = pygame.font.SysFont('Times New Roman', 20)
    text_font.set_bold(True)
    coordinates = ((12, 6), (12, 22), (12, 38), (12, 53), (12, 68), (12, 83), (12, 98))
    texts = [text_font.render(lines[i][:-1], True, (0, 0, 0)) for i in range(7)]
    screen2.blit(background, (0, 0))
    [screen2.blit(texts[i], coordinates[i]) for i in range(7)]
    pygame.display.update()
    pygame.image.save(screen2, f"images/texts/{name}.png")


# modifies a specific color turning it slightly different from the original
def modify_color(color: (int, int, int)) -> (int, int, int):
    new_color = []
    for i in range(3):
        while True:
            new_tone = color[i] + randint(0, 50) * choice([-1, 1])
            if 0 <= new_tone < 256:
                break
        new_color.append(new_tone)
    return tuple(new_color)


# creates a sample of colors, which are slightly modifications of pre-existing colors
def create_firework_colors(color_number: int) -> [(int, int, int)]:
    base_colors = [(255, 0, 0), (34, 177, 76), (0, 0, 255), (0, 255, 0), (255, 255, 0), (0, 255, 255), (255, 0, 255),
                   (255, 90, 0), (130, 0, 255)]
    return [modify_color(choice(base_colors)) for _ in range(color_number)]


# returns x and y values for a square like firework
def calculate_rs_rhomb(x: int, y: int, radius: int) -> (int, int):
    if random() > 0.5:
        additional = randint(0, int(radius)) * choice([-1, 1])
        r_x = x + additional
        max_y_size = int(radius - abs(additional))
        r_y = y + randint(0, max_y_size) * choice([-1, 1])
    else:
        additional = randint(0, int(radius)) * choice([-1, 1])
        r_y = y + additional
        max_x_size = int(radius - abs(additional))
        r_x = x + randint(0, max_x_size) * choice([-1, 1])
    return r_x, r_y


# returns x and y values for a square like firework
def calculate_rs_square(x: int, y: int, radius: int) -> (int, int):
    r_x = x + randint(0, int(radius - radius * 0.3)) * choice([-1, 1])
    r_y = y + randint(0, int(radius - radius * 0.3)) * choice([-1, 1])
    return r_x, r_y


# returns x and y values for a circle like firework
def calculate_rs_circle(x: int, y: int, radius: int) -> (int, int):
    # condition for a point to be inside a circle: (x - center_x)**2 + (y - center_y)**2 < radius**2
    if random() > 0.5:
        r_x = x + randint(0, int(radius)) * choice([-1, 1])
        r_y = y + randint(0, int(abs(((r_x - x) ** 2 - radius ** 2) ** (1 / 2)))) * choice([-1, 1])
    else:
        r_y = y + randint(0, int(radius)) * choice([-1, 1])
        r_x = x + randint(0, int(abs(((r_y - y) ** 2 - radius ** 2) ** (1 / 2)))) * choice([-1, 1])
    return r_x, r_y
