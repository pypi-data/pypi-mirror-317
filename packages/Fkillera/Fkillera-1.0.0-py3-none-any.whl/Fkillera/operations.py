def add_matrices(matrix1, matrix2):
    """Add two matrices."""
    if len(matrix1) != len(matrix2) or len(matrix1[0]) != len(matrix2[0]):
        raise ValueError("Matrices must have the same dimensions for addition.")
    
    result = []
    for i in range(len(matrix1)):
        row = []
        for j in range(len(matrix1[0])):
            row.append(matrix1[i][j] + matrix2[i][j])
        result.append(row)
    return result

def multiply_matrices(matrix1, matrix2):
    """Multiply two matrices."""
    if len(matrix1[0]) != len(matrix2):
        raise ValueError("Number of columns in the first matrix must be equal to the number of rows in the second matrix.")
    
    result = []
    for i in range(len(matrix1)):
        row = []
        for j in range(len(matrix2[0])):
            sum_product = 0
            for k in range(len(matrix2)):
                sum_product += matrix1[i][k] * matrix2[k][j]
            row.append(sum_product)
        result.append(row)
    return result