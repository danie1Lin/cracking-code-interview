from abc import abstractmethod
import asyncio
import enum
import math
import os
import time
import random
import sys
from types import SimpleNamespace
from typing import Tuple
import unittest
from dataclasses import dataclass
from termutils import mouse
from termutils.color import C8, DEEP_COLOR, C8Background, colorized
from termutils.mouse import MouseEvent, MouseEventType

def get_size():
    size = os.get_terminal_size(sys.stdin.fileno()) 
    return size.columns, size.lines

@dataclass
class BoardCommand:
    command: str
    x: int
    y: int
    @classmethod
    def parse(cls, raw_cmd: str):
        command, x, y = "", 0, 0
        parts = raw_cmd.split(" ")
        if not parts:
            raise ValueError(f"invalid command {raw_cmd}")
        match len(parts):
            case 1:
                command = parts[0]
            case 2:
                x = int(parts[1])
                y = int(parts[0])
            case 3:
                x = int(parts[1])
                y = int(parts[0])
                command = parts[2]
        return cls(command, x, y)

    @classmethod
    def from_mouse_event(cls, event: mouse.MouseEvent):
        match event.action:
            case MouseEventType.press:
                return cls("", event.x, event.y)
            case MouseEventType.shift_press:
                return cls("", event.x, event.y)

class GameState(enum.Enum):
    Init = 0
    Start = 1
    End = 2

class BaseBoardGame:
    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def execute(self, cmd: BoardCommand):
        pass

    @abstractmethod
    def get_info(self) -> str:
        pass

    @abstractmethod
    def get_input_box(self) -> str:
        pass

    @abstractmethod
    def str(self, x: int, y: int):
        pass

    @abstractmethod
    def get_height(self) -> int:
        pass

    @abstractmethod
    def get_width(self) -> int:
        pass

    @abstractmethod
    def get_state(self) -> GameState:
        pass

# Cell 
# status: hidden/shown
# when shown, have to calculate the mine around them or it is the bomb 
class Cell(SimpleNamespace):
    shown: bool
    is_bomb: bool
    is_noted: bool

    @classmethod
    def default(cls):
        return cls(is_shown=False, is_bomb=False, is_noted=False)

    def open(self):
        self.is_shown = True

    def note_as_bomb(self):
        self.is_noted = True
