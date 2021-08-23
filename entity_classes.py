# This module contains all the classes that are used in the game classes in order to make the game work.
# Everything that needs to appear in the game is an instance of these classes.
# for those entities that need to appear multiple times, can be of different kinds or comes and goes from the screen,
# there is a class that represents a group of these instances, and can be differentiated from the normal classes by
# looking if his name is plural

# ---------------------------------------------------- IMPORTS ---------------------------------------------------------
import pygame
import functions as f

# ---------------------------------------------------- SOUNDS ----------------------------------------------------------
fire_sound = f.load_sound("game/level failed.WAV")
part_sound = f.load_sound("game/part_collection.WAV")
hit_sound = f.load_sound("game/impact.WAV")

# ----------------------------------------------- GLOBAL VARIABLES -----------------------------------------------------
obstacles_distance = 290
parts_distance = 5
space_between_obstacles = [o for o in range(300, 1290, obstacles_distance)]


# ----------------------------------------------------- CAR ------------------------------------------------------------
class Car:
    def __init__(self):
        self.y_values = [20, 121, 240]
        self.middle = (self.y_values[1]-1, self.y_values[1], self.y_values[1]-1)  # +-1 error when checking if centered
        self.image = self.get_car_image()
        self.fire_image = None
        self.fire_image_time = 0
        self.last_fire = False
        self.speed = 10
        self.direction = "STOP"
        self.x = 290
        self.y = self.y_values[1]
        self.damage_period = 0.0
        self.hit_box = pygame.mask.from_surface(self.image.convert_alpha())
        self.rect = (self.x, self.y, self.image.get_size()[0], self.image.get_size()[1])
        self.vision_coo = None
        self.seen_values = []
        self.update_vision_coordinates()

    def update_vision_coordinates(self):
        begin, step = 20, 10
        up = tuple((self.x+begin+step*i, self.y-80) for i in range(22))
        # up_left, up_center_left, up_center_right, up_right, up_right_front, up_front = up

        center = ((self.x+150, self.y+27), (self.x+155+step, self.y+27))

        dwn = tuple((self.x+begin+step*i, self.y+140) for i in range(22))
        # dwn_left, dwn_center_left, dwn_center_right, dwn_right, dwn_right_front, dwn_front= dwn

        self.vision_coo = up+center+dwn

    def activate_fire(self, fire_type):
        if self.last_fire != fire_type:
            self.last_fire = fire_type
            self.fire_image_time = 0
        if self.fire_image_time < 1:
            self.fire_image_time += 1
        if fire_type:
            f.play(fire_sound)
            self.fire_image = pygame.image.load("images/cars/car effects/nitro/blue.png").convert_alpha()
        else:
            self.fire_image = pygame.image.load("images/cars/car effects/nitro/red.png").convert_alpha()

    @staticmethod
    def get_car_image():
        try:
            file = open("saves/active_user.txt", "r")
            level = file.readline().split(" ")[3]
            file.close()
        except IndexError:
            level = 21
        return pygame.image.load(f"images/cars/{level}.png").convert_alpha()

    def obstacle_collision(self, l_obstacles):
        for obst in l_obstacles:
            if self.hit_box.overlap(obst.hit_box, (self.x - obst.x + obst.adjust, self.y - obst.y + obst.adjust)):
                f.play(hit_sound)
                return True
        return False

    def vision(self, screen):
        self.seen_values = []
        for i in self.vision_coo:
            self.seen_values.append(f.see(screen, i))

    def parts_collision(self, l_parts):
        value = 0
        new_parts = []
        for part in l_parts:
            if part.x + 44 >= self.rect[0] and part.x <= self.rect[0] + self.rect[2]:
                if part.y + 24 >= self.rect[1] and part.y <= self.rect[1] + self.rect[3]:
                    value += part.value
                    f.play(part_sound)
                    continue
                else:
                    new_parts.append(part)
            else:
                new_parts.append(part)
        return new_parts, value

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        if self.fire_image_time and self.x < 350:
            screen.blit(self.fire_image, (self.x - 40, self.y + 15))
            self.fire_image_time = 0
        # pygame.draw.rect(screen, (255, 255, 0), self.rect, 5)
        """for i in self.vision_coo:
            pygame.draw.circle(screen, (255, 242, 0), i, 2, 1)"""

    def movement(self, event):
        directions = {None: self.direction, "UP": "UP", "DWN": "DWN"}
        self.direction = directions[event]
        if self.direction == "UP":
            self.y -= self.speed
        elif self.direction == "DWN":
            self.y += self.speed

        if self.y >= self.y_values[2]:
            self.direction = "STOP"
            self.y = self.y_values[2]
        elif self.y <= self.y_values[0]:
            self.direction = "STOP"
            self.y = self.y_values[0]
        elif self.y in self.middle:
            self.direction = "STOP"
            self.y = self.y_values[1]

        self.update_vision_coordinates()  # update the position of the vision coordinates preventing them staying fix
        self.rect = (self.x, self.y, self.image.get_size()[0], self.image.get_size()[1])


