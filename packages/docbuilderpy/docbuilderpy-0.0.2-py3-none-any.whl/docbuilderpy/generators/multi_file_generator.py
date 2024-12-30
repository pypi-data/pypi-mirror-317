import abc
import os
from docbuilderpy.generators.generator import Generator
from docbuilderpy.load_file import load_file
from docbuilderpy.analyze_definitions import analyze_definitions


class MultiFileGenerator(Generator, abc.ABC):
    def generate(self, source_path: str, output_path: str) -> None:
        for root, _, files in os.walk(source_path):
            for file in files:
                if file.endswith(".py") and not file.endswith("__init__.py"):
                    file_path = os.path.join(root, file)
                    code = load_file(file_path)
                    definitions = analyze_definitions(code, file_path)

                    relative_path = os.path.relpath(file_path, source_path)
                    output_file_path = os.path.join(output_path, relative_path)

                    output_dir = os.path.dirname(output_file_path)
                    os.makedirs(output_dir, exist_ok=True)

                    content = self.generate_file(definitions)

                    with open(
                        output_file_path + "." + self.get_file_format(), "w"
                    ) as output_file:
                        output_file.write(content)

    @abc.abstractmethod
    def generate_file(self, definitions):
        pass

    @abc.abstractmethod
    def get_file_format(self):
        pass
