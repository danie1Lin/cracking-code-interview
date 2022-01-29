from collections import defaultdict
import enum
import random
from typing import DefaultDict, Dict, Optional, Tuple
import unittest
class Side(enum.Enum):
    White = 0
    Black = 1 

    def opposite(self):
        return self.__class__(1^self.value)

    def __str__(self) -> str:
        if self.value == 1:
            return "◎"
        return "●"

class Piece:
    side: Side 

    def __init__(self, side: Side) -> None:
        self.side = side

    def flip(self):
        self.side = self.side.opposite()

    def __repr__(self) -> str:
        return f'Piece({self.side})'

class Board:
    board: list[list[Optional[Piece]]]
    n: int

    def __init__(self, n: int=8) -> None:
        if n % 2 != 0:
            raise ValueError('n should be even.')
        self.n = 8 
        self.board = []
        center = int(self.n / 2)
        for x in range(n):
            self.board.append([])
            for y in range(n):
                self.board[x].append(None)
        self.board[center][center] = Piece(Side.White)
        self.board[center-1][center-1] = Piece(Side.White)
        self.board[center][center-1] = Piece(Side.Black)
        self.board[center-1][center] = Piece(Side.Black)

    def place(self, piece: Piece, x: int, y: int):
        if self.board[x][y]:
            raise RuntimeError(f'({x}, {y}) had already been placed.')
        postion_to_flip = self.can_flip_around(piece.side, x, y)
        if not postion_to_flip:
            raise RuntimeError('please capture at least one')
        self.board[x][y] = piece
        for p in postion_to_flip:
            self.flip(p[0], p[1])

    def can_flip_around(self, side: Side, x: int, y: int) -> list[Tuple[int, int]]:
        to_post_pieces = defaultdict[Tuple[int,int], list[Piece]](lambda: [])
        if x < self.n - 2:
            temp_x = x + 1
            for x1 in range(x+1, x+3):
                if not self.board[x1][y]:
                    break
                to_post_pieces[(temp_x, y)].append(self.board[x1][y])
        if x > 1:
            temp_x = x - 1
            for x1 in range(x-1, x - 3, -1):
                if not self.board[x1][y]:
                    break
                to_post_pieces[(temp_x, y)].append(self.board[x1][y])
        if y < self.n - 2:
            tmp_y = y + 1
            for y1 in range(y+1, y+3):
                if not self.board[x][y1]:
                    break
                to_post_pieces[(x, tmp_y)].append(self.board[x][y1])
        if y > 1:
            tmp_y = y - 1
            for y1 in range(y-1, y - 3, -1):
                if not self.board[x][y1]:
                    break
                to_post_pieces[(x, tmp_y)].append(self.board[x][y1])
        res = []
        for pos, pieces in to_post_pieces.items():
            if len(pieces) < 2:
                continue
            if pieces[0].side == side.opposite() and pieces[1].side == side:
                res.append(pos)
        return res

    def placable_position(self, side: Side) -> list[Tuple[int, int]]:
        res = []
        for x, line in enumerate(self.board):
            for y, p in enumerate(line):
                if not p and self.can_flip_around(side, x, y):
                    res.append((x, y))
        return res 

    def score(self) -> Dict[Side, int]:
        res = DefaultDict(lambda: 0)
        for line in self.board:
            for p in line:
                if p:
                    res[p.side] += 1
        return res


    def flip(self, x, y):
        if self.board[x][y]:
            self.board[x][y].flip()

    def __str__(self):
        left_space = " " * 1
        res = "\n"
        res += left_space + " "
        for c in range(ord("A"), ord("A")+self.n):
            res += f"{chr(c).center(4)}"
        res += "\n"
        for i, line in enumerate(self.board):
            res += left_space
            res += "+"
            res += "---+" * self.n
            res += "\n"
            res += f"{i}" 
            for piece in line:
                res += "|"
                match piece:
                    case None:
                        res += "   "
                    case Piece(side=x) if x == Side.Black:
                        res += " ◎ "
                    case Piece(side=x) if x == Side.White:
                        res += " ● "
            res += "|"
            res += "\n"
        res += left_space + "+"
        res += "---+" * self.n
        return res

class TestOthello(unittest.TestCase):
    def setUp(self):
        self.game = Board()

    def test(self):
        self.game.place(Piece(Side.White), 2, 4)
        self.assertEqual(self.game.board[3][4].side, Side.White)

    def test_display(self):
        print(self.game)

def pos_to_represent(p):
    return f'{p[0]}{chr(p[1] + ord("A"))}'


class Game:
    def __init__(self) -> None:
        self.board = Board()
        self.turn = Side.White
        self.automode = DefaultDict(lambda: False)
        self.warn = ""
        self.skipped = False

    def refresh(self):
        print('\033c')
        print(self.board)

    def run(self):
        while True:
            try:
                self.refresh()
                print(self.warn)
                print(f"It's {self.turn} turn, enter the postion or pass using empty:", end="")
                placing_pos = None
                if not self.automode[self.turn]:
                    pos = input("")
                    pos = pos.strip()
                    match pos:
                        case "":
                            pass
                        case "a":
                            self.automode[self.turn] = True
                        case _:
                            placing_pos = (int(pos[0]), ord(pos[1]) - ord("A"))
                if self.automode[self.turn]:
                    p = self.board.placable_position(self.turn)
                    if p:
                        placing_pos = p[random.randint(0, len(p) - 1)]
                        print(pos_to_represent(placing_pos))
                if placing_pos:
                    self.board.place(Piece(self.turn), *placing_pos)
                    self.skipped = False
                elif self.skipped:
                    print("no placable position")
                    break
                else:
                    self.skipped = True
                self.turn = self.turn.opposite()
                self.warn = ""
            except Exception as e:
                self.warn = str(e)

    def print_score(self):
        print("Result: ", end="")
        score_info = self.board.score()
        if score_info[Side.White] > score_info[Side.Black]:
            print(Side.White, "wins")
        elif score_info[Side.White] < score_info[Side.Black]:
            print(Side.Black, "wins")
        else:
            print("Even")
        for side, score in score_info.items():
            print(side, score)

if __name__ == '__main__':
    game = Game()
    game.run()
    game.print_score()

