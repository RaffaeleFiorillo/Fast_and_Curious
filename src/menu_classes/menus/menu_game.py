from pygame.event import Event
from src.auxiliary_modules import user_data_management as udm
from src.auxiliary_modules import display
from src.menu_classes.menus.user_menu import UserMenu


# Used for the Game Menu. Just implements some changes in the way some buttons work
class GameMenu(UserMenu):
    def get_effect_by_input(self, event: Event = None):
        effect = super().get_effect_by_input(event)
        if effect == "m_ai":
            if udm.get_user_level() < 13:
                return effect
            else:
                display.show_error_message(self.screen, 12)
        else:
            return effect
