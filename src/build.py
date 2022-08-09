import shutil as shut
from pathlib import Path
import os

directories = ["saves/R.F.J.8/data.txt", "saves/Raffaele/data.txt", "saves/teste/data.txt",
               "saves/R.F.J.8/next_level.txt", "saves/Raffaele/next_level.txt", "saves/teste/next_level.txt",
               "parameters/levels info/1.txt", "parameters/levels info/2.txt", "parameters/levels info/3.txt",
               "parameters/levels info/4.txt", "parameters/levels info/5.txt", "parameters/levels info/6.txt",
               "parameters/levels info/7.txt", "parameters/levels info/8.txt", "parameters/levels info/9.txt",
               "parameters/levels info/10.txt", "parameters/levels info/11.txt", "parameters/levels info/12.txt",
               "parameters/levels info/13.txt", "texts/1.txt", "texts/2.txt", "texts/3.txt", "texts/4.txt",
               "texts/5.txt", "texts/6.txt", "texts/7.txt", "texts/8.txt", ]


# Af.encrypt_all_files(directories)

# [print(f'"{directory}",') for directory in directories]


def create_executable():
    print("\n ############### Creating File ###############\n")
    ico_directory = "images\Icons\\fire.ico"  # location of the Icon that will be set to the .exe
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
        return None
    print("\n ######## Authentication Successful ##########\n")
    os.remove('Game.exe')  # delete the old version of the game
    create_executable()  # create the new version of the game
    # delete the unnecessary files created in the previous step
    print("\n ############### Deleting Trash ###############\n")
    shut.rmtree("dist")
    shut.rmtree("build")
    os.remove("Game.spec")
    print("\n ############### Trash Deleted ###############\n")
    print("\n ############### Game Built ###############\n")


if __name__ == "__main__":
    create_game_executable()
