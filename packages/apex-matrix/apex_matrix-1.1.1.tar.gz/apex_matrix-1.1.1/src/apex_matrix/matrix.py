class Matrix:
    """
    Simple matrix class

    :param matrix: 2D list representing a matrix
    :type matrix: list
    :param validate: Validate the 2D list passed in as matrix (defaults to True)
    :type validate: bool, optional
    :ivar rows: Number of rows in the matrix
    :type rows: int
    :ivar columns: Number of columns in matrix
    :type columns: int
    """

    def __init__(self, matrix, validate=True):
        """
        Matrix Constructor
        """

        if validate:
            self.validate(matrix)

        self._multiplication_valid_types = [type(self)]
        self._multiplication_valid_scalars = [int, float]

        self.matrix = matrix
        self.rows = len(matrix)
        self.columns = len(matrix[0])


    @staticmethod
    def validate(matrix):
        """
        Validates if the 2D list passed into the constructor is a valid matrix

        :param matrix:
        :type matrix: 2D list
        :raises TypeError: If matrix parameter is not a 2D list
        :raises ValueError: If all rows are not the same length
        :return: Returns True if validations passed else raises an exception
        :rtype: bool
        """

        if type(matrix) != list:
            raise TypeError(f'Expected matrix to be of type {list}. Received {type(matrix)}')

        column_length = None

        for row in matrix:
            if type(row) != list:
                raise TypeError(f'Expected matrix row to be of type {list}. Received {type(row)}')

            if column_length is None:
                column_length = len(row)

            if len(row) != column_length:
                raise ValueError(f'Matrix rows are not the same length. {len(row)} != {column_length}')

    @staticmethod
    def zero(size, dtype=float):
        """
        Creates a matrix of dtype zeros using the dimensions specified in size

        :param size: Tuple container the row end column length e.g. (row, column)
        :type size: tuple
        :param dtype: data type of the matrix elements (defaults to Float)
        :type dtype: type, optional
        :raises TypeError: If size is not a tuple of ints
        :return: A 2D matrix of zeros of type dtype with the dimensions defined in the size tuple
        """

        if type(size) != tuple:
            raise TypeError(f'Expected {tuple} of (rows, columns). Received {type(size)}')

        if type(size[0]) != int or type(size[1]) != int:
            raise TypeError(f'Expected {tuple} of ({int}, {int}). Received {type(size[0]), type(size[1])}')

        return Matrix([ [dtype(0)] * size[1] for _ in range(size[0])])

    def transpose(self):
        """
        Returns the transpose of the current matrix

        :return: Transpose of current matrix
        :rtype Matrix
        """

        transposed_matrix = self.zero((self.columns, self.rows), dtype=int)

        for row in range(transposed_matrix.rows):
            for column in range(transposed_matrix.columns):
                transposed_matrix[row][column] = self.matrix[column][row]

        return transposed_matrix

    def element_wise_product(self, other):
        """
        Calculates the element wise product of two matrices. This is also known as the hadamard_product.

        The two matrices must have the same number of rows and columns and the result is a matrix of the
        same dimensions of the two matrices that equal the product of row i and column j for each element
        in both matrices.


        :param other: A matrix to multiply with the current matrix.
        :type other: Matrix
        :raises TypeError: If the parameter other is not a matrix.
        :raises ValueError: If dimensions of the two matrices don't match.
        :return: Returns a new matrix
        :rtype Matrix
        """

        if type(other) != type(self):
            raise TypeError(f'Cannot perform an element wise multiplication with {type(Matrix)} and {type(other)}')

        if other.rows != self.rows or other.columns != self.columns:
            raise ValueError(
                f'Cannot perform element wise multiplication with a matrix of size {self.rows}x{self.columns} with {other.rows}x{other.columns}')

        new_matrix = self.zero((self.rows, self.columns))

        for row in range(self.rows):
            for column in range(self.columns):
                new_matrix[row][column] = self.matrix[row][column] * other[row][column]

        return new_matrix

    def __matrix_x_matrix(self, other):
        """
        Multiplies this matrix with another matrix.

        The method checks if the matrices are compatible for multiplication
        (i.e., the number of columns in the first matrix must be equal to
        the number of rows in the second matrix). If the matrices are compatible,
        it performs the multiplication and returns a new matrix.

        :param other: The matrix multiply with.
        :type other: Matrix
        :raises ValueError: If the matrices have incompatible dimensions for multiplication.
        :return: A new Matrix instance of the current matrix multiplied by another matrix.
        :rtype: Matrix
        """

        if self.columns != other.rows:
            raise ValueError(f'Cannot multiply matrix[{self.rows}][{self.columns}] by matrix[{other.rows}][{other.columns}]')

        new_matrix = self.zero((self.rows, other.columns), dtype=type(self.matrix[0][0]))

        for row in range(self.rows):
            for column in range(other.columns):
                for i in range(self.columns):
                    new_matrix[row][column] += self.matrix[row][i] * other.matrix[i][column]

        return new_matrix

    def __matrix_x_scalar(self, scalar):
        """
        Multiplies this matrix by a scalar.

        Multiplies each element in the matrix by the scalar

        :param scalar: The scalar to multiply with.
        :type scalar: int, float
        :return: A new Matrix instance of the current matrix multiplied by a scalar
        :rtype: Matrix
        """

        new_matrix = Matrix(self.matrix)

        for row in range(new_matrix.rows):
            for column in range(new_matrix.columns):
                new_matrix[row][column] *= scalar

        return new_matrix

    def __mul__(self, other):
        """
        Multiplies this matrix with another matrix or this matrix by a scalar.

        Matrix x Matrix
        The method checks if the matrices are compatible for multiplication
        (i.e., the number of columns in the first matrix must be equal to
        the number of rows in the second matrix). If the matrices are compatible,
        it performs the multiplication and returns a new matrix.

        Matrix x Scaler
        Multiplies each element in the matrix by the scalar

        :param other: The matrix or scalar to multiply with.
        :type other: Matrix, int, float
        :raises TypeError: If the other operand is not of type Matrix, int or float.
        :raises ValueError: If the matrices have incompatible dimensions for multiplication.
        :return: A new Matrix instance of the current matrix multiplied by another matrix or scalar
        :rtype: Matrix
        """

        if type(other) not in self._multiplication_valid_types and type(other) not in self._multiplication_valid_scalars:
            raise TypeError(f'Cannot multiply {type(Matrix)} with {type(other)}')

        if type(other) == type(self):
            return self.__matrix_x_matrix(other)

        if type(other) in self._multiplication_valid_scalars:
            return self.__matrix_x_scalar(other)

    def __rmul__(self, other):
        """
        Multiplies this matrix by a scalar.

        Matrix x Scaler
        Multiplies each element in the matrix by the scalar

        :param other: The scalar to multiply with.
        :type other: int, float
        :raises TypeError: If the other operand is not of type int or float.
        :return: A new Matrix instance scaled by the scalar.
        :rtype: Matrix
        """

        if type(other) not in self._multiplication_valid_scalars:
            raise TypeError(f'Cannot multiply {type(Matrix)} with {type(other)}')

        return self.__matrix_x_scalar(other)

    def __add__(self, other):
        """
        Adds current matrix with another matrix

        :param other: The matrix to add to the current matrix.
        :type other: Matrix
        :raises TypeError: If the other operand is not of type Matrix.
        :raises ValueError: If the matrices have incompatible dimensions for addition.
        :return: A new matrix instance of the current matrix + the other matrix.
        :rtype: Matrix
        """

        if self.rows != other.rows or self.columns != other.columns:
            raise ValueError(f'Cannot add matrix[{self.rows}][{self.columns}] to matrix[{other.rows}][{other.columns}]')

        new_matrix = self.zero((self.rows, self.columns))

        for row in range(self.rows):
            for column in range(self.columns):
                new_matrix[row][column] = self.matrix[row][column] + other[row][column]

        return new_matrix

    def __sub__(self, other):
        """
        Subtracts current matrix with another matrix

        :param other: The matrix to subtract from the current matrix.
        :type other: Matrix
        :raises TypeError: If the other operand is not of type Matrix.
        :raises ValueError: If the matrices have incompatible dimensions for subtraction.
        :return: A new matrix instance of the current matrix - the other matrix.
        :rtype: Matrix
        """

        if self.rows != other.rows or self.columns != other.columns:
            raise ValueError(f'Cannot subtract matrix[{self.rows}][{self.columns}] from matrix[{other.rows}][{other.columns}]')

        new_matrix = self.zero((self.rows, self.columns))

        for row in range(self.rows):
            for column in range(self.columns):
                new_matrix[row][column] = self.matrix[row][column] - other[row][column]

        return new_matrix

    def __eq__(self, other):
        """
        Checks if the current matrix is equal to the other matrix

        :param other: matrix to compare with
        :return: bool
        """

        if self.rows != other.rows or self.columns != other.columns:
            return False

        for row in range(self.rows):
            for column in range(self.columns):
                if self.matrix[row][column] != other[row][column]:
                    return False

        return True

    def __getitem__(self, index):
        """
        Returns the element in the matrix based on the index.

        :param index: index of the element you want to access.
        :return: The row at the specified index of the element in [row][column] if chained together.
        :rtype: list, type
        """

        if type(index) != int:
            raise TypeError(f'matrix[{type(index)}] is not a valid index. Expected matrix[{int}]')

        return self.matrix[index]

    def __str__(self):
        """
        Returns a string of the values and visualization of the matrix dimensions by creating
        a string of each row in the matrix seperated by a new line.

        :return: a string of each row in the matrix seperated by a new line
        :rtype: str
        """

        string = ''

        for row in self.matrix:
            string += str(row) + '\n'

        return string
