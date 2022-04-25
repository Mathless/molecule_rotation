import collections
import urllib.request
import urllib.parse
import json
from collections import deque


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


# Recieve JSON representation of molecule by HTTP Request
def get_info(name, dim=3) -> str:
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{name}/record/JSON/?"
    params = {'record_type': f'{dim}d', 'response_type': 'display'}
    url += urllib.parse.urlencode(params)
    request = urllib.request.Request(url, data={}, headers={}, method='GET')
    response = urllib.request.urlopen(request)
    return response


# Parse and convert JSON to graph
def convert_to_graph(raw) -> Graph:
    data = json.load(raw)
    amount = data['PC_Compounds'][0]['atoms']['aid'][-1]
    atoms = []
    bonds = dict([(i, []) for i in range(amount)])
    order_graph = collections.defaultdict(dict)

    aid1 = data['PC_Compounds'][0]['bonds']['aid1']
    aid2 = data['PC_Compounds'][0]['bonds']['aid2']
    order = data['PC_Compounds'][0]['bonds']['order']
    coords = data['PC_Compounds'][0]['coords'][0]['conformers'][0]
    for i in range(amount):
        bonds[aid1[i] - 1].append(aid2[i] - 1)
        bonds[aid2[i] - 1].append(aid1[i] - 1)
        atoms.append(Atom(coords['x'][i], coords['y'][i], coords['z'][i]))
        order_graph[aid1[i] - 1][aid2[i] - 1] = order[i]
        order_graph[aid2[i] - 1][aid1[i] - 1] = order[i]

    graph = Graph(atoms, bonds, order_graph)
    return graph


if __name__ == '__main__':
    # molecule_file_name = "Conformer3D_CID_2244.json"
    # f = open("./molecules"+molecule_file_name)
    # convert_to_graph(f)

    name = 'aspirin'
    raw = get_info(name)
    graph = convert_to_graph(raw)

    for atom in graph.atoms: print(atom)
    print(graph.bonds)

    # TODO: В идеале бы ещё тесты написать, но пофиг
    # Выводит 5 рёбер, если посмотреть на картинку в 3d там действительно 3 подходящих ребра
    print(graph.find_good_edges())
