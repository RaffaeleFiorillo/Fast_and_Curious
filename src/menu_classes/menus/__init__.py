# This module contains all the classes responsible for displaying and managing all the Menus and interfaces available
# In the Game. There are also some classes that makes it easier for all the menu classes to do their job.
# Every menu class has three major methods that are very similar if not the same: - display_menu(); - manage_buttons();
# - refresh(); display_menu is the one called after instantiating a new object of a menu class, it is the only method
# used externally of the class. It is the most important, and his job is to display the events of a menu.
# The manage_buttons method is for transforming input from the keyboard into the correct output. And the refresh method
# just updates the menu after every alteration the User makes.


from src.menu_classes.menus.basic_input_manager import BasicInputManagement
from src.menu_classes.menus.basic_menu import BasicMenu
from src.menu_classes.menus.user_menu import UserMenu
from src.menu_classes.menus.menu_add_text import AddText
from src.menu_classes.menus.menu_choose_account import ChooseAccount
from src.menu_classes.menus.menu_create_modify_account import CreateModifyAccount
from src.menu_classes.menus.menu_enter_password import EnterPassword
from src.menu_classes.menus.menu_exit import Exit
from src.menu_classes.menus.menu_game import GameMenu
from src.menu_classes.menus.menu_image_sequence import MenuImageSequence
from src.menu_classes.menus.menu_management import Management
from src.menu_classes.menus.menu_report_mission_ai import ReportMissionAI
from src.menu_classes.menus.menu_report_mission_parts import ReportMissionParts
from src.menu_classes.menus.menu_start import Start
from src.menu_classes.menus.menu_unlock_level import UnlockLevel
from src.menu_classes.menus.menu_winner import WinnerMenu
