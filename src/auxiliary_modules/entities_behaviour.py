from .global_variables import road_colors, parts_colors, WEIGHTS, BIAS
from math import tanh

# ----------------------------------------- CAR AI/VISION FUNCTIONS ----------------------------------------------------
# These functions are used to make the car see the obstacles in the road and choose what to do


# based on given screen coordinates, gives back what type of object is at that position
def see(screen, coo: (int, int)) -> int:
    x, y = coo
    if y <= 0:
        return 0
    elif y > 308:
        return 0
    color = list(screen.get_at((x, y)))[:-1]
    if color in road_colors:
        current_code = 0
    elif color in parts_colors:
        current_code = 1
    else:
        current_code = -1
    # sign = code_meaning[current_code]  # -> turns rgb values into words
    # print(sign)
    return current_code


# Given all seen values, gives back a code value for what to do
def make_a_choice(info: [int], weights=None, bias=None) -> int:
    if weights is None:
        weights, bias = WEIGHTS, BIAS
    soma = sum([weights[i] * info[i] + bias[i] for i in range(len(info))])
    refined_value = tanh(soma)
    if refined_value >= 0.70:
        return 1
    elif refined_value <= -0.70:
        return -1
    else:
        return 0
