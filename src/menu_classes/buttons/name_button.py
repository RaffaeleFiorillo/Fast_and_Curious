from .button import Button
from pygame import Surface


class NameButton(Button):
    def __init__(self, x: int, y: int, active_image: Surface, passive_image: Surface, name: str):
        super().__init__(x, y, "", "")
        self.name = name
        self.active_image = active_image
        self.passive_image = passive_image
        self.image = passive_image

    def activate(self):
        self.image = self.active_image

    def deactivate(self):
        self.image = self.passive_image