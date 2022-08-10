from src.menu_classes import menus as mc, buttons as btn
import pygame
from src.auxiliary_modules import audio, files, user_data_management as um
from src.link_functions.sounds import change_menu_sound, delete_account_sound


# display the Change Password Menu. It leads to the Account Management Menu (after password verification)
def change_password(screen: pygame.Surface):
    audio.play(change_menu_sound)
    buttons = [btn.Button(335, 210, "/menu/buttons/5/0.png", None),
               btn.Button(335, 356, "/menu/buttons/5/0.png", None),
               btn.Button(335, 495, "/menu/buttons/9/1.png", False),
               btn.Button(573, 495, "/menu/buttons/9/2.png", True)]
    cma = mc.CreateModifyAccount("menu/interfaces/Main/change password.png", screen, buttons, True)
    effect = cma.display_menu()
    if effect == "change_password":
        return effect
    return "manage_us"


# display Delete Account Menu. It leads to the Main Menu (after password verification) or Management User Menu
def delete_account(screen: pygame.Surface):
    audio.play(change_menu_sound)
    buttons = [btn.Button(240, 410, f"menu/buttons/3/1.png", True),
               btn.Button(580, 410, f"menu/buttons/3/2.png", False)]
    if mc.Exit("menu/exit/delete_account.png", screen, buttons).display_menu():
        user_name = files.read_file_content("saves/active_user.txt", 1)[0].split(" ")[0]
        verification_password = mc.EnterPassword(screen, True).display_menu()
        if verification_password == "MainMenu":
            audio.play(delete_account_sound)
            um.delete_user_account(user_name)
        return verification_password
    return "manage_us"


# display Delete Statistics Menu. It leads to the Account Management User Menu
def delete_statistics(screen: pygame.Surface):
    audio.play(change_menu_sound)
    buttons = [btn.Button(240, 410, f"menu/buttons/3/1.png", True),
               btn.Button(580, 410, f"menu/buttons/3/2.png", False)]
    if mc.Exit("menu/exit/delete_account.png", screen, buttons).display_menu():
        user_name = files.read_file_content("saves/active_user.txt", 1)[0].split(" ")[0]
        verification_password = mc.EnterPassword(screen, True).display_menu()
        if verification_password == "MainMenu":
            audio.play(delete_account_sound)
            um.delete_user_account(user_name)
        return verification_password
    return "manage_us"