# Board
# init to random generate cell
class Board(BaseBoardGame):
    def __init__(self, n: int, num_bomb: int) -> None:
        self.n = n
        self.num_bomb = num_bomb
        self.init()

    def init(self):
        self.last_command = None
        self.cells = []
        self.state = GameState.Init
        for y in range(self.n):
            self.cells.append([])
            for x in range(self.n):
                self.cells[y].append(Cell.default())
        self.random()
        self.start_time = None

    def get_state(self) -> GameState:
        return self.state

    def get_info(self) -> str:
        match self.state:
            case GameState.Init:
                return f"Ready?"
            case GameState.Start:
                return f"{self.state.name} {self.last_command} {round(time.time() - self.start_time, 3)}"
            case GameState.End:
                return f"{self.result}!, took {round(self.end_time - self.start_time, 3)}s"

    def get_input_box(self) -> str:
        return "Left Click to open a cell, ⇧ + Left Click to note a cell as bomb"

    def random(self):
        n = self.num_bomb
        while n > 0:
            p = [random.randint(0, self.n-1) for _ in range(2)]
            cell = self.get_cell(p[0], p[1])
            if cell.is_bomb:
                continue
            cell.is_bomb = True
            n -= 1

    def execute(self, cmd: BoardCommand):
        if self.state is GameState.Init:
            self.state = GameState.Start
            self.start_time = time.time()
        self.last_command = cmd
        match cmd.command:
            case "":
                self.click(cmd.x, cmd.y)
            case "n":
                self.note(cmd.x, cmd.y)
        self.check_result()

    def check_result(self):
        if self.is_win():
            self.state = GameState.End
            self.end_time = time.time()
            self.result = "WIN"
        if self.is_lose():
            self.state = GameState.End
            self.end_time = time.time()
            self.result = "LOSE"
        if self.is_win() or self.is_lose():
            for line in self.cells:
                for cell in line:
                    cell.open()

    def is_win(self):
        for line in self.cells:
            for cell in line:
                if cell.is_bomb and not cell.is_noted:
                    return False
                if not cell.is_bomb and not cell.is_shown:
                    return False
        return True

    def is_lose(self):
        for line in self.cells:
            for cell in line:
                if cell.is_bomb and cell.is_shown:
                    return True
        return False

    def note(self, x: int, y: int):
        cell = self.get_cell(x, y)
        if cell.is_shown:
            raise RuntimeError("already openned")
        cell.is_noted = not cell.is_noted

    def click(self, x: int, y: int):
        # check x y
        # if not bomb show number of bombs around
        # if number of bombs around is zero than open zero bombs around too.
        cell = self.get_cell(x, y)
        if cell.is_noted:
            raise RuntimeError("can not open noted cell")
        cell.open()
        if not cell.is_bomb and self.calcutate_bomb_around(x, y) == 0:
            for tmp_x in range(max(0, x-1), min(self.n, x+2)):
                for tmp_y in range(max(0, y-1), min(self.n, y+2)):
                    cell = self.get_cell(tmp_x, tmp_y)
                    if not cell.is_shown and not cell.is_bomb:
                        self.click(tmp_x, tmp_y)

    def get_cell(self, x: int, y: int) -> Cell:
        return self.cells[y][x]

    def get_width(self) -> int:
        return self.n

    def get_height(self) -> int:
        return self.n

    def calcutate_bomb_around(self, x: int, y: int) -> int:
        count = 0 
        for check_x in range(max(0, x-1),min(x+2, self.n)):
            for check_y in range(max(0, y-1), min(y+2, self.n)):
                if self.get_cell(check_x, check_y).is_bomb:
                    count += 1
        return count

    def str(self, x: int, y: int):
        cell = self.get_cell(x, y)
        if cell.is_noted:
            return "✽"
        elif not cell.is_shown:
            return "▩"
        elif cell.is_bomb:
            return colorized(" ☠ ", C8.Black, C8Background.Cyan)
        else:
            num = self.calcutate_bomb_around(x, y)
            if num == 0:
                return " "
            else:
                return str(num)

