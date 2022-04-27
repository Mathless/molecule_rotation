from parse import convert_to_graph, get_info

if __name__ == '__main__':
    name = 'aspirin'
    raw = get_info(name)
    graph = convert_to_graph(raw)

    for atom in graph.atoms: print(atom)
    print(graph.bonds)

    print(graph.find_good_edges())

    #TODO: в find_good_edges() добавить обратные рёбра
    #TODO: сделать функцию, чтобы из полученного списка выбирались n рёбер случайным образом (без повторений)
