import solver


def test_difference_elimination():
    input_sets = [{1, 2, 3}, {1, 5}, {1, 2, 4}, {1, 5}, {1, 5, 6}, {1, 2, 4}]
    expected = [{3}, {1, 5}, {1, 2, 4}, {1, 5}, {6}, {1, 2, 4}]

    actual = solver.difference_elimination(input_sets)

    assert expected == actual


def test_get_row_set_difference():
    grid = [[7, 9, {1, 2, 3}, {1, 5}, {1, 2, 4}, 8, {1, 5}, {1, 5, 6}, {1, 2, 4}]]
    expected_solved = [(0, 2, 3), (0, 7, 6)]

    actual_solved = solver.set_difference_rows(grid)

    assert expected_solved == actual_solved


def test_get_col_set_difference():
    grid = [
        [7, 0, 0, 0, 0, 0, 0, 0, 0],
        [9, 0, 0, 0, 0, 0, 0, 0, 0],
        [{1, 2, 3}, 0, 0, 0, 0, 0, 0, 0, 0],
        [{1, 5}, 0, 0, 0, 0, 0, 0, 0, 0],
        [{1, 2, 4}, 0, 0, 0, 0, 0, 0, 0, 0],
        [8, 0, 0, 0, 0, 0, 0, 0, 0],
        [{1, 5}, 0, 0, 0, 0, 0, 0, 0, 0],
        [{1, 5, 6}, 0, 0, 0, 0, 0, 0, 0, 0],
        [{1, 2, 4}, 0, 0, 0, 0, 0, 0, 0, 0],
    ]

    expected_solved = [(2, 0, 3), (7, 0, 6)]
    actual_solved = solver.set_difference_columns(grid)

    assert expected_solved == actual_solved

