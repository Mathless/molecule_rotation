from random import uniform
from math import degrees, radians, cos, sin
from matrix import Matrix
from vector import CVector

DEBUG = 0


# Rotate one vertex around one edge
def rotateVertex(verticies, vertexInd, edge, angle):
    vertex = CVector(verticies[vertexInd])
    edgeS = CVector(verticies[edge[0]])
    edgeF = CVector(verticies[edge[1]])
    vector = edgeF - edgeS  # edge vector
    e = vector * (1 / vector.norm())  # unit vector
    offset = edgeF  # offset from coord. system origin
    c, s, v = cos(angle), sin(angle), 1 - cos(angle)  # cosine, sine, versine
    rotation = Matrix([  # rotation matrix
        [v * e.x ** 2 + c, v * e.x * e.y - e.z * s, v * e.x * e.z + e.y * s],
        [v * e.x * e.y + e.z * s, v * e.y ** 2 + c, v * e.y * e.z - e.x * s],
        [v * e.x * e.z - e.y * s, v * e.y * e.z + e.x * s, v * e.z ** 2 + c]
    ])
    rotation.round(6)  # round to float

    if DEBUG == 2:
        print(c, s, v)
        print(vertex, e, offset)
        print(rotation)

    vertex, offset = Matrix(vertex), Matrix(offset)
    result = rotation * (vertex - offset) + offset  # compute changed coordinates
    result = result.transpose().data[0]
    return (result[0], result[1], result[2])


# Rotate all verticies around edges in order
def rotateGraph(vertices, edges, angles, bonds):
    newVertices = vertices.copy()
    for edge, angle in zip(edges, angles):
        if not edge: break
        for index in turnedVertices(edge, bonds):
            if DEBUG >= 1:
                print(f'Vertices: {newVertices}')
                print(f'index: {index}, edge: {edge}, angle: {angle}\n')
            newVertices[index] = rotateVertex(newVertices, index, edge, angle)
    return newVertices


# Find vertices affected by rotation
def turnedVertices(edge, bonds):
    visited = [edge[0], edge[1]]
    queue = [edge[1]]
    while queue:
        v = queue.pop(0)
        for child in bonds[v]:
            if child not in visited:
                queue.append(child)
                visited.append(child)
    return visited[2:]


# Generate a random angle in degrees and radians
def randAngle(N=1):
    angles = [round(uniform(-180, 180), 2) for _ in range(N)]
    return (angles, list(map(radians, angles)))

def angleConvert(angle, isRad = True):
    return round(degrees(angle), 2) if isRad else round(radians(angle), 6)



if __name__ == "__main__":
    DEBUG = 2
    print(randAngle(4))
    verticies = [(0, 2, 0), (0, 2, 3), (0, 4, 3), (0, 4, 5)]
    edges = [(1, 2), (0, 1)]
    angles = [radians(90), radians(90)]
    bonds = {0: [1], 1: [0, 2], 2: [1, 3], 3: [2]}
    print(turnedVertices(edges[1], bonds))
    print(rotateVertex(verticies, 3, edges[0], angles[0]))
    print(rotateGraph(verticies, edges, angles, bonds))

    vertices = [(0, 0, 0), (0, 0, 4), (0, 2, 5), (3, 2, 3)]
    edges = [(1, 2), (0, 1)]
    angles = [radians(180), radians(-90)]
    bonds = {0: [1], 1: [0, 2], 2: [1, 3], 3: [2]}
    print(rotateGraph(vertices, edges, angles, bonds))
