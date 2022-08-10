from src.auxiliary_modules.audio import load_sound


go_sound = load_sound("game/car_ignition.WAV")                # sound of after the final count-down alert (GO)
count_down_sound = load_sound("game/count_down.WAV")          # sound of the usual count down (3, 2, 1)
tic_toc_sound = load_sound("game/tic_toc.WAV")                # sound of the final clock ticking
game_over_sound = load_sound("game/game_over.WAV")            # sound of the match ending
start_sound = load_sound("game/go.WAV")                       # sound of the GO image
wrong_letter_sound = load_sound("game/letter_wrong.WAV")      # sound of the User typing a character wrong
