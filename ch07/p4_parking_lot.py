# Is it free? How to charge?
# Only car or motorcycle as well?
# Do I need to consider the space layout? 
from types import SimpleNamespace
from typing import Deque, Dict, Tuple
from enum import Enum
import unittest

class VehicleType(Enum):
    Car = 1
    Bike = 2
    Motorcycle = 3


class Vehicle:
    no: str
    vechichle_type: VehicleType 
    def __init__(self, no, vehicle_type) -> None:
        self.no = no
        self.vechichle_type = vehicle_type

class Space:
    vehicle: Vehicle|None
    vehicle_type: VehicleType

    def __init__(self, type) -> None:
        self.ocuppied_duration = 0
        self.vehicle = None
        self.vehicle_type = type

    def left(self) -> Tuple[Vehicle, int]:
        if self.is_empty():
            raise RuntimeError('no vehicle in the space')
        vehicle, duration = self.vehicle, self.ocuppied_duration
        self.vehicle, self.ocuppied_duration = None, 0
        return vehicle, duration
    
    def is_fit(self, vehicle: Vehicle) -> bool:
        return True

    def is_empty(self) -> bool:
        return not self.vehicle

    def tick(self):
        self.ocuppied_duration += 1

class ParkingLot:
    spaces: Dict[VehicleType, Deque[Space]]
    vehicles: Dict[Vehicle, Space]
    def __init__(self, spaces: Dict[VehicleType, int]) -> None:
        self.spaces = dict()
        for type, num in spaces.items():
            self.spaces[type] = Deque([Space(type) for _ in range(num)])

        self.vehicles = dict() 
        self.unit_price = 10

    def enter(self, car: Vehicle):
        space = self.find_empty(car.vechichle_type)
        if space:
            space.vehicle = car
            self.vehicles[car] = space
            return True
        return False

    def left(self, car: Vehicle):
        space = self.vehicles[car]
        del(self.vehicles[car])
        _, duration = space.left()
        return duration * self.unit_price
        
    def find_empty(self, type: VehicleType) -> Space | None:
        tmp = None
        while not tmp:
            tmp = self.spaces[type].popleft()
            self.spaces[type].append(tmp)
            if tmp.is_empty():
                return tmp
        return

    def tick(self):
        for space in self.vehicles.values():
            space.tick()

class TestParkingLot(unittest.TestCase):
    def setUp(self):
        self.parking_lot = ParkingLot({VehicleType.Car: 1, VehicleType.Motorcycle: 1})
    def test_park(self):
        car = Vehicle(no="2022", vehicle_type=VehicleType.Car)
        self.parking_lot.enter(car) 
        for _ in range(10):
            self.parking_lot.tick()
        self.assertEqual(100, self.parking_lot.left(car))
        cars = [Vehicle(no=str(i), vehicle_type=VehicleType.Car) for i in range(2)]
        self.assertTrue(self.parking_lot.enter(cars[0]))
        self.assertFalse(self.parking_lot.enter(cars[0]))

if __name__ == '__main__':
    unittest.main()