# TextDisplay 
# call board.str(x, y)-> numeric / ? / * (bomb)
class TextDisplayController:
    def __init__(self, board: BaseBoardGame, loop=None) -> None:
        self.background = C8Background.Cyan  
        self.border = C8Background.Blue  
        self.board = board
        self.cell_content_len = 1 
        self.left_padding = int(math.log10(self.board.get_height()) + 1)
        if loop:
            self.loop = loop
        else:
            self.loop = asyncio.get_event_loop()
        self.reader_writer = mouse.MouseEventProxy(mouse.Stdio(self.loop))
        self.mouse_event_getter = self.reader_writer 


    @property
    def cell_width(self):
        return self.cell_content_len + 3 
    
    @property
    def cell_height(self):
        return self.cell_content_len + 1 

    def board_view(self)->str:
        width, height = self.board.get_width(), self.board.get_height()
        right_border = colorized(" " * (self.left_padding + 1), "", self.border)
        left_space = colorized(" " * (self.left_padding + 1), "", self.border)
        corner = colorized("+", C8.Blue, self.background)
        row_boundary_unit = colorized("-" * (self.cell_content_len+2), C8.Blue, self.background)
        col_boundary_unit = colorized("|", C8.Blue, self.background)
        row_boundary = left_space + corner + (row_boundary_unit+corner) * width  + right_border 
        res = "\n"
        res += left_space + colorized(" ", "", self.border)
        for c in range(width):
            res += colorized(f"{str(c).center(self.cell_width)}", "", self.border)
        res += right_border + "\n"
        for y in range(height):
            res += row_boundary
            res += "\n"
            res += colorized(f"{y:^{self.left_padding + 1}}", "", self.border)
            for x in range(width):
                res += col_boundary_unit 
                res += colorized(f"{self.board.str(x, y):^{self.cell_content_len+2}}", C8.White, self.background)
            res += col_boundary_unit + right_border + "\n"
        res += row_boundary
        res += "\n" + left_space + colorized(" " * (width * (self.cell_width)+1), "", self.border ) + right_border
        return res

    def receive_mouse_event(self, event: mouse.MouseEvent):
        x, y = self.transform_from_terminal(event.x, event.y)
        match event.action:
            case MouseEventType.press: 
                self.board.execute(BoardCommand("", x, y))
            case MouseEventType.shift_press: 
                self.board.execute(BoardCommand("n", x, y))

    def transform_from_terminal(self, x: int, y: int) -> Tuple[int, int]:
        _, h = get_size()
        x = (x - self.cell_content_len - 2) // self.cell_width
        upper_space = h - len(self.screen.split("\n"))
        y = (y - upper_space) // self.cell_height - 1
        return x, y

    @property
    def screen(self) -> str:
        return "\n".join([self.board_view(), self.board.get_info(), self.board.get_input_box()]) + "\n"

    @property
    def clear_control_sequence(self):
        return '\033[2J' 

    async def init(self):
        await self.mouse_event_getter.init()

    async def show(self):
        while True:
            self.reader_writer.write(self.clear_control_sequence + self.screen)
            await asyncio.sleep(0.3)

    async def main(self):
        while True:
            try:
                await self.mouse_event_getter.process_event(self.receive_mouse_event)
                state = self.board.get_state()
                match state:
                    case GameState.End:
                        await self.mouse_event_getter.process_event(lambda _: None)
                        await self.mouse_event_getter.process_event(lambda _: None)
                        self.board.init()
            except Exception as e:
                self.reader_writer.write(bytearray(f"{e}",encoding="utf8"))
                await self.mouse_event_getter.process_event(lambda _: None)


    def run(self):
        tasks = []
        self.loop.run_until_complete(self.init())
        tasks.append(self.reader_writer.run())
        tasks.append(self.main())
        tasks.append(self.show())
        self.loop.run_until_complete(asyncio.gather(*tasks))

class TestBoardGame(unittest.TestCase):
    def setUp(self):
        self.board = Board(8, 4)
        self.display = TextDisplayController(self.board)

    def test_receive_command(self):
        self.board.cells[0][1].is_bomb = True
        self.board.execute(BoardCommand.parse("0 1"))
        self.assertEqual(True, self.board.cells[0][1].is_bomb)
        self.assertEqual(True, self.board.cells[0][1].is_shown)

    def test_disclose_around(self):
        self.board.cells[3][3].is_bomb = True
        self.board.click(0, 0)
        self.assertEqual(True, self.board.cells[0][0].is_shown)
        self.assertEqual(True, self.board.cells[1][1].is_shown)
        self.assertEqual(True, self.board.cells[2][2].is_shown)
        self.assertEqual(False, self.board.cells[3][3].is_shown)

    def test_calculate_bomb(self):
        self.board.cells[0][1].is_bomb = True
        self.assertEqual(1, self.board.calcutate_bomb_around(0, 0))


    def test_display(self):
        print(self.display.screen)
        cell = self.board.cells[-1][-1]
        cell.is_shown = True 
        print(self.display.screen)
        cell.is_bomb = True 
        print(self.display.screen)
        cell.is_shown = False
        cell.is_noted = True
        print(self.display.screen)

if __name__ == '__main__':
    #unittest.main()
    
    n, bomb = 10, 10 
    board = Board(n, bomb)
    board.random()
    display = TextDisplayController(board)
    display.run()
