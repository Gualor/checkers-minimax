import os
import random

import numpy as np
import pygame

# GAME CONSTANTS

WIN_SIZE = (WIDTH, HEIGHT) = (600, 600)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORANGE = (255, 156, 0)
BLUE = (1, 212, 180)

# CLASSES


class AI:
    def __init__(self, diff, ply_num):
        self.diff = diff
        self.ply = ply_num
        self.pieceVal = 10
        self.kingVal = 50
        self.sideVal = 20
        self.wallVal = 10

    def find_moves(self, board):
        moves = list()
        for i in range(10):
            for j in range(10):
                if not board[i][j] == 0:
                    if str(list(board[i][j].keys())[0]) == "ply" + str(self.ply):
                        for k in range(-1, 2, 2):
                            for h in range(-1, 2, 2):
                                if (
                                    i + k >= 0
                                    and i + k < 10
                                    and j + h >= 0
                                    and j + h < 10
                                ):
                                    if self.ply == 1:
                                        if (
                                            int(list(board[i][j].values())[0]) == 2
                                            or h > 0
                                        ):
                                            if board[i + k][j + h] == 0:
                                                moves.append(((i, j), (i + k, j + h)))
                                            elif str(
                                                list(board[i + k][j + h].keys())[0]
                                            ) != "ply" + str(self.ply):
                                                if (
                                                    i + 2 * k >= 0
                                                    and i + 2 * k < 10
                                                    and j + 2 * h >= 0
                                                    and j + 2 * h < 10
                                                ):
                                                    if board[i + 2 * k][j + 2 * h] == 0:
                                                        moves.append(
                                                            (
                                                                (i, j),
                                                                (i + 2 * k, j + 2 * h),
                                                            )
                                                        )
                                    elif self.ply == 2:
                                        if (
                                            int(list(board[i][j].values())[0]) == 2
                                            or h < 0
                                        ):
                                            if board[i + k][j + h] == 0:
                                                moves.append(((i, j), (i + k, j + h)))
                                            elif str(
                                                list(board[i + k][j + h].keys())[0]
                                            ) != "ply" + str(self.ply):
                                                if (
                                                    i + 2 * k >= 0
                                                    and i + 2 * k < 10
                                                    and j + 2 * h >= 0
                                                    and j + 2 * h < 10
                                                ):
                                                    if board[i + 2 * k][j + 2 * h] == 0:
                                                        moves.append(
                                                            (
                                                                (i, j),
                                                                (i + 2 * k, j + 2 * h),
                                                            )
                                                        )
        random.shuffle(moves)
        return moves

    def evaluate_state(self, board):
        value = 0
        n1 = 0
        n2 = 0
        for i in range(10):
            for j in range(10):
                if not board[i][j] == 0:
                    if str(list(board[i][j].keys())[0]) == "ply" + str(self.ply):
                        n1 += 1
                        if i < 5:
                            value += int(1 / (i + 1)) * self.sideVal
                        else:
                            value += int(1 / (abs(i - 10))) * self.sideVal
                        value += int((j + 1) / 10) * self.wallVal
                        if int(list(board[i][j].values())[0]) == 1:
                            value += self.pieceVal
                        elif int(list(board[i][j].values())[0]) == 2:
                            value += self.kingVal
                    else:
                        n2 += 1
                        if i < 5:
                            value -= int(1 / (i + 1)) * self.sideVal
                        else:
                            value -= int(1 / (abs(i - 10))) * self.sideVal
                        value -= int(abs(j - 10) / 10) * self.wallVal
                        if int(list(board[i][j].values())[0]) == 1:
                            value -= self.pieceVal
                        elif int(list(board[i][j].values())[0]) == 2:
                            value -= self.kingVal
        if n2 == 0 and n1 > 0:
            value = 10000
        elif n1 == 0 and n2 > 0:
            value = -10000
        return value

    def update_board(self, board, move):
        selected = move[0]
        moveto = move[1]
        if abs(selected[0] - moveto[0]) == 2 and abs(selected[1] - moveto[1]) == 2:
            dir = (moveto[0] - selected[0], moveto[1] - selected[1])
            board[selected[0] + dir[0]][selected[1] + dir[1]] = 0
        piece = board[selected[0]][selected[1]]
        board[moveto[0]][moveto[1]] = piece
        board[selected[0]][selected[1]] = 0
        return board

    def minimax(self, board, depth, isMax):
        currVal = self.evaluate_state(board)
        moves = self.find_moves(board)
        if abs(currVal) == 1000:
            return currVal
        if depth > 0:
            if isMax:
                bestVal = -100000
                bestMove = None
                for move in moves:
                    board = self.update_board(board, move)
                    valueMove = self.minimax(board, depth - 1, False)
                    tmp = bestVal
                    bestVal = max(bestVal, valueMove[0])
                    if tmp != bestVal:
                        bestMove = move
                return bestVal, bestMove
            else:
                bestVal = 100000
                bestMove = None
                for move in moves:
                    board = self.update_board(board, move)
                    valueMove = self.minimax(board, depth - 1, True)
                    tmp = bestVal
                    bestVal = min(bestVal, valueMove[0])
                    if tmp != bestVal:
                        bestMove = move
                return bestVal, bestMove
        else:
            return currVal, None


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


