import urllib.request
import urllib.parse
import json

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
    def __init__(self, atoms: list, bonds: dict) -> None:
        self.atoms = atoms
        self.bonds = bonds

# Recieve JSON representation of molecule by HTTP Request
def get_info(name, dim = 3) -> str:
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

    aid1 = data['PC_Compounds'][0]['bonds']['aid1']
    aid2 = data['PC_Compounds'][0]['bonds']['aid2']
    coords = data['PC_Compounds'][0]['coords'][0]['conformers'][0]
    for i in range(amount):
        bonds[aid1[i]-1].append(aid2[i]-1)
        bonds[aid2[i]-1].append(aid1[i]-1)
        atoms.append(Atom(coords['x'][i], coords['y'][i], coords['z'][i]))

    graph = Graph(atoms, bonds)
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

    #TODO: find single bonds

