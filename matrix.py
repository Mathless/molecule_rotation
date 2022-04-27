from vector import CVector

class Matrix:
    def __init__(self, data) -> None:
        if isinstance(data, CVector):
            self.data = Matrix([[data.x, data.y, data.z]]).transpose().data
        else:
            self.data = data or []

    @staticmethod
    def E(m, n):
        return Matrix([[1 for _ in range(m)] for __ in range(n)])

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