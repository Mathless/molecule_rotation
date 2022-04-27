class Atom:
    def __init__(self, x, y, z) -> None:
        self.x = x
        self.y = y
        self.z = z

    def coords(self) -> tuple:
        return (self.x, self.y, self.z)

    def __str__(self) -> str:
        return self.coords().__str__()


class Graph:
    def __init__(self, atoms: list, bonds: dict, order: dict) -> None:
        self.atoms = atoms
        self.bonds = bonds
        self.order = order

    @staticmethod
    def __is_reachable(s: int, d: int, graph: dict):
        visited = [False] * (len(graph.keys()))
        queue = [s]
        visited[s] = True
        while queue:
            n = queue.pop(0)
            if n == d:
                return True
            for i in graph[n]:
                if not visited[i]:
                    queue.append(i)
                    visited[i] = True
        return False

    def is_edge_in_cycle(self, a: int, b: int):
        """Возвращает False, если ребро содержится в цикле или такого ребра нет."""
        if a not in self.bonds.keys() or b not in self.bonds[a]:
            return False
        self.bonds[a].remove(b)
        res = self.__is_reachable(a, b, self.bonds)
        self.bonds[a].append(b)
        return res

    def find_good_edges(self):
        "Возвращает множество(set) кортежей(tuple). Где кортеж состоит из двух элементов "
        good_edges = set()
        for el in self.bonds.keys():
            for neighbour in self.bonds[el]:
                if self.is_edge_good(el, neighbour):
                    good_edges.add(tuple(sorted([el, neighbour])))
        return good_edges

    def is_edge_good(self, el: int, neighbour: int):
        """Проверяет, что ребро удовлетворяет следующим свойствам:
        1) Вершины на концах не являются висячими
        2) Порядок ребра - 1
        3) Ребро не принадлежит циклам"""
        return len(self.bonds[el]) > 1 and len(self.bonds[neighbour]) > 1 and self.order[el][
            neighbour] == 1 and not self.is_edge_in_cycle(el, neighbour)