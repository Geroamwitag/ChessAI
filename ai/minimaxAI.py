import copy

class MinimaxAI:
    def __init__(self, color, depth=2):
        self.color = color
        self.depth = depth

    def generate_move(self, board):
        best_score = float('-inf')
        best_move = None

        # get all legal moves for color
        for piece, moves in board.get_all_legal_moves(self.color):
            
            for move in moves:
                # simulate the move on a copy of the board and score
                # save the best move
                simulation_board = copy.deepcopy(board)
                new_piece = simulation_board.get_piece_at(piece.row, piece.col)
                simulation_board.move_piece(new_piece, move[0], move[1], is_simulation=True)
                
                score = self.minimax(simulation_board, self.depth - 1, float('-inf'), float('inf'), False)
                
                if score > best_score:
                    best_score = score
                    best_move = (piece, move)

        return best_move

    # the brain
    def minimax(self, board, depth, alpha, beta, is_maximizing):
        if depth == 0 or board.game_over:
            return self.evaluate_board(board)

        color = self.color if is_maximizing else ('black' if self.color == 'white' else 'white')

        # AI turn, best move for the AI, maximize
        if is_maximizing:
            max_eval = float('-inf')
            for piece, moves in board.get_all_legal_moves(color):
                for move in moves:
                    new_board = copy.deepcopy(board)
                    new_piece = new_board.get_piece_at(piece.row, piece.col)
                    new_board.move_piece(new_piece, move[0], move[1], is_simulation=True)

                    eval = self.minimax(new_board, depth - 1, alpha, beta, False)
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)

                    if beta <= alpha:
                        return max_eval
                    
            return max_eval

        # opponent turn, worst move against us, minimize
        else:
            min_eval = float('inf')
            for piece, moves in board.get_all_legal_moves(color):
                for move in moves:
                    new_board = copy.deepcopy(board)
                    new_piece = new_board.get_piece_at(piece.row, piece.col)
                    new_board.move_piece(new_piece, move[0], move[1], is_simulation=True)

                    eval = self.minimax(new_board, depth - 1, alpha, beta, True)
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)

                    if beta <= alpha:
                        return min_eval
                    
            return min_eval

    def evaluate_board(self, board):
        # AI piece importance values
        piece_values = {
            'pawn': 1,
            'knight': 3,
            'bishop': 3,
            'rook': 5,
            'queen': 9,
            'king': 0  # king is priceless, game over is handled separately
        }

        score = 0

        # scire tge board based on pieces
        for row in board.pieces:
            for piece in row:
                if piece:
                    value = piece_values.get(piece.name.lower(), 0)
                    # add score if friendly piece
                    if piece.color == self.color:
                        score += value
                    # subtract score if unfriendly piece
                    else:
                        score -= value

        return score
