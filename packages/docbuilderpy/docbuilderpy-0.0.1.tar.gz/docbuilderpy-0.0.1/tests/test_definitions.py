from docbuilderpy.definitions import (
    Definition,
    FunctionDefinition,
    ClassDefinition,
    MethodDefinition,
)


def test_definition_initialization():
    definition = Definition(
        type="base", name="BaseDefinition", docstring="This is a base definition"
    )
    assert definition.type == "base"
    assert definition.name == "BaseDefinition"
    assert definition.docstring == "This is a base definition"


def test_function_definition_initialization():
    function_def = FunctionDefinition(
        type="function",
        name="my_function",
        docstring="This is a function",
        file="file.py",
        arguments=["arg1", "arg2"],
    )
    assert function_def.type == "function"
    assert function_def.name == "my_function"
    assert function_def.docstring == "This is a function"
    assert function_def.file == "file.py"
    assert function_def.arguments == ["arg1", "arg2"]


def test_class_definition_initialization():
    method_def = FunctionDefinition(
        type="method",
        name="my_method",
        docstring="This is a method",
        file="file.py",
        arguments=["self", "arg1"],
    )
    class_def = ClassDefinition(
        type="class",
        name="MyClass",
        docstring="This is a class",
        file="file.py",
        methods=[method_def],
    )
    assert class_def.type == "class"
    assert class_def.name == "MyClass"
    assert class_def.docstring == "This is a class"
    assert class_def.file == "file.py"
    assert class_def.methods == [method_def]


def test_method_definition_initialization():
    method_def = MethodDefinition(
        type="method",
        name="my_method",
        docstring="This is a method",
        arguments=["self", "arg1"],
    )
    assert method_def.type == "method"
    assert method_def.name == "my_method"
    assert method_def.docstring == "This is a method"
    assert method_def.arguments == ["self", "arg1"]