# ----------------------------------------------- SPACE-TIME ENTITY ----------------------------------------------------
class Space_Time_Entity:
    def __init__(self):
        self.images = [pygame.image.load(f"images/Characters/Space-Time Entity/{i + 1}.png").convert_alpha()
                       for i in range(6)]
        self.index = 0

    def draw(self, screen):
        self.index += 0.5
        if self.index >= 6:
            self.index = 0
        screen.blit(self.images[int(self.index)], (0, 0))


# ---------------------------------------------------- ROAD ------------------------------------------------------------
class Road:
    def __init__(self):
        self.current_frame = 0
        self.images_road = [pygame.image.load("images/estrada/frame" + str(num + 1) + ".png").convert_alpha()
                            for num in range(19)]
        self.frames = len(self.images_road)

    def draw(self, screen):
        screen.blit(self.images_road[self.current_frame], self.images_road[self.current_frame].get_rect())
        self.current_frame += 1
        if self.current_frame == self.frames:
            self.current_frame = 0


# ------------------------------------------------ SINGLE OBSTACLE -----------------------------------------------------
class _obstacle:
    def __init__(self, location, ultimo_y):
        self.x = location
        self.adjust = -10
        self.y = self.calculate_position_y(ultimo_y)
        self.folder = None
        self.image = None
        self.hit_box = None
        self.rect = None
        self.choose_image()
        self.length = 100

    def choose_image(self):
        self.folder = str(f.randint(1, 4))
        if self.folder == "4":
            self.image = pygame.image.load(f"images/obstacles/4/{f.randint(1, 11)}.png").convert_alpha()
        else:
            self.image = pygame.image.load("images/obstacles/" + self.folder + "/1.png").convert_alpha()
        self.hit_box = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

    def calculate_position_y(self, ultimo_y):
        if ultimo_y == 0:
            return f.choice([20, 130, 240]) + self.adjust
        possibilities = {20: [130, 240], 130: [20, 240], 240: [130, 20]}
        return f.choice(possibilities[ultimo_y - self.adjust]) + self.adjust

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def mover(self):
        init_m, nxt = 650, 20
        change = {init_m: f"images/obstacles/{self.folder}/2.png",
                  init_m - nxt: f"images/obstacles/{self.folder}/3.png",
                  init_m - nxt * 2: f"images/obstacles/{self.folder}/4.png",
                  init_m - nxt * 3: f"images/obstacles/{self.folder}/5.png",
                  init_m - nxt * 4: f"images/obstacles/{self.folder}/6.png",
                  init_m - nxt * 5: f"images/obstacles/{self.folder}/7.png"
                  }
        self.x -= 10
        if self.x in change and self.folder != "4":
            self.image = pygame.image.load(change[self.x])


# ---------------------------------------------- OBSTACLE COLLECTION ---------------------------------------------------
class Obstacles:
    def __init__(self):
        self.internal_list = []
        self.max = len(space_between_obstacles)
        self.first_born = True
        self.ultimo_y = 0

    def control_last(self):
        if self.internal_list[-1].x <= space_between_obstacles[-2]:
            return True
        else:
            return False

    def create_obstacles(self):
        if self.first_born:
            for i in range(self.max):
                self.first_born = False
                ob = _obstacle(space_between_obstacles[i], self.ultimo_y)
                if ob.x >= 700:
                    self.internal_list.append(ob)
        elif self.control_last():
            self.internal_list.append(_obstacle(space_between_obstacles[-1], self.ultimo_y))
        self.ultimo_y = self.internal_list[-1].y

    def remove_obstacles(self):
        for obst in self.internal_list:
            if obst.x < -obst.length:
                self.internal_list.remove(obst)
        if len(self.internal_list) <= self.max:
            self.create_obstacles()

    def draw(self, screen):
        for obst in self.internal_list:
            obst.draw(screen)
            obst.mover()


