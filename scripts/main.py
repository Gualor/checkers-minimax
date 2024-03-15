import os
import random

import pygame
import numpy as np

from checkers import CheckerBoard, Player
from minimax import Minimax

WIN_SIZE = (WIDTH, HEIGHT) = (600, 600)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORANGE = (255, 156, 0)
BLUE = (1, 212, 180)


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

    ProGamer = Minimax("hard", 1)

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
