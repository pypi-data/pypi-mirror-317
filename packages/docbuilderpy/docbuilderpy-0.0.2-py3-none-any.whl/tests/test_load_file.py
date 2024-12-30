import pytest
from docbuilderpy.load_file import load_file


def test_load_file(tmp_path):
    file_path = tmp_path / "test_file.txt"
    content = "print('Hello, world!')"
    file_path.write_text(content)

    result = load_file(file_path)
    assert result == content


def test_load_file_nonexistent():
    with pytest.raises(FileNotFoundError):
        load_file("nonexistent_file.txt")
