import datetime
from copy import deepcopy

CELLS_FILLED = 0
WOOPS_COUNT = 0
GUESSES = []

def setup(grid):
    global CELLS_FILLED
    initial_solved = []
    for row_index in range(len(grid)):
        for column_index in range(len(grid[row_index])):
            if grid[row_index][column_index] == 0:
                grid[row_index][column_index] = {1, 2, 3, 4, 5, 6, 7, 8, 9}
            else:
                initial_solved.append((row_index, column_index, grid[row_index][column_index]))
                CELLS_FILLED += 1
    return initial_solved


def pretty_print(grid):
    for r_index, row in enumerate(grid):
        print()
        if r_index % 3 == 0:
            print('--'*(len(row) + 3))
        for c_index, cell in enumerate(row):
            if c_index % 3 == 0:
                print('|', end=' ')
            if isinstance(cell, set):
                print('_', end=' ')
            else:
                print(cell, end=' ')
        print('|', end=' ')
    print('\n\n')


def solve(grid, solved=None):
    global CELLS_FILLED
    global GUESSES
    if solved is not None:
        solve_for_uniques(grid, solved)

    if CELLS_FILLED == 81:
        return grid
    row, column = find_first_unknown(grid)

    # TODO handle random guesses
    # except:
    #     pretty_print(grid)
    #     return grid
    # original = deepcopy(grid)
    # for option in original[row][column]:
    #     try:
    #         message = f'{option} guessed in ({row},{column})'
    #         print(message)
    #         grid[row][column] = option
    #         solved = [(row, column, option)]
    #         cells_filled = CELLS_FILLED
    #         solve(grid, solved)
    #     except Woops:
    #         message += ' - incorrect'
    #         GUESSES.append(message)
    #         CELLS_FILLED = cells_filled
    #         del grid
    #         grid = deepcopy(original)
    #         continue
    #     message += ' - correct'
    #     GUESSES.append(message)
    #     if CELLS_FILLED == 81:
    #         return grid
    # return grid

def find_first_unknown(grid):
    for row_index in range(len(grid)):
        for col_index in range(len(grid)):
            if isinstance(grid[row_index][col_index], set):
                return row_index, col_index


def solve_for_uniques(grid, solved=None):
    global CELLS_FILLED
    for solved_row_index, solved_column_index, solved_value in solved:
        # check row
        row = grid[solved_row_index]
        for col_index, cell in enumerate(row):
            if col_index == solved_column_index:
                continue
            if isinstance(cell, set) and solved_value in cell:
                cell.remove(solved_value)
                if len(cell) == 1:
                    value = cell.pop()
                    grid[solved_row_index][col_index] = value
                    solved.append((solved_row_index, col_index, value))
                    CELLS_FILLED += 1
            else:
                if cell == solved_value:
                    # you done goofed
                    raise Woops

        # check column
        for r_index, row in enumerate(grid):
            if r_index == solved_row_index:
                continue
            cell = row[solved_column_index]
            if isinstance(cell, set) and solved_value in cell:
                cell.remove(solved_value)
                if len(cell) == 1:
                    value = cell.pop()
                    grid[r_index][solved_column_index] = value
                    solved.append((r_index, solved_column_index, value))
                    CELLS_FILLED += 1
            else:
                if cell == solved_value:
                    raise Woops

        # check square
        square_row_start = solved_row_index - solved_row_index % 3
        square_col_start = solved_column_index - solved_column_index % 3
        for r_index in range(3):
            r_index = square_row_start + r_index
            if r_index == solved_row_index:
                continue
            for c_index in range(3):
                c_index = square_col_start + c_index
                if c_index == solved_column_index:
                    continue
                cell = grid[r_index][c_index]
                if isinstance(cell, set) and solved_value in cell:
                    cell.remove(solved_value)
                    if len(cell) == 1:
                        value = cell.pop()
                        grid[r_index][c_index] = value
                        solved.append((r_index, c_index, value))
                        CELLS_FILLED += 1
                elif cell == solved_value:
                    raise Woops
        if grid[4][2] == 6:
            print(solved_row_index, solved_column_index, solved_value)


class Woops(Exception):
    def __init__(self):
        global WOOPS_COUNT
        WOOPS_COUNT += 1


if __name__ == '__main__':
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
    hard = [
        [0, 0, 5, 2, 0, 0, 0, 0, 4],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 2, 3, 0, 5, 9, 0, 7],
        [0, 5, 0, 0, 2, 9, 3, 0, 0],
        [0, 9, 0, 0, 0, 0, 0, 2, 0],
        [0, 0, 1, 4, 3, 0, 0, 0, 0],
        [9, 0, 3, 5, 0, 4, 8, 0, 6],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [7, 0, 0, 0, 0, 3, 5, 0, 0]
    ]
    grid = easy
    print('Input is')
    pretty_print(grid)
    now = datetime.datetime.now()
    initial_solved = setup(grid)
    output = solve(grid, initial_solved)
    duration = datetime.datetime.now() - now
    print('\n\n')
    print('Output is:')
    pretty_print(output)
    print(f'Incorrect guesses: {WOOPS_COUNT}')
    print(f'Duration: {duration}')
    print(CELLS_FILLED)
