def load_file(file_path: str) -> str:
    with open(file_path, "r") as file:
        code = file.read()
    return code
