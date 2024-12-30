from unittest.mock import MagicMock
from docbuilderpy.generate import generate
from docbuilderpy.generators.generator import Generator


def test_generate():
    class Mock(Generator):
        def generate(self, source_path: str, output_path: str):
            pass

        def generate_file(self, definitions):
            pass

        def get_file_format(self):
            pass

    source_path = "source/path"
    output_path = "output/path"
    generator = MagicMock(spec=Mock)

    generate(source_path, output_path, generator)

    generator.generate.assert_called_once_with(source_path, output_path)
