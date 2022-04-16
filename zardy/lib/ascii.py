from dataclasses import dataclass
from enum import Enum, auto
from typing import Tuple, Optional, cast

from .types import AsciiOperator

class AsciiError(Exception):
    '''
    Namespace for unhandled text operation.
    '''
    pass


BLANK = ''
SPACE = ' '
NEWLINE = '\n'
DEFAULT = '\033[0m'
BOLD = '\033[1m'

class Align(Enum):
    TOP = auto()
    TOPLEFT = auto()
    TOPRIGHT = auto()
    CENTER = auto()
    CENTERLEFT = auto()
    CENTERRIGHT = auto()
    BOTTOM = auto()
    BOTTOMLEFT = auto()
    BOTTOMRIGHT = auto()
    LEFT = auto()
    RIGHT = auto()

    @property
    def left(self) -> bool:
        if self in [Align.TOPLEFT, Align.CENTERLEFT, Align.BOTTOMLEFT]:
            return True
        return False

    @property
    def right(self) -> bool:
        if self in [Align.TOPRIGHT, Align.CENTERRIGHT, Align.BOTTOMRIGHT]:
            return True
        return False

    @property
    def top(self) -> bool:
        if self in [Align.TOP, Align.TOPLEFT, Align.TOPRIGHT]:
            return True
        return False

    @property
    def bottom(self) -> bool:
        if self in [Align.BOTTOM, Align.BOTTOMLEFT, Align.BOTTOMRIGHT]:
            return True
        return False


@dataclass(frozen=True)
class Sprite:
    '''
    ASCII Sprite represents a rectangular area that encloses some ascii text. Sprites
    are immutable to faciliate piecing them together efficiently (copies can share a
    reference)

    Attributes
    ----------
    __ascii : str
        private reference to ascii text to be placed within the sprite.
    padding : str
        provides the background fill. ascii.SPACE makes a transparent box, ascii.BLANK
        collapses the box, and anything else like '.' will create an opaque background

    Usage
    -----
    sprite = Sprite('=(XXXX)=\n  XXXX\n  XXXX\n=(XXXX)=')
    sprite.dim -> 8, 4
    print(f"{sprite}") ->
    =(XXXX)=
      XXXX
      XXXX
    =(XXXX)=
    '''
    __ascii: str
    padding: str = SPACE
    align: Align = Align.LEFT

    @property
    def padded_string(self) -> str:
        lines = self.__ascii.splitlines()
        padded_lines = []
        x, _ = self.dim
        for line in lines:
            this_x = len(line)
            if this_x < x:
                sep = self.padding * (x - this_x)
                if self.align.right:
                    padded_lines.append(f"{sep}{line}")
                elif self.align.left:
                    padded_lines.append(f"{line}{sep}")
                else:
                    padded_lines.append(line)
            else:
                padded_lines.append(line)

        return '\n'.join(line for line in padded_lines)

    @property
    def dim(self) -> Tuple[int, int]:
        lines = self.__ascii.splitlines()
        lines_width = [len(line) for line in lines]
        width = max(lines_width)
        height = len(lines)

        if len(set(lines_width)) > 1 and not(self.align.left or self.align.right):
            raise AsciiError(f'Misaligned ASCII sprite: unequal line widths '
                    'without left/right alignment given!')

        return width, height

    @property
    def rows(self) -> list[str]:
        return f"{self}".splitlines()

    def row(self, index: int, padding: Optional[str] = None) -> str:
        try:
            line = self.rows[index]
            return line
        except IndexError:
            if padding:
                x, _ = self.dim
                return cast(str, padding) * x

        return ''  # Should be unreachable, needed for type annotations


    def __repr__(self):
        return self.padded_string


def merge(*sprites: Sprite) -> AsciiOperator:
    if len(sprites) == 0:
        return Sprite(BLANK)

    if len(sprites) == 1:
        return sprites[0]

    this, next = sprites[0], merge(*sprites[1:]) 

    merged_lines = []
    for row, line in enumerate(this.rows):
        adjacent_line = cast(Sprite, next).row(row, SPACE)
        merged_lines.append(f"{line}{adjacent_line}")

    return Sprite(NEWLINE.join([line for line in merged_lines]), align=this.align)
