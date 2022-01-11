# Question
# How many songs?
# How many users in the same time?
# How to charge? You can pcik any sony you want in the limit time? Or, A pick a limit amount of songs a time? Or, both / Many?
# How user pick song? searching by what? Ranking? Artist? Title? Album?
# user stroy:
# 1. User picks a charge model
# 2. After begin, user can pick song to (1)the next/(2)right now(cut off the playing song)/(3) last song in the playing list.
# 3. If there is out of quota(time/songs) then stopping and going to first step.
import sys
from types import SimpleNamespace
from typing import Any, Deque, Generic, Tuple
import typing
from enum import Enum
import asyncio
import os
import termios

class Song:
    content: Any
    duration: int
    title: str
    Album: str
    Singer: str
    def __init__(self, title, duration) -> None:
        self.title = title
        self.duration = duration

    def __str__(self) -> str:
        return f'Song(Title: {self.title})'

class Playlist:
    songs: list[Song]
    playing: Song | None
    playing_cursor: int
    def __init__(self) -> None:
        self.songs = []
        self.playing = None
        self.playing_cursor = 0

    def queue(self, song):
        self.songs.append(song)

    def play(self):
        if self.playing == None or self.playing_cursor > self.playing.duration:
            raise RuntimeError("end of song")
        self.playing_cursor += 1

    def out_of_song(self) -> bool:
        return len(self.songs) == 0

    def play_next(self):
        self.playing = self.songs.pop()
        if self.playing == None:
            raise RuntimeError("Out of the song")
        self.playing_cursor = 0

class Usage(SimpleNamespace):
    song: int
    duration: int

    def reset(self):
        self.song = 0
        self.duration = 0

    def __mul__(self, other: int):
        new = self.__class__()
        new.song = self.song * other
        new.duration = self.duration * other
        return new

    def __ge__(self, other):
        return self.song >= other.song and self.duration >= other.duration

TUsage = typing.TypeVar('TUsage', bound='Usage')
class ChargeStrategy(Generic[TUsage]):
    price_per_unit = 10
    limit_per_unit: TUsage

    @classmethod
    def from_mony(cls, money: int) -> Tuple[Any, int]:
        return cls(money // cls.price_per_unit), money % cls.price_per_unit  

    def __init__(self, unit: int) -> None:
        self.unit = unit

    def is_enough(self, usage: Usage) -> bool:
        return self.limit_per_unit * self.unit >= usage

class DefaultChargeStrategy(ChargeStrategy):
    limit_per_unit = Usage()
    limit_per_unit.song = 10
    limit_per_unit.duration = 10

class JukeboxState(Enum):
    Init = 1
    Charged = 2
    OutOfQuota = 3

class Operation:
    def __init__(self, op_type: str, song: Song|None) -> None:
        self.op_type = op_type
        self.song = song

    def __repr__(self) -> str:
        return f'Op({self.op_type} {self.song})'

class Jukebox:
    state: JukeboxState
    strategy: ChargeStrategy
    songs: list[Song]
    playlist: Playlist
    def __init__(self) -> None:
        self.charge_strategy_cls = DefaultChargeStrategy 
        self.playlist = Playlist()
        self.usage = Usage()
        self.usage.reset()
        self.operations = asyncio.Queue[Operation](100) 
        self.typing_cmd = ""
        self.message = ""
        self.back = 0

    def pay(self, price):
        self.strategy, change = self.charge_strategy_cls.from_mony(price)
        return change

    def search_by(self, attr: str, query: str)-> list[Song]:
        pass

    async def operate(self, operation: Operation):
        await self.operations.put(operation)

    def __str__(self):
        return f'>{self.typing_cmd}\n{self.message}\nquota {self.strategy.limit_per_unit * self.strategy.unit} \nused {self.usage}\noperations {self.operations}\nplaylist {self.playlist.playing} {self.playlist.playing_cursor}'

    async def show(self):
        while True:
            print('\033c')
            screen = str(box)
            print(screen)
            await asyncio.sleep(1)



    async def deal_operation(self):
        while True:
            op = await self.operations.get()
            match op.op_type:
                case 'append':
                    self.playlist.songs.append(op.song)
                case 'insert':
                    self.playlist.songs.insert(0, op.song)
                case 'cut_off':
                    self.usage.song += 1
                    self.playlist.play_next()
                case _:
                    self.message = f'unsupported operation {op}'
            self.operations.task_done()

    async def run(self):
        while True:
            play = self.play()
            one = asyncio.sleep(1)
            await asyncio.gather(play, one)
            if not self.strategy.is_enough(self.usage):
                return

    async def play(self):
        self.usage.duration += 1
        try:
            self.playlist.play()
        except RuntimeError:
            if not self.playlist.out_of_song():
                self.playlist.play_next()
                self.usage.song += 1

if __name__ == '__main__':
    box = Jukebox()
    box.pay(30)
    for i in range(5):
        print()
    async def get_cmd():
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocal = asyncio.StreamReaderProtocol(reader)

        # not work
        #os.system("stty -echo")
        buf = bytearray() 
        await loop.connect_read_pipe(lambda: protocal, sys.stdin)
        while True:
            fd = sys.stdin.fileno()
            old = termios.tcgetattr(fd)
            new = termios.tcgetattr(fd)
            new[3] = new[3] & ~(termios.ECHO|termios.ICANON)          # lflags
            try:
                termios.tcsetattr(fd, termios.TCSADRAIN, new)
                read_byte = await reader.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old)
            buf.extend(read_byte)
            box.typing_cmd = buf.decode('utf-8')
            if read_byte == b'\n':
                line = box.typing_cmd 
                box.typing_cmd = ""
                buf = bytearray() 
                cmd = line.split(" ")
                song = None
                if len(cmd) >= 3:
                    song = Song(cmd[1], int(cmd[2]))
                await box.operate(Operation(cmd[0], song))

    async def main():
        await asyncio.gather(get_cmd(), box.run(), box.show(), box.deal_operation())

    asyncio.run(main())



