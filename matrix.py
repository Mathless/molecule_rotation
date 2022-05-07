from vector import CVector

class Matrix:
    def __init__(self, data) -> None:
        if isinstance(data, CVector):
            self.data = Matrix([[data.x, data.y, data.z]]).transpose().data
        elif isinstance(data, list) and isinstance(data[0], CVector):
            self.data = Matrix([[vector.x, vector.y, vector.z] for vector in data]).transpose().data
        else:
            self.data = data or []

    @staticmethod
    def E(m: int, n: int):
        return Matrix([[1 for _ in range(m)] for __ in range(n)])

    def det3x3(self):
        rows, cols = self.size()
        if (rows, cols) != (3, 3):
            raise Exception(f'Matrix is not 3x3, it is {rows}x{cols}')
        a = self.data
        return (a[0][0] * (a[1][1] * a[2][2] - a[2][1] * a[1][2])
           -a[1][0] * (a[0][1] * a[2][2] - a[2][1] * a[0][2])
           +a[2][0] * (a[0][1] * a[1][2] - a[1][1] * a[0][2]))

    def size(self):
        return (len(self.data), len(self.data[0]))

    def __add__(self, other):
        if isinstance(other, Matrix):
            if self.size() != other.size(): raise ValueError("Matricies have different size!")
            X, Y = self.data, other.data
            return Matrix([[X[i][j] + Y[i][j]  for j in range(len(X[0]))] for i in range(len(X))])

    def __sub__(self, other):
        if isinstance(other, Matrix):
            if self.size() != other.size(): raise ValueError("Matricies have different size!")
            X, Y = self.data, other.data
            return Matrix([[X[i][j] - Y[i][j]  for j in range(len(X[0]))] for i in range(len(X))])

    def __mul__(self, other):
        if isinstance(other, Matrix):
            if self.size()[1] != other.size()[0]: raise ValueError("These matricies can't be multiplied!")
            X, Y = self.data, other.data
            return Matrix([[sum(a*b for a,b in zip(X_row,Y_col)) for Y_col in zip(*Y)] for X_row in X])
    
    def transpose(self):
        m, n = self.size()
        return Matrix([[self.data[j][i] for j in range(m)] for i in range(n)])

    def round(self, digits):
        self.data = [[round(el, digits) for el in row] for row in self.data]

    def __str__(self):
        maxSize = len(max([max(map(str, row), key=len) for row in self.data], key=len))+1
        return f'Matrix {self.size()[1]}x{self.size()[0]}:\n' + '\n'.join([''.join([f'{{:{maxSize}}}'.format(item) for item in row]) for row in self.data])


if __name__ == "__main__":
    m1 = Matrix([[0, 0, 1], [0, 1, 0], [-1, 0, 0]])
    m2 = Matrix(CVector((0, 4, 5)))
    m3 = Matrix([[0, 4, 3]]).transpose()
    e = Matrix.E(1, 1)
    print(m1)
    print(m2)
    print(m3)
    print(e)
    print((m1*(m2-m3)+m3)*e)

    m1 = Matrix([[ -1, 0, 0],[ 0, -1, -1],[ 0, 0, 1]])
    m2 = Matrix(CVector((-2, 0, 0)))
    m3 = Matrix([[0, 0, 0]]).transpose()
    print(m1*(m2-m3)+m3)

    m = Matrix([[1, 0, 0], [0, 10, 0], [0, 0, -1]])
    print(m.det3x3())

    v1 = CVector((1, 2, 3))
    v2 = v1*20
    v3 = v1*300
    m = Matrix([v1, v2, v3])
    print(v1, v2, v3)
    print(m)