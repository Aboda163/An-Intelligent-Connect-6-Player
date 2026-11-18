import copy
from .Heuristic import Heuristic

class SearchEngine:
    """This class is made to apply the minimax algorithm and alpha beta pruning to find the best move."""
    
    WIN_SCORE = 1_000_000.0

    def __init__(self, max_depth = 4, heuristic=None):
        self.max_depth = max_depth
        self.heuristic = heuristic if heuristic is not None else Heuristic()
        self.ai_id = None
        self.nodes_visited = 0

    def generate_candidate_move(self, board):
        """"gives the best move for the AI player and return its (row, col)"""
        size = board.size
        grid = board.grid
        candidates = set()
        has_stones = False

        for r in range(size):
            for c in range(size):
                if grid[r][c] != 0:
                    has_stones = True
                    for dr in range(-2, 3):
                        nr = r + dr
                        if 0 <= nr < size:
                            for dc in range(-2, 3):
                                nc = c + dc
                                if 0 <= nc < size and grid[nr][nc] == 0:
                                    candidates.add((nr, nc))
        if not has_stones:
            return [(size // 2, size // 2)]

        return sorted(candidates)

    def _is_winning_move(self, board, move, player_id):
        """Return true if placing player_id's stone at move wins immediately."""
        copy_board = copy.copy(board)
        if copy_board.place_stone(move[0], move[1], player_id):
            return copy_board.check_winner() == player_id
        return False

    def _count_adjacent_stones(self, grid, size, r, c):
        """Count the non_empty cells in the  neighbors around (r, c)"""
        count = 0
        for dr in (-1, 0, 1):
            nr = r + dr
            if 0 <= nr < size:
                for dc in (-1, 0, 1):
                    if dr == 0 and dc == 0:
                        continue
                    nc = c + dc
                    if 0 <= nc < size and grid[nr][nc] != 0:
                        count += 1
        return count

    def order_move(self, board, moves, player_id):
        """
        Priority 
        1. Winning move
        2. Block opponent's winning move
        3.Adjacent stone count
        4. Centrality
        """

        opponent_id = 2 if player_id == 1 else 1
        size = board.size
        grid = board.grid
        center = size // 2

        def priority(move):
            r, c = move
            is_winning = 1 if self._is_winning_move(board, move, player_id) else 0
            is_blocking = 1 if self._is_winning_move(board, move, opponent_id) else 0
            adj_count = self._count_adjacent_stones(grid, size, r, c)
            neg_center_dist = -(abs(r - center) + abs(c - center))
            return (is_winning, is_blocking, adj_count, neg_center_dist, (-r, -c))
        return sorted(moves, key=priority, reverse=True)

    def _next_turn_state(self, player_id, stones_remaining):
       """Compute (next_player_id, next_stones_remaining) after placing one stone."""
       remaining = stones_remaining - 1
       if remaining == 0:
              next_player = 2 if player_id == 1 else 1
              return next_player, 2
       return player_id, remaining
    
    def minimax(self, board, depth, player_id, stones_remaining,):
        """Pure turn-aware Minimax search (without alpha-beta pruning)."""
        
        self.nodes_visited += 1

        winner = board.check_winner()
        if winner != 0:
            if winner == self.ai_id:
                return self.WIN_SCORE + depth
            return -self.WIN_SCORE - depth

        if depth == 0:
            return float(self.heuristic.evaluate_board(board, self.ai_id))

        moves = self.generate_candidate_move(board)
        if not moves:
            return float(self.heuristic.evaluate_board(board, self.ai_id))

        ordered_moves = self.order_move(board, moves, player_id)
        ordered_moves = ordered_moves[:12]
        next_player, next_remaining = self._next_turn_state(player_id, stones_remaining)

        if player_id == self.ai_id:
            best_score = float("-inf")
            for move in ordered_moves:
                child = copy.copy(board)
                child.place_stone(move[0], move[1], player_id)
                score = self.minimax(child, depth - 1, next_player, next_remaining)
                if score > best_score:
                    best_score = score
            return best_score
        else:
            best_score = float("inf")
            for move in ordered_moves:
                child = copy.copy(board)
                child.place_stone(move[0], move[1], player_id)
                score = self.minimax(child, depth - 1, next_player, next_remaining)
                if score < best_score:
                    best_score = score
            return best_score

    def alpha_beta(self, board, depth, player_id, stones_remaining, alpha=float("-inf"), beta = float("inf")):
        """MiniMax with Alpha-beta pruning search."""

        self.nodes_visited += 1

        winner = board.check_winner()
        if winner != 0:
            if winner == self.ai_id:
                return self.WIN_SCORE + depth
            return -self.WIN_SCORE - depth

        if depth == 0:
            return float(self.heuristic.evaluate_board(board, self.ai_id))

        moves = self.generate_candidate_move(board)
        if not moves:
            return float(self.heuristic.evaluate_board(board, self.ai_id))

        ordered_moves = self.order_move(board, moves, player_id)
        ordered_moves = ordered_moves[:12]
        next_player_id, next_remaining = self._next_turn_state(player_id, stones_remaining)
        if player_id == self.ai_id:
            best_score = float("-inf")
            for move in ordered_moves:
                copy_board = copy.copy(board)
                copy_board.place_stone(move[0], move[1], player_id)
                score = self.alpha_beta(copy_board, depth - 1, next_player_id, next_remaining, alpha, beta)
                if score > best_score:
                    best_score = score
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
            return best_score
        else:
            best_score = float("inf")
            for move in ordered_moves:
                copy_board = copy.copy(board)
                copy_board.place_stone(move[0], move[1], player_id)
                score = self.alpha_beta(copy_board, depth - 1, next_player_id, next_remaining, alpha, beta)
                if score < best_score:
                    best_score = score
                beta = min(beta, best_score)
                if beta <= alpha:
                    break
            return best_score

    def choose_move(self, board, player_id, stones_remaining):
        """Choose the best move for the AI player using alpha-beta pruning."""
        
        self.ai_id = player_id
        self.nodes_visited = 0

        moves = self.generate_candidate_move(board)
        if len(moves) == 1:
            return moves[0]

        ordered_moves = self.order_move(board, moves, player_id)
        ordered_moves = ordered_moves[:12]
        if self._is_winning_move(board, ordered_moves[0], player_id):
            return ordered_moves[0]

        best_move = ordered_moves[0]
        best_score = float("-inf")
        alpha = float("-inf")
        beta = float("inf")

        next_player, next_remaining = self._next_turn_state(player_id, stones_remaining)

        for move in ordered_moves:
            copy_board = copy.copy(board)
            copy_board.place_stone(move[0], move[1], player_id)
            score = self.alpha_beta(copy_board, self.max_depth - 1, next_player, next_remaining, alpha, beta)
            if score > best_score:
                best_score = score
                best_move = move
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break
        return best_move