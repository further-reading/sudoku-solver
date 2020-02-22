def setup(grid):
    solved = []
    for row_index in range(len(grid)):
        for column_index in range(len(grid[row_index])):
            if grid[row_index][column_index] == 0:
                grid[row_index][column_index] = {1, 2, 3, 4, 5, 6, 7, 8, 9}
            else:
                solved.append((row_index, column_index))
    return solved


def solve(grid):
    solved = setup(grid)
    while solved:
        for row, column in solved:
            print(row, column)


if '__name__' == '__main__':
    easy = [
        [0, 0, 2, 0, 0, 0, 0, 1, 0],
        [0, 8, 5, 4, 0, 0, 0, 6, 0],
        [0, 0, 4, 0, 6, 1, 0, 0, 8],
        [5, 3, 1, 9, 8, 0, 0, 0, 0],
        [0, 4, 9, 2, 0, 0, 8, 3, 0],
        [0, 2, 7, 6, 0, 0, 0, 0, 9],
        [4, 0, 0, 0, 3, 2, 1, 5, 7],
        [0, 0, 8, 7, 0, 5, 0, 0, 0],
        [0, 5, 0, 0, 9, 6, 2, 8, 0]
    ]
    solve(easy)
