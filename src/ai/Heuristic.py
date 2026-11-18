class Heuristic:
    def __init__(self) -> None:
        pass

    def analyze_line(self, line, player):
        count = 0
        start = None
        end = None
        patterns = []

        for index, cell in enumerate(line):
            if cell == player:
                if count == 0:
                    start = index
                count += 1
                end = index
            else:
                if count > 0:
                    empty_left = start > 0 and line[start - 1] == 0
                    empty_right = end < len(line) - 1 and line[end + 1] == 0
                    patterns.append((count, empty_left, empty_right))
                count = 0

        if count > 0:
            empty_left = start > 0 and line[start - 1] == 0
            empty_right = end < len(line) - 1 and line[end + 1] == 0

            patterns.append((count, empty_left, empty_right))

        return patterns

    
    def get_line_score(self, line, player):
        patterns = self.analyze_line(line, player)
        score = 0
        scores = {
            1: 10,
            2: 100,
            3: 1000,
            4: 10000,
            5: 100000,
            6: 1000000
        }

        for count, empty_left, empty_right in patterns:
            if count >= 6:
                score += scores[6]

            elif empty_right and empty_left:
                score += scores[count]
            elif empty_right or empty_left:
                if count == 5:
                    score += scores[count] / 2
                else:
                    score += scores[count] / 5

        return score

    
    def get_all_lines(self, board):
        grid = board.grid
        size = board.size
        lines = []

        # Horizontal
        for r in range(size):
            line = [grid[r][c] for c in range(size)]
            lines.append(line)

        # Vertical
        for c in range(size):
            line = [grid[r][c] for r in range(size)]
            lines.append(line)

        # Diagonal: down-right
        for c in range(size):
            r, col = 0, c
            line = []

            while r < size and col < size:
                line.append(grid[r][col])
                r += 1
                col += 1

            lines.append(line)

        for r in range(1, size):
            row, c = r, 0
            line = []

            while row < size and c < size:
                line.append(grid[row][c])
                row += 1
                c += 1

            lines.append(line)

        # Diagonal: down-left
        for c in range(size):
            r, col = 0, c
            line = []

            while r < size and col >= 0:
                line.append(grid[r][col])
                r += 1
                col -= 1

            lines.append(line)

        for r in range(1, size):
            row, c = r, size - 1
            line = []

            while row < size and c >= 0:
                line.append(grid[row][c])
                row += 1
                c -= 1

            lines.append(line)

        return lines


    def evaluate_board(self, board, ai_id):
        opponent_id = 2 if ai_id == 1 else 1

        lines = self.get_all_lines(board)

        ai_score = sum(self.get_line_score(line, ai_id) for line in lines)

        opponent_score = sum(self.get_line_score(line, opponent_id) for line in lines)

        # Positive score --> ai has the advantage
        # Negative score --> human has the advantage
        # zero --> both are equal
        return ai_score - opponent_score