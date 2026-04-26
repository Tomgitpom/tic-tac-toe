import os
from database import init_db, get_player_wins, save_win

TEST_DB = "test_database.db"


def cleanup():
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)


def test_new_player_has_zero_wins():
    init_db(TEST_DB)
    assert get_player_wins("Matti", TEST_DB) == 0


def test_save_win_adds_one_win():
    init_db(TEST_DB)
    save_win("Matti", TEST_DB)
    assert get_player_wins("Matti", TEST_DB) == 1


def test_save_win_adds_multiple_wins():
    init_db(TEST_DB)
    save_win("Matti", TEST_DB)
    save_win("Matti", TEST_DB)
    save_win("Matti", TEST_DB)
    assert get_player_wins("Matti", TEST_DB) == 3


def test_different_players_have_separate_scores():
    init_db(TEST_DB)
    save_win("Matti", TEST_DB)
    save_win("Liisa", TEST_DB)
    save_win("Liisa", TEST_DB)

    assert get_player_wins("Matti", TEST_DB) == 1
    assert get_player_wins("Liisa", TEST_DB) == 2


if __name__ == "__main__":
    cleanup()

    test_new_player_has_zero_wins()
    cleanup()

    test_save_win_adds_one_win()
    cleanup()

    test_save_win_adds_multiple_wins()
    cleanup()

    test_different_players_have_separate_scores()
    cleanup()

    print("Kaikki testit menivät läpi.")