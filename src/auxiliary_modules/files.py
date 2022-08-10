from .encryption import decrypt_file, encrypt_file


# reads  an encrypted file and returns its decrypted content. Takes the directory of the encrypted file and the number
# of lines that we need to be returned. the output is a list of strings (every string is a different line of the file).
def read_file_content(file_directory: str, lines_to_read: int = 0) -> [str]:
    file_directory = f"assets/{file_directory}"
    decrypt_file(file_directory)
    with open(file_directory, "r") as file:
        if lines_to_read == 0:
            file_content = file.readlines()
        else:
            file_content = [file.readline() for _ in range(lines_to_read)]
    encrypt_file(file_directory)
    return file_content


# Takes as parameters the file directory where the data will be written; and the content (to be written). content is
# a string containing all the data to be written in the file.
def write_file_content(file_directory: str, content: [str]) -> None:
    file_directory = f"assets/{file_directory}"
    with open(file_directory, "w") as file:
        file.writelines(content)
    encrypt_file(file_directory)
