from shutil import rmtree
from os import walk, mkdir
from .files import read_file_content, write_file_content


# creates a folder inside the root_directory with the name of the User creating the account
def create_folder(user_name: str) -> None:
    mkdir(f"assets/saves/{user_name}")


# returns current User's information
def get_user_data() -> ([str], [int]):
    # active User format: "Name speed best_time level parts password volume1 volume2"
    values_p = read_file_content("saves/active_user.txt", 1)[0].split(" ")
    str_val = [values_p[0], values_p[5]]
    int_val = [int(value) for value in values_p if value.isdigit()]
    return str_val, int_val


# returns a list with all the usernames currently existing, but only on Windows, linux and macOS
def list_users() -> [str]:
    return list(walk("assets/saves"))[0][1]


# saves current User's new information
def save_user_data(data: (str, int, int, int, int, str, int, int)) -> None:
    name, b_speed, b_time, level, parts, password, volume1, volume2 = data
    line = f"{name} {b_speed} {b_time} {level} {parts} {password} {volume1} {volume2}"
    write_file_content("saves/active_user.txt", line)
    line = f"{b_speed} {b_time} {level} {parts} {password} {volume1} {volume2}"
    write_file_content(f"saves/{name}/data.txt", line)


# erases the data inside the file: "active User data.txt" when the User logs out or exits the game
def erase_active_user_data() -> None:
    file = open("assets/saves/active_user.txt", "w")
    file.close()


# gets the requirement values in order to verify if User has leveled up from the parameters file and returns them
def get_requirements() -> (int, int):
    user_level = int(read_file_content("saves/active_user.txt", 1)[0].split(" ")[3])  # get User level in his file
    speed, precision, _parts = read_file_content(f"parameters/levels info/{user_level}.txt", 1)[0].split(" ")
    return int(speed), int(precision)


# returns the current User's level
def get_user_level() -> int:
    user_level = int(read_file_content("saves/active_user.txt", 1)[0].split(" ")[3])
    return user_level


# returns True if the User has already won the game before, and False in the opposite case
def user_is_a_winner() -> int:
    user_name = int(read_file_content("saves/active_user.txt", 1)[0].split(" ")[3])
    is_a_winner = int(read_file_content(f"saves/{user_name}/next_level.txt")[1])
    return is_a_winner


# updates the data in the next_level.txt file
def save_next_level_data(user_name: str, m_ai_data: int, winner_data: int) -> None:
    write_file_content(f"saves/{user_name}/next_level.txt", [f"{m_ai_data} \n{winner_data}"])


# updates User information after a played match is over, for Mission AI
def save_performance_ai(go_to_next_level: bool, parts: int, speed: int) -> None:
    str_val, int_val = get_user_data()
    if go_to_next_level:  # change User data in case he levels up
        if get_user_level() < 13:  # level 13 is the highest in the game
            int_val[2] += 1
            save_next_level_data(str_val[0], 0, 0)
        else:
            save_next_level_data(str_val[0], 0, 1)
    int_val[3] += parts
    if int_val[3] < 0:
        int_val[3] = 0
    if int_val[0] < speed:
        int_val[0] = int(speed)
    data = (str_val[0], int_val[0], int_val[1], int_val[2], int_val[3], str_val[1], int_val[4], int_val[5])
    save_user_data(data)


# updates User information after a played match is over, for Mission Parts
def save_performance_parts(parts: int, speed: int, time: int) -> None:
    str_val, int_val = get_user_data()
    int_val[3] += parts
    if int_val[3] < 0:
        int_val[3] = 0
    if int_val[0] < speed:
        int_val[0] = int(speed)
    if int_val[1] < time:
        int_val[1] = int(time)
    # name best-speed best-time level 'parts' password music-volume sound-volume
    data = (str_val[0], int_val[0], int_val[1], int_val[2], int_val[3], str_val[1], int_val[4], int_val[5])
    save_user_data(data)


# deletes the folder that has the data of the users that is requesting it to be deleted
def delete_user_account(user_name: str) -> None:
    rmtree(f'assets/saves/{user_name}')


# returns a list with all the names of the texts that the User will type in the matches
def get_text_names() -> [str]:
    texts = walk("assets/texts")
    texts = [text for text in texts][0][1:][1][:-1]
    return texts


# returns the number of the last existing text
def get_last_text_number() -> int:
    texts = get_text_names()
    last_text_name = texts[-1].split(".")[0]
    return int(last_text_name)
