from molecule import Graph
import plotly as py
from plotly import graph_objects as go


def generate_edges(graph: Graph):
    """Выдаёт массив всех рёбер"""
    graph = graph.bonds
    edges = []
    for node in graph:
        for neighbour in graph[node]:
            edges.append((node, neighbour))
    return edges


def plot_graph_3d(graph: Graph, stage: str):
    """Визуализирует граф. Открывает окно в браузере."""
    N = len(graph.atoms)

    Edges = generate_edges(graph)

    Xn = [graph.atoms[k].x for k in range(N)]
    Yn = [graph.atoms[k].y for k in range(N)]
    Zn = [graph.atoms[k].z for k in range(N)]
    Xe = []
    Ye = []
    Ze = []
    for e in Edges:
        Xe += [graph.atoms[e[0]].x, graph.atoms[e[1]].x, None]  # x-coordinates of edge ends
        Ye += [graph.atoms[e[0]].y, graph.atoms[e[1]].y, None]
        Ze += [graph.atoms[e[0]].z, graph.atoms[e[1]].z, None]

    trace1 = go.Scatter3d(x=Xe,
                          y=Ye,
                          z=Ze,
                          mode='lines',
                          line=dict(color='rgb(125,125,125)', width=1),
                          hoverinfo='none'
                          )

    trace2 = go.Scatter3d(x=Xn,
                          y=Yn,
                          z=Zn,
                          mode='markers',
                          name='actors',
                          hoverinfo='text'
                          )

    axis = dict(showbackground=False,
                showline=True,
                zeroline=True,
                showgrid=True,
                showticklabels=True,
                title=''
                )

    layout = go.Layout(
        title="Graph Visualization",
        width=1000,
        height=1000,
        showlegend=False,
        scene=dict(
            xaxis=dict(axis),
            yaxis=dict(axis),
            zaxis=dict(axis),
        ),
        margin=dict(
            t=100
        ),
        hovermode='closest',
        )

    data = [trace1, trace2]
    fig = go.Figure(data=data, layout=layout)
    py.offline.plot(fig, filename=f'result\molecule-3d-{stage}.html', auto_open=False)
