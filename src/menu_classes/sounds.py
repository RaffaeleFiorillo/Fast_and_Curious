from src.auxiliary_modules.audio import load_sound

button_y_sound = load_sound("menu/button_activation.WAV")  # sound for changing button on y-axis
button_x_sound = load_sound("menu/button_lateral.WAV")  # sound for changing button on x-axis
volume_change_sound = load_sound("menu/volume_change.WAV")  # sound for changing volume
erase_letter_sound = load_sound("menu/typing.WAV")  # sound for every time a letter is erased
error_sound = load_sound("menu/error_message2.WAV")  # sound for every time an error occurs
success_sound = load_sound("menu/success.WAV")  # sound for every time a success occurs
