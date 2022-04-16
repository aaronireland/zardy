from typing import Iterable, Union
from .ascii import Sprite

AsciiOperator = Union[Sprite, Iterable['AsciiOperator']]
