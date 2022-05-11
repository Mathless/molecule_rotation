import numpy as np
from matrix import Matrix
from vector import CVector
from rotation import rotateGraph
from math import acos
from SVD import svd

# Kabsch algorithm for 3dim points, translation given
def Kabsch3D(A: Matrix, B: Matrix, dt: Matrix):
    h1, w1 = A.size()
    h2, w2 = B.size()

    # Size check
    if (h1, w1) != (h2, w2):
        raise Exception(f"Matrices A ({h1}x{w1}) and B ({h2}x{w2}) are not the same size")
    if h1 != 3:
        raise Exception(f"Matrix A is not 3xN, it is {h1}x{w1}")
    if h2 != 3:
        raise Exception(f"Matrix B is not 3xN, it is {h2}x{w2}")

    # Translation
    Am = A - dt
    Bm = B - dt

    # Covariance matrix computation
    H = Am * Bm.transpose()

    # Computation of the optimal rotation matrix
    U, S, Vt = SVD(H)
    R = Vt.transpose() * U.transpose()

    # Special reflection case
    if R.det3x3() < 0:
        Vt = Matrix([[1, 0, 0], [0, 1, 0], [0, 0, -1]]) * Vt
        R = Vt.transpose() * U.transpose()

    return R

# Get angle from rotation matrix
def getAngle(R, x, y, z):
    R = R.data
    cos, sin = 0, 0
    if abs(x) != 1:
        cos = (R[0][0] - x*x)/(1-x*x)
    elif abs(y) != 1:
        cos = (R[1][1] - y*y)/(1-y*y)
    else:
        cos = (R[2][2] - z*z)/(1-z*z)

    if x != 0:
        sin = (y*z*(1-cos)-R[1][2])/x
    elif y != 0:
        sin = (x*z*(1-cos)-R[2][0])/y
    else:
        sin = (x*y*(1-cos)-R[0][1])/z

    angle = (acos(cos) * (-1 if (sin < 0) else 1))
    return angle


# Prepare and use Kabsch algorith for 3 points
def update_graph(c1, c2, v, P, Q, bonds):
    edge = (c1, c2)
    c1, c2, v0, v1 = CVector(P[c1]), CVector(P[c2]), CVector(P[v]), CVector(Q[v])
    A = Matrix([c1, c2, v0])
    B = Matrix([c1, c2, v1])
    dt = Matrix([c2, c2, c2])
    R = Kabsch3D(A, B, dt)

    vector = c2-c1
    n = vector*(1/vector.norm())
    angle = getAngle(R, n.x, n.y, n.z)

    newVertices = rotateGraph(Q, [edge], [-angle], bonds)
    return newVertices, angle

# Restores the graph by rotating it
# Returns list of edges to be turned and list of angles
def restore(old_coordinates, new_coordinates, bonds, vertex = 1):
    P, Q = old_coordinates, new_coordinates
    edges, angles = [],[]
    
    if vertex >= 0:
        visited = [vertex]
        queue = [vertex]
        while queue:
            v = queue.pop(0)
            for n1 in bonds[v]:
                if n1 not in visited:
                    visited.append(n1)
                    queue.append(n1)
                    for n2 in bonds[n1]:
                        if n2 not in visited:
                            if P[n2] != Q[n2]:
                                Q, a = update_graph(v, n1, n2, P, Q, bonds)
                                edge = (v, n1)
                                if edge in edges:
                                    angles[-1] += a
                                else:
                                    edges.append(edge)
                                    angles.append(a)
    return edges, angles, Q

# Singular value decomposition
def SVD(matrix: Matrix):
    M = np.array(matrix.data)
    U, S, Vt = np.linalg.svd(M)
    U, S, Vt = Matrix(U.tolist()), Matrix(S.tolist()), Matrix(Vt.tolist())
    return U, S, Vt

if __name__ == "__main__":
    bonds = {0: [1], 1: [0, 2], 2: [1, 3], 3: [2]}
    P = [
        (0, 0, 0),
        (0, 0, 2),
        (5, 0, 2),
        (5, 0, 0)
    ]
    Q = [
        (0, 0, 0),
        (0, 0, 2),
        (0, 5, 2),
        (0, 5, 4)
    ]
    print('Result:')
    res = restore(P, Q, bonds, 0)
    restored = res[2]

    for i in range(len(P)):
        print(P[i], '->', restored[i])

    for pair in zip(res[0], res[1]):
        print(pair[0], pair[1])