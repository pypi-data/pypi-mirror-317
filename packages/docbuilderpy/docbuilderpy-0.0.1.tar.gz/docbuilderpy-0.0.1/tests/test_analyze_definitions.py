from docbuilderpy.analyze_definitions import analyze_definitions
from docbuilderpy.definitions import (
    FunctionDefinition,
    ClassDefinition,
    MethodDefinition,
)


def test_analyze_definitions_with_function():
    code = '''
def foo(a, b):
    """This is a test function"""
    return a + b
'''
    file = "test_file.py"
    result = analyze_definitions(code, file)

    assert len(result) == 1
    assert isinstance(result[0], FunctionDefinition)
    assert result[0].type == "function"
    assert result[0].file == file
    assert result[0].name == "foo"
    assert result[0].docstring == "This is a test function"
    assert result[0].arguments == ["a", "b"]


def test_analyze_definitions_with_class():
    code = '''
class Foo:
    """This is a test class"""
    def bar(self, x):
        """This is a test method"""
        return x
'''
    file = "test_file.py"
    result = analyze_definitions(code, file)

    assert len(result) == 1
    assert isinstance(result[0], ClassDefinition)
    assert result[0].type == "class"
    assert result[0].file == file
    assert result[0].name == "Foo"
    assert result[0].docstring == "This is a test class"
    assert len(result[0].methods) == 1
    assert isinstance(result[0].methods[0], MethodDefinition)
    assert result[0].methods[0].type == "method"
    assert result[0].methods[0].name == "bar"
    assert result[0].methods[0].docstring == "This is a test method"
    assert result[0].methods[0].arguments == ["self", "x"]


def test_analyze_definitions_with_empty_code():
    code = ""
    file = "test_file.py"
    result = analyze_definitions(code, file)

    assert result == []
