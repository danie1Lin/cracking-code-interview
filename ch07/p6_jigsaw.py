from types import SimpleNamespace
from typing import Any, NamedTuple, Set, Tuple, Optional
import enum
import unittest
from PIL import Image
import random

class Orientation(enum.Enum):
    Left = 0 
    Up = 1
    Right = 2
    Down = 3
    def degree(self) -> int:
        return 90 * self.value

    def __add__(self, other):
        return self.__class__(( 4 + self.value + other.value ) % 4)

    def __sub__(self, other):
        return self.__class__(( 4 + self.value - other.value ) % 4)

    def opposite(self):
        return self.__class__(self - self.__class__(2))

class Splitable:
    def split(self, n: int) -> list[Any]:
        pass
    
    def turn(self, orientation: Orientation):
        pass

    def paste(self, other, x, y):
        pass

    def show(self):
        pass

class SplitableImage(Splitable):
    def __init__(self, image: Image.Image) -> None:
        self.img = image
        self.w, self.h = image.size

    def split(self, n: int) -> list[Any]:
        res = []
        w, h = self.w / n, self.h / n
        for y in range(n):
            for x in range(n):
                ox, oy = x * w, y * h 
                box = (ox, oy, ox+w, oy+h)
                res.append(self.__class__(self.img.crop(box)))
        return res

    def paste(self, img, box: Tuple[int,int,int,int], rotation=Orientation.Left):
        print(box)
        print(self.img.size)
        print(img.img.size)
        img.img.paste(self.img.rotate(rotation.degree()), box)

    def show(self):
        self.img.show()


class Edge(NamedTuple):
    puzzle: Any
    orientation: Orientation

    def __str__(self) -> str:
        return f'{id(self)} {self.puzzle} {self.orientation}'

class EdgeBinding:
    edges: Set[Edge]
    def __init__(self, *edges):
        self.edges = set(edges)

    def __repr__(self) -> str:
        return f'[bind: {self.edges}]'
    
class PuzzlePiece:
    image: Any
    orientation: Orientation
    edgebindings: list[EdgeBinding|None]
    def __init__(self, image) -> None:
        self.orientation = Orientation(0)
        self.edgebindings = [None] * 4
        self.image = image

    def __repr__(self) -> str:
        return f'{self.image}'

    def bind(self, puzzle, orientation: Orientation):
        left_orientation = orientation - self.orientation
        right_orientation = orientation + Orientation(2) - puzzle.orientation
        e1, e2 = Edge(self, left_orientation),            Edge(puzzle, right_orientation)
        edge_binding = EdgeBinding(e1, e2)
        match self.edgebindings[left_orientation.value]:
            case None:
                self.edgebindings[left_orientation.value] = edge_binding
            case _ as bind:
                bind = self.edgebindings[left_orientation.value]
                assert(e1 in bind.edges)
                assert(e2 in bind.edges)

        if not puzzle.edgebindings[right_orientation.value]:
            puzzle.edgebindings[right_orientation.value] = edge_binding
        else:
            bind = puzzle.edgebindings[right_orientation.value]
            assert(e1 in bind.edges)
            assert(e2 in bind.edges)

        
class Postion(SimpleNamespace):
    x: int
    y: int

