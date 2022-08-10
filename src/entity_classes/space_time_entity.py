import pygame
from src.auxiliary_modules import audio, global_variables
from src.auxiliary_modules import graphics as grp
from src.auxiliary_modules import useful_functions as uf


class Lightning:
    internal_beam_color = (0, 255, 255)
    external_beam_color = (0, 0, 255)
    starting_point_coo = (95, 150)
    frame = 0
    space_time_hit_sound = audio.load_sound("game/space_time_hit.WAV")  # sound of the space-time entity hitting
    segments_coo = ()

    def __init__(self):
        self.segment_number = None  # how many segments the lightning has
        self.internal_beam_radius = None  # radius of the central part of the beam
        self.external_beam_radius = None  # radius of the external part of the beam
        self.last_segment_direction = None  # last segment goes up or down alternatively
        self.change_properties()  # gives new valid values to the attributes

    def change_properties(self):
        self.segment_number = uf.randint(5, 7)
        self.internal_beam_radius = 2*self.segment_number
        self.external_beam_radius = uf.get_fibonacci(self.segment_number)
        self.frame = 0
        self.segments_coo = [self.starting_point_coo]
        self.last_segment_direction = uf.choice([-1, 1])

    def add_segment(self, car_x, car_y):
        if self.frame == self.segment_number:  # last segment is always the car's position
            self.segments_coo.append((car_x, car_y))
            return None
        medium_segment_length = (car_x - self.segments_coo[0][0])//self.segment_number  # (Xf-Xi)/ n
        segment_x = self.segments_coo[-1][0] + uf.randint(int(medium_segment_length*0.75), medium_segment_length)
        segment_y = self.segments_coo[-1][1] + uf.randint(10, 70)*self.last_segment_direction
        self.last_segment_direction *= -1  # invert next segment direction
        self.segments_coo.append((segment_x, segment_y))

    def draw_segments(self, screen):
        starting_point = self.starting_point_coo
        for adjust, ending_point in enumerate(self.segments_coo):
            central_segment_width = int(self.internal_beam_radius*(1 - adjust/self.segment_number))+4
            pygame.draw.line(screen, self.internal_beam_color, starting_point, ending_point, central_segment_width)
            pygame.draw.line(screen, (255, 255, 255), starting_point, ending_point, 2)
            external_beam_width = (self.segment_number-adjust)//2+1
            upper_coo_start = (starting_point[0], starting_point[1]-central_segment_width//2)
            upper_coo_ending = (ending_point[0], ending_point[1] - central_segment_width // 2)
            pygame.draw.line(screen, self.external_beam_color, upper_coo_start, upper_coo_ending, external_beam_width)

            lower_coo_start = (starting_point[0], starting_point[1] + central_segment_width//2)
            lower_coo_ending = (ending_point[0], ending_point[1] + central_segment_width // 2)
            pygame.draw.line(screen, self.external_beam_color, lower_coo_start, lower_coo_ending, external_beam_width)

            starting_point = ending_point  # make next segment start where last one ended

    def draw(self, screen, car_x, car_y):
        if self.frame == 0:
            audio.play(self.space_time_hit_sound)
        if car_x > global_variables.CAR_STE_MIN_DAMAGE_DISTANCE:  # lightning should not hit car if car is too far
            car_x = global_variables.CAR_STE_MIN_DAMAGE_DISTANCE

        car_y += 25  # adjust y coordinate to match car center
        car_x += 25  # adjust y coordinate to match car center
        self.frame += 1

        self.add_segment(car_x, car_y)  # create a new segment of the lightning
        self.draw_segments(screen)  # draw all segments

        if self.frame == self.segment_number:  # lightning has been fully drawn
            self.change_properties()
            return False
        return True


class SpaceTimeEntity:
    def __init__(self):
        self.images = [grp.load_image(f"Characters/Space-Time Entity/{i + 1}.png") for i in range(6)]
        self.draw_lightning = False
        self.already_hit_target = False
        self.lightning = Lightning()
        self.index = 0

    def take_action(self, car_x):
        if car_x <= global_variables.CAR_STE_MIN_DAMAGE_DISTANCE and not self.already_hit_target:
            self.draw_lightning = True

    def draw(self, screen, car_x, car_y):
        self.index = (self.index + 0.5) % 5
        screen.blit(self.images[int(self.index)], (0, 0))
        if self.draw_lightning:
            self.draw_lightning = self.lightning.draw(screen, car_x, car_y)