def test_get_square_set_difference():
    input_grid = [
        [7, 9, {1, 2, 3}, 0, 0, 0, 0, 0, 0],
        [{1, 5}, {1, 2, 4}, 8, 0, 0, 0, 0, 0, 0],
        [{1, 5}, {1, 5, 6}, {1, 2, 4}, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]

    expected_solved = [(0, 2, 3), (2, 1, 6)]
    actual_solved = solver.set_difference_squares(input_grid)

    assert expected_solved == actual_solved


def test_row_pairs():
    input_grid = [
        [{3, 4, 5}, {3, 4}, 2, {3, 5, 6, 7, 8, 9}, {3, 4}],
    ]
    expected_grid = [
        [5, {3, 4}, 2, {5, 6, 7, 8, 9}, {3, 4}],
    ]
    expected_solved = [(0, 0, 5)]

    actual_solved = solver.pairs_rows(input_grid)
    assert input_grid == expected_grid
    assert actual_solved == expected_solved


def test_col_pairs():
    input_grid = [
        [{3, 4, 5}, 6, 0, 0, 0, 0, 0, 0, 0],
        [{3, 4}, {5, 7}, 0, 0, 0, 0, 0, 0, 0],
        [{4, 5}, 4, 0, 0, 0, 0, 0, 0, 0],
        [{4, 5, 6}, {8, 9}, 0, 0, 0, 0, 0, 0, 0],
        [{3, 4}, 2, 0, 0, 0, 0, 0, 0, 0],
    ]
    expected_grid = [
        [5, 6, 0, 0, 0, 0, 0, 0, 0],
        [{3, 4}, {5, 7}, 0, 0, 0, 0, 0, 0, 0],
        [5, 4, 0, 0, 0, 0, 0, 0, 0],
        [{5, 6}, {8, 9}, 0, 0, 0, 0, 0, 0, 0],
        [{3, 4}, 2, 0, 0, 0, 0, 0, 0, 0],
    ]
    expected_solved = [(0, 0, 5), (2, 0, 5)]

    actual_solved = solver.pairs_columns(input_grid)
    assert input_grid == expected_grid
    assert actual_solved == expected_solved


def test_get_square():
    input_grid = [
        [1, 2, 3, 0, 0, 0, 0, 0, 0],
        [4, 5, 6, 0, 0, 0, 0, 0, 0],
        [7, 8, 9, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
    expected = [
        (0, 0, 1),
        (0, 1, 2),
        (0, 2, 3),
        (1, 0, 4),
        (1, 1, 5),
        (1, 2, 6),
        (2, 0, 7),
        (2, 1, 8),
        (2, 2, 9),
    ]

    input_row_start = 0
    input_col_start = 0

    actual = solver.get_square(input_grid, input_row_start, input_col_start)

    assert actual == expected


def test_square_pairs():
    input_grid = [
        [{8, 9}, 2, {3, 7, 8}, 0, 0, 0, 0, 0, 0],
        [4, {5, 8, 9}, 6, 0, 0, 0, 0, 0, 0],
        [1, {3, 7}, {8, 9}, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
    expected_grid = [
        [{8, 9}, 2, {3, 7}, 0, 0, 0, 0, 0, 0],
        [4, 5, 6, 0, 0, 0, 0, 0, 0],
        [1, {3, 7}, {8, 9}, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]

    expected_solved = [(1, 1, 5)]

    actual_solved = solver.pairs_squares(input_grid)
    assert input_grid == expected_grid
    assert actual_solved == expected_solved


def test_find_guess_cells():
    input_grid = [
        [{1, 2, 3, 4, 5}, 0, 5, 2, 0, 0, 0, {1, 2, 3}, 4],
        [0, 0, 0, 0, {1, 2, 3, 4}, 0, 0, 0, 0],
        [4, 0, 2, 3, 0, 5, 9, 0, 7],
        [0, 5, 0, 0, 2, 9, 3, 0, 0],
        [0, 9, {1, 2}, 0, 0, 0, 0, 2, 0],
        [0, 0, 1, 4, 3, 0, 0, 9, 0],
        [9, 0, 3, 5, 0, 4, 8, 0, 6],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [7, 0, 0, 0, 0, 3, 5, 0, 0]
    ]

    expected = [(4, 2), (0, 7), (1, 4), (0, 0)]

    actual = solver.find_guess_cells(input_grid)

    assert actual == expected

def test_hard_end_to_end():
    input_grid = [
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
    initial_solved = solver.setup(input_grid)

    expected = [
        [1, 3, 5, 2, 9, 7, 6, 8, 4],
        [6, 7, 9, 8, 4, 1, 2, 5, 3],
        [4, 8, 2, 3, 6, 5, 9, 1, 7],
        [8, 5, 4, 7, 2, 9, 3, 6, 1],
        [3, 9, 7, 1, 5, 6, 4, 2, 8],
        [2, 6, 1, 4, 3, 8, 7, 9, 5],
        [9, 2, 3, 5, 1, 4, 8, 7, 6],
        [5, 4, 8, 6, 7, 2, 1, 3, 9],
        [7, 1, 6, 9, 8, 3, 5, 4, 2],
]
    actual = solver.solve(input_grid, initial_solved)
    assert actual == expected


def test_easy_end_to_end():
    input_grid = [
        [0, 0, 2, 0, 0, 0, 0, 1, 0],
        [0, 8, 5, 4, 0, 0, 0, 6, 0],
        [0, 0, 4, 0, 6, 1, 0, 0, 8],
        [5, 3, 1, 9, 8, 0, 0, 0, 0],
        [0, 4, 9, 2, 0, 0, 8, 3, 0],
        [0, 2, 7, 6, 0, 0, 0, 0, 9],
        [4, 0, 0, 0, 3, 2, 1, 5, 7],
        [0, 0, 8, 7, 0, 5, 0, 0, 0],
        [0, 5, 0, 0, 9, 6, 2, 8, 0],
    ]
    initial_solved = solver.setup(input_grid)

    expected = [
        [9, 6, 2, 3, 7, 8, 4, 1, 5],
        [1, 8, 5, 4, 2, 9, 7, 6, 3],
        [3, 7, 4, 5, 6, 1, 9, 2, 8],
        [5, 3, 1, 9, 8, 4, 6, 7, 2],
        [6, 4, 9, 2, 5, 7, 8, 3, 1],
        [8, 2, 7, 6, 1, 3, 5, 4, 9],
        [4, 9, 6, 8, 3, 2, 1, 5, 7],
        [2, 1, 8, 7, 4, 5, 3, 9, 6],
        [7, 5, 3, 1, 9, 6, 2, 8, 4],
    ]
    actual = solver.solve(input_grid, initial_solved)
    assert actual == expected
