import numpy as np
import pygame


class CheckerBoard:
    def __init__(self, surface, size, col1, col2):
        self.surface = surface
        self.win_size = size
        self.tile_size = (int(size[0] / 10), int(size[1] / 10))
        self.col1 = col1
        self.col2 = col2
        self.board = [[0 for x in range(10)] for y in range(10)]

    def draw(self, turn):
        self.surface.fill(self.col2)
        for i in range(0, self.win_size[0], 2 * self.tile_size[0]):
            for j in range(0, self.win_size[1], 2 * self.tile_size[1]):
                pygame.draw.rect(
                    self.surface,
                    self.col1,
                    (i, j, self.tile_size[0], self.tile_size[1]),
                )
        for i in range(self.tile_size[0], self.win_size[0], 2 * self.tile_size[0]):
            for j in range(self.tile_size[1], self.win_size[1], 2 * self.tile_size[1]):
                pygame.draw.rect(
                    self.surface,
                    self.col1,
                    (i, j, self.tile_size[0], self.tile_size[1]),
                )
        pygame.draw.rect(self.surface, turn.col, ((0, 0), self.win_size), 3)

    def update_board(self, ply1, ply2):
        for i in range(10):
            for j in range(10):
                if ply1[i][j] > 0:
                    self.board[i][j] = {"ply1": ply1[i][j]}
                elif ply2[i][j] > 0:
                    self.board[i][j] = {"ply2": ply2[i][j]}
                else:
                    self.board[i][j] = 0

    def print_board(self):
        print("\nGameboard:")
        for i in range(10):
            for j in range(10):
                if not self.board[i][j] == 0:
                    if list(self.board[i][j].keys())[0] == "ply1":
                        print(int(list(self.board[i][j].values())[0]), end=" ")
                    else:
                        print(int(list(self.board[i][j].values())[0] + 2), end=" ")
                else:
                    print(0, end=" ")
            print("")
        print("")