# FUNCTIONS


def select_piece(surface, player, selected, moveto, event):
    pos = event.__dict__["pos"]
    posgrid = (int(pos[0] / player.tile_size[0]), int(pos[1] / player.tile_size[1]))
    if selected is None and moveto is None:
        if player.pos_pieces[posgrid[0], posgrid[1]]:
            return posgrid
        else:
            return False
    elif selected is not None and moveto is None:
        return posgrid
    else:
        return False


def draw_selected(surface, posgrid, player):
    if player.pos_pieces[posgrid[0], posgrid[1]]:
        col = (player.col[0], player.col[1], player.col[2])
        rect = (
            posgrid[0] * player.tile_size[0],
            posgrid[1] * player.tile_size[1],
            player.tile_size[0],
            player.tile_size[1],
        )
        pygame.draw.rect(surface, col, rect, 3)
        pygame.display.flip()


def switch_turn(board, turn, sel):
    if turn == player1:
        type = list(board.board[sel[0]][sel[1]].values())[0]
        near_enemy = list()
        dir_enemy = list()
        for i in range(-1, 2, 2):
            for j in range(-1, 2, 2):
                if (sel[0] + i >= 0 and sel[0] + i < 10) and (
                    sel[1] + j >= 0 and sel[1] + j < 10
                ):
                    if board.board[sel[0] + i][sel[1] + j] == {
                        "ply2": 1
                    } or board.board[sel[0] + i][sel[1] + j] == {"ply2": 2}:
                        near_enemy.append((sel[0] + i, sel[1] + j))
                        dir_enemy.append((i, j))
                        newpos = (
                            near_enemy[-1][0] + dir_enemy[-1][0],
                            near_enemy[-1][1] + dir_enemy[-1][1],
                        )
                        if (
                            newpos[0] >= 0
                            and newpos[0] < 10
                            and newpos[1] >= 0
                            and newpos[1] < 10
                        ):
                            if board.board[newpos[0]][newpos[1]] == 0:
                                if type == 1 and dir_enemy[-1][1] == -1:
                                    pass
                                else:
                                    return player1
        return player2
    elif turn == player2:
        type = list(board.board[sel[0]][sel[1]].values())[0]
        near_enemy = list()
        dir_enemy = list()
        for i in range(-1, 2, 2):
            for j in range(-1, 2, 2):
                if (sel[0] + i >= 0 and sel[0] + i < 10) and (
                    sel[1] + j >= 0 and sel[1] + j < 10
                ):
                    if board.board[sel[0] + i][sel[1] + j] == {
                        "ply1": 1
                    } or board.board[sel[0] + i][sel[1] + j] == {"ply1": 2}:
                        near_enemy.append((sel[0] + i, sel[1] + j))
                        dir_enemy.append((i, j))
                        newpos = (
                            near_enemy[-1][0] + dir_enemy[-1][0],
                            near_enemy[-1][1] + dir_enemy[-1][1],
                        )
                        if (
                            newpos[0] >= 0
                            and newpos[0] < 10
                            and newpos[1] >= 0
                            and newpos[1] < 10
                        ):
                            if board.board[newpos[0]][newpos[1]] == 0:
                                if type == 1 and dir_enemy[-1][1] == 1:
                                    pass
                                else:
                                    return player2
        return player1


