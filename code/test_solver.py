import solver


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
