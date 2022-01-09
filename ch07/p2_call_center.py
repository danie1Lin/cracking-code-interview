from types import SimpleNamespace
from typing import DefaultDict, Deque, Dict
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
        self.supervisor = None
        if direct_reports == None:
            self.direct_reports = []
        else:
            self.direct_reports = direct_reports
        self.is_free = True
        self.hierarchy = hierarchy
        for direct_report in self.direct_reports:
            direct_report.supervisor = self

    def answer_the_call(self, problem) -> bool:
        if self.is_free:
            can_solve = self.hierarchy.can_solve_problem(problem.level)
            if can_solve:
                problem.assignee = self
                problem.solved = True
                print(f'{self} answer the call')
                return True
        if self.supervisor:
            return self.supervisor.answer_the_call(problem)

    def __str__(self) -> str:
        return f'{self.hierarchy.name} {self.name}'

class Problem(SimpleNamespace):
    level: int
    solved: bool
    assignee: Employee

class CallCenter:
    def __init__(self, director) -> None:
        self.employee_level_map = DefaultDict(lambda: Deque()) 
        temp = Deque()
        temp.append(director)
        while len(temp) != 0:
            employee = temp.pop()
            self.employee_level_map[employee.hierarchy.value].append(employee)
            for report in employee.direct_reports:
                temp.append(report)

    def dispatchCall(self, problem: Problem) -> bool:
        return self.get_assignee_by_problem(problem).answer_the_call(problem)

    def get_assignee_by_problem(self, problem) -> Employee:
        employee = self.employee_level_map[problem.level].popleft()
        self.employee_level_map[problem.level].append(employee)
        return employee

class TestCallCenter(unittest.TestCase):
    def setUp(self) -> None:
        self.respondents = [Employee(i) for i in range(9)]
        self.managers = [Employee(i, Hierarchy.Manager, self.respondents[i: i+3]) for i in range(3)]
        self.director = Employee(0, Hierarchy.Director, self.managers)
        self.call_center = CallCenter(self.director)
        return super().setUp()

    def test_find_respondent_is_free(self):
        problem = Problem(level=1, solved=False, assignee=None)
        self.assertTrue(self.call_center.dispatchCall(problem))

    def test_respondent_can_not_handle(self):
        problem = Problem(level=2, Solved=False, Assignee=None)
        self.assertTrue(self.call_center.dispatchCall(problem))

    def test_respondent_are_not_available(self):
        problem = Problem(level=1, Solved=False, Assignee=None)
        for respondent in self.respondents:
            respondent.is_free = False
        self.assertTrue(self.call_center.dispatchCall(problem))
        self.assertTrue(problem.solved)
        self.assertEqual(problem.assignee.hierarchy, Hierarchy.Manager)

    def test_manager_is_not_free(self):
        problem = Problem(level=1, Solved=False, Assignee=None)
        for respondent in self.respondents:
            respondent.is_free = False
        for manager in self.managers:
            manager.is_free = False
        self.assertTrue(self.call_center.dispatchCall(problem))
        self.assertTrue(problem.solved)
        self.assertEqual(problem.assignee.hierarchy, Hierarchy.Director)

if __name__ == '__main__':
    unittest.main()
