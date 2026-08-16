from game import move_row_left


def test_move_two_equal_tiles():
    assert move_row_left([0, 2, 0, 2]) == [4, 0, 0, 0]


def test_move_multiple_tiles():
    assert move_row_left([2, 2, 4, 2]) == [4, 4, 2, 0]


def test_four_equal_tiles():
    assert move_row_left([2, 2, 2, 2]) == [4, 4, 0, 0]


def test_three_equal_tiles():
    assert move_row_left([4, 4, 4, 0]) == [8, 4, 0, 0]


def test_no_merge():
    assert move_row_left([2, 4, 8, 16]) == [2, 4, 8, 16]