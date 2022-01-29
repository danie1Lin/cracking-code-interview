# How to charge?
# borrow / buy the reading privilege lifetime?

# 1. Users can buy/borrow book
# 2. Users can read it until the expiry
# 3. The books might not provide buying/borrowing in the same time.
import time
from typing import Dict

def current_time() -> int:
    return int(time.time())

class Book:
    title: str
    ID: int

    def __init__(self, title: str, pages: list[str]) -> None:
        self.pages = pages
        self.title = title

    def total_page(self) -> int:
        return len(self.pages)

    def page(self, n: int) -> str:
        return self.pages[n-1]

class BookReader:
    def __init__(self, book: Book) -> None:
        self.cursor = 1
        self.book = book

    def show(self):
        return self.book.page(self.cursor)

    def next_page(self):
        self.cursor += 1
        if self.cursor > self.book.total_page():
            raise RuntimeError('last page')

    def last_page(self):
        pass

    def jump(self, n):
        if n < 1 or n > self.book.total_page():
            raise RuntimeError('no such page')
        self.cursor = n

class License:
    expiry: int # unix time
    book: Book

    def expired(self) -> bool:
        return current_time() > self.expiry


class BookStore:
    books: list[Book]
    def borrow(self, book: Book, expiry: int) -> License|None:
        pass

    def buy(self, book: Book) -> License|None:
        pass


class User:
    licenses: Dict[int, License] 

    def get_book(self, book_id: int) -> Book:
        license = self.find_license_by_book_id(book_id)
        if not license:
            raise RuntimeError('book not found')
        if license.expired():
            raise RuntimeError('license expires')
        book = license.book
        return book

    def find_license_by_book_id(self, book_id: int) -> License|None:
        pass

    def borrow(self, book: Book, store: BookStore, expiry: int):
        pass

    def buy(self, book: Book, store: BookStore):
        pass

class OnlineBookSystem:
    users: list[User]
    books: Dict[int, Book]
