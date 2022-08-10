# This module contains all the classes that are used in the game classes in order to make the game work.
# Everything that needs to appear in the game is an instance of these classes.
# for those entities that need to appear multiple times, can be of different kinds or comes and goes from the screen,
# there is a class that represents a group of these instances, and can be differentiated from the normal classes by
# looking if his name is plural


from src.entity_classes.car import Car
from src.entity_classes.fireworks import Fireworks
from src.entity_classes.hud import HUD
from src.entity_classes.obstacles import Obstacles
from src.entity_classes.parts import Parts
from src.entity_classes.road import Road
from src.entity_classes.space_time_entity import SpaceTimeEntity
