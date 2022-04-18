from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Tuple, Union, Iterable, cast, Dict, Any, List, Literal

from .align import Alignment
from .ascii import SPACE, BLANK, NEWLINE


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
    text = sprite.text
    text_box = sprite.textbox
    assert(text_box == f"{sprite}")
    '''
    __ascii: str
    padding: str = SPACE
    align: Alignment = Alignment.LEFT
    min_width: int = 0
    min_height: int = 0

    def __repr__(self):
        return self.textbox

    @property
    def text(self) -> str:
        '''getter property for the unpadded text'''
        return self.__ascii 

    @property
    def textbox(self) -> str:
        '''getter property for the aligned and padded sprite text'''
        padded_lines = []
        for line in self.__ascii.splitlines():
            left_margin, right_margin = Sprite.margins(len(line), self.min_width, self.align)
            left_pad, right_pad = (self.padding * left_margin), (self.padding * right_margin)
            padded_lines.append(f"{left_pad}{line}{right_pad}")

        x, y = self.dim
        pad = (self.padding * x)
        height = len(padded_lines)
        if height >= max(y, self.min_height):
            return NEWLINE.join(padded_lines)

        top_margin, bottom_margin = Sprite.margins(height, self.min_height, self.align, vertical=True)
        top_padding, bottom_padding = [pad] * top_margin, [pad] * bottom_margin

        return NEWLINE.join(top_padding + padded_lines + bottom_padding)

    @property
    def dim(self) -> Tuple[int, int]:
        '''width x height dimensions of the unpadded text'''
        lines = self.__ascii.splitlines()
        lines_width = [len(line) for line in lines]
        width = max(lines_width)
        width = max(width, self.min_width)
        height = max(len(lines), self.min_height)

        return width, height

    @property
    def rows(self) -> List[str]:
        '''accessor for aligned/padded sprite text box split into rows'''
        return self.textbox.splitlines()

    @property
    def options(self) -> Dict[str, Any]:
        '''
        accessor for current Sprite formatting options.

        Returns
        -------
        Dict[str, Any] :
            All the dataclass fields/values excluding private ascii text reference

        Usage
        -----
        # Copy the options from one sprite to another
        sprite_1 = Sprite('example', **some_other_sprite.options)
        '''
        return asdict(self, dict_factory = lambda x: {k: v for (k, v) in x if '__ascii' not in k})

    def row(self, index: int) -> str:
        '''
        Accesses a single line from the aligned/padded sprite text

        Parameters
        ----------
        index : int
            The index of the line requested

        Returns
        -------
        str : 
           The requested line if it exists, if not then a blank padded row 
        '''
        try:
            line = self.rows[index]
            return line
        except IndexError:
            x, _ = self.dim
            return self.padding * x

    @staticmethod
    def margins(dim: int, min_dim: int, alignment: Alignment, vertical: bool = False) ->  Tuple[int, int]:
        if dim >= min_dim:
            return 0, 0

        front = alignment.top if vertical else alignment.left
        back = alignment.bottom if vertical else alignment.right

        if front:
            return 0, (min_dim - dim)

        if back:
            return (min_dim - dim), 0

        # center justified
        return int((min_dim - dim) / 2), int((min_dim - dim) / 2) + ((min_dim - dim) %  2)


RecursiveSpriteOperation = Union[Sprite, Iterable['RecursiveSpriteOperation']]
MergeableEdge = Literal[Alignment.RIGHT, Alignment.BOTTOM]
def merge(edge: MergeableEdge, align: Alignment, *sprites: Sprite) -> RecursiveSpriteOperation:
    '''
    Recursively merge a 1D array of Sprites either from left-to-right, or top-to-bottom

    Parameters
    ----------
    edge : MergeableEdge
        The direction in which to append the sprite textboxes
    align : Alignment
        The desired alignment of the final merged Sprite
    sprites : List[Sprite]
        Zero or more sprites to merge
    '''
    if len(sprites) == 0:
        return NullSprite

    if len(sprites) == 1:
        return sprites[0]

    this, next = sprites[0], merge(edge, align, *sprites[1:]) 

    merged_lines = []
    for row, line in enumerate(this.rows):
        adjacent_line = cast(Sprite, next).row(row)
        if Alignment.RIGHT:
            merged_lines.append(f"{line}{adjacent_line}")
        if Alignment.BOTTOM:
            merged_lines += [line, adjacent_line]

    return Sprite(NEWLINE.join(merged_lines), align=align)

NullSprite = Sprite(BLANK, padding=BLANK)
