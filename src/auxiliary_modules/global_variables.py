obstacle_colors = ((196, 15, 23), (239, 10, 9), (191, 15, 23), (245, 71, 20), (252, 130, 18), (255, 17, 11),
                   (255, 18, 11), (255, 18, 12), (195, 195, 195), (163, 73, 164), (248, 12, 35), (255, 255, 255))
parts_colors = ((255, 128, 0), (255, 242, 0), (34, 177, 76), (252, 130, 19), (237, 28, 36), (255, 0, 255),
                (120, 0, 120), (0, 255, 255), (0, 0, 255))
road_colors = ((0, 0, 0), (108, 108, 108))
code_meaning = {3: "unknown", 0: "road", 1: "parts", -1: "lava"}
valid_characters = "abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ _,.'"
# AI variables achieved by a genetic algorithm that can be found in the genetic_algorithm module
WEIGHTS = [-0.024636661554064646, 0.9490338548623168, 0.9490338548623168, 0.17090764398454833, 1.0661495372951384]
BIAS = [0.2670813587084078, -0.6691533200275781, -0.5723370239650385, 0.25406116993577665, -0.486196069971221]
FRAME_RATE = 30
SCREEN_LENGTH, SCREEN_WIDTH = 1080, 700
CAR_MAX_SPEED = 10
CAR_STE_MIN_DAMAGE_DISTANCE = 400  # distance at which the car starts getting damage from the Space-Time-Entity
CAR_MAX_DISTANCE = 470  # maximum distance the car can reach (right)
CAR_MIN_DISTANCE = CAR_STE_MIN_DAMAGE_DISTANCE - 20  # minimum distance the car can reach (left)
obstacles_distance = 290
parts_distance = 5
space_between_obstacles = [o for o in range(300, 1290, obstacles_distance)]