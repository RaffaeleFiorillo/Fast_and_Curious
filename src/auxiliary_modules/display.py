import pygame
from .audio import play, error_sound, success_sound
from .graphics import load_image


# displays on the screen an error message specified by his code
def show_error_message(screen, code: int, waiting_time=3) -> None:
    play(error_sound)
    screen.blit(load_image(f"menu/messages/error{code}.png"), (230, 200))
    pygame.display.update()
    pygame.time.wait(waiting_time)
    pygame.event.clear()  # all pressed buttons are dismissed in this phase


# displays on the screen a success message specified by his code
def show_success_message(screen, code: int, waiting_time=3) -> None:
    play(success_sound)
    screen.blit(load_image(f"menu/messages/success{code}.png"), (230, 200))
    pygame.display.update()
    pygame.time.wait(waiting_time)
    pygame.event.clear()  # all pressed buttons are dismissed in this phase
