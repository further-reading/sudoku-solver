import datetime
from copy import deepcopy

WOOPS_COUNT = 0


def setup(grid):
    initial_solved = []
    for row_index in range(len(grid)):
        for column_index in range(len(grid[row_index])):
            if grid[row_index][column_index] == 0:
                grid[row_index][column_index] = {1, 2, 3, 4, 5, 6, 7, 8, 9}
            else:
                initial_solved.append((row_index, column_index, grid[row_index][column_index]))
    return initial_solved


def pretty_print(grid):
    for r_index, row in enumerate(grid):
        print()
        if r_index % 3 == 0:
            print('--'*(len(row) + 3))
        for c_index, cell in enumerate(row):
            if c_index % 3 == 0:
                print('|', end=' ')
            if isinstance(cell, set) or cell == 0:
                print('_', end=' ')
            else:
                print(cell, end=' ')
        print('|', end=' ')
    print('\n\n')


def is_solved(grid):
    return all(isinstance(cell, int) for row in grid for cell in row)


def solve(grid, solved_to_propagate):
    propagate_constraints(grid, solved_to_propagate)
    if is_solved(grid):
        return grid

    # TODO pair elimination
    solved_rows = pairs_rows(grid)
    if solved_rows:
        propagate_constraints(grid, solved_rows)
    if is_solved(grid):
        return grid

    solved_cols = pairs_columns(grid)
    if solved_cols:
        propagate_constraints(grid, solved_cols)
    if is_solved(grid):
        return grid

    solved_squares = pairs_squares(grid)
    if solved_squares:
        propagate_constraints(grid, solved_squares)
    if is_solved(grid):
        return grid

    # TODO Odd one out eliminations
    solved_odd_one_out = odd_ones_out(grid)
    if solved_odd_one_out:
        propagate_constraints(grid, solved_odd_one_out)
        if is_solved(grid):
            return grid

    # TODO backtracking
    # if here then not solved and no additional constraints to propagate
    # will eventually implement backtracking here
    print('failed')
    return grid


def propagate_constraints(grid, solved):
    changes_made = False
    for solved_tuple in solved:
        new_solved = solve_row(grid, *solved_tuple)
        if new_solved:
            solved += new_solved
            changes_made = True

        new_solved = solve_column(grid, *solved_tuple)
        if new_solved:
            solved += new_solved
            changes_made = True

        new_solved = solve_square(grid, *solved_tuple)
        if new_solved:
            solved += new_solved
            changes_made = True
    return changes_made


def solve_row(grid, solved_row_index, solved_column_index, solved_value):
    new_solved = []
    row = grid[solved_row_index]
    for col_index, cell in enumerate(row):
        if col_index == solved_column_index:
            continue
        if isinstance(cell, set) and solved_value in cell:
            cell.remove(solved_value)
            if len(cell) == 1:
                value = cell.pop()
                grid[solved_row_index][col_index] = value
                new_solved.append((solved_row_index, col_index, value))
        else:
            if cell == solved_value:
                raise BadChoice
    return new_solved


def solve_column(grid, solved_row_index, solved_column_index, solved_value):
    new_solved = []
    for r_index, row in enumerate(grid):
        if r_index == solved_row_index:
            continue
        cell = row[solved_column_index]
        if isinstance(cell, set) and solved_value in cell:
            cell.remove(solved_value)
            if len(cell) == 1:
                value = cell.pop()
                grid[r_index][solved_column_index] = value
                new_solved.append((r_index, solved_column_index, value))
        else:
            if cell == solved_value:
                raise BadChoice
    return new_solved


def solve_square(grid, solved_row_index, solved_column_index, solved_value):
    new_solved = []
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
                    new_solved.append((r_index, c_index, value))
            elif cell == solved_value:
                raise BadChoice
    return new_solved


def pairs_rows(grid):
    new_solved = []
    for row_index, row in enumerate(grid):
        pairs = []
        for col_index, cell in enumerate(row[:-1]):
            if isinstance(cell, int):
                continue
            elif len(cell) == 2:
                if cell in row[col_index + 1:]:
                    pairs.append(cell)
        for pair in pairs:
            for col_index, cell in enumerate(row):
                if cell == pair:
                    continue
                if isinstance(cell, int):
                    continue
                for choice in pair:
                    if choice in cell:
                        cell.remove(choice)
                        if len(cell) == 1:
                            value = cell.pop()
                            grid[row_index][col_index] = value
                            new_solved.append((row_index, col_index, value))
    return new_solved


def pairs_columns(grid):
    new_solved = []
    for col_index in range(9):
        pairs = []
        for row_index, row in enumerate(grid[:-1]):
            cell = row[col_index]
            if isinstance(cell, int):
                continue
            if len(cell) == 2:
                for next_row in grid[row_index + 1:]:
                    if cell == next_row[col_index]:
                        pairs.append(cell)

        for pair in pairs:
            for row_index, row in enumerate(grid):
                cell = row[col_index]
                if cell == pair:
                    continue
                if isinstance(cell, int):
                    continue
                for choice in pair:
                    if choice in cell:
                        cell.remove(choice)
                        if len(cell) == 1:
                            value = cell.pop()
                            grid[row_index][col_index] = value
                            new_solved.append((row_index, col_index, value))
    return new_solved


def pairs_squares(grid):
    new_solved = []
    return new_solved

def odd_ones_out(grid):
    return []

class BadChoice(Exception):
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
        [4, 0, 2, 3, 0, 5, 9, 0, 7],
        [0, 5, 0, 0, 2, 9, 3, 0, 0],
        [0, 9, 0, 0, 0, 0, 0, 2, 0],
        [0, 0, 1, 4, 3, 0, 0, 9, 0],
        [9, 0, 3, 5, 0, 4, 8, 0, 6],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [7, 0, 0, 0, 0, 3, 5, 0, 0]
    ]
    input_grid = easy
    print('Input is')
    pretty_print(input_grid)
    now = datetime.datetime.now()
    initial_solved = setup(input_grid)
    output = solve(input_grid, initial_solved)
    duration = datetime.datetime.now() - now
    print('\n\n')
    print('Output is:')
    pretty_print(output)
    print(f'Incorrect guesses: {WOOPS_COUNT}')
    print(f'Duration: {duration}')