class Jigsaw:
    puzzles: list[PuzzlePiece] 
    h: int
    w: int
    def __init__(self, n, img: Optional[Splitable]=None) -> None:
        self.original_img = img
        self.w = self.h = n
        if img:
            imgs = img.split(n)
            self.puzzles = [PuzzlePiece(imgs[i]) for i in range(n*n)]
        else:
            self.puzzles = [PuzzlePiece(i) for i in range(n*n)]
        for x in range(n):
            for y in range(n):
                p = self.puzzle(x, y)
                for i, neighbor in enumerate(self.neighbors(x, y)):
                    if neighbor:
                        p.bind(neighbor, Orientation(i))
    def check_fit(self) -> bool:
        fit = True
        for x in range(self.w):
            for y in range(self.h):
                p = self.puzzle(x, y)
                for i, neighbor in enumerate(self.neighbors(x, y)):
                    if neighbor:
                        fit &= p.edgebindings[i] == neighbor.edgebindings[Orientation(i).opposite().value]
                    else:
                        fit &= p.edgebindings[i] == None
        return fit

    def move(self, old: Postion, new: Postion, turn=Orientation.Left):
        old_idx, new_idx = self.pos_to_idx(old), self.pos_to_idx(new)
        self.puzzles[old_idx].orientation += turn
        self.puzzles[old_idx], self.puzzles[new_idx] = self.puzzles[new_idx], self.puzzles[old_idx]

    def puzzle(self, x, y):
        return self.puzzles[self.pos_to_idx(Postion(x=x, y=y))]

    def neighbors(self, x, y):
        def f(p: Postion|None):
            if not p:
                return None
            return self.puzzle(p.x, p.y)
        return list(map(f, self.neighbor_position(Postion(x=x, y=y))))

    def pos_to_idx(self, p: Postion) -> int:
        if p.y >= self.h:
            raise IndexError(f'{p} exceeds {self.h}X{self.w}')
        return p.x + p.y * self.w

    def neighbor_position(self, p: Postion) -> list[Postion|None]:
        if p.x >= self.w - 1:
            right = None 
            left = Postion(x=p.x - 1, y=p.y)
        elif p.x <= 0:
            left = None 
            right = Postion(x=p.x + 1, y=p.y)
        else:
            right = Postion(x=p.x + 1, y= p.y)
            left = Postion(x=p.x - 1, y=p.y)

        if p.y >= self.h - 1:
            down = None
            up = Postion(x=p.x, y=p.y - 1)
        elif p.y <= 0:
            up = None
            down = Postion(x=p.x, y=p.y + 1)
        else:
            down = Postion(x=p.x, y=p.y + 1)
            up = Postion(x=p.x, y=p.y - 1)
        return [left, up, right, down]

    def fits_with(self, left: Edge, right: Edge) -> bool:
        for p in self.puzzles:
            for edgebinding in p.edgebindings:
                if edgebinding and left in edgebinding.edges and right in edgebinding.edges:
                    return True
        return False

    def random(self):
        random.shuffle(self.puzzles)
        for p in self.puzzles:
            p.orientation += Orientation(random.randint(0, 3))

    def display(self):
        w_pixel, y_pixel = self.original_img.img.size
        w_pixel, y_pixel = round(w_pixel/self.w), round(y_pixel/self.h)
        for y in range(self.h):
            for x in range(self.w):
                box = (x*w_pixel, y*y_pixel, (x+1)*w_pixel, (y+1)*y_pixel)
                p = self.puzzle(x, y)
                p.image.paste(self.original_img, box, p.orientation)
        self.original_img.show()
        

class TestJigsaw(unittest.TestCase):
    def setUp(self) -> None:
        self.jigsaw = Jigsaw(3, SplitableImage(Image.open("dl.jpg")))
        return super().setUp()

    def test_puzzle_count(self):
        self.assertEqual(9, len(self.jigsaw.puzzles))

    def test_puzzle(self):
        self.assertEqual(self.jigsaw.puzzles[4], self.jigsaw.puzzle(1, 1))
        self.assertEqual(self.jigsaw.puzzles[0], self.jigsaw.puzzle(0, 0))

    def test_puzzle_neighbor(self):
        self.assertEqual([self.jigsaw.puzzle(0, 1), self.jigsaw.puzzle(1, 0), self.jigsaw.puzzle(2, 1), self.jigsaw.puzzle(1, 2)], self.jigsaw.neighbors(1, 1))
        self.assertEqual([None, None, self.jigsaw.puzzle(1, 0), self.jigsaw.puzzle(0, 1)], self.jigsaw.neighbors(0, 0))

    def test_puzzle_edge(self):
        p_center = self.jigsaw.puzzle(1, 1)
        edgebindings = p_center.edgebindings
        self.assertEqual(4, len([i for i in edgebindings if i is not None]))
        neighbors = self.jigsaw.neighbors(1, 1)
        for i in range(4):
            self.assertIn(Edge(puzzle=p_center, orientation=Orientation(i)), edgebindings[i].edges)
            self.assertIn(Edge(puzzle=neighbors[i], orientation=Orientation(i).opposite()), edgebindings[i].edges)
        self.assertEqual(Edge(puzzle=p_center, orientation=Orientation.Left), Edge(puzzle=p_center, orientation=Orientation.Left))

    def test_fits_with(self):
        p_center = self.jigsaw.puzzle(1, 1)
        e1 = Edge(p_center, Orientation.Up)
        e2 = Edge(self.jigsaw.puzzle(1, 0), Orientation.Down)
        self.assertTrue(self.jigsaw.fits_with(e1, e2))

    def test_move(self):
        self.assertTrue(self.jigsaw.check_fit())
        p = self.jigsaw.puzzle(1, 1)
        self.jigsaw.move(Postion(x=1, y=1), Postion(x=0, y=0), Orientation.Up)
        self.assertFalse(self.jigsaw.check_fit())
        self.assertEqual(p, self.jigsaw.puzzle(0, 0))
        self.assertEqual(p.orientation, Orientation.Up)
        self.jigsaw.move(Postion(x=0, y=0), Postion(x=0, y=0), Orientation.Up)
        self.assertEqual(p.orientation, Orientation.Right)
        self.assertFalse(self.jigsaw.check_fit())
        self.jigsaw.move(Postion(x=0, y=0), Postion(x=1, y=1), Orientation.Up)
        self.assertTrue(self.jigsaw.check_fit())

class TestJigsawDisplay(unittest.TestCase):
    def setUp(self) -> None:
        self.jigsaw = Jigsaw(4, SplitableImage(Image.open("dl.jpg")))
        return super().setUp()

    def test_display(self):
        self.jigsaw.random()
        self.jigsaw.display()

if __name__ == '__main__':
    unittest.main()
