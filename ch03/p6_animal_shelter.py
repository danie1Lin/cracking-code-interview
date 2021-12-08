from typing import Optional
from .fifo import Fifo
from enum import Enum
from collections import defaultdict

# ask:
# 1. Should all operation be O(1)?
# 2. Can I use two queue?


class Specie(Enum):
    CAT = 1
    DOG = 2

class Animal:
    no: Optional[int]
    name: str
    specie: Specie

    @classmethod
    def new_cat(cls, name):
        return cls(name, Specie.CAT)

    @classmethod
    def new_dog(cls, name):
        return cls(name, Specie.DOG)

    def __init__(self, name, specie) -> None:
        self.name = name
        self.specie = specie
        self.no = None 

class AnimalShelter():
    def __init__(self) -> None:
        self.queue = defaultdict(lambda: Fifo())
        self.incr_id = 0 # increase only

    def dequeue_cat(self):
        return self.queue[Specie.CAT].remove()

    def dequeue_dog(self):
        return self.queue[Specie.DOG].remove()

    def dequeue(self) -> Optional[Animal]:
        oldest_queue = None
        for queue in self.queue.values():
            if oldest_queue == None: oldest_queue = queue
            last_animal = queue.peek()
            last_animal_of_oldest_queue = oldest_queue.peek()
            if not last_animal_of_oldest_queue or (last_animal and last_animal.no < last_animal_of_oldest_queue.no):
                oldest_queue = queue

        if oldest_queue: 
            return oldest_queue.remove()

    def enqueue(self, value: Animal):
        value.no = self.incr_id
        self.queue[value.specie].add(value)
        self.incr_id += 1

if __name__ == '__main__':
    shelter = AnimalShelter()
    shelter.enqueue(Animal.new_cat("a"))
    shelter.enqueue(Animal.new_dog("b"))

    cat = shelter.dequeue()
    assert cat and Specie.CAT == cat.specie

    dog = shelter.dequeue()
    assert dog 
    assert Specie.DOG == dog.specie


    shelter.enqueue(Animal.new_cat("a"))
    shelter.enqueue(Animal.new_dog("b"))
    shelter.enqueue(Animal.new_cat("c"))
    shelter.enqueue(Animal.new_dog("d"))
    shelter.enqueue(Animal.new_cat("e"))

    dog = shelter.dequeue_dog()
    assert dog
    assert Specie.DOG == dog.specie
    assert dog.name == "b"

    cat = shelter.dequeue_cat()
    assert cat
    assert cat and Specie.CAT == cat.specie
    assert cat.name == "a"

    animal = shelter.dequeue()
    assert animal
    assert animal and Specie.CAT == animal.specie
    assert animal.name == "c"

