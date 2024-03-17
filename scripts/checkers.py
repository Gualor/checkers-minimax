from typing import Tuple, Union, List
import numpy as np


PosType = Tuple[int, int]
BoardElemType = Union[int, Tuple[str, int]]
BoardType = List[List[BoardElemType]]
MoveType = Tuple[PosType, PosType]


class CheckerBoard:
    def __init__(self) -> None:
        self.board: BoardType = [[0 for _ in range(10)] for _ in range(10)]

    def __str__(self) -> str:
        board_str = "Gameboard:\n"
        for i in range(10):
            for j in range(10):
                if isinstance(self.board[i][j], tuple):
                    ply_str, ply_val = self.board[i][j]
                    if ply_str == "ply2":
                        ply_val += 2
                    board_str += str(ply_val)
                else:
                    board_str += "0"
                board_str += " "
            board_str += "\n"
        return board_str

    def update_board(self, ply1: np.ndarray, ply2: np.ndarray) -> None:
        for i in range(10):
            for j in range(10):
                if ply1[i][j] > 0:
                    self.board[i][j] = ("ply1", ply1[i][j])
                elif ply2[i][j] > 0:
                    self.board[i][j] = ("ply2", ply2[i][j])
                else:
                    self.board[i][j] = 0


class Player:
    def __init__(self, num) -> None:
        self.n_men = 15
        self.n_kings = 0
        self.n_eaten = 0
        self.ply = num
        self.init_pos()

    def init_pos(self) -> None:
        self.pos_pieces = np.zeros(shape=(10, 10), dtype=int)
        if self.ply == 1:
            for i in range(3):
                for j in range(0, 10, 2):
                    if i in [0, 2]:
                        self.pos_pieces[i, j] = 1
                    elif i == 1:
                        self.pos_pieces[i, j + 1] = 1
        if self.ply == 2:
            for i in range(3):
                for j in range(0, 10, 2):
                    if i in [0, 2]:
                        self.pos_pieces[9 - i, j + 1] = 1
                    elif i == 1:
                        self.pos_pieces[9 - i, j] = 1
        self.pos_pieces = self.pos_pieces.transpose()

    def move(
        self, selected: PosType, moveto: PosType, board: BoardType
    ) -> bool:
        moves = self.check_forced_move(board)
        if ((selected, moveto) in moves) or (len(moves) == 0):
            dead = self.check_eating_move(selected, moveto, board)
            if not dead:
                # moves without eating pieces
                if self.check_valid_move(selected, moveto, board):
                    # update position from selected to moveto
                    self.pos_pieces[moveto] = self.pos_pieces[selected]
                    self.pos_pieces[selected] = 0
                    # kings promotion
                    if self.ply == 1 and moveto[1] == 9:
                        self.promote_king(moveto)
                    elif self.ply == 2 and moveto[1] == 0:
                        self.promote_king(moveto)
                    return True
                return False
            else:
                # valid eating move
                self.n_eaten = self.n_eaten + 1
                # update position from selected to moveto
                self.pos_pieces[moveto] = self.pos_pieces[selected]
                self.pos_pieces[selected] = 0
                # kings promotion
                if self.ply == 1 and moveto[1] == 9:
                    self.promote_king(moveto)
                elif self.ply == 2 and moveto[1] == 0:
                    self.promote_king(moveto)
                return dead
        else:
            return False

    def check_forced_move(self, board: BoardType) -> List[MoveType]:
        moves = []
        for i in range(10):
            for j in range(10):
                if self.pos_pieces[i, j] == 0:
                    continue
                selected = (i, j)
                for k in range(-2, 3, 4):
                    for h in range(-2, 3, 4):
                        moveto = (k + i, h + j)
                        if (
                            (moveto[0] < 0) or (moveto[0] >= 10) or
                            (moveto[1] < 0) or (moveto[1] >= 10)
                        ):
                            continue
                        if self.check_eating_move(selected, moveto, board):
                            moves.append((selected, moveto))
        return moves

    def check_eating_move(
        self, selected: PosType, moveto: PosType, board: BoardType
    ) -> Union[bool, PosType]:
        dir = (
            np.sign(moveto[0] - selected[0]),
            np.sign(moveto[1] - selected[1])
        )
        if self.ply == 1 and self.pos_pieces[selected] == 1:
            if dir[1] < 0:
                return False
        elif self.ply == 2 and self.pos_pieces[selected] == 1:
            if dir[1] > 0:
                return False
        if (
            (board[selected[0] + dir[0]][selected[1] + dir[1]] != 0) and
            (board[selected[0] + dir[0]][selected[1] + dir[1]] != (f"ply{self.ply}", 1)) and
            (board[selected[0] + dir[0]][selected[1] + dir[1]] != (f"ply{self.ply}", 2))
        ):
            if (
                (abs(selected[0] - moveto[0]) == 2) and
                (abs(selected[1] - moveto[1]) == 2) and
                (board[moveto[0]][moveto[1]] == 0)
            ):
                return (selected[0] + dir[0], selected[1] + dir[1])
            return False
        return False

    def check_valid_move(
        self, selected: PosType, moveto: PosType, board: BoardType
    ) -> bool:
        if board[selected[0]][selected[1]] == 0:
            return False
        if board[moveto[0]][moveto[1]] != 0:
            return False
        _, ply_val = board[selected[0]][selected[1]]
        if ply_val == 2:
            if (
                (abs(moveto[0] - selected[0]) == 1) and
                (abs(moveto[1] - selected[1]) == 1)
            ):
                return True
        elif ply_val == 1:
            if abs(moveto[0] - selected[0]) == 1:
                if (self.ply == 1) and ((moveto[1] - selected[1]) == 1):
                    return True
                if (self.ply == 2) and ((moveto[1] - selected[1]) == -1):
                    return True
        return False

    def promote_king(self, pos: PosType) -> None:
        self.pos_pieces[pos] = 2

    def update_dead(self, dead: PosType) -> None:
        if not (dead is True or dead is False):
            self.pos_pieces[dead] = 0
