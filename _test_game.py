from game import move_row_left


def test_move_two_equal_tiles():
    new_row, score = move_row_left([0, 2, 0, 2])
    assert new_row == [4, 0, 0, 0]
    assert score == 4


def test_move_multiple_tiles():
    new_row, score = move_row_left([2, 2, 4, 2])
    assert new_row == [4, 4, 2, 0]
    assert score == 4


def test_four_equal_tiles():
    new_row, score = move_row_left([2, 2, 2, 2])
    assert new_row == [4, 4, 0, 0]
    assert score == 8


def test_three_equal_tiles():
    new_row, score = move_row_left([4, 4, 4, 0])
    assert new_row == [8, 4, 0, 0]
    assert score == 8


def test_no_merge():
    new_row, score = move_row_left([2, 4, 8, 16])
    assert new_row == [2, 4, 8, 16]
    assert score == 0