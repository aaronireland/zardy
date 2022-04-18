from enum import Enum, auto

class Alignment(Enum):
    TOPLEFT = auto()
    LEFT = auto()
    BOTTOMLEFT = auto()

    TOPRIGHT = auto()
    RIGHT = auto()
    BOTTOMRIGHT = auto()

    TOP = auto()
    CENTER = auto()
    BOTTOM = auto()

    @classmethod
    def list(cls):
        return list(map(lambda c: c, cls))

    @property
    def left(self) -> bool:
        if self in [Alignment.TOPLEFT, Alignment.LEFT, Alignment.BOTTOMLEFT]:
            return True
        return False

    @property
    def center(self) -> bool:
        if self in [Alignment.TOP, Alignment.CENTER, Alignment.BOTTOM]:
            return True
        return False

    @property
    def right(self) -> bool:
        if self in [Alignment.TOPRIGHT, Alignment.RIGHT, Alignment.BOTTOMRIGHT]:
            return True
        return False

    @property
    def top(self) -> bool:
        if self in [Alignment.TOPLEFT, Alignment.TOP, Alignment.TOPRIGHT]:
            return True
        return False

    @property
    def middle(self) -> bool:
        if self in [Alignment.LEFT, Alignment.CENTER, Alignment.RIGHT]:
            return True
        return False

    @property
    def bottom(self) -> bool:
        if self in [Alignment.BOTTOMLEFT, Alignment.BOTTOM, Alignment.BOTTOMRIGHT]:
            return True
        return False
