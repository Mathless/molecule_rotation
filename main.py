from parse import convert_to_graph, get_info
from rotation import randAngle, angleConvert, rotateGraph
from restore import restore
from plot import plot_graph_3d as plot

MIN_ANGLE = 0.0001745329252

if __name__ == '__main__':
    name = 'Antazoline'
    raw = get_info(name)
    graph = convert_to_graph(raw)
    graph.find_good_edges()

    vertices = graph.get_vertices()
    edges, vertex = graph.select_edges()
    angles = randAngle(len(edges))[1]
    rotated = rotateGraph(vertices, edges, angles, graph.bonds)

    res = restore(vertices, rotated, graph.bonds, vertex)
    restored = res[2]

    result = ''

    result += 'Vertex coordinates:\n'
    result +='{:31} {:37} {:30}\n'.format("INITIAL", "ROTATED", "RESTORED")
    for i in range(len(vertices)):
        v, n, r = vertices[i], map(lambda x: round(x, 6), rotated[i]), map(lambda x: round(x, 6), restored[i])
        result +='({:-8} {:-8} {:-8}) -> ({:-10} {:-10} {:-10}) -> ({:-10} {:-10} {:-10})\n'.format(*v, *n, *r)

    result += '\nInitial rotation angles:\n'
    result += '{:11} {:8} {:8}\n'.format("EDGE", "DEG", "RAD")
    for i in range(len(edges)):
        rad_angle, angle = angleConvert(angles[i], True, False), angleConvert(angles[i])
        result += '{:8} {:8}° {:10}rad\n'.format(str(edges[i]), angle, rad_angle)

    result += '\nRestored angles\n'
    result += '{:11} {:9} {:8}\n'.format("EDGE", "DEG", "RAD")
    for pair in zip(res[0], res[1]):
        if abs(pair[1]) < MIN_ANGLE: continue
        rad_angle, angle = angleConvert(pair[1], True, False), angleConvert(pair[1])
        result += '{:8} {:8}° {:10}rad\n'.format(str(pair[0]), angle, rad_angle)

    print(result)
    f = open("result/result.txt", "w")
    f.write(result)
    f.close()

    plot(graph, "init")
    graph.set_vertices(rotated)
    plot(graph, "rotated")
    graph.set_vertices(restored)
    plot(graph, "restored")