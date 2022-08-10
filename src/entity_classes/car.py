import pygame
import src.auxiliary_modules.entities_behaviour as eb
import src.auxiliary_modules.global_variables as gv
import src.auxiliary_modules.graphics as grp
from src.auxiliary_modules import audio
from src.auxiliary_modules import files
from .sounds import fire_sound, hit_sound, part_sound


class Car:
    def __init__(self):
        self.y_values = [20, 121, 240]
        self.middle = (self.y_values[1]-1, self.y_values[1], self.y_values[1]-1)  # +-1 error when checking if centered
        self.image = self.get_car_image()
        self.fire_image = None
        self.fire_image_time = 0
        self.last_fire = False
        self.speed = gv.CAR_MAX_SPEED
        self.direction = "STOP"
        self.x = gv.CAR_MAX_DISTANCE-20
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
            audio.play(fire_sound)
            self.fire_image = grp.load_image("cars/car effects/nitro/blue.png")
        else:
            self.fire_image = grp.load_image("cars/car effects/nitro/red.png")

    @staticmethod
    def get_car_image():
        try:
            level = files.read_file_content("saves/active_user.txt", 1)[0].split(" ")[3]
        except IndexError:
            level = 21
        return grp.load_image(f"cars/{level}.png")

    def obstacle_collision(self, l_obstacles):
        for obst in l_obstacles:
            if self.hit_box.overlap(obst.hit_box, (self.x - obst.x + obst.adjust, self.y - obst.y + obst.adjust)):
                audio.play(hit_sound)
                return True
        return False

    def vision(self, screen):
        self.seen_values = []
        for i in self.vision_coo:
            self.seen_values.append(eb.see(screen, i))

    def parts_collision(self, l_parts):
        value = 0
        new_parts = []
        for part in l_parts:
            if part.x + 44 >= self.rect[0] and part.x <= self.rect[0] + self.rect[2]:
                if part.y + 24 >= self.rect[1] and part.y <= self.rect[1] + self.rect[3]:
                    value += part.value
                    audio.play(part_sound)
                    continue
                else:
                    new_parts.append(part)
            else:
                new_parts.append(part)
        return new_parts, value

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        if self.fire_image_time and self.x < gv.CAR_MAX_DISTANCE:
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
