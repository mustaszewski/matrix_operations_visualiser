class MatrixShapeError(ValueError):
    pass

class Matrix:
    def __init__(self, matrix):
        self.matrix = matrix
        self.__shape = (len(matrix), len(matrix[0]))
        self.__n_rows = len(matrix)
        self.__n_cols = len(matrix[0])

    @property
    def n_rows(self):
        return self.__n_rows

    @property
    def n_cols(self):
        return self.__n_cols

    @n_rows.setter
    def n_rows(self, new_value):
        self.__n_rows = new_value

    @n_cols.setter
    def n_cols(self, new_value):
        self.__n_cols = new_value
    @property
    def shape(self):
        return self.__shape

    @shape.setter
    def shape(self, new_value):
        self.__shape = new_value

    @property
    def items(self):
        return self.matrix

    @staticmethod
    def initialise_empty(n_rows, n_cols):
        # method to initialise empty list of lists having specified shape
        return [[0 for i in range(n_cols)] for r in range(n_rows)]

    def __str__(self):
        mat_to_str = "[" + "\n ".join(['\t'.join(map(str, c)) for c in self.matrix])
        mat_to_str += "]"
        return mat_to_str

    def __add__(self, other):
        if not (isinstance(self, Matrix) and isinstance(other, Matrix)):
            raise TypeError("Both objects must be of type Matrix")

        if not (self.shape == other.shape):
            raise MatrixShapeError("Both Matrix objects must be of same shape")

        res = Matrix.initialise_empty(self.__n_rows, self.__n_cols)

        for row in range(self.__n_rows):
            for col in range(self.__n_cols):
                res[row][col] = self.matrix[row][col] + other.matrix[row][col]
        return Matrix(res)

    def __mul__(self, other):
        if not (isinstance(self, (Matrix, int, float)) and isinstance(other, (Matrix, int, float))):
            raise TypeError("Objects must be of type Matrix or int or float")

        if isinstance(self, Matrix) and isinstance(other, Matrix): # if both objects are of type Matrix
            if self.__n_cols != other.__n_rows:
                raise MatrixShapeError("Number of columns of Matrix 1 must be equal to number of rows of Matrix 2!")

            res = Matrix.initialise_empty(self.__n_rows, other.__n_cols)
            for r in range(self.__n_rows):
                for c in range(other.n_cols):
                    for i in range(self.__n_cols):
                        #print("  {} x {}".format(self.matrix[r][i], other.matrix[i][c]))
                        res[r][c] += self.matrix[r][i] * other.matrix[i][c]

        else: # scalar multiplication:
            res = Matrix.initialise_empty(self.__n_rows, self.__n_cols)
            for r in range(self.n_rows):
                for c in range(self.n_cols):
                    res[r][c] = other * self.matrix[r][c]
        return Matrix(res)

    def __matmul__(self, other):
        if not (isinstance(self, Matrix) and isinstance(other, Matrix)):
            raise TypeError("Both objects must be of type Matrix")
        if not (self.shape == other.shape):
            raise ValueError("Both Matrix objects must be of same shape")

        # initialise empty list of lists having desired shape
        res = Matrix.initialise_empty(self.__n_rows, self.__n_cols)

        for row in range(self.__n_rows):
            for col in range(self.__n_cols):
                res[row][col] = self.matrix[row][col] * other.matrix[row][col]
        return Matrix(res)


    def __rmul__(self, other):
        if not (isinstance(self, Matrix) and isinstance(other, (int, float))):
            raise TypeError("Object 1 must be of type int or float and Object 2 must be of type Matrix")

        res = Matrix.initialise_empty(self.__n_rows, self.__n_cols)
        for r in range(self.__n_rows):
            for c in range(self.__n_cols):
                res[r][c] = other * self.matrix[r][c]
        return Matrix(res)

    def __invert__(self): # transpose Matrix using ~ operator
        if not isinstance(self, Matrix):
            raise TypeError("Object must be of type Matrix")
        res = Matrix.initialise_empty(self.__n_cols, self.__n_rows)

        for r in range(self.__n_rows):
            for c in range(self.__n_cols):
                res[c][r] = self.matrix[r][c]
        return Matrix(res)

    def __setitem__(self, key, value):
        assert type(key) == tuple
        assert key[0] < self.n_rows and key[1] < self.n_cols
        self.matrix[key[0]][key[1]] = value