class Player:
    def __init__(self, surface, size, num, col):
        self.surface = surface
        self.win_size = size
        self.tile_size = (int(size[0] / 10), int(size[1] / 10))
        self.n_men = 15
        self.n_kings = 0
        self.n_eaten = 0
        self.col = col
        self.ply = num
        self.init_pos(self.ply)

    def init_pos(self, n):
        self.pos_pieces = np.zeros(shape=(10, 10))
        if n == 1:
            for i in range(3):
                for j in range(0, 10, 2):
                    if i == 0 or i == 2:
                        self.pos_pieces[i][j] = 1
                    elif i == 1:
                        self.pos_pieces[i][j + 1] = 1
        if n == 2:
            for i in range(3):
                for j in range(0, 10, 2):
                    if i == 0 or i == 2:
                        self.pos_pieces[9 - i][j + 1] = 1
                    elif i == 1:
                        self.pos_pieces[9 - i][j] = 1
        self.pos_pieces = self.pos_pieces.transpose()

    def move(self, selected, moveto, board):
        moves = self.check_forced_move(board)
        if ((selected, moveto) in moves) or (len(moves) == 0):
            dead = self.check_eating_move(selected, moveto, board)
            if not dead:
                # moves without eating pieces
                if self.check_valid_move(selected, moveto, board):
                    # print("Player" + str(self.ply), "moved piece from", selected, "to", moveto)
                    # update position from selected to moveto
                    self.pos_pieces[moveto[0]][moveto[1]] = self.pos_pieces[
                        selected[0]
                    ][selected[1]]
                    self.pos_pieces[selected[0]][selected[1]] = 0
                    # kings promotion
                    if self.ply == 1 and moveto[1] == 9:
                        self.promote_king(moveto)
                    elif self.ply == 2 and moveto[1] == 0:
                        self.promote_king(moveto)
                    return True
                else:
                    return False
            else:
                # valid eating move
                self.n_eaten = self.n_eaten + 1
                # update position from selected to moveto
                self.pos_pieces[moveto[0]][moveto[1]] = self.pos_pieces[selected[0]][
                    selected[1]
                ]
                self.pos_pieces[selected[0]][selected[1]] = 0
                # kings promotion
                if self.ply == 1 and moveto[1] == 9:
                    self.promote_king(moveto)
                elif self.ply == 2 and moveto[1] == 0:
                    self.promote_king(moveto)
                return dead
        else:
            return False

    def check_forced_move(self, board):
        moves = list()
        for i in range(10):
            for j in range(10):
                if self.pos_pieces[i][j] != 0:
                    selected = (i, j)
                    for k in range(-2, 3, 4):
                        for h in range(-2, 3, 4):
                            moveto = (k + i, h + j)
                            dead = None
                            if (
                                moveto[0] >= 0
                                and moveto[0] < 10
                                and moveto[1] >= 0
                                and moveto[1] < 10
                            ):
                                dead = self.check_eating_move(selected, moveto, board)
                            if dead:
                                moves.append((selected, moveto))
        return moves

    def check_eating_move(self, selected, moveto, board):
        dir = (np.sign(moveto[0] - selected[0]), np.sign(moveto[1] - selected[1]))
        if self.ply == 1 and self.pos_pieces[selected[0]][selected[1]] == 1:
            if dir[1] < 0:
                return False
        elif self.ply == 2 and self.pos_pieces[selected[0]][selected[1]] == 1:
            if dir[1] > 0:
                return False
        if (
            board[selected[0] + dir[0]][selected[1] + dir[1]] != 0
            and board[selected[0] + dir[0]][selected[1] + dir[1]]
            != {"ply" + str(self.ply): 1}
            and board[selected[0] + dir[0]][selected[1] + dir[1]]
            != {"ply" + str(self.ply): 2}
        ):
            if (
                abs(selected[0] - moveto[0]) == 2
                and abs(selected[1] - moveto[1]) == 2
                and board[moveto[0]][moveto[1]] == 0
            ):
                return (selected[0] + dir[0], selected[1] + dir[1])
            else:
                return False
        else:
            return False

    def check_valid_move(self, selected, moveto, board):
        if board[moveto[0]][moveto[1]] == 0:
            if board[selected[0]][selected[1]] != 0:
                if list(board[selected[0]][selected[1]].values())[0] == 2:
                    if (
                        abs(moveto[0] - selected[0]) == 1
                        and abs(moveto[1] - selected[1]) == 1
                    ):
                        return True
                elif list(board[selected[0]][selected[1]].values())[0] == 1:
                    if abs(moveto[0] - selected[0]) == 1:
                        if self.ply == 1 and (moveto[1] - selected[1]) == 1:
                            return True
                        elif self.ply == 2 and (moveto[1] - selected[1]) == -1:
                            return True
                return False
            else:
                return False

    def promote_king(self, pos):
        self.pos_pieces[pos[0]][pos[1]] = 2

    def update_dead(self, dead):
        if not (dead is True or dead is False):
            self.pos_pieces[dead[0]][dead[1]] = 0

    def draw(self):
        for i in range(10):
            for j in range(10):
                if self.pos_pieces[i][j] == 1:
                    centre = (
                        i * self.tile_size[0] + int(self.tile_size[0] / 2),
                        j * self.tile_size[1] + int(self.tile_size[1] / 2),
                    )
                    radius = int(self.tile_size[0] / 2 * (9 / 10))
                    pygame.draw.circle(self.surface, self.col, centre, radius)
                elif self.pos_pieces[i][j] == 2:
                    centre = (
                        i * self.tile_size[0] + int(self.tile_size[0] / 2),
                        j * self.tile_size[1] + int(self.tile_size[1] / 2),
                    )
                    radius = int(self.tile_size[0] / 2 * (9 / 10))
                    pygame.draw.circle(self.surface, self.col, centre, radius)
                    invcol = (255 - self.col[0], 255 - self.col[1], 255 - self.col[2])
                    radius = int(self.tile_size[0] / 2 * (2 / 10))
                    pygame.draw.circle(self.surface, invcol, centre, radius)
                    pygame.draw.circle(
                        self.surface, invcol, (centre[0] + 10, centre[1]), radius
                    )
                    pygame.draw.circle(
                        self.surface, invcol, (centre[0], centre[1] + 10), radius
                    )
                    pygame.draw.circle(
                        self.surface, invcol, (centre[0] - 10, centre[1]), radius
                    )
                    pygame.draw.circle(
                        self.surface, invcol, (centre[0], centre[1] - 10), radius
                    )
