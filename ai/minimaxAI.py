import copy

class MinimaxAI:
    def __init__(self, color, depth=2):
        self.color = color
        self.depth = depth

    def generate_move(self, board):
        best_score = float('-inf')
        best_move = None

        # Get all legal moves for this color
        for piece, moves in board.get_all_legal_moves(self.color):
            for move in moves:
                # Make a deep copy of the board
                new_board = copy.deepcopy(board)
                new_piece = new_board.get_piece_at(piece.row, piece.col)
                new_board.move_piece(new_piece, move[0], move[1], is_simulation=True)

                # Evaluate the position using minimax
                score = self.minimax(new_board, self.depth - 1, False)

                if score > best_score:
                    best_score = score
                    best_move = (piece, move)

        return best_move


    def minimax(self, board, depth, is_maximizing):
        if depth == 0 or board.game_over:
            return self.evaluate_board(board)

        color = self.color if is_maximizing else ('black' if self.color == 'white' else 'white')

        if is_maximizing:
            max_eval = float('-inf')
            for piece, moves in board.get_all_legal_moves(color):
                for move in moves:
                    new_board = copy.deepcopy(board)
                    new_piece = new_board.get_piece_at(piece.row, piece.col)
                    new_board.move_piece(new_piece, move[0], move[1], is_simulation=True)
                    eval = self.minimax(new_board, depth - 1, False)
                    max_eval = max(max_eval, eval)
            return max_eval

        else:
            min_eval = float('inf')
            for piece, moves in board.get_all_legal_moves(color):
                for move in moves:
                    new_board = copy.deepcopy(board)
                    new_piece = new_board.get_piece_at(piece.row, piece.col)
                    new_board.move_piece(new_piece, move[0], move[1], is_simulation=True)
                    eval = self.minimax(new_board, depth - 1, True)
                    min_eval = min(min_eval, eval)
            return min_eval

    def evaluate_board(self, board):
        # Simple material count:
        piece_values = {
            'pawn': 1,
            'knight': 3,
            'bishop': 3,
            'rook': 5,
            'queen': 9,
            'king': 0  # King is priceless, game over is handled separately
        }

        score = 0

        for row in board.pieces:
            for piece in row:
                if piece:
                    value = piece_values.get(piece.name.lower(), 0)
                    if piece.color == self.color:
                        score += value
                    else:
                        score -= value

        return score
