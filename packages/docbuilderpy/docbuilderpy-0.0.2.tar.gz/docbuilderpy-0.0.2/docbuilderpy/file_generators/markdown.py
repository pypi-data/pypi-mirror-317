from typing import List
from docbuilderpy.definitions import Definition
from docbuilderpy.generators.multi_file_generator import MultiFileGenerator


class Markdown(MultiFileGenerator):
    def generate_file(self, definitions: List[Definition]):
        content = "# Documentation"
        for item in definitions:

            if item.type == "function":
                content += f"\n\n## Function: `{item.name}`\n"
                content += f"- File: {item.file}\n"
                content += f"- Args: {', '.join(item.arguments)}\n"

            elif item.type == "class":
                content += f"\n\n## Class: `{item.name}`\n"
                content += f"- File: {item.file}\n"

                for method in item.methods:
                    content += f"\n\n### Method: `{method.name}`\n"
                    content += f"- Args: {', '.join(method.arguments)}\n"

            if item.docstring:
                content += f"- Description: {item.docstring}"

        return content

    def get_file_format(self):
        return "md"
