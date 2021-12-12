# we have to raise error if no way to build, like cycling dependency.

# 1. 
# Q: 有可能要移動已經插入的點，有點麻煩，我怎麼記錄這個點能不能移動
# A: 如果我不要一次把一個 node 所有dependency 建立完，用 DFS 的方法


# tips:
# 1. 沒有 dependency 的點就是最後的點
# 2. 需要表示 state 來知道有沒有環, 可以用 set 記錄
# 3. 如果 b depends on a , 表示為 {"a": ['b']} 比較好做計算, 不過實際上應該先問一下輸入的表示法應該是什麼
from collections import defaultdict
import unittest
import copy

# 這個方式應該行不通
class MyList(list[str]):
    def find_or_append(self, value):
        idx = None
        try:
            return self.index(value)
        except ValueError:
            self.append(value)
            return self.index(value)

    def merge(self, li):
        # 要能偵測到衝突的 dependency, ex: self A->B  li B->A
        self_cur, li_cur = 0, 0
        new_list = MyList()
        print(self, li)
        while len(self) > 0 and len(li) > 0:
            v1 = self.pop()
            v2 = li.pop()
            if v1 == v2:
                new_list.append(v1)
                continue
            v1_in_li, v2_in_self = -1, -1
            try:
                v1_in_li = li.index(v1)
            except ValueError:
                pass
            try:
                v2_in_self = self.index(v2)
            except ValueError:
                pass
            if v1_in_li >= 0 and v2_in_self >= 0:
                raise ValueError(f'{v1} in {self}, {v2} in {li}')
            elif v1_in_li >= 0:
                new_list.append(v2)
            elif v2_in_self >= 0:
                new_list.append(v1)
            else:
                # TODO: 怎麼確定後面不需要交換
                new_list.append(v1)
                new_list.append(v2)
        while len(self) > 0:
            new_list.append(self.pop())
        while len(li) > 0:
            new_list.append(li.pop())
        return new_list

def build_list_v1(graph) -> list[str]:
    result = MyList() 
    for node, dependency in graph.items():
        result = result.merge(build_v1(graph, node))
    return result

def build_v1(graph, node) -> MyList:
    dependencies = graph[node]
    result = MyList()
    result.append(node)
    for dependency in dependencies:
        sub_list = build_v1(graph, dependency)
        if node in sub_list:
            raise ValueError(f'{node} in dependen itself in {sub_list}')
        result = result.merge(sub_list)
    return result


def build_dependency_dfs(graph) -> list[str]:
    result = []
    visited = set()
    for node in graph:
        if node in visited:
            continue
        do_dfs(graph, node, visited, result)
    return result

def build_dependency_toplogical_sort(graph) -> list[str]:
    node_len = len(graph)
    result = []
    depends = defaultdict(lambda: set())
    for node, dependencies in graph.items():
        depends[node]
        for d in dependencies:
            depends[d].add(node)

    while len(result) < node_len:
        zero_depends_node = None
        for node, depend_on in depends.items():
            if len(depend_on) == 0:
                zero_depends_node = node
                break
        if not zero_depends_node:
            raise ValueError(f'circular dependency {depends} {result}')
        result.append(zero_depends_node)
        del(depends[zero_depends_node])
        for node, depend_on in depends.items():
            if zero_depends_node in depend_on:
                depend_on.remove(zero_depends_node)
                depends[node] = depend_on 
    return result
        

def do_dfs(graph, node, visiting=None, result = None):
    if result is None:
        result = []
    if visiting is None:
        visiting = set(node)
    # 有更好的方式嗎？解答是標識在 node 上面這樣只需要 O(n), 我們可以多一個 visited 的 set 但是這樣再多一個狀態就會多一個 set
    elif node in visiting: # 還沒加入 result 但是已經走過
        # 怎麼分要跳過還是環?
        raise ValueError(f'{node} already in {visiting}')
    elif node in result: # 已經在上一輪完成加入 result 就跳過 
        return
    else:
        visiting.add(node)
    dependencies = graph[node]
    if not dependencies:
        result.insert(0, node)
        visiting.remove(node) # 已經完成的 node 要移除掉
    else:
        for dependency in dependencies:
            do_dfs(graph, dependency, visiting, result)
        result.insert(0, node)
        visiting.remove(node)

def build_graph(projects: list[str], dependencies: list[list[str]]) -> dict[str, list[str]]:
    res = dict()
    for proj in projects:
        res[proj] = []
    for dependency in dependencies:
        res[dependency[0]].extend(dependency[1:])
    return res

class TestBuildSeq(unittest.TestCase):
    testCases = [
        dict(
            projects = ['a', 'b', 'c', 'd', 'e', 'f'],
            dependencies = [['a', 'd'], ['f', 'b'], ['b', 'd'], ['f', 'a'], ['d', 'c']],
            graph = {
                # means a must build before d
                "a": ['d'],
                "f": ['b', 'a'],
                "b": ['d'],
                "d": ['c'],
                "c": [],
                "e": []
            },
            expect = ['f','e','a','b','d','c']
        ),
        dict(
            projects = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'],
            dependencies = [['f', 'c'], ['f', 'a'], ['f', 'b'], ['c', 'a'], ['b', 'a'],['b', 'h'], ['a', 'e'], ['d', 'g']],
            graph = {
                "f": ['c', 'a', 'b'],
                "c": ['a'],
                "b": ['a', 'h'],
                "a": ['e'],
                "d": ['g'],
                "e": [],
                "g": [],
                "h": [],
            },
            expect = ['']
        )
    ]

    def test_generate_graph(self):
        for test_case in self.testCases:
            self.assertDictEqual(test_case['graph'], build_graph(test_case['projects'], test_case['dependencies']))

    def test_build_dependency_dfs(self):
        for test_case in self.testCases:
            print("dfs", build_dependency_dfs(test_case['graph']))
            # 順序有多種可能
            # self.assertIs(test_case['expect'], build_dependency_dfs(test_case['dependency']))
    def test_buiild_dependency(self):
        for test_case in self.testCases:
            print("", build_dependency_toplogical_sort(test_case['graph']))
        


if __name__ == '__main__':
    unittest.main()
