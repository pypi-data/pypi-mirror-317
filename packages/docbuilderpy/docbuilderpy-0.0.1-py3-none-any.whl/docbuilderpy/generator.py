import abc
from typing import List
from docbuilderpy.definitions import Definition


class Generator(abc.ABC):
    @abc.abstractmethod
    def generate(self, definitions: List[Definition]) -> str:
        pass
