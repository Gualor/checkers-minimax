from typing import Optional, Union
import random
import os

import pygame
from pygame.event import EventType

from checkers import CheckerBoard, Player, PosType, BoardType
from minimax import Minimax

# Defining window size and colours used for the game
WIN_SIZE = (WIDTH, HEIGHT) = (600, 600)
TILE_SIZE = (WIN_SIZE[0] // 10, WIN_SIZE[1] // 10)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORANGE = (255, 156, 0)
BLUE = (1, 212, 180)
BOARD_COLOR = [WHITE, BLACK]
PLAYER_COLOR = [ORANGE, BLUE]


def draw_board(surface: pygame.Surface, turn: int) -> None:
    surface.fill(BOARD_COLOR[0]) # Fills entire surface of window with a white
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
                (i, j, TILE_SIZE[0], TILE_SIZE[1]), # Draw squares/board tiles in both x and y direction in black and white 
            )
    pygame.draw.rect(surface, PLAYER_COLOR[turn-1], ((0, 0), WIN_SIZE), 3) # Draw outline with colour of the current players turn


def draw_selected(
    surface: pygame.Surface, posgrid: PosType, player: Player
) -> None:
    if player.pos_pieces[posgrid]: #If there is a piece belonging to the current player at chosen square
        pygame.draw.rect(
            surface,
            PLAYER_COLOR[player.ply-1],
            (
                posgrid[0] * TILE_SIZE[0], posgrid[1] * TILE_SIZE[1],
                TILE_SIZE[0], TILE_SIZE[1],
            ),
            3
        ) # Draw rectangle outline around the square to show it has been selected


def draw_player(surface: pygame.Surface, player: Player) -> None:
    for i in range(10):
        for j in range(10): # For every square in x and y direction
            if player.pos_pieces[i, j] == 1: # If selected square has one of the chosen players counters in
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
    pos = event.dict["pos"] # Extract the position of the mouse click
    posgrid = (pos[0] // TILE_SIZE[0], pos[1] // TILE_SIZE[1]) # Calculates grid position using mouse click position
    if (selected is None) and (moveto is None): # Checks if no piece is currently selected and there is no pending moves
        if player.pos_pieces[posgrid]: # If there is a piece belonging to the player at clicked grid
            return posgrid
        return False
    if (selected is not None) and (moveto is None):
        return posgrid
    return False



def copy_board(board: BoardType) -> BoardType:
    copy: BoardType = [[0 for _ in range(10)] for _ in range(10)] # Initializes a new 10 x 10 matrix with 0s
    for i in range(10):
        for j in range(10):
            copy[i][j] = board[i][j] # For each position on this new matrix/board, fill it with contents of the original board
    return copy # Return the copied board


def clear() -> None:
    os.system("cls") # Clear the contents of the terminal



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
    if ply1.n_eaten == 15: # If player one taken all opposing pieces, announce player one wins
        print("\nPLAYER1 WON!")
    elif ply2.n_eaten == 15: # If player two taken all opposing pieces, announce player two wins
        print("\nPLAYER2 WON!")


if __name__ == "__main__": # Code begins running here

    pygame.display.init() # Initializes Pygames display module allowing for window creation and display settings
    pygame.display.set_caption("Checker Minimax") # Creating title of window
    surface = pygame.display.set_mode(WIN_SIZE) # Creating a game window surface
    clock = pygame.time.Clock()

    gameboard = CheckerBoard() # Creates instance of checkerboard class to represent gameboard
    player1 = Player(1) # Creates an instance of the Player class for player 1, passing 1 as the player's ID
    player2 = Player(2) # Creates an instance of the Player class for player 2, passing 2 as the player's ID
    ai = Minimax(ply_num=1) # Creates instance of the Minimax class, representing the AI player

    gameboard.update_board(player1.pos_pieces, player2.pos_pieces) # Update the board with required graphics such as pieces

    clear() # Clear terminal
    print(gameboard) # Print the current gameboard

    selected = None
    moveto = None
    movedfrom = (100,100)
    lastmove = None
    taken = False
    turn = random.choice([1, 2]) # Initialise variables to track the game activity

    print_score(player1, player2)
    print(f"Player{turn}'s turn\n. . . . . . . .")

    while True: # Game Loop
        draw_board(surface, turn) # Draw the game board on Pygame surface
        draw_player(surface, player1) # Draw the pieces of Player 1 on the Pygame surface
        draw_player(surface, player2) # Draw the pieces of Player 2 on the Pygame surface
        player = player1 if (turn == 1) else player2 # Switch the turn/ Switch the next player to move

        if selected: # If a square has been selected by a mouse click
            draw_selected(surface, selected, player) # Draw an outline around selected square

        # detect mouse event
        for event in pygame.event.get(): # Iterate through all events detected, this line will be ran infinitely until an event such as mouseclick
            if event.type == pygame.MOUSEBUTTONDOWN:
                if selected:
                    tmp = select_piece(player, selected, moveto, event)
                    if tmp != selected:
                        moveto = tmp #selected not none, move from selected to new square
                else:
                    selected = select_piece(player, selected, moveto, event)
                    movedfrom = selected # Selected square will be where the counter is moving from, hence define position of moved from

        #AI's turn
        if player == player1: # If it is the AI's turn
            board = copy_board(gameboard.board) # Make a copy of the board
            try: # Try make an AI move
                _, ai_move = ai.minimax(board, 100, True) # Use minimax to find AI's move
                selected, moveto = ai_move 
            except TypeError: 
                selected = None
                moveto = None # Reset selected and moveto upon error in minimax
        #move piece
        
        if moveto is not None: # Due to while True loop, will run over and over -  Waits till moveto != None
            if player == player1:
                check = "ply1"
                tmp = player1.move(selected, moveto, gameboard.board,taken,lastmove,movedfrom)
                player2.update_dead(tmp)
            else:
                check = "ply2"
                tmp = player2.move(selected, moveto, gameboard.board,taken,lastmove,movedfrom)
                player1.update_dead(tmp)

            # update the position of the player's pieces
            forced_moves_before = player.check_forced_move(gameboard.board) 
            gameboard.update_board(player1.pos_pieces, player2.pos_pieces)
            if tmp is not False:
                taken = True if abs(movedfrom[0]-moveto[0]) == 2 else False
                clear()
                old_turn = turn
                turn = 1 if (turn == 2) else 2
                if isinstance(tmp, tuple) and player.has_forced_moves(gameboard.board):
                    for move in forced_moves_before:
                        if move[0] == moveto:
                            turn = old_turn
                            break
                taken = False if turn != old_turn else taken
                if old_turn != turn:
                    print(f"Player{turn}'s turn\n. . . . . . . .")
                    old_turn = turn
                print_score(player1, player2)

                lastmove = moveto

            moveto = None
            selected = None

        pygame.display.flip()
