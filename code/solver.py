import datetime
from copy import deepcopy

WOOPS_COUNT = 0
GUESSES = 0
RESETS = 0
LOOPS = 0


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


def check_solved(grid):
    is_solved = all(isinstance(cell, int) for row in grid for cell in row)
    if is_solved:
        print('Solved')
    return is_solved


def solve(grid, solved_to_propagate):
    global LOOPS
    global GUESSES
    global RESETS
    propagate_constraints(grid, solved_to_propagate)
    if check_solved(grid):
        return grid

    not_stalled = True
    while not_stalled:
        LOOPS += 1
        not_stalled = False

        for set_diff_check in [set_difference_rows, set_difference_columns, set_difference_squares]:
            solved_diffs = set_diff_check(grid)
            if solved_diffs:
                not_stalled = True
                propagate_constraints(grid, solved_diffs)
            if check_solved(grid):
                return grid

        for pair_check in [pairs_rows, pairs_columns, pairs_squares]:
            solved_pairs = pair_check(grid)
            if solved_pairs:
                not_stalled = True
                propagate_constraints(grid, solved_pairs)
            if check_solved(grid):
                return grid

    unknown_cells = find_guess_cells(grid)
    old_grid = deepcopy(grid)
    for r_index, c_index in unknown_cells:
        # handling mutability
        grid = old_grid
        old_grid = deepcopy(grid)
        for guess in old_grid[r_index][c_index]:
            GUESSES += 1
            grid[r_index][c_index] = guess
            new_solved = [(r_index, c_index, guess)]
            try:
                return solve(grid, new_solved)
            except BadChoice:
                # Try next guess if first fails
                continue
    # if gets here tried all possibilities, failure was earlier
    RESETS += 1
    raise BadChoice


def propagate_constraints(grid, solved):
    solvers = [solve_row, solve_square, solve_column]
    for solved_tuple in solved:
        for solver in solvers:
            new_solved = solver(grid, *solved_tuple)
            if new_solved:
                solved += new_solved


def get_square(grid, row_start, col_start):
    square = []
    for r_index in range(row_start, row_start + 3):
        for c_index in range(col_start, col_start + 3):
            square.append((r_index, c_index, grid[r_index][c_index]))
    return square


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
    square = get_square(grid, square_row_start, square_col_start)
    for r_index, c_index, cell in square:
        if isinstance(cell, set) and solved_value in cell:
            cell.remove(solved_value)
            if len(cell) == 1:
                value = cell.pop()
                grid[r_index][c_index] = value
                new_solved.append((r_index, c_index, value))
        elif r_index == solved_row_index and c_index == solved_column_index:
            continue
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
    for square_row_start in range(0, 9, 3):
        for square_col_start in range(0, 9, 3):
            square = get_square(grid, square_row_start, square_col_start)
            pairs = []
            for index, cell_details in enumerate(square):
                cell = cell_details[2]
                if isinstance(cell, int):
                    continue
                if len(cell) == 2:
                    for next_cell_details in square[index + 1:]:
                        next_cell = next_cell_details[2]
                        if next_cell == cell:
                            pairs.append(cell)
            for pair in pairs:
                for r_index, c_index, cell in square:
                    if cell == pair:
                        continue
                    if isinstance(cell, int):
                        continue
                    for choice in pair:
                        if choice in cell:
                            cell.remove(choice)
                            if len(cell) == 1:
                                value = cell.pop()
                                grid[r_index][c_index] = value
                                new_solved.append((r_index, c_index, value))
    return new_solved


def difference_elimination(set_list):
    for index, num_set in enumerate(set_list):
        other_sets_union = set()
        for i2, other_set in enumerate(set_list):
            if i2 != index:
                other_sets_union = other_sets_union | other_set
        difference = num_set - other_sets_union
        if difference:
            # if no difference then its a subset
            set_list[index] = difference
    return set_list


def update_sets(update_list, grid):
    new_solved = []
    for cell, coords in update_list:
        row_index, col_index = coords
        if len(cell) == 1:
            cell = cell.pop()
            new_solved.append((row_index, col_index, cell))
            grid[row_index][col_index] = cell

    return new_solved


def set_difference_rows(grid):
    new_solved = []
    for row_index, row in enumerate(grid):
        coordinates = []
        sets = []
        for col_index, cell in enumerate(row):
            if isinstance(cell, set):
                sets.append(cell)
                coordinates.append((row_index, col_index))
        sets = difference_elimination(sets)
        new_solved += update_sets(zip(sets, coordinates), grid)

    return new_solved


def set_difference_columns(grid):
    new_solved = []
    for col_index in range(9):
        coordinates = []
        sets = []
        for row_index, row in enumerate(grid):
            cell = row[col_index]
            if isinstance(cell, set):
                sets.append(cell)
                coordinates.append((row_index, col_index))
        sets = difference_elimination(sets)
        new_solved += update_sets(zip(sets, coordinates), grid)

    return new_solved


def set_difference_squares(grid):
    new_solved = []
    for row_start in range(0, 9, 3):
        for col_start in range(0, 9, 3):
            square = get_square(grid, row_start, col_start)
            sets = [x for r, c, x in square if isinstance(x, set)]
            coordinates = [(r, c) for r, c, x in square if isinstance(x, set)]
            sets = difference_elimination(sets)
            new_solved += update_sets(zip(sets, coordinates), grid)

    return new_solved


def find_guess_cells(grid):
    output = []
    for r_index, row in enumerate(grid):
        for c_index, cell in enumerate(row):
            if isinstance(cell, set):
                output.append((r_index, c_index))
    return sorted(output, key=lambda x: len(grid[x[0]][x[1]]))


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
    guesses_needed = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [4, 0, 0, 0, 0, 0, 9, 0, 7],
        [0, 0, 0, 0, 0, 0, 3, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 2, 0],
        [0, 0, 1, 4, 3, 0, 0, 9, 0],
        [0, 0, 0, 5, 0, 4, 0, 0, 6],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
    empty_guesses_needed = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
    input_grid = guesses_needed
    print('Input is')
    pretty_print(input_grid)
    now = datetime.datetime.now()
    initial_solved = setup(input_grid)
    output = solve(input_grid, initial_solved)
    duration = datetime.datetime.now() - now
    print('\n\n')
    print('Output is:')
    pretty_print(output)
    print(f'Amount of guesses: {GUESSES}')
    print(f'Incorrect guesses: {WOOPS_COUNT}')
    print(f'Resets needed: {RESETS}')
    print(f'Duration: {duration}')
    print(f'Constraint Loops: {LOOPS}')
