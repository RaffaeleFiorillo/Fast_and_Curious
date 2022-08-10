from random import randint

valid_characters = "abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ _,.'"
Directories = ["saves/R.F.J.8/data.txt", "saves/Raffaele/data.txt", "saves/teste/data.txt",
               "saves/R.F.J.8/next_level.txt", "saves/Raffaele/next_level.txt", "saves/teste/next_level.txt",
               "parameters/levels info/1.txt", "parameters/levels info/2.txt", "parameters/levels info/3.txt",
               "parameters/levels info/4.txt", "parameters/levels info/5.txt", "parameters/levels info/6.txt",
               "parameters/levels info/7.txt", "parameters/levels info/8.txt", "parameters/levels info/9.txt",
               "parameters/levels info/10.txt", "parameters/levels info/11.txt", "parameters/levels info/12.txt",
               "parameters/levels info/13.txt", "texts/1.txt", "texts/2.txt", "texts/3.txt", "texts/4.txt",
               "texts/5.txt", "texts/6.txt", "texts/7.txt", "texts/8.txt", ]


# encrypts a letter based on a given key_value
def encrypt_letter(letter: str, key: int) -> str:
    new_index = (valid_characters.index(letter) + key) % len(valid_characters)
    return valid_characters[new_index]


# given a string, returns the encrypted version of it
def encrypt_line(data: str, key: int) -> str:
    data = data.strip() if "\n" not in data else data[:-1]
    encrypted_data = "".join(reversed([encrypt_letter(char, key) for char in data]))
    return encrypted_data


# encrypts a file given his directory
def encrypt_file(directory: str) -> None:
    with open(directory, "r") as file:  # get file content
        lines = file.readlines()
    if len(lines) == 0:  # prevents list index error if file is empty
        return None
    with open(directory, "w") as file:
        for line in lines:
            key = randint(1, len(valid_characters) - 1)
            if line is not lines[-1]:
                file.write(f"{key} {encrypt_line(line, key)}\n")
            else:
                file.write(f"{key} {encrypt_line(lines[-1], key)}")


# encrypts a letter based on a given key_value
def decrypt_letter(letter: str, key: int) -> str:
    new_index = (valid_characters.index(letter) - key) % len(valid_characters)
    return valid_characters[new_index]


# given a string, returns the decrypted version of it
def decrypt_line(data: str, key) -> str:
    data = data if "\n" not in data else data[:-1]
    decrypted_data = "".join(reversed([decrypt_letter(char, key) for char in data]))
    return decrypted_data


# de crypts a file given his directory
def decrypt_file(directory: str) -> None:
    with open(directory, "r") as file:  # get file content
        lines = file.readlines()
    if len(lines) == 0:  # prevents list index error if file is empty
        return None
    with open(directory, "w") as file:
        for line in lines:
            key = int(line.split(" ")[0])
            start_index = line.index(" ") + 1
            if line is not lines[-1]:
                file.write(f"{decrypt_line(line[start_index:], key)}\n")
            else:
                file.write(decrypt_line(lines[-1][start_index:], key))


# encrypts all .txt files  in a list of directories passed as parameter
def encrypt_all_files(directories: [str]) -> None:
    for directory in directories:
        print(f"encrypting: {directory}")
        try:
            encrypt_file(directory)
        except ValueError:
            print(f"!!! Error in current directory: {directory} !!!")


# decrypts all .txt files  in a list of directories passed as parameter
def decrypt_all_files(directories: [str]) -> None:
    for directory in directories:
        print(f"decrypting: {directory}")
        try:
            decrypt_file(directory)
        except ValueError:
            print(f"!!! Error in current directory: {directory} !!!")


if __name__ == "__main__":
    information = "encrypt file: --> *file_directory* -e <--\n" \
                  "decrypt file: --> *file_directory* -d <--\n" \
                  "exit:         --> exit"

    print(information)
    while True:
        command = input("Enter Encryption Comand: ")
        if "exit" in command:
            break
        file_dir, action = command.split("-")
        if action == "d":
            decrypt_file(file_dir.strip())
        elif action == "e":
            encrypt_file(file_dir.strip())
        else:
            print("invalid command")
