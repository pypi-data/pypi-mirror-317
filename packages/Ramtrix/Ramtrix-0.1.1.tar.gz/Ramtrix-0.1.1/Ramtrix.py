#all matrices must be rectangular
def precise_row_reduce(inputMatrix):
    """
    WARNING SLOWISH. This is marginally slower than the other one but might maybe have less rounding error(?) Idrk.
    Outputs Matrix in Row Reduced Echelon Format.
    """
    if not check_matrix(inputMatrix):
        print("Please input a valid matrix")
        return
    matrix1 = [row[:] for row in inputMatrix]
    matrix1Len = len(matrix1)
    matrix1RowLen = len(matrix1[0])
    for rownum in range(matrix1Len):
        pivot_column = None
        for colnum in range(matrix1RowLen):
            if matrix1[rownum][colnum] != 0:
                pivot_column = colnum
                break

        if pivot_column is None:
            continue

        pivot = matrix1[rownum][pivot_column]

        for colnum in range(matrix1RowLen):
            matrix1[rownum][colnum] /= pivot

        for nest_rownum in range(matrix1Len):
            if nest_rownum != rownum and matrix1[nest_rownum][pivot_column] != 0:
                scalar = matrix1[nest_rownum][pivot_column]
                for nest_colnum in range(matrix1RowLen):
                    matrix1[nest_rownum][nest_colnum] -= scalar * matrix1[rownum][nest_colnum]

    return matrix1

def row_reduce(matrix1):
    """
    Outputs Matrix in Row Reduced Echelon Format.
    """
    if not check_matrix(matrix1):
        print("Please input a valid matrix")
        return
    inputMatrix = [row[:] for row in matrix1]
    inputMatrixLen = len(inputMatrix)
    inputMatrixRowLen = len(inputMatrix[0])
    for rownum in range(inputMatrixLen):
        pivot = 0
        pivot_colnum = None
        for colnum in range(inputMatrixRowLen):
            if pivot == 0:
                pivot = inputMatrix[rownum][colnum]
            if pivot != 0:
                if pivot_colnum == None: pivot_colnum = colnum
                #divide everything by the pivot
                inputMatrix[rownum][colnum] = inputMatrix[rownum][colnum]/pivot
        if pivot_colnum == None:
            continue
        for nest_rownum in range (inputMatrixLen):
            #check every row to ensure the pivot alone is the nonzero one(literally)
            if inputMatrix[nest_rownum][pivot_colnum] != 0 and nest_rownum != rownum:
                scalar = inputMatrix[nest_rownum][pivot_colnum]/inputMatrix[rownum][pivot_colnum]
                for nest_colnum in range(inputMatrixRowLen):
                    inputMatrix[nest_rownum][nest_colnum] -= inputMatrix[rownum][nest_colnum]*scalar
    return inputMatrix


def transpose(matrix1):
    """
    Transposes matrix(rows to columns columns to rows)
    """
    if not check_matrix(matrix1):
        print("Please input a valid matrix")
        return
    matrixColLen = len(matrix1)
    matrixRowLen = len(matrix1[0])
    new_matrix=[([0] * matrixColLen) for _ in range(matrixRowLen)]
    for row in range(matrixColLen):
        for col in range(matrixRowLen):
            new_matrix[col][row] = matrix1[row][col]
    return new_matrix


def cofactor(matrix1):
    """
    Creates a cofactor matrix(checkerboard signs)
    """
    if not check_matrix(matrix1):
        print("Please input a valid matrix")
        return
    matrixColLen = len(matrix1)
    matrixRowLen = len(matrix1[0])
    result = [[matrix1[row][col] * pow(-1,(row+col)) for col in range(matrixRowLen)] for row in range(matrixColLen)]
    return result


def flatten(matrix1):
    """
    Flattens Matrix/Turns N-Dimension Matrix to 1-Dimension Matrix. Does not re-sort.
    """
    flat_matrix = [matrix1[row][col] for row in range(len(matrix1)) for col in range(len(matrix1[row]))]
    return flat_matrix


def laplace_determinant(matrix1):
    """
    WARNING: SLOW. Recommended you use determinant unless you're trying to stress test your computer.
    Finds determinant of a matrix through laplace expansion. Requires a NxN square Matrix where N>1.
    """
    if not check_matrix(matrix1, check_Square=True):
        print("Please input a valid matrix")
        return
    determ = 0
    matrix1Len = len(matrix1)
    if matrix1Len>2:
        matrix1RowLen = len(matrix1[0])
        for item in range(matrix1RowLen):
            relevant_matrix = [row[:] for row in matrix1]
            relevant_matrix.pop(0)
            relevant_matrixLen = len(relevant_matrix)
            for row in range(relevant_matrixLen):
                relevant_matrix[row].pop(item)
            determ+=laplace_determinant(relevant_matrix)*matrix1[0][item]*pow(-1,item)
    elif matrix1Len == 2:
        determ = matrix1[0][0]*matrix1[1][1]-matrix1[0][1]*matrix1[1][0]
    else:
        determ = "Unable to calculate Matrix. Ensure the dimensions of your matrix are greater than 1."
    return determ

