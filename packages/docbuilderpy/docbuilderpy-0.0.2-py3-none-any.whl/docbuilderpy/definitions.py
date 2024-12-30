import abc
from typing import List
from dataclasses import dataclass


@dataclass
class Definition(abc.ABC):
    type: str
    name: str
    docstring: str


@dataclass
class FunctionDefinition(Definition):
    file: str
    arguments: list


@dataclass
class ClassDefinition(Definition):
    file: str
    methods: List[FunctionDefinition]


@dataclass
class MethodDefinition(Definition):
    arguments: list
