from src.game.board import Board
from src.ai.heuristic import Heuristic

def test_empty_board():
    board = Board()
    heuristic = Heuristic()

    score = heuristic.evaluate_board(board, 1)
    assert score == 0


def test_ai_advantage():
    board = Board()
    heuristic = Heuristic()

    for c in range(4):
        board.place_stone(5, c, 1)

    score = heuristic.evaluate_board(board, 1)
    assert score > 0


def test_opponent_advantage():
    board = Board()
    heuristic = Heuristic()

    for c in range(4):
        board.place_stone(5, c, 2)

    score = heuristic.evaluate_board(board, 1)
    assert score < 0


def test_open_four_scores_higher_than_blocked_four():
    heuristic = Heuristic()

    open_line = [0, 1, 1, 1, 1, 0]
    blocked_line = [2, 1, 1, 1, 1, 0]

    open_score = heuristic.get_line_score(open_line, 1)
    blocked_score = heuristic.get_line_score(blocked_line, 1)

    assert open_score > blocked_score


def test_diagonal_advantage():
    board = Board()
    heuristic = Heuristic()

    for i in range(4):
        board.place_stone(i, i, 1)

    score = heuristic.evaluate_board(board, 1)
    assert score > 0


def test_down_left_diagonal_advantage():
    board = Board()
    heuristic = Heuristic()

    for i in range(4):
        board.place_stone(i, 3 - i, 1)

    score = heuristic.evaluate_board(board, 1)
    assert score > 0


def test_six_in_a_row_scores_high():
    heuristic = Heuristic()

    line = [1, 1, 1, 1, 1, 1, 0]

    score = heuristic.get_line_score(line, 1)
    assert score >= 1_000_000


def test_detect_broken_pattern():
    heuristic = Heuristic()

    line = [0, 1, 1, 0, 1, 1, 0]

    patterns = heuristic.detect_5orm_pattern(line, 1)
    assert len(patterns) > 0


def test_ignore_consecutive_patterns():
    heuristic = Heuristic()

    line = [0, 1, 1, 1, 1, 0]

    patterns = heuristic.detect_5orm_pattern(line, 1)
    assert patterns == []