def determinant(matrix1):
    """
    Finds determinant of a matrix through LU Facotrization. Requires a NxN square Matrix where N>1.
    """
    L, U = LU_factorize(matrix1)
    det = 1
    matrix1Len = len(matrix1)
    for i in range(matrix1Len):
        det *= U[i][i]
    return det

def brute_inverse(matrix1, multiplyDet=True):
    """
    WARNING: SLOW. Recommended you use inverse unless you're trying to stress test your computer.
    Finds the inverse of the provided matrix. Requires a square Matrix.
    """
    if not check_matrix(matrix1, check_Square=True):
        print("Please input a valid matrix")
        return
    determ = determinant(matrix1)
    if determ == 0:
        return("No inverse exists; determinant is 0")
    result = [row[:] for row in matrix1]

    matrix1Len = len(matrix1)
    matrix1RowLen = len(matrix1[0])
    #Make Matrix of Minors(DONE)
    if len(matrix1)>2:
        for row in range(matrix1Len):
            for col in range(matrix1RowLen):
                relevant_matrix = [row[:] for row in matrix1]
                relevant_matrix.pop(row)
                for row_nest in range(len(relevant_matrix)):
                    relevant_matrix[row_nest].pop(col)
                result[row][col] = determinant(relevant_matrix)
    elif len(matrix1)==2:
        result = [[matrix1[(row + 1)%2][(col+1)%2] for col in range(matrix1RowLen)] for row in range(matrix1Len)]
    else:
        print("bad matrix")
    #Make Cofactors(DONE)
    result = cofactor(result)
    #Make Adjugate(DONE)
    result = transpose(result)
    # Multiply by 1/determinant(DONE)
    if multiplyDet:
        result = scale(result, 1/determ)
        return result
    else:
        return result, determ

def dot(vector1, vector2):
    """Finds dot product of vectors. Vectors must be the same length."""
    if (len(vector1) != len(vector2)) or (vector1[0] is None) or ((type(vector1[0]) != type(1.02)) and (type(vector1[0]) != type(1))) or ((type(vector2[0]) != type(1.02)) and (type(vector2[0]) != type(1))):
        
        print("Please input valid vectors")
        return
    vectorLen = len(vector1)
    result=[vector1[item]*vector2[item] for item in range(vectorLen)]
    return sum(result)


def add(matrix1, matrix2):
    """Adds Matrices. Matrices must have the same dimensions"""
    matrix1Len = len(matrix1)
    matrix1RowLen = len(matrix1[0])
    if not(check_matrix(matrix1) and check_matrix(matrix2) and matrix1Len == len(matrix2) and matrix1RowLen == len(matrix2[0])):
        print("Please input valid matrices")
        return
    result = [[matrix1[row][col] + matrix2[row][col] for col in range(matrix1RowLen)] for row in range(matrix1Len)]
    return result


def subtract(matrix1, matrix2):
    """Subtracts Matrices. Matrices must have the same dimensions."""
    matrix1Len = len(matrix1)
    matrix1RowLen = len(matrix1[0])
    if not(check_matrix(matrix1) and check_matrix(matrix2) and matrix1Len == len(matrix2) and matrix1RowLen == len(matrix2[0])):
        print("Please input valid matrices")
        return
    result = [[matrix1[row][col] - matrix2[row][col] for col in range(matrix1RowLen)] for row in range(matrix1Len)]
    return result



def scale(matrix1, scalar):
    """Multiplies Matrix by a scalar."""
    if not check_matrix(matrix1):
        print("Please input valid matrix")
        return
    matrix1Len = len(matrix1)
    matrix1RowLen = len(matrix1[0])
    result = [[matrix1[row][col]*scalar for col in range(matrix1RowLen)] for row in range(matrix1Len)]
    return result


def matrix_multiply(matrix1,matrix2):
    """Multiplies two matrices. Matrix1 must be an MxN matrix and Matrix2 must be an NxO matrix. Resulting Matrix will be MxO."""
    if not (check_matrix(matrix1) and check_matrix(matrix2) and (len(matrix1[0]) == len(matrix2))):
        print("Please input valid matrices") 
        return
    matrix1Len = len(matrix1)
    matrix2_adjust = transpose(matrix2)
    matrix2_adjustLen = len(matrix2_adjust)
    result = [[dot(matrix1[row],matrix2_adjust[row2]) for row2 in range(matrix2_adjustLen)] for row in range(matrix1Len)]
    return result

