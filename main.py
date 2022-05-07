from parse import convert_to_graph, get_info
from rotation import randAngle, angleConvert, rotateGraph
from restore import restore

MIN_ANGLE = 0.0001745329252

if __name__ == '__main__':
    name = 'aspirin'
    raw = get_info(name)
    graph = convert_to_graph(raw)
    graph.find_good_edges()

    vertices = graph.get_vertices()
    edges, vertex = graph.select_edges()
    angles = randAngle(len(edges))[1]
    newVertices = rotateGraph(vertices, edges, angles, graph.bonds)

    res = restore(vertices, newVertices, graph.bonds, vertex)
    restored = res[2]

    print('Vertex coordinates:')
    print('{:31} {:37} {:30}'.format("INITIAL", "ROTATED", "RESTORED")) 
    for i in range(len(vertices)):
        v, n, r = vertices[i], map(lambda x: round(x, 6), newVertices[i]), map(lambda x: round(x, 6), restored[i])
        print('({:-8} {:-8} {:-8}) -> ({:-10} {:-10} {:-10}) -> ({:-10} {:-10} {:-10})'.format(*v, *n, *r)) 

    print('\nInitial rotation angles:')
    print('{:11} {:8} {:8}'.format("EDGE", "DEG", "RAD"))
    for i in range(len(edges)):
        angle = angleConvert(angles[i])
        print('{:8} {:8}° {:10}rad'.format(str(edges[i]), angle, angleConvert(angle, False)))

    print('\nRestored angles')
    print('{:11} {:9} {:8}'.format("EDGE", "DEG", "RAD"))
    for pair in zip(res[0], res[1]):
        if abs(pair[1]) < MIN_ANGLE: continue
        angle = angleConvert(pair[1])
        print('{:8} {:8}° {:10}rad'.format(str(pair[0]), angle, angleConvert(angle, False)))

