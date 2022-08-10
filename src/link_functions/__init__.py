# This module contains all the functions called by the main module.
# All the functions take the screen where the images are going to be displayed as a parameter
# For each of the functions there is a correspondent class that manages the functionality of the function
# Each function in this module returns values that correspond to the functionality that the game should open next
# A function's comment in this module has a description and the functions it can lead to when it finishes
# This module is divided in categories like: --- CATEGORY NAME --- ; in order to make it more understandable

from src.link_functions.start import start_page
from src.link_functions.password_verification import enter_password
from src.link_functions.GameMenu import *
from src.link_functions.MainMenu import *
