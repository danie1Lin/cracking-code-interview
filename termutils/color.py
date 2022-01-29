import os
from abc import abstractmethod
from enum import Enum

RED = "\033[0;31m"
DEEP_COLOR = "\033[0;30m" # black
FGBG = os.environ['COLORFGBG'].split(';')
if len(FGBG) > 1 and FGBG[1] == '0':
    DEEP_COLOR = "\033[1;30m" # gray
NO_COLOR = "\033[0m"

class Color:
    @abstractmethod
    def __str__(self) -> str:
        pass

class C8(Color, Enum):
    Black=30
    Red = 31
    Green = 32
    Yellow = 33
    Blue = 34
    Magenta=35
    Cyan=36
    White=37

    def __str__(self) -> str:
        return f"\033[0;{self.value}m"

class C8Background(Color, Enum):
    Black=40
    Red = 41
    Green = 42
    Yellow = 43
    Blue = 44
    Magenta=45
    Cyan=46
    White=47
    def __str__(self) -> str:
        return f"\033[{self.value}m"

def colorized(s: str, color: Color, background: Color|str=""):
    return f"{color}{background}{s}{NO_COLOR}"