# -------------------------------------------------- SINGLE PART -------------------------------------------------------
class _part:
    def __init__(self, x, type_p, y, cardinality):
        self.type_p = type_p
        self.adjust = 15
        self.y_middle = y + self.adjust
        self.y = self.y_middle + cardinality
        self.x = x
        self.value = self.type_p ** 2
        self.image = pygame.image.load("images/parts/part" + str(self.type_p) + ".png").convert_alpha()
        self.hit_box = pygame.mask.from_surface(self.image.convert_alpha())
        self.rect = self.image.get_rect()
        self.length = 32
        self.movement_module = 10
        self.upwards = True

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def mover(self):
        alternation = {True: -1, False: 1}
        advancement_y = alternation[self.upwards]
        self.x -= 10
        self.y += advancement_y
        if self.y_middle + self.movement_module * advancement_y == self.y and self.upwards:
            self.upwards = not self.upwards
        elif self.y_middle + self.movement_module * advancement_y == self.y and not self.upwards:
            self.upwards = not self.upwards


# ----------------------------------------------- PARTS COLLECTION -----------------------------------------------------
class parts:
    def __init__(self):
        self.internal_list = []
        self.first_parts = True
        self.choices = [20, 121, 240]
        self.y = f.choice(self.choices)
        self.dist_between_parts = 5 + 44
        self.min_dist_between_blocs = 100
        self.max_dist_between_blocs = 200
        self.min_parts = 3
        self.max_parts = 7

    def control_last(self):
        if self.internal_list[-1].x <= space_between_obstacles[-2]:
            return True
        else:
            return False

    def create_parts(self):
        dist_between_blocs = f.randint(self.min_dist_between_blocs, self.max_dist_between_blocs)
        type_p = self.calculate_type_part()
        if self.first_parts:
            for i in range(f.randint(self.min_parts, self.max_parts)):
                self.internal_list.append(
                    _part(space_between_obstacles[-1] + dist_between_blocs + i * self.dist_between_parts, type_p,
                          self.y, i % 10))
            self.first_parts = False
            return 0
        if self.control_last():
            for i in range(f.randint(self.min_parts, self.max_parts)):
                self.internal_list.append(
                    _part(space_between_obstacles[-1] + dist_between_blocs + i * self.dist_between_parts,
                          type_p, self.y, i % 10))
            self.y = f.choice(self.choices)
            return 0

    @staticmethod
    def calculate_type_part():
        probability = f.random()
        if probability <= 0.3:
            return 1
        elif 0.3 < probability <= 0.55:
            return 2
        elif 0.55 < probability <= 0.75:
            return 3
        elif 0.75 < probability <= 0.9:
            return 4
        else:
            return 5

    def remover_parts(self, internal_list_obst):
        for part, obst in zip(self.internal_list, internal_list_obst):
            if part.x < -part.length:
                self.internal_list.remove(part)

    def draw(self, screen):
        for part in self.internal_list:
            part.draw(screen)
            part.mover()


# ------------------------------------------------ HUD INTERFACE -------------------------------------------------------
class HUD:
    def __init__(self, screen, mode=False):
        self.screen = screen
        self.speed_meter_image = pygame.image.load("images/HUD/meter/7.png").convert_alpha()
        self.precision_meter_image = pygame.image.load("images/HUD/meter/7.png").convert_alpha()
        self.background = pygame.image.load("images/HUD/HUD_background.png").convert_alpha()
        self.speed = 0
        self.precision = 0
        self.energy = 0
        self.resistance = 0
        self.parts = 0
        self.mode = mode
        if mode:
            self.time = "infinite"
        else:
            self.time = 60
        self.set_up_HUD()

    def set_up_HUD(self):
        self.screen.blit(self.background, (0, 308))
        pygame.display.update()

    def draw(self, number_parts, time, speed, precision, energy, resistance):
        f.write_HUD_parts_value(self.screen, number_parts)
        f.write_HUD_time_value(self.screen, time)
        f.display_HUD_speed_meter(self.screen, speed)
        f.display_HUD_precision_meter(self.screen, precision)
        f.display_HUD_energy_bar(self.screen, energy)
        f.display_HUD_resistance_bar(self.screen, resistance)
