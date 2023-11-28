import chess
import chess.svg
import random
from collections import defaultdict
from IPython.display import display, SVG


class ChessAI:
    def __init__(self, depth=4):
        self.depth = depth
        self.transposition_table = defaultdict(dict)
        self.opening_table = {
            chess.Move.from_uci("e2e4"): 20,
            chess.Move.from_uci("d2d4"): 15,
            chess.Move.from_uci("g1f3"): 10,
            chess.Move.from_uci("c2c4"): 10
        }

    def alphabeta(self, board, depth, alpha, beta, maximizing_player):
        if depth == 0 or board.is_game_over():
            return self.evaluate_board(board)

        hash_key = str(board)
        if hash_key in self.transposition_table[depth]:
            return self.transposition_table[depth][hash_key]

        legal_moves = list(board.legal_moves)
        legal_moves.sort(key=lambda move: -self.opening_table.get(move, 0))

        if maximizing_player:
            max_eval = float('-inf')
            for move in legal_moves:
                board.push(move)
                eval = self.alphabeta(board, depth - 1, alpha, beta, False)
                board.pop()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            self.transposition_table[depth][hash_key] = max_eval
            return max_eval
        else:
            min_eval = float('inf')
            for move in legal_moves:
                board.push(move)
                eval = self.alphabeta(board, depth - 1, alpha, beta, True)
                board.pop()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            self.transposition_table[depth][hash_key] = min_eval
            return min_eval

    def evaluate_board(self, board):
        evaluation = 0
        evaluation += self.material_score(board)
        evaluation += self.control_score(board)
        return evaluation

    def display_board(board):
        svg_data = chess.svg.board(board=board)
        display(SVG(svg_data))
    def material_score(self, board):
        score = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece is not None:
                value = self.piece_value(piece, piece.color)
                if piece.color == chess.WHITE:
                    score += value
                else:
                    score -= value
        return score

    def piece_value(self, piece, color):
        piece_value_dict = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 0
        }
        return piece_value_dict.get(piece.piece_type, 0) if color == chess.WHITE else -piece_value_dict.get(piece.piece_type, 0)

    def control_score(self, board):
        control_score = 0
        center_squares = [chess.E4, chess.D4, chess.E5, chess.D5]
        for square in center_squares:
            control_score += len(board.attackers(chess.WHITE, square))
            control_score -= len(board.attackers(chess.BLACK, square))
        return control_score

    def get_best_move(self, board):
        best_move = None
        max_eval = float('-inf')
        legal_moves = list(board.legal_moves)
        random.shuffle(legal_moves)
        for move in legal_moves:
            board.push(move)
            eval = self.alphabeta(board, self.depth - 1, float('-inf'), float('inf'), False)
            board.pop()
            if eval > max_eval:
                max_eval = eval
                best_move = move
        return best_move

def print_board(board):
    print(board)

def display_board(board):
    return chess.svg.board(board=board)

def player_move(board):
    move_uci = input("Digite sua jogada (notação UCI): ")
    while not chess.Move.from_uci(move_uci) in board.legal_moves:
        print("Jogada inválida. Tente novamente.")
        move_uci = input("Digite sua jogada (notação UCI): ")
    return chess.Move.from_uci(move_uci)

def choose_color():
    color = input("Escolha a cor que deseja jogar (B para brancas, P para pretas): ").upper()
    while color not in ['B', 'P']:
        print("Escolha inválida. Tente novamente.")
        color = input("Escolha a cor que deseja jogar (B para brancas, P para pretas): ").upper()
    return color

def main():
    color_choice = choose_color()
    if color_choice == 'B':
        player_color = chess.WHITE
        ai_color = chess.BLACK
    else:
        player_color = chess.BLACK
        ai_color = chess.WHITE

    board = chess.Board()
    depth = 4  # Ajuste a profundidade conforme necessário
    ai = ChessAI(depth)

    print(f"Bem-vindo ao jogo de xadrez! Você joga com as peças {color_choice}.")

    while not board.is_game_over():
        print_board(board)
        display(board)

        # Vez do jogador humano
        if board.turn == player_color:
            move = player_move(board)
        else:
            print("Vez da IA...")
            move = ai.get_best_move(board)
            print("IA jogou:", move.uci())

        board.push(move)

    print("Fim de jogo!")
    print("Resultado:", board.result())

if __name__ == "__main__":
    main()
