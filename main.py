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

    def __isReachable(self, s, d, graph):
        # Mark all the vertices as not visited
        visited = [False] * (len(graph.keys()))

        # Create a queue for BFS
        queue = [s]

        # Mark the source node as visited and enqueue it
        visited[s] = True

        while queue:

            # Dequeue a vertex from queue
            n = queue.pop(0)

            # If this adjacent node is the destination node,
            # then return true
            if n == d:
                return True

            #  Else, continue to do BFS
            for i in graph[n]:
                if not visited[i]:
                    queue.append(i)
                    visited[i] = True
        # If BFS is complete without visited d
        return False

    def is_edge_in_cycle(self, a, b):
        if a not in self.bonds.keys() or b not in self.bonds[a]:
            return False

        self.bonds[a].remove(b)
        res = self.__isReachable(a, b, self.bonds)
        self.bonds[a].append(b)
        return res

    def find_good_edges(self):
        good_edges = set()
        for el in self.bonds.keys():
            for neigbour in self.bonds[el]:
                if len(self.bonds[el]) > 1 and len(self.bonds[neigbour]) > 1 and self.order[el][
                    neigbour] == 1 and not self.is_edge_in_cycle(el, neigbour):
                    good_edges.add(tuple(sorted([el, neigbour])))
        return good_edges


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

    # TODO: find single bonds
    print(graph.find_good_edges())
