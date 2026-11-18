class Board:

    def __init__(self, size: int = 19):
        if not isinstance(size, int) or isinstance(size, bool) or size <= 0:
            raise ValueError("Board size must be a positive integer.")
        self.size: int = size
        self.grid: list[list[int]] = [[0 for _ in range(size)] for _ in range(size)]
        self.last_move: tuple[int, int] | None = None

    def is_valid_move(self, row: int, col: int):
        if (
            not isinstance(row, int)
            or isinstance(row, bool)
            or not isinstance(col, int)
            or isinstance(col, bool)
        ):
            return False
        if not (0 <= row < self.size and 0 <= col < self.size):
            return False

        return self.grid[row][col] == 0

    def place_stone(self, row: int, col: int, player: int):
        if not self.is_valid_move(row, col):
            return False

        self.grid[row][col] = player
        self.last_move = (row, col)
        return True

    def check_winner(self):

        if self.last_move is None:
            return 0

        last_row, last_col = self.last_move
        player = self.grid[last_row][last_col]
        if player == 0:
            return 0

        directions = [
            (0, 1),
            (1, 0), 
            (1, 1),
            (1, -1),
        ]

        for d_row, d_col in directions:
            count = 1  
            r, c = last_row + d_row, last_col + d_col
            while 0 <= r < self.size and 0 <= c < self.size and self.grid[r][c] == player:
                count += 1
                r += d_row
                c += d_col
            r, c = last_row - d_row, last_col - d_col
            while 0 <= r < self.size and 0 <= c < self.size and self.grid[r][c] == player:
                count += 1
                r -= d_row
                c -= d_col
            if count >= 6:
                return player

        return 0

    def is_full(self):
        return all(cell != 0 for row in self.grid for cell in row)

    def get_empty_position(self) -> list[tuple[int, int]]:
        return [
            (r, c)
            for r in range(self.size)
            for c in range(self.size)
            if self.grid[r][c] == 0
        ]

    def __copy__(self):
        new_board = Board.__new__(Board)
        new_board.size = self.size
        new_board.grid = [row[:] for row in self.grid]
        new_board.last_move = self.last_move
        return new_board