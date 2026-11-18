from src.game.board import Board

def board_from_ascii(rows: list[str], last_move: tuple[int, int] | None = None):
    if not rows:
        raise ValueError("Rows list cannot be empty.")
    size = len(rows)
    board = Board(size=size)
    for r, row_str in enumerate(rows):
        cleaned = row_str.replace(" ", "")
        if len(cleaned) != size:
            raise ValueError(f"Row {r} length ({len(cleaned)}) does not match board size ({size}).")
        for c, char in enumerate(cleaned):
            if char in (".", "0"):
                board.grid[r][c] = 0
            elif char == "1":
                board.grid[r][c] = 1
            elif char == "2":
                board.grid[r][c] = 2
            else:
                raise ValueError(f"Invalid character '{char}' at ({r}, {c}).")
    board.last_move = last_move
    return board