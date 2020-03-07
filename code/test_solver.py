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
    expected = {
        (0, 0): 1,
        (0, 1): 2,
        (0, 2): 3,
        (1, 0): 4,
        (1, 1): 5,
        (1, 2): 6,
        (2, 0): 7,
        (2, 1): 8,
        (2, 2): 9,
    }

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
