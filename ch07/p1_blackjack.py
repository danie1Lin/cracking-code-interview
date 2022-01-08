import unittest

import enum

import random

from types import SimpleNamespace

from typing import NamedTuple
import os

red = "\033[0;31m"
deep_color = "\033[0;30m" # black
fgbg = os.environ['COLORFGBG'].split(';')
if len(fgbg) > 1 and fgbg[1] == '0':
    deep_color = "\033[1;30m" # gray
no_colored = "\033[0m"
class Suite(enum.Enum):
    Club = 1
    Diamond = 2
    Heart = 3
    Spade = 4
    def __str__(self) -> str:
        return {
            4:f'{deep_color}♠{no_colored}',
            3:f'{red}♥{no_colored}',
            2:f'{red}♦{no_colored}',
            1:f'{deep_color}♣{no_colored}',
        }[self.value] 

# inherent from SimpleNamespace for writable attribute
class Card(SimpleNamespace):
    face_value: int
    suite: Suite
    opened: bool

    def __repr__(self) -> str:
        return f'{self.suite}{self.face_value}'

class Hand:
    cards: list[Card]
    def __init__(self) -> None:
        self.cards = []

    def add(self, card: Card):
        self.cards.append(card)

class Deck:
    cards: list[Card]
    def __init__(self) -> None:
        self.cards = []
        for suite in range(1, 5):
            for number in range(1,14):
                self.cards.append(Card(face_value=number, suite=Suite(suite), opened=False))
        random.shuffle(self.cards)

    def dispatch(self, hand: Hand, open=False):
        card = self.cards.pop()
        card.opened = open
        hand.add(card)

class BlackjackHand(Hand):
    def add(self, card: Card):
        super().add(card)
        self.calculate()

    def calculate(self):
        pass

    def is_bust(self):
        return self.points() > 21

    def points(self):
        total = 0
        ace_count = 0
        for card in self.cards:
            if card.face_value == 1:
                ace_count += 1 
            elif 11 <= card.face_value and card.face_value <= 13:
                total += 10
            else:
                total += card.face_value
        while ace_count != 0:
            if 11 + total > 21:
                total += 1
            else:
                total += 11
            ace_count -= 1
        return total

    def __repr__(self) -> str:
        return f'[point: {self.points()}, cards: {self.cards}]'


class TestBlackjackHand(unittest.TestCase):
    def test_points_should_works(self):
        hand = BlackjackHand()
        hand.cards.append(Card(face_value=1,suite=Suite.Spade, opened=True))
        hand.cards.append(Card(face_value=1,suite=Suite.Spade, opened=False))
        self.assertEqual(12, hand.points())

        hand = BlackjackHand()
        hand.cards.append(Card(face_value=1,suite=Suite.Spade, opened=True))
        hand.cards.append(Card(face_value=10,suite=Suite.Spade, opened=False))
        self.assertEqual(21, hand.points())

        hand = BlackjackHand()
        hand.cards.append(Card(face_value=1,suite=Suite.Spade, opened=True))
        hand.cards.append(Card(face_value=10,suite=Suite.Spade, opened=False))
        hand.cards.append(Card(face_value=10,suite=Suite.Spade, opened=False))
        self.assertEqual(21, hand.points())

        hand = BlackjackHand()
        hand.cards.append(Card(face_value=1,suite=Suite.Spade, opened=True))
        hand.cards.append(Card(face_value=1,suite=Suite.Spade, opened=True))
        hand.cards.append(Card(face_value=10,suite=Suite.Spade, opened=False))
        hand.cards.append(Card(face_value=10,suite=Suite.Spade, opened=False))
        self.assertEqual(22, hand.points())

    def test_is_bust_should_works(self):
        hand = BlackjackHand()
        hand.cards.append(Card(face_value=1,suite=Suite.Spade, opened=True))
        hand.cards.append(Card(face_value=1,suite=Suite.Spade, opened=True))
        hand.cards.append(Card(face_value=10,suite=Suite.Spade, opened=False))
        hand.cards.append(Card(face_value=10,suite=Suite.Spade, opened=False))
        self.assertTrue(hand.is_bust())

    def test_play(self):
        hands = []
        for i in range(5):
           hands.append(BlackjackHand())
        deck = Deck()
        for hand in hands:
            deck.dispatch(hand)

        for hand in hands:
            deck.dispatch(hand, open=True)

        print(hands)

if __name__ == '__main__':
    unittest.main()
