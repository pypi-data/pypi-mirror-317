import ast
from typing import List
from docbuilderpy.definitions import (
    Definition,
    FunctionDefinition,
    ClassDefinition,
    MethodDefinition,
)


def analyze_definitions(code: str, file: str) -> List[Definition]:
    tree = ast.parse(code)
    definitions = []

    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            definitions.append(
                FunctionDefinition(
                    type="function",
                    file=file,
                    name=node.name,
                    docstring=ast.get_docstring(node),
                    arguments=[arg.arg for arg in node.args.args],
                )
            )
        elif isinstance(node, ast.ClassDef):
            methods = [
                MethodDefinition(
                    type="method",
                    name=n.name,
                    docstring=ast.get_docstring(n),
                    arguments=[arg.arg for arg in n.args.args],
                )
                for n in node.body
                if isinstance(n, ast.FunctionDef)
            ]

            definitions.append(
                ClassDefinition(
                    type="class",
                    file=file,
                    name=node.name,
                    docstring=ast.get_docstring(node),
                    methods=methods,
                )
            )

    return definitions
