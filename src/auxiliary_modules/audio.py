from pygame import mixer
from .files import read_file_content
mixer.init()


def get_sound_volume() -> float:
    line = read_file_content("saves/active_user.txt", 1)[0].split(" ")
    if len(line) != 1:
        return float(line[7]) / 10
    else:
        return 1.0


def get_music_volume() -> float:
    line = read_file_content("saves/active_user.txt", 1)[0].split(" ")
    if len(line) != 1:
        return float(line[6]) / 20.0
    else:
        return 0.5


# uses the pygame module to load a sound to memory and returns it
def load_sound(directory: str):
    return mixer.Sound(f"assets/sounds/{directory}")


# plays a sound passed as argument
def play(sound, volume=False) -> None:
    volume = get_sound_volume() if volume is False else volume / 10  # 0->10 must be divided by ten to be in 0->1 range
    sound.set_volume(volume)
    sound.play()


# ------------------------------------------ SOUNDS --------------------------------------------------------------------
error_sound = load_sound("menu/error_message2.WAV")  # sound for every time an error occurs
success_sound = load_sound("menu/success.WAV")  # sound for every time a success occurs
music_sound = load_sound("game/music.WAV")


def play_music() -> None:
    sound = music_sound
    volume = get_music_volume()
    sound.set_volume(volume)
    sound.play(-1)


def music_fade_out() -> None:
    music_sound.fadeout(2)


# stops all currently playing sounds
def stop_all_sounds() -> None:
    mixer.stop()
