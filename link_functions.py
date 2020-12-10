import classes_menu as cm
import loops as lp
import pygame
import funcoes as f

USER = None


def exit_game(screen):
    if cm.Exit("imagens/menu/exit/exit_game.png", screen).display_menu():
        exit("Exit Game")
    return "main_menu"


def exit_game_menu(screen):
    if cm.Exit("imagens/menu/exit/exit_menu.png", screen).display_menu():
        return "main_menu"
    return "continue"


def exit_tutorial(screen):
    if cm.Exit("imagens/menu/exit/exit_menu.png", screen).display_menu():
        return "continue"
    return "tutorial"


# Main Menu
def main_menu(screen):
    posicx_main = (1080 - 260)//2
    posicy_main = [y for y in range(150,600,150)]
    efeitos_main = ["continue", "new", "exit1"]
    butns_main = [cm.Button(posicx_main, y, f"imagens/menu/buttons/1/{posicy_main.index(y)+1}.png", efeitos_main[posicy_main.index(y)], posicy_main.index(y)) for y in posicy_main[:len(efeitos_main)]]
    m_m = cm.Menu(butns_main, f"imagens/menu/interfaces/main menu.png", screen)
    return m_m.display_menu()

#Choose User
def choose_user(screen):
    if USER is None:
        posicx_game = (1080 - 260) // 2
        c_m = cm.Choose_Account(screen)
        return g_m.display_menu()
    else:
        return "continue"


# Game Menu
def game_menu(screen):
    posicx_game = (1080 - 260)//2
    posicy_game = [y for y in range(110, 600, 100)]
    efeitos_game = ["story", "mai", "mpart", "tutorial", "exit2"]
    butns_game = [cm.Button(posicx_game, y, f"imagens/menu/buttons/2/{posicy_game.index(y)+1}.png", efeitos_game[posicy_game.index(y)], posicy_game.index(y)) for y in posicy_game[:len(efeitos_game)]]
    g_m = cm.Menu(butns_game, f"imagens/menu/interfaces/game menu.png", screen)
    return g_m.display_menu()


def tutorial(screen):
    posicx_tutorial = (1080 - 260)//2
    posicy_tutorial = [y for y in range(110, 600, 100)]
    efeitos_tutorial = ["comands", "t_save", "enemies", "level_up", "exit3"]
    butns_tutorial = [cm.Button(posicx_tutorial, y, f"imagens/menu/buttons/4/{posicy_tutorial.index(y)+1}.png", efeitos_tutorial[posicy_tutorial.index(y)], posicy_tutorial.index(y)) for y in posicy_tutorial[:len(efeitos_tutorial)]]
    t = cm.Menu(butns_tutorial, f"imagens/menu/interfaces/tutorial.png", screen)
    return t.display_menu()


def create_new_account(screen):
    ac = cm.Create_Account("imagens/menu/interfaces/create account.png", screen)
    if ac.display_menu():
        USER = ac.user
        return "main_menu"
    return "continue"

def display_story(screen):
    pass


def game_ai(screen):
    background = pygame.Surface((1080, 700))
    background.fill((0, 255, 0))
    r = lp.Mission_AI(screen, background)
    results_mission_ai(r)
    return "continue"


def game_parts(screen):
    background = pygame.Surface((1080, 700))
    background.fill((0, 255, 0))
    r = lp.Mission_Parts(screen, background)
    results_mission_p(r)
    return "continue"


def tutorial_s(screen):
    pass


def tutorial_c(screen):
    pass


def tutorial_e(screen):
    pass


def tutorial_lu(screen):
    pass


def results_mission_ai(r):
    pass


def results_mission_p(r):
    pass
