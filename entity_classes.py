# This module contains all the classes that are used in the game classes in order to make the game work.
# Everything that needs to appear in the game is an instance of these classes.
# for those entities that need to appear multiple times, can be of different kinds or comes and goes from the screen,
# there is a class that represents a group of these instances, and can be differentiated from the normal classes by
# looking if his name is plural

# ---------------------------------------------------- IMPORTS ---------------------------------------------------------
import pygame
import Auxiliary_Functionalities as Af

# ---------------------------------------------------- SOUNDS ----------------------------------------------------------
fire_sound = Af.load_sound("game/level failed.WAV")
part_sound = Af.load_sound("game/part_collection.WAV")
hit_sound = Af.load_sound("game/impact.WAV")

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
        self.x = 420
        self.y = self.y_values[1]
        self.damage_period = 0.0
        self.hit_box = pygame.mask.from_surface(self.image)
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
            Af.play(fire_sound)
            self.fire_image = Af.load_image("cars/car effects/nitro/blue.png")
        else:
            self.fire_image = Af.load_image("cars/car effects/nitro/red.png")

    @staticmethod
    def get_car_image():
        try:
            with open("saves/active_user.txt", "r") as file:
                level = file.readline().split(" ")[3]
        except IndexError:
            level = 21
        return Af.load_image(f"cars/{level}.png")

    def obstacle_collision(self, l_obstacles):
        for obst in l_obstacles:
            if self.hit_box.overlap(obst.hit_box, (self.x - obst.x + obst.adjust, self.y - obst.y + obst.adjust)):
                Af.play(hit_sound)
                return True
        return False

    def vision(self, screen):
        self.seen_values = []
        for i in self.vision_coo:
            self.seen_values.append(Af.see(screen, i))

    def parts_collision(self, l_parts):
        value = 0
        new_parts = []
        for part in l_parts:
            if part.x + 44 >= self.rect[0] and part.x <= self.rect[0] + self.rect[2]:
                if part.y + 24 >= self.rect[1] and part.y <= self.rect[1] + self.rect[3]:
                    value += part.value
                    Af.play(part_sound)
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


# -----------------------------------------------    LIGHTNING    ------------------------------------------------------
class Lightning:
    internal_beam_color = (255, 255, 0)  # (0, 255, 255)
    external_beam_color = (0, 0, 255)
    starting_point_coo = (95, 150)
    frame = 0
    segments_coo = ()

    def __init__(self):
        self.segment_number = None  # how many segments the lightning has
        self.internal_beam_radius = None  # radius of the central part of the beam
        self.external_beam_radius = None  # radius of the external part of the beam
        self.last_segment_direction = None  # last segment goes up or down alternatively
        self.change_properties()  # gives new valid values to the attributes

    def change_properties(self):
        self.segment_number = Af.randint(5, 7)
        self.internal_beam_radius = Af.randint(5, 10)
        self.external_beam_radius = Af.randint(15, 25)
        self.frame = 0
        self.segments_coo = [self.starting_point_coo]
        self.last_segment_direction = Af.choice([-1, 1])

    def get_segment_angle(self, hypotenuse, car_y):
        opposite = self.starting_point_coo[1] - car_y
        base_angle = Af.arc_sin(opposite/hypotenuse)
        segment_angle = base_angle+Af.randint(-int(60-base_angle), int(60-base_angle))
        print(f"Frame: {self.frame} | Opposite: {opposite} | Base angle: {base_angle} | Segment_angle: {segment_angle}")
        return segment_angle

    def add_segment(self, car_x, car_y):
        if self.frame == self.segment_number:  # last segment is always the car's position
            self.segments_coo.append((car_x, car_y))
            return None
        medium_segment_length = (car_x - self.segments_coo[0][0])//self.segment_number  # (Xf-Xi)/ n
        segment_x = self.segments_coo[-1][0] + Af.randint(int(medium_segment_length*0.75), medium_segment_length)
        segment_y = self.segments_coo[-1][1] + Af.randint(10, 70)*self.last_segment_direction
        self.last_segment_direction *= -1  # invert next segment direction
        self.segments_coo.append((segment_x, segment_y))

    def draw_segments(self, screen):
        starting_point = self.starting_point_coo
        for ending_point in self.segments_coo:
            pygame.draw.line(screen, self.internal_beam_color, starting_point, ending_point, 4)
            starting_point = ending_point

    def draw(self, screen, car_x, car_y):
        car_y += 25  # adjust y coordinate to match car center
        if car_x > Af.CAR_STE_MIN_DAMAGE_DISTANCE:  # lightning should not hit car if car is too far
            car_x = Af.CAR_STE_MIN_DAMAGE_DISTANCE
        self.frame += 1

        self.add_segment(car_x, car_y)  # create a new segment of the lightning
        
        self.draw_segments(screen)

        if self.frame == self.segment_number:  # lightning has been fully drawn
            self.change_properties()
            return False
        return True


