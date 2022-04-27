import collections
import urllib.request
import urllib.parse
import json
from molecule import Graph, Atom

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