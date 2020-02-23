import solver

import solver


def test_difference_elimination():
    input = [{1, 2, 3}, {1, 5}, {1, 2, 4}, {1, 5}, {1, 5, 6}, {1, 2, 4}]
    expected = [{3}, {1, 5}, {1, 2, 4}, {1, 5}, {6}, {1, 2, 4}]

    actual = solver.difference_elimination(input)

    assert expected == actual


# def test_get_row_set_difference():
#     grid = [
#         [7, 9, {1, 2, 3}, {1, 5}, {1, 2, 4}, 8, {1, 5}, {1, 5, 6}, {2, 4}]
#     ]
#     expected_grid = [[7, 9, {1, 2, 3}, {1, 5}, {1, 2, 4}, 8, {1, 5}, {1, 5, 6}, {2, 4}]]
#     expected_solved = [7, 9, 3, {1, 5}, {2, 4}, 8, {1, 5}, 6, {2, 4}]
#
#     actual_solved = solver.set_difference_rows(grid)
#
#     assert expected_solved == actual_solved
#     assert expected_grid == grid



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
