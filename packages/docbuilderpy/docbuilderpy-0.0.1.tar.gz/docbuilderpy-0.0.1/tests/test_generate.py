import pytest
from unittest.mock import MagicMock, patch
from docbuilderpy.generate import generate
from docbuilderpy.generator import Generator


@pytest.fixture
def mock_generator():
    return MagicMock(spec=Generator)


@patch("docbuilderpy.generate.analyze_definitions")
@patch("docbuilderpy.generate.load_file")
@patch("os.walk")
def test_generate(
    mock_os_walk, mock_load_file, mock_analyze_definitions, mock_generator, tmp_path
):
    mock_os_walk.return_value = [
        ("/some/path", ("subdir",), ("file1.py", "file2.py")),
        ("/some/path/subdir", (), ("file3.py",)),
    ]
    mock_load_file.side_effect = ["code1", "code2", "code3"]
    mock_analyze_definitions.side_effect = [["def1"], ["def2"], ["def3"]]
    mock_generator.generate.return_value = "generated content"

    output_file = tmp_path / "output.txt"

    generate("/some/path", str(output_file), mock_generator)

    mock_os_walk.assert_called_once_with("/some/path")
    assert mock_load_file.call_count == 3
    assert mock_analyze_definitions.call_count == 3
    mock_generator.generate.assert_called_once_with(["def1", "def2", "def3"])

    with open(output_file, "r") as file:
        content = file.read()

    assert content == "generated content"
