import abc
import os
from docbuilderpy.generators.generator import Generator
from docbuilderpy.load_file import load_file
from docbuilderpy.analyze_definitions import analyze_definitions


class SingleFileGenerator(Generator, abc.ABC):
    def generate(self, source_path: str, output_path: str) -> None:
        definitions = []
        for root, _, files in os.walk(source_path):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    code = load_file(file_path)
                    definitions.extend(analyze_definitions(code, file_path))

        content = self.generate_file(definitions)
        with open(output_path + "." + self.get_file_format(), "w") as file:
            file.write(content)

    @abc.abstractmethod
    def generate_file(self, definitions):
        pass

    @abc.abstractmethod
    def get_file_format(self):
        pass
