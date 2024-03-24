from typing import Optional, Union
import random
import os

import pygame
from pygame.event import EventType

from checkers import CheckerBoard, Player, PosType, BoardType
from minimax import Minimax

WIN_SIZE = (WIDTH, HEIGHT) = (600, 600)
TILE_SIZE = (WIN_SIZE[0] // 10, WIN_SIZE[1] // 10)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORANGE = (255, 156, 0)
BLUE = (1, 212, 180)
BOARD_COLOR = [WHITE, BLACK]
PLAYER_COLOR = [ORANGE, BLUE]


def draw_board(surface: pygame.Surface, turn: int) -> None:
    surface.fill(BOARD_COLOR[0])
    for i in range(0, WIN_SIZE[0], 2 * TILE_SIZE[0]):
        for j in range(0, WIN_SIZE[1], 2 * TILE_SIZE[1]):
            pygame.draw.rect(
                surface, BOARD_COLOR[1],
                (i, j, TILE_SIZE[0], TILE_SIZE[1]),
            )
    for i in range(TILE_SIZE[0], WIN_SIZE[0], 2 * TILE_SIZE[0]):
        for j in range(TILE_SIZE[1], WIN_SIZE[1], 2 * TILE_SIZE[1]):
            pygame.draw.rect(
                surface, BOARD_COLOR[1],
                (i, j, TILE_SIZE[0], TILE_SIZE[1]),
            )
    pygame.draw.rect(surface, PLAYER_COLOR[turn-1], ((0, 0), WIN_SIZE), 3)


def draw_selected(
    surface: pygame.Surface, posgrid: PosType, player: Player
) -> None:
    if player.pos_pieces[posgrid]:
        pygame.draw.rect(
            surface,
            PLAYER_COLOR[player.ply-1],
            (
                posgrid[0] * TILE_SIZE[0], posgrid[1] * TILE_SIZE[1],
                TILE_SIZE[0], TILE_SIZE[1],
            ),
            3
        )


def draw_player(surface: pygame.Surface, player: Player) -> None:
    for i in range(10):
        for j in range(10):
            if player.pos_pieces[i, j] == 1:
                centre = (
                    round(i * TILE_SIZE[0] + (TILE_SIZE[0] / 2)),
                    round(j * TILE_SIZE[1] + (TILE_SIZE[1] / 2)),
                )
                radius = round(TILE_SIZE[0] / 2 * (9 / 10))
                pygame.draw.circle(surface, PLAYER_COLOR[player.ply-1], centre, radius)
            elif player.pos_pieces[i, j] == 2:
                centre = (
                    round(i * TILE_SIZE[0] + (TILE_SIZE[0] / 2)),
                    round(j * TILE_SIZE[1] + (TILE_SIZE[1] / 2)),
                )
                radius = round(TILE_SIZE[0] / 2 * (9 / 10))
                pygame.draw.circle(surface, PLAYER_COLOR[player.ply-1], centre, radius)
                invcol = (
                    255 - PLAYER_COLOR[player.ply-1][0],
                    255 - PLAYER_COLOR[player.ply-1][1],
                    255 - PLAYER_COLOR[player.ply-1][2],
                )
                radius = round(TILE_SIZE[0] / 2 * (2 / 10))
                pygame.draw.circle(surface, invcol, centre, radius)
                pygame.draw.circle(
                    surface, invcol, (centre[0] + 10, centre[1]), radius
                )
                pygame.draw.circle(
                    surface, invcol, (centre[0], centre[1] + 10), radius
                )
                pygame.draw.circle(
                    surface, invcol, (centre[0] - 10, centre[1]), radius
                )
                pygame.draw.circle(
                    surface, invcol, (centre[0], centre[1] - 10), radius
                )


def select_piece(
    player: Player,
    selected: Optional[PosType],
    moveto: Optional[PosType],
    event: EventType
) -> Union[bool, PosType]:
    pos = event.dict["pos"]
    posgrid = (pos[0] // TILE_SIZE[0], pos[1] // TILE_SIZE[1])
    if (selected is None) and (moveto is None):
        if player.pos_pieces[posgrid]:
            return posgrid
        return False
    if (selected is not None) and (moveto is None):
        return posgrid
    return False


def switch_turn(board: BoardType, turn: int, sel: PosType) -> int:
    print("SWITCH TURN")
    print("Board:",board)
    if board[sel[0]][sel[1]] == 0:
        return turn
    _, ply_val = board[sel[0]][sel[1]]
    if turn == 1:
        near_enemy = []
        dir_enemy = []
        for i, j in [(x, y) for x in [-1, 1] for y in [-1, 1]]:
            if (
                (sel[0] + i < 0) or (sel[0] + i >= 10) or
                (sel[1] + j < 0) or (sel[1] + j >= 10)
            ):
                continue
            if (
                board[sel[0] + i][sel[1] + j] == ("ply2", 1) or
                board[sel[0] + i][sel[1] + j] == ("ply2", 2)
            ):
                near_enemy.append((sel[0] + i, sel[1] + j))
                dir_enemy.append((i, j))
                newpos = (
                    near_enemy[-1][0] + dir_enemy[-1][0],
                    near_enemy[-1][1] + dir_enemy[-1][1],
                )
                print("Newpos0=",newpos[0],"Newpos1=",newpos[1])
                if (
                    (newpos[0] < 0) or (newpos[0] >= 10) or
                    (newpos[1] < 0) or (newpos[1] >= 10)
                ):
                    if board[newpos[0]][newpos[1]] == 0:
                        if (ply_val == 1) and (dir_enemy[-1][1] == -1):
                            pass
                        else:
                            return 1
        return 2
    else:
        near_enemy = []
        dir_enemy = []
        for i, j in [(x, y) for x in [-1, 1] for y in [-1, 1]]:
            if (
                (sel[0] + i < 0) or (sel[0] + i >= 10) or
                (sel[1] + j < 0) or (sel[1] + j >= 10)
            ):
                continue
            if (
                board[sel[0] + i][sel[1] + j] == ("ply1", 1) or
                board[sel[0] + i][sel[1] + j] == ("ply1", 2)
            ):
                near_enemy.append((sel[0] + i, sel[1] + j))
                dir_enemy.append((i, j))
                newpos = (
                    near_enemy[-1][0] + dir_enemy[-1][0],
                    near_enemy[-1][1] + dir_enemy[-1][1],
                )
                if (
                    (newpos[0] < 0) or (newpos[0] >= 10) or
                    (newpos[1] < 0) or (newpos[1] >= 10)
                ):
                    if board[newpos[0]][newpos[1]] == 0:
                        if (ply_val == 1) and (dir_enemy[-1][1] == 1):
                            pass
                        else:
                            return 2
        return 1


def copy_board(board: BoardType) -> BoardType:
    copy: BoardType = [[0 for _ in range(10)] for _ in range(10)]
    for i in range(10):
        for j in range(10):
            copy[i][j] = board[i][j]
    return copy


def clear() -> None:
    os.system("cls")


def print_score(ply1: Player, ply2: Player) -> None:
    score_str = ""
    score_str += "+------------------------------+\n"
    score_str += "|                              |\n"
    score_str += "|  SCORE:                      |\n"
    score_str += "|                              |\n"
    score_str += \
        f"|  Player1: {ply1.n_eaten:>2}    Player2: {ply2.n_eaten:>2}  |\n"
    score_str += "|                              |\n"
    score_str += "+------------------------------+\n"
    print(score_str)
    if ply1.n_eaten == 15:
        print("\nPLAYER1 WON!")
    elif ply2.n_eaten == 15:
        print("\nPLAYER2 WON!")


if __name__ == "__main__":

    pygame.display.init()
    pygame.display.set_caption("Checker Minimax")
    surface = pygame.display.set_mode(WIN_SIZE)
    clock = pygame.time.Clock()

    gameboard = CheckerBoard()
    player1 = Player(1)
    player2 = Player(2)
    ai = Minimax(ply_num=1)

    gameboard.update_board(player1.pos_pieces, player2.pos_pieces)

    clear()
    print(gameboard)

    selected = None
    moveto = None
    turn = random.choice([1, 2])

    print_score(player1, player2)
    print(f"Player{turn}'s turn\n. . . . . . . .")

    while True:
        draw_board(surface, turn)
        draw_player(surface, player1)
        draw_player(surface, player2)
        player = player1 if (turn == 1) else player2

        if selected:
            draw_selected(surface, selected, player)

        # detect mouse event
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                print("selected before",selected)
                if selected:
                    tmp = select_piece(player, selected, moveto, event)
                    if tmp != selected:
                        moveto = tmp #selected not none, move from selected to new square
                        print("move to:",moveto)
                else:
                    selected = select_piece(player, selected, moveto, event)
                print("selected after:",selected)

        # AI's turn
        if player == player1:
            board = copy_board(gameboard.board)
            try:
                _, ai_move = ai.minimax(board, 100, True)
                selected, moveto = ai_move
            except TypeError:
                selected = None
                moveto = None
        # move piece
        if moveto is not None:
            if player == player1:
                tmp = player1.move(selected, moveto, gameboard.board)
                player2.update_dead(tmp)
                print("p1 move")
                print("tmp=",tmp)
            else:
                tmp = player2.move(selected, moveto, gameboard.board)
                player1.update_dead(tmp)
                print("p2 move")
                print("tmp=",tmp)

            # update the position of the player's pieces
            gameboard.update_board(player1.pos_pieces, player2.pos_pieces)
            print("board update")
            if tmp is not False:
                #clear()
                old_turn = turn
                if not(isinstance(tmp, tuple) and player.has_forced_moves(gameboard.board)):
                    turn = 1 if (turn == 2) else 2
                if old_turn != turn:
                    print(f"Player{turn}'s turn\n. . . . . . . .")
                    old_turn = turn
                print_score(player1, player2)

            moveto = None
            selected = None

        pygame.display.flip()
