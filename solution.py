"""
Skiing in Singapore solution
Author: Karthik Balakrishnan
"""

import time

# Global variables
solution = {}
best = (-1, -1, -1, -1)

def get_matrix(filename):
    """
    Get the matrix from stdin
    """
    with open(filename) as f:
        lines = f.readlines()
    values = [int(_) for _ in lines[0].rstrip().split(' ')]
    M = values[0]
    N = values[1]

    matrix = []
    for idx in range(1, M + 1):
        matrix.append([int(_) for _ in lines[idx].rstrip().split(' ')])

    return M, N, matrix

def solve(matrix, M, N, x, y, soln):
    """
    Solve the given matrix using dynamic programming
    """
    global solution, best
    # base case
    base_case = True
    if x + 1 < M:
        if matrix[x + 1][y] < matrix[x][y]:
            base_case = False
    if base_case and x - 1 > -1:
        if matrix[x - 1][y] < matrix[x][y]:
            base_case = False
    if base_case and y + 1 < N:
        if matrix[x][y + 1] < matrix[x][y]:
            base_case = False
    if base_case and y - 1 > -1:
        if matrix[x][y - 1] < matrix[x][y]:
            base_case = False

    if base_case:
        soln = (soln[0], matrix[x][y])
        if best[2] < soln[0]:
            best = (x, y, soln[0], matrix[x][y] - soln[1])
        elif best[2] == soln[0]:
            if best[3] < matrix[x][y] - soln[1]:
                best = (x, y, soln[0], matrix[x][y] - soln[1])
        return soln

    key = x * N + y

    solutions = []

    if x + 1 < M and matrix[x + 1][y] < matrix[x][y]:
        try:
            solutions.append((1 + solution[(x + 1) * M + y][0], solution[(x + 1) * M + y][1]))
        except (KeyError, TypeError) as error:
            solution[(x + 1) * N + y] = solve(matrix, M, N, x + 1, y, soln)
            solutions.append((1 + solution[(x + 1) * M + y][0], solution[(x + 1) * M + y][1]))
    if x - 1 > -1 and matrix[x - 1][y] < matrix[x][y]:
        try:
            solutions.append((1 + solution[(x - 1) * M + y][0], solution[(x - 1) * M + y][1]))
        except (KeyError, TypeError) as error:
            solution[(x - 1) * N + y] = solve(matrix, M, N, x - 1, y, soln)
            solutions.append((1 + solution[(x - 1) * M + y][0], solution[(x - 1) * M + y][1]))
    if y + 1 < N and matrix[x][y + 1] < matrix[x][y]:
        try:
            solutions.append((1 + solution[x * M + y + 1][0], solution[x * M + y + 1][1]))
        except (KeyError, TypeError) as error:
            solution[x * N + y + 1] = solve(matrix, M, N, x, y + 1, soln)
            solutions.append((1 + solution[x * M + y + 1][0], solution[x * M + y + 1][1]))
    if y - 1 > -1 and matrix[x][y - 1] < matrix[x][y]:
        try:
            solutions.append((1 + solution[x * M + y - 1][0], solution[x * M + y - 1][1]))
        except (KeyError, TypeError) as error:
            solution[x * N + y - 1] = solve(matrix, M, N, x, y - 1, soln)
            solutions.append((1 + solution[x * M + y - 1][0], solution[x * M + y - 1][1]))

    solutions.sort(key=lambda x: x[0], reverse=True)

    soln = solutions[0]

    for idx in range(len(solutions)):
        if solutions[idx][0] == solutions[0][0]:
            if (matrix[x][y] - solutions[idx][1]) > (matrix[x][y] - solutions[0][1]):
                soln = solutions[idx]
        else:
            break

    if best[2] < soln[0]:
    	best = (x, y, soln[0], matrix[x][y] - soln[1])
    elif best[2] == soln[0]:
    	if best[3] < matrix[x][y] - soln[1]:
    		best = (x, y, soln[0], matrix[x][y] - soln[1])

    return soln


if __name__ == '__main__':
    #M, N, matrix = get_matrix('test_map.txt')
    M, N, matrix = get_matrix('map.txt')
    start_time = time.time()
    for idx_i in range(M):
       for idx_j in range(N):
           solution[idx_i * N + idx_j] = solve(matrix, M, N, idx_i, idx_j, (1, matrix[idx_i][idx_j]))
    end_time = time.time()
    print 'Took %f s to solve the matrix' % (end_time - start_time)
    print 'Length: %d, Drop: %d' % (best[2], best[3])