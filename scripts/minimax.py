from typing import Optional, List, Tuple
import random

from checkers import BoardType, MoveType

class Minimax:
    PIECE_VAL = 10
    KING_VAL = 50
    SIDE_VAL = 20
    WALL_VAL = 10

    def __init__(self, ply_num: int) -> None:
        self.ply = ply_num

    def find_moves(self, board: BoardType) -> List[MoveType]:
        moves = []
        for i in range(10):
            for j in range(10):
                if board[i][j] == 0:
                    continue
                ply_str, ply_val = board[i][j]
                if ply_str != f"ply{self.ply}":
                    continue
                for k, h in [(x, y) for x in [-1, 1] for y in [-1, 1]]:
                    if (
                        (i + k < 0) or (i + k >= 10) or
                        (j + h < 0) or (j + h >= 10)
                    ):
                        continue
                    dst_str, dst_val = board[i + k][j + h]
                    if self.ply == 1:
                        if (ply_val == 2) or (h > 0):
                            if dst_val == 0:
                                moves.append(((i, j), (i + k, j + h)))
                            elif dst_str != f"ply{self.ply}":
                                if (
                                    (i + 2 * k < 0) or (i + 2 * k >= 10) or
                                    (j + 2 * h < 0) or (j + 2 * h >= 10)
                                ):
                                    continue
                                if board[i + 2 * k][j + 2 * h] == 0:
                                    moves.append(
                                        ((i, j), (i + 2 * k, j + 2 * h))
                                    )
                    elif self.ply == 2:
                        if (ply_val == 2) or (h < 0):
                            if board[i + k][j + h] == 0:
                                moves.append(((i, j), (i + k, j + h)))
                            elif dst_str != f"ply{self.ply}":
                                if (
                                    (i + 2 * k < 0) or (i + 2 * k >= 10) or
                                    (j + 2 * h < 0) or (j + 2 * h >= 10)
                                ):
                                    continue
                                if board[i + 2 * k][j + 2 * h] == 0:
                                    moves.append(
                                        ((i, j), (i + 2 * k, j + 2 * h))
                                    )
        random.shuffle(moves)
        return moves

    def evaluate_state(self, board: BoardType) -> int:
        value = 0
        n1 = 0
        n2 = 0
        for i in range(10):
            for j in range(10):
                if board[i][j] == 0:
                    continue
                ply_str, ply_val = board[i][j]
                if ply_str == f"ply{self.ply}":
                    n1 += 1
                    if i < 5:
                        value += int(1 / (i + 1)) * Minimax.SIDE_VAL
                    else:
                        value += int(1 / (abs(i - 10))) * Minimax.SIDE_VAL
                    value += int((j + 1) / 10) * Minimax.WALL_VAL
                    if ply_val == 1:
                        value += Minimax.PIECE_VAL
                    elif ply_val == 2:
                        value += Minimax.KING_VAL
                else:
                    n2 += 1
                    if i < 5:
                        value -= int(1 / (i + 1)) * Minimax.SIDE_VAL
                    else:
                        value -= int(1 / (abs(i - 10))) * Minimax.SIDE_VAL
                    value -= int(abs(j - 10) / 10) * Minimax.WALL_VAL
                    if ply_val == 1:
                        value -= Minimax.PIECE_VAL
                    elif ply_val == 2:
                        value -= Minimax.KING_VAL
        if n2 == 0 and n1 > 0:
            value = 10000
        elif n1 == 0 and n2 > 0:
            value = -10000
        return value

    def update_board(self, board: BoardType, move: MoveType) -> BoardType:
        selected = move[0]
        moveto = move[1]
        if (
            (abs(selected[0] - moveto[0]) == 2) and
            (abs(selected[1] - moveto[1]) == 2)
        ):
            dir = (moveto[0] - selected[0], moveto[1] - selected[1])
            board[selected[0] + dir[0]][selected[1] + dir[1]] = 0
        piece = board[selected[0]][selected[1]]
        board[moveto[0]][moveto[1]] = piece
        board[selected[0]][selected[1]] = 0
        return board

    def minimax(
        self, board: BoardType, depth: int, is_max: bool
    ) -> Tuple[int, Optional[MoveType]]:
        curr_val = self.evaluate_state(board)
        moves = self.find_moves(board)
        if abs(curr_val) == 1000:
            return curr_val, None
        if depth > 0:
            if is_max:
                best_val = -100000
                best_move = None
                for move in moves:
                    board = self.update_board(board, move)
                    value_move = self.minimax(board, depth - 1, False)
                    tmp = best_val
                    best_val = max(best_val, value_move[0])
                    if tmp != best_val:
                        best_move = move
                return best_val, best_move
            else:
                best_val = 100000
                best_move = None
                for move in moves:
                    board = self.update_board(board, move)
                    value_move = self.minimax(board, depth - 1, True)
                    tmp = best_val
                    best_val = min(best_val, value_move[0])
                    if tmp != best_val:
                        best_move = move
                return best_val, best_move
        else:
            return curr_val, None
