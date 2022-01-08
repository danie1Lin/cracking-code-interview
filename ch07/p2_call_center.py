from types import SimpleNamespace
import unittest
from enum import Enum

class Hierarchy(Enum):
    Respondent = 1
    Manager = 2
    Director = 3
    def can_solve_problem(self, level: int):
        return self.value > level

class Employee:
    def __init__(self, name, hierarchy=Hierarchy.Respondent, direct_reports=None) -> None:
        self.name = name
        if direct_reports == None:
            self.direct_reports = []
        else:
            self.direct_reports = direct_reports
        self.is_free = True
        self.hierarchy = hierarchy

    def answer_the_call(self, problem) -> bool:
        for report in self.direct_reports:
            if report.answer_the_call(problem):
                return True
        if self.is_free:
            can_solve = self.hierarchy.can_solve_problem(problem.level)
            if can_solve:
                problem.assignee = self
                problem.solved = True
                print(f'{self} answer the call')
            return can_solve
        else:
            return False

    def __str__(self) -> str:
        return f'{self.hierarchy.name} {self.name}'

class Problem(SimpleNamespace):
    level: int
    solved: bool
    assignee: Employee

class CallCenter:
    def __init__(self, director) -> None:
        self.director = director

    def dispatchCall(self, problem: Problem) -> bool:
        return self.director.answer_the_call(problem)

class TestCallCenter(unittest.TestCase):
    def setUp(self) -> None:
        self.respondents = [Employee(i) for i in range(9)]
        self.managers = [Employee(i, Hierarchy.Manager, self.respondents[i: i+3]) for i in range(3)]
        self.director = Employee(0, Hierarchy.Director, self.managers)
        self.call_center = CallCenter(self.director)
        return super().setUp()

    def test_find_respondent_is_free(self):
        problem = Problem(level=0, solved=False, assignee=None)
        self.assertTrue(self.call_center.dispatchCall(problem))

    def test_respondent_can_not_handle(self):
        problem = Problem(level=0, Solved=False, Assignee=None)
        self.assertTrue(self.call_center.dispatchCall(problem))

    def test_respondent_are_not_available(self):
        problem = Problem(level=0, Solved=False, Assignee=None)
        for respondent in self.respondents:
            respondent.is_free = False
        self.assertTrue(self.call_center.dispatchCall(problem))
        self.assertTrue(problem.solved)
        self.assertEqual(problem.assignee.hierarchy, Hierarchy.Manager)

    def test_manager_is_not_free(self):
        problem = Problem(level=0, Solved=False, Assignee=None)
        for respondent in self.respondents:
            respondent.is_free = False
        for manager in self.managers:
            manager.is_free = False
        self.assertTrue(self.call_center.dispatchCall(problem))
        self.assertTrue(problem.solved)
        self.assertEqual(problem.assignee.hierarchy, Hierarchy.Director)

if __name__ == '__main__':
    unittest.main()
