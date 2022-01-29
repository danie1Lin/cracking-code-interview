
# https://invisible-island.net/xterm/ctlseqs/ctlseqs.html#h3-Normal-tracking-mode
# MOUSE EVENT
import asyncio
from dataclasses import dataclass
import enum
from functools import singledispatch
from os import read
import os
import sys
import termios
import atexit
from types import FunctionType
from typing import Any, Callable
from overload import overload
import itertools


OPEN = "h" 
CLOSE = "l" 
MOUSE_CLICK = "\033[?1000"

def get_terminal_attr():
    fd = sys.stdin.fileno()
    return termios.tcgetattr(fd)

def set_terminal_attr(attr):
    termios.tcsetattr(fd, termios.TCSADRAIN, attr)

def get_mouse_event(loop):
    fd = sys.stdin.fileno()
    old_attr = get_terminal_attr()
    new = get_terminal_attr()
    print(MOUSE_CLICK+OPEN)
    new[3] = new[3] & ~(termios.ECHO|termios.ICANON)          # lflags
    q = asyncio.Queue(maxsize=100)
    reader = asyncio.StreamReader()
    protocol = asyncio.StreamReaderProtocol(reader)
    def reset():
        termios.tcsetattr(fd, termios.TCSADRAIN, old_attr)
        print(MOUSE_CLICK+CLOSE)
    async def task():
        await loop.connect_read_pipe(lambda: protocol, sys.stdin)
        termios.tcsetattr(fd, termios.TCSADRAIN, new)
        atexit.register(reset)
        buf = bytearray()
        try:
            async def read():
                while True:
                    read_byte = await reader.read(1)
                    buf.extend(read_byte)
            async def cleanup():
                while True:
                    await asyncio.sleep(0.3)
                    if len(buf) == 0:
                        continue
                    first = buf.find(b"\x1b[")
                    mouse_event_length = 6 
                    if first >= 0:
                        event = MouseEvent.from_byte(buf[first:])
                        if event:
                            await q.put(event)
                    buf.clear()
            await asyncio.gather(cleanup(), read())
        finally:
            reset()
    return loop.create_task(task()), q


class MouseEventType(enum.Enum):
    press = ord(" ")
    release = ord("#")
    shift_press = ord("$")
    shift_release = ord("'")

@dataclass
class MouseEvent:
    action: MouseEventType
    x: int
    y: int
    @classmethod
    def from_byte(cls, b: bytearray):
        if len(b) < 6:
            return
        if int(b[3]) in [i.value for i in MouseEventType.__members__.values()]:
            return MouseEvent(MouseEventType(int(b[3])), b[4]-33, b[5]-33)

def get_protocol():
    reader = asyncio.StreamReader()
    return asyncio.StreamReaderProtocol(reader)

class Stdio:
    def __init__(self, loop=None) -> None:
        if loop:
            self.loop = loop
        else:
            self.loop = asyncio.get_event_loop()
        self.reader = None

    async def init_writer(self):
        transport, protocol = await self.loop.connect_write_pipe(asyncio.BaseProtocol, sys.stdout)
        self.writer = asyncio.StreamWriter(transport=transport, protocol=protocol, reader=None, loop=self.loop)

    async def init_reader(self):
        self.reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(self.reader)
        await self.loop.connect_read_pipe(lambda: protocol, sys.stdin)

    def write(self, data):
        self.writer.write(data)

    async def read(self, n):
        if not self.reader:
            await self.init_reader()
        return await self.reader.read(n)

class MouseEventProxy:
    def __init__(self, read_writer: Stdio) -> None:
        self.read_writer = read_writer
        self.mouse_event_queue = asyncio.Queue[MouseEvent](maxsize=100)
        self.read_data_queue = asyncio.Queue[int](maxsize=100)

    async def init(self):
        self.setup_terminal()
        await asyncio.gather(self.read_writer.init_reader(), self.read_writer.init_writer())
        self.write(bytearray(MOUSE_CLICK+OPEN, encoding="utf8"))
        atexit.register(self.reset)

    def reset(self):
        termios.tcsetattr(self.stdin_fd, termios.TCSADRAIN, self.old_terminal_attr)
        self.write(bytearray(MOUSE_CLICK+CLOSE, encoding="utf8"))

    def setup_terminal(self):
        self.stdin_fd = sys.stdin.fileno()
        self.old_terminal_attr = termios.tcgetattr(self.stdin_fd)
        new = termios.tcgetattr(self.stdin_fd)
        new[3] = new[3] & ~(termios.ECHO|termios.ICANON)          # lflags
        termios.tcsetattr(self.stdin_fd, termios.TCSADRAIN, new)

    async def run(self):
        await self.init()
        await self.main()

    async def main(self):
        buf = bytearray()
        async def read():
            while True:
                read_byte = await self.read_writer.read(1)
                buf.extend(read_byte)
        async def cleanup():
            while True:
                await asyncio.sleep(0.5)
                if len(buf) == 0:
                    continue
                first = buf.find(b"\x1b[")
                mouse_event_length = 6 
                if first >= 0:
                    event = MouseEvent.from_byte(buf[first:first+mouse_event_length])
                    if event:
                        await self.mouse_event_queue.put(event)
                # for byte in itertools.chain(buf[:first], buf[first+mouse_event_length:]):
                    # if self.read_data_queue.full():
                        # await self.read_data_queue.get()
                    # await self.read_data_queue.put(byte)
                buf.clear()
        await asyncio.gather(cleanup(), read())

    @overload
    def write(self, data: str):
        self.read_writer.write(bytearray(data, encoding="utf8"))

    @write.add
    def write(self, data: bytearray|bytes):
        self.read_writer.write(data)

    async def process_event(self, f: Callable[[MouseEvent], Any]):
        try:
            event = await self.mouse_event_queue.get() 
            f(event)
        finally:
            self.mouse_event_queue.task_done()

    async def read(self, n: int):
        data = bytearray()
        for i in range(n):
            data[i]
            data.append(await self.read_data_queue.get())
            self.mouse_event_queue.task_done()
        return data


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    task, q = get_mouse_event(loop)
    async def p():
        while True:
            b = await q.get()
            print("echo:", b)
            q.task_done()
    loop.run_until_complete(asyncio.gather(task, p()))
