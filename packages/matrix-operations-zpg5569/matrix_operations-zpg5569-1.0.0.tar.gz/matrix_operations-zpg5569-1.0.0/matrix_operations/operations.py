def add_matrices(matrix1, matrix2):
    #Add two matrices.
    # 检查两个矩阵是否具有相同的维度，如果不相同则抛出异常
    if len(matrix1) != len(matrix2) or len(matrix1[0]) != len(matrix2[0]):
        raise ValueError("Matrices must have the same dimensions for addition.")

    # 初始化结果矩阵，初始为空列表
    result = []
    # 遍历第一个矩阵的行
    for i in range(len(matrix1)):
        # 初始化当前行的结果列表
        row = []
        # 遍历当前行的列
        for j in range(len(matrix1[0])):
            # 将两个矩阵相同位置的元素相加，并添加到当前行的结果列表中
            row.append(matrix1[i][j] + matrix2[i][j])
        # 将当前行的结果列表添加到结果矩阵中
        result.append(row)
    # 返回结果矩阵
    return result

def multiply_matrices(matrix1, matrix2):
    #Multiply two matrices.
    # 检查矩阵是否满足乘法条件，即第一个矩阵的列数是否等于第二个矩阵的行数
    if len(matrix1[0]) != len(matrix2):
        raise ValueError(
            "Number of columns in the first matrix must be equal to the number of rows in the second matrix.")

    # 初始化结果矩阵，初始为空列表
    result = []
    # 遍历第一个矩阵的行
    for i in range(len(matrix1)):
        # 初始化当前行的结果列表
        row = []
        # 遍历第二个矩阵的列
        for j in range(len(matrix2[0])):
            # 初始化当前元素的乘积和
            sum_product = 0
            # 遍历第二个矩阵的行，计算第一个矩阵的行与第二个矩阵的列的点积
            for k in range(len(matrix2)):
                sum_product += matrix1[i][k] * matrix2[k][j]
            # 将计算出的乘积和添加到当前行的结果列表中
            row.append(sum_product)
        # 将当前行的结果列表添加到结果矩阵中
        result.append(row)
    # 返回结果矩阵
    return result