# ----------------------------------------------- SPACE-TIME ENTITY ----------------------------------------------------
class Space_Time_Entity:
    def __init__(self):
        self.images = [Af.load_image(f"Characters/Space-Time Entity/{i + 1}.png") for i in range(6)]
        self.draw_lightning = False
        self.lightning = Lightning()
        self.index = 0

    def take_action(self, car_x):
        if car_x <= Af.CAR_STE_MIN_DAMAGE_DISTANCE:
            self.draw_lightning = True

    def draw(self, screen, car_x, car_y):
        self.index = (self.index + 0.5) % 5
        screen.blit(self.images[int(self.index)], (0, 0))
        if self.draw_lightning:
            self.draw_lightning = self.lightning.draw(screen, car_x, car_y)


# ---------------------------------------------------- ROAD ------------------------------------------------------------
class Road:
    def __init__(self):
        self.current_frame = 0
        self.images_road = [Af.load_image(f"estrada/frame{frame + 1}.png") for frame in range(19)]
        self.frames = len(self.images_road)

    def draw(self, screen):
        screen.blit(self.images_road[self.current_frame], self.images_road[self.current_frame].get_rect())
        self.current_frame = (self.current_frame + 1) % self.frames


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
        self.folder = str(Af.randint(1, 4))
        if self.folder == "4":
            self.image = Af.load_image(f"obstacles/4/{Af.randint(1, 11)}.png")
        else:
            self.image = Af.load_image(f"obstacles/{self.folder}/1.png")
        self.hit_box = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

    def calculate_position_y(self, ultimo_y):
        if ultimo_y == 0:
            return Af.choice([20, 130, 240]) + self.adjust
        possibilities = {20: [130, 240], 130: [20, 240], 240: [130, 20]}
        return Af.choice(possibilities[ultimo_y - self.adjust]) + self.adjust

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def mover(self):
        init_m, nxt = 650, 20
        change = {init_m: f"/obstacles/{self.folder}/2.png",
                  init_m - nxt: f"/obstacles/{self.folder}/3.png",
                  init_m - nxt * 2: f"/obstacles/{self.folder}/4.png",
                  init_m - nxt * 3: f"/obstacles/{self.folder}/5.png",
                  init_m - nxt * 4: f"/obstacles/{self.folder}/6.png",
                  init_m - nxt * 5: f"/obstacles/{self.folder}/7.png"
                  }
        self.x -= 10
        if self.x in change and self.folder != "4":
            self.image = Af.load_image(change[self.x])


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
        self.image = Af.load_image(f"parts/part{self.type_p}.png")
        self.hit_box = pygame.mask.from_surface(self.image)
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
        self.y = Af.choice(self.choices)
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
        dist_between_blocs = Af.randint(self.min_dist_between_blocs, self.max_dist_between_blocs)
        type_p = self.calculate_type_part()
        if self.first_parts:
            for i in range(Af.randint(self.min_parts, self.max_parts)):
                self.internal_list.append(
                    _part(space_between_obstacles[-1] + dist_between_blocs + i * self.dist_between_parts, type_p,
                          self.y, i % 10))
            self.first_parts = False
            return 0
        if self.control_last():
            for i in range(Af.randint(self.min_parts, self.max_parts)):
                self.internal_list.append(
                    _part(space_between_obstacles[-1] + dist_between_blocs + i * self.dist_between_parts,
                          type_p, self.y, i % 10))
            self.y = Af.choice(self.choices)
            return 0

    @staticmethod
    def calculate_type_part():
        probability = Af.random()
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
        self.speed_meter_image = Af.load_image("HUD/meter/7.png")
        self.precision_meter_image = Af.load_image("HUD/meter/7.png")
        self.background = Af.load_image("HUD/HUD_background.png")
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
        Af.write_HUD_parts_value(self.screen, number_parts)
        Af.write_HUD_time_value(self.screen, time)
        Af.display_HUD_speed_meter(self.screen, speed)
        Af.display_HUD_precision_meter(self.screen, precision)
        Af.display_HUD_energy_bar(self.screen, energy)
        Af.display_HUD_resistance_bar(self.screen, resistance)
