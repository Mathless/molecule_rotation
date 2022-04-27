from math import sqrt

class CVector:
    def __init__(self, data: tuple) -> None:
        if len(data) != 3: raise ValueError('The passed argument is not coordinate vector')
        self.x = data[0]
        self.y = data[1]
        self.z = data[2]

    def norm(self):
        return sqrt(self.x**2 + self.y**2 + self.z**2)

    def __add__(self, other):
        if isinstance(other, CVector):
            return CVector((self.x + other.x, self.y + other.y, self.z + other.z))

    def __sub__(self, other):
        if isinstance(other, CVector):
            return CVector((self.x - other.x, self.y - other.y, self.z - other.z))

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return CVector((self.x * other, self.y * other, self.z * other))
    
    def transpose(self):
        m, n = self.size()
        self.data = [[self.data[j][i] for j in range(m)] for i in range(n)]

    def __str__(self):
        return (self.x, self.y, self.z).__str__()


if __name__ == "__main__":
    v1 = CVector((0, 0, 0))
    v2 = CVector((1, 2, 3))
    print(v1, v2)
    print(v1+v2, v2-v2, v2*100, v2*0.1)

    v = CVector((5, 0, 0))
    print(v.norm())
    print(v*(1/v.norm()))