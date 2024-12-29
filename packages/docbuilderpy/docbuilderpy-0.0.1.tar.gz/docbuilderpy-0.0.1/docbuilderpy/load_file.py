def load_file(file_path):
    with open(file_path, "r") as file:
        code = file.read()
    return code