def create_identity(size):
    result = [[0 for col in range(size)] for row in range(size)]
    for row in range(size): result[row][row] = 1
    return result

def inverse_by_rows(matrix1):
    """WARNING: SLOW & INNACURATE. Recommended you use inverse unless you're trying to stress test your computer.
        Attempts to inverse a matrix through Gaussian Elimination. Required a square matrix."""
    if not check_matrix(matrix1, check_Square=True):
        print("Please input a valid matrix")
        return
    if laplace_determinant(matrix1) == 0:
        print("No inverse exists; determinant is 0")
        return
    inputMatrix = [row[:] for row in matrix1]
    identityMatrix = create_identity(len(matrix1))
    for rownum in range(len(inputMatrix)):
        pivot = 0
        pivot_colnum = "WAIT"
        for colnum in range(len(inputMatrix[rownum])):
            if pivot == 0:
                pivot = inputMatrix[rownum][colnum]
            if pivot != 0:
                if pivot_colnum == "WAIT": pivot_colnum = colnum
                #result = [[matrix1[row][col]*scalar for col in range(len(matrix1[row]))] for row in range(len(matrix1))]
                inputMatrix[rownum] = [inputMatrix[rownum][col]/pivot for col in range(len(inputMatrix[rownum]))]
                identityMatrix[rownum] = [identityMatrix[rownum][col]/pivot for col in range(len(identityMatrix[rownum]))]
        if pivot_colnum == "WAIT":
            continue
        for nest_rownum in range (len(inputMatrix)):
            #check every row to ensure the pivot alone is the nonzero one(literally)
            if inputMatrix[nest_rownum][pivot_colnum] != 0 and nest_rownum != rownum:
                scalar = inputMatrix[nest_rownum][pivot_colnum]/inputMatrix[rownum][pivot_colnum]
                for nest_colnum in range(len(inputMatrix[nest_rownum])):
                    inputMatrix[nest_rownum][nest_colnum] -= inputMatrix[rownum][nest_colnum]*scalar
                    identityMatrix[nest_rownum][nest_colnum] -= identityMatrix[rownum][nest_colnum]*scalar
    return identityMatrix


def LU_factorize(matrix1):
    """Perform LU decomposition of a square matrix.
    Returns L (lower triangular) and U (upper triangular) matrices."""
    if not check_matrix(matrix1, check_Square=True):
        print("Please input a valid matrix")
        return
    matrix1Len = len(matrix1)
    L = [[0.0] * matrix1Len for _ in range(matrix1Len)]
    U = [[0.0] * matrix1Len for _ in range(matrix1Len)]

    for i in range(matrix1Len):
        #Upper Triangular
        for k in range(i, matrix1Len):
            U[i][k] = matrix1[i][k] - sum(L[i][j] * U[j][k] for j in range(i))

        #Lower Triangular
        for k in range(i, matrix1Len):
            if i == k:
                L[i][i] = 1
            else:
                L[k][i] = (matrix1[k][i] - sum(L[k][j] * U[j][i] for j in range(i))) / U[i][i]

    return L, U

def inverse(matrix1):
    """Finds the inverse of the provided matrix. Requires a square Matrix."""
    if not check_matrix(matrix1, check_Square=True):
        print("Please input a valid matrix")
        return
    L,U = LU_factorize(matrix1)
    matrix1Len = len(matrix1)
    identityMatrix = create_identity(matrix1Len)
    inverse_matrix = [[0.0] * matrix1Len for _ in range(matrix1Len)]

    Y = [[0.0] * matrix1Len for _ in range(matrix1Len)]
    for col in range(matrix1Len):
        for row in range(matrix1Len):
            Y[row][col] = identityMatrix[row][col] - sum(L[row][k] * Y[k][col] for k in range(row))

    # Solve U * X = Y for each column of Y
    for col in range(matrix1Len):
        for row in reversed(range(matrix1Len)):
            inverse_matrix[row][col] = (Y[row][col] - sum(U[row][k] * inverse_matrix[k][col] for k in range(row + 1, matrix1Len))) / U[row][row]

    return inverse_matrix


def print_matrix(matrix1):
    """Prints Matrices more legibly"""
    for row in matrix1:
        print(row)


def check_matrix(matrix1, check_Square = False):
    """Checks if the input is a valid matrix. 
        Set check_Square to True if you'd like it to check if the input is a valid square matrix."""
    if not matrix1 or not isinstance(matrix1, list) or not isinstance(matrix1[0], list):
        return False
    matrix1Len = len(matrix1)
    col_len = len(matrix1[0])
    if not all(isinstance(row, list) and len(row) == col_len for row in matrix1):
        return False
    if check_Square == True:
        return (col_len==matrix1Len)
    return True

def tell_version():
    print("v0.1.1")