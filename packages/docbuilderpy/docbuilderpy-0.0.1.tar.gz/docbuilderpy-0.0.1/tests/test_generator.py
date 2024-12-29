from typing import List
from docbuilderpy.generator import Generator
from docbuilderpy.definitions import Definition


class TestGenerator(Generator):
    def generate(self, definitions: List[Definition]) -> str:
        return "test"


def test_generator():
    generator = TestGenerator()
    definitions = []
    result = generator.generate(definitions)
    assert result == "test"
