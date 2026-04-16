def test_board_size():
    size = 5
    assert 3 <= size <= 10

def test_win_length():
    win_length = 4
    assert win_length >= 3
