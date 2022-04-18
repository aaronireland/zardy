from typing import Mapping, cast

from ..align import Alignment
from ..ascii import AsciiError, SPACE
from ..sprites import Sprite, merge

MIN_PADDING = 1

def err(msg: str) -> str:
    return f"ASCII border misconfigured: {msg}"


class Border:
    def __init__(self, sprites: Mapping[Align, Sprite]):
        try:
            self.top_left = sprites[Align.TOPLEFT]
            self.top_right = sprites[Align.TOPRIGHT]
            self.bottom_left = sprites[Align.BOTTOMLEFT]
            self.bottom_right = sprites[Align.BOTTOMRIGHT]
        except KeyError:
            raise AsciiError(err("all four corners are required"))
       
        top = sprites.get(Align.TOP)
        bottom = sprites.get(Align.BOTTOM)

        if not(top or bottom):
            raise AsciiError(err("missing top and bottom sprites"))

        self.top = cast(Sprite, top or bottom)
        self.bottom = cast(Sprite, bottom or top)

        top_x, _ = self.top.dim
        bottom_x, _ = self.bottom.dim

        if top_x != bottom_x:
            raise AsciiError(f"top and bottom sprites must match widths, {top_x} != {bottom_x}")


        left = sprites.get(Align.LEFT)
        right = sprites.get(Align.RIGHT)

        if not(left or right):
            raise AsciiError(err("missing left and right sprites"))

        self.left = cast(Sprite, left or right)
        self.right = cast(Sprite, right or left)

        _, left_y = self.left.dim
        _, right_y = self.right.dim

        if left_y != right_y:
            raise AsciiError(err(f"left and right sprites must match heigths, {left_y} != {right_y}"))

    def __call__(self, text: str, align: Align = Align.LEFT, fill: str = SPACE) -> Sprite:

        if len(fill) != 1:
            fill = SPACE
        # Align the text within the inner text box, centered not supported
        text_box = Sprite(text, align=Align.RIGHT if align.right else Align.LEFT)
        text_width, text_height = text_box.dim
        h_sprite_width, _ = self.top.dim
        _, v_sprite_height = self.left.dim

        margin, margins = MIN_PADDING, (MIN_PADDING * 2)
        inner_width = int((text_width + margins) / h_sprite_width) + 1
        inner_height = int((text_height + margins)/ v_sprite_height) + 1

        h_buffer = int(inner_width * h_sprite_width) - text_width
        v_buffer = int(inner_height * v_sprite_height) - text_height

        if align.top:
            top_margin = fill * margin
            bottom_margin = fill * (v_buffer + margin)
        elif align.bottom:
            top_margin = fill * (v_buffer + margin)
            bottom_margin = fill * margin
        else:  # align center
            top_margin = fill * (int(v_buffer / 2) + margin)
            bottom_margin = fill * (int(v_buffer / 2) + margin + (0 if v_buffer % 2 == 0 else 1))

        if align.left:
            left_margin = fill * margin
            right_margin = fill * (h_buffer + margin)
        elif align.right:
            left_margin = fill * (h_buffer + margin)
            right_margin = fill * margin
        else:  # align center
            left_margin = fill * (int(h_buffer / 2) + margin)
            right_margin = fill * (int(h_buffer / 2) + margin + (0 if h_buffer % 2 == 0 else 1))

        top = [self.top_left] + [self.top] * inner_width + [self.top_right]
        top_line = merge(*top)

        bottom = [self.bottom_left] + [self.bottom] * inner_width + [self.bottom_right]
        bottom_line = merge(*bottom)

        
        rendered_border = NEWLINE.join(f"{line}" for line in [top_line, bottom_line])
        return Sprite(rendered_border, align=align)
