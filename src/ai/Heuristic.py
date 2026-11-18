class Heuristic:
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


    def detect_5orm_pattern(self, line, player):
        patterns = {}
        opponent = 2 if player == 1 else 1
        window_size = 6

        for i in range(len(line) - window_size + 1):
            window = line[i:i + window_size]

            player_count = window.count(player)
            opponent_count = window.count(opponent)
            empty_count = window.count(0)

            if opponent_count == 0 and player_count >= 2 and empty_count > 0:
                positions = tuple(
                    i + index
                    for index, cell in enumerate(window)
                    if cell == player
                )

                has_gap = positions[-1] - positions[0] + 1 > player_count

                if has_gap:
                    patterns[positions] = (player_count, empty_count)

        return list(patterns.values())


    def get_5orm_pattern_score(self, line, player):
        patterns = self.detect_5orm_pattern(line, player)

        scores = {
            2: 50,
            3: 500,
            4: 5000,
            5: 100000
        }

        score = 0

        for player_count, empty_count in patterns:
            score += scores.get(player_count, 0)

        return score


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
            elif empty_left and empty_right:
                score += scores[count]
            elif empty_left or empty_right:
                score += scores[count] / (2 if count == 5 else 5)

        score += self.get_5orm_pattern_score(line, player)

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