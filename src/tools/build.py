import shutil as shut
from pathlib import Path
import os


def create_executable():
    print("\n ############### Creating File ###############\n")
    ico_directory = "assets\images\Icons\\fire.ico"  # location of the Icon that will be set to the .exe
    options = "--onefile --noconsole --windowed --name Game"  # options for the creation of the .exe
    command = f"pyinstaller {options} --icon={ico_directory} main.py"
    os.system(f'cmd /c "{command}"')  # create Game.exe with *pyinstaller* set with the options defined before
    print("\n ############### Moving file ###############\n")
    shut.move("dist/Game.exe", Path.cwd())  # Move Game.exe from source to destination (Destination is the current path)
    print("\n ############### File Moved ###############\n")
    print("\n ############### File Created ###############\n")


def create_game_executable():
    print("\n ############### Building Game ###############\n")
    print("\n ############## Authentication ###############\n")
    if input("Password: ") != "Raffaele8":
        print("Error: Wrong Password")
        print("\n ######### Authentication Failed #############\n")
        input("")
        return None
    print("\n ######## Authentication Successful ##########\n")
    try:
        print("\n ############ Deleting Game.exe #############\n")
        os.remove('Game.exe')  # delete the old version of the game
    except FileNotFoundError:
        print("\n ######## Game.exe was already deleted ######## \n")
    create_executable()  # create the new version of the game
    # delete the unnecessary files created in the previous step
    print("\n ############### Deleting Trash ###############\n")
    shut.rmtree("dist")
    shut.rmtree("build")
    os.remove("Game.spec")
    print("\n ############### Trash Deleted ###############\n")
    print("\n ########## Game Built Successfully ##########\n")
    input("")


if __name__ == "__main__":
    create_game_executable()
