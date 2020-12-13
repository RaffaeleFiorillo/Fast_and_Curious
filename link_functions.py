import classes_menu as cm
import loops as lp
import pygame
import funcoes as f


def exit_game(screen):
    if cm.Exit("images/menu/exit/exit_game.png", screen).display_menu():
        exit("Exit Game")
    return "main_menu"


def exit_game_menu(screen):
    if cm.Exit("images/menu/exit/exit_menu.png", screen).display_menu():
        return "main_menu"
    return "continue"


def exit_tutorial(screen):
    if cm.Exit("images/menu/exit/exit_menu.png", screen).display_menu():
        return "continue"
    return "tutorial"


# Main Menu
def main_menu(screen):
    posicx_main = (1080 - 260)//2
    posicy_main = [y for y in range(150,600,150)]
    effects_main = ["choose", "new", "exit1"]
    butns_main = [cm.Button(posicx_main, y, f"images/menu/buttons/1/{posicy_main.index(y)+1}.png", effects_main[posicy_main.index(y)], posicy_main.index(y)) for y in posicy_main[:len(effects_main)]]
    m_m = cm.Menu(butns_main, f"images/menu/interfaces/Main/main menu.png", screen)
    return m_m.display_menu()


# Enter_Password_Menu
def enter_password(screen):
    e_m = cm.Enter_Password(screen)
    return e_m.display_menu()


# Choose User
def choose_user(screen):
    m_m = cm.Choose_Account(screen)
    return m_m.display_menu()


# Game Menu
def game_menu(screen):
    posicx_game = (1080 - 260)//2
    posicy_game = [y for y in range(107, 600, 80)]
    effects_game = ["story", "mai", "mpart", "tutorial", "manage", "exit2"]
    butns_game = [cm.Button(posicx_game, y, f"images/menu/buttons/2/{posicy_game.index(y)+1}.png", effects_game[posicy_game.index(y)], posicy_game.index(y)) for y in posicy_game[:len(effects_game)]]
    user = cm.User()
    user.get_active_user()
    user.get_texts()
    g_m = cm.Menu(butns_game, f"images/menu/interfaces/Main/game menu.png", screen, user)
    #f.erase_active_user_data()
    return g_m.display_menu()


def tutorial(screen):
    posicx_tutorial = (1080 - 260)//2
    posicy_tutorial = [y for y in range(110, 600, 100)]
    effects_tutorial = ["comands", "t_save", "enemies", "level_up", "exit3"]
    butns_tutorial = [cm.Button(posicx_tutorial, y, f"images/menu/buttons/4/{posicy_tutorial.index(y)+1}.png", effects_tutorial[posicy_tutorial.index(y)], posicy_tutorial.index(y)) for y in posicy_tutorial[:len(effects_tutorial)]]
    user = cm.User()
    user.get_active_user()
    user.get_texts()
    t = cm.Menu(butns_tutorial, f"images/menu/interfaces/Main/tutorial.png", screen, user)
    return t.display_menu()


def create_new_account(screen):
    if len(f.lista_utilizadores()) == 7:
        f.show_error_message(screen, 6)
        return "main_menu"
    ac = cm.Create_Account("images/menu/interfaces/Main/create account.png", screen)
    effect = ac.display_menu()
    if effect == "new":
        return effect
    elif effect:
        return "continue"
    return "main_menu"

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


def manage_account(screen):
    posicx = (1080 - 260)//2
    posicy = [y for y in range(110, 600, 100)]
    effects = ["", "", "add_text", "elmnt_account", "exit3"]
    butns = [cm.Button(posicx, y, f"images/menu/buttons/8/{posicy.index(y)+1}.png",
                                effects[posicy.index(y)], posicy.index(y))
                      for y in posicy[:len(effects)]]
    posicx -= 55
    button1 = cm.Button2(posicx, 130, f"images/menu/buttons/8/{posicy.index(110)+1}.png",
                                effects[posicy.index(110)], posicy.index(110), 0)
    button2 = cm.Button2(posicx, 230, f"images/menu/buttons/8/{posicy.index(210)+1}.png",
                                effects[posicy.index(210)], posicy.index(210), 1)
    butns = [button1, button2]+butns[2:]
    user = cm.User()
    user.get_active_user()
    user.get_texts()
    m = cm.Management(butns, f"images/menu/interfaces/Main/management.png", screen, user)
    return m.display_menu()


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