def copy_board(board):
    copy = [[0 for x in range(10)] for y in range(10)]
    for i in range(10):
        for j in range(10):
            copy[i][j] = board[i][j]
    return copy


def clear_window():
    os.system("cls")


def print_score(ply1, ply2):
    print("")
    print("      +------------------------------+")
    print("      |                              |")
    print("      |  SCORE:                      |")
    print("      |                              |")
    str1 = str(ply1.n_eaten)
    str2 = str(ply2.n_eaten) + " "
    if ply1.n_eaten >= 10:
        str1 = str1 + " "
    if ply2.n_eaten >= 10:
        str2 = str(ply2.n_eaten)
    print("      |  Player1: " + str1 + "\tPlayer2: " + str2 + "  |")
    print("      |                              |")
    print("      +------------------------------+")
    if ply1.n_eaten == 15:
        print("\n\n\tPLAYER1 WIN!")
    elif ply2.n_eaten == 15:
        print("\n\n\tPLAYER2 WIN!")


if __name__ == "__main__":

    pygame.display.init()
    clear_window()
    pygame.display.set_caption("Checker Minimax")
    window = pygame.display.set_mode(WIN_SIZE)
    clock = pygame.time.Clock()

    gameboard = CheckerBoard(window, WIN_SIZE, BLACK, WHITE)
    player1 = Player(window, WIN_SIZE, 1, ORANGE)
    player2 = Player(window, WIN_SIZE, 2, BLUE)

    ProGamer = AI("hard", 1)

    gameboard.update_board(player1.pos_pieces, player2.pos_pieces)
    gameboard.print_board()

    selected = None
    moveto = None
    if np.random.randint(1, 3) == 1:
        Player_turn = player1
        print("\n\tPlayer1's turn")
    else:
        Player_turn = player2
        print("\n\tPlayer2's turn")
    print("\t. . . . . . . .")
    print_score(player1, player2)

    while True:

        gameboard.draw(Player_turn)
        player1.draw()
        player2.draw()

        if selected:
            draw_selected(window, selected, Player_turn)

        # detect mouse event
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not selected:
                    selected = select_piece(
                        window, Player_turn, selected, moveto, event
                    )
                elif selected:
                    tmp = select_piece(window, Player_turn, selected, moveto, event)
                    if tmp != selected:
                        moveto = tmp

        # ProGamer's turn
        if Player_turn == player1:
            board = copy_board(gameboard.board)
            try:
                valMove, aiMove = ProGamer.minimax(board, 100, True)
                selected = aiMove[0]
                moveto = aiMove[1]
            except TypeError:
                Selected = None
                moveto = None

        # move piece
        if moveto is not None:
            if Player_turn == player1:
                tmp = player1.move(selected, moveto, gameboard.board)
                player2.update_dead(tmp)
            elif Player_turn == player2:
                tmp = player2.move(selected, moveto, gameboard.board)
                player1.update_dead(tmp)

            # update the position of the player's pieces
            gameboard.update_board(player1.pos_pieces, player2.pos_pieces)

            if tmp is not False:
                clear_window()
                if type(tmp) == tuple:
                    Player_turn = switch_turn(gameboard, Player_turn, moveto)
                    if Player_turn == player1:
                        print("\n\tPlayer1's turn")
                        print("\t. . . . . . . .")
                    else:
                        print("\n\tPlayer2's turn")
                        print("\t. . . . . . . .")
                else:
                    if Player_turn == player1:
                        Player_turn = player2
                        print("\n\tPlayer2's turn")
                        print("\t. . . . . . . .")

                    else:
                        Player_turn = player1
                        print("\n\tPlayer1's turn")
                        print("\t. . . . . . . .")
                print_score(player1, player2)

            moveto = None
            selected = None

        pygame.display.flip()
