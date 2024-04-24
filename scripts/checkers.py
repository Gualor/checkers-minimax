from typing import Tuple, Union, List, Optional
import numpy as np


PosType = Tuple[int, int]
BoardElemType = Union[int, Tuple[str, int]]
BoardType = List[List[BoardElemType]]
MoveType = Tuple[PosType, PosType] # Set variable types


class CheckerBoard:
    def __init__(self) -> None:
        self.board: BoardType = [[0 for _ in range(10)] for _ in range(10)] # Initialised the board as a 10 x 10 grid with each cell empty

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
        return board_str #Returns the board as a string representation

    def update_board(self, ply1: np.ndarray, ply2: np.ndarray) -> None:
        for i in range(10):
            for j in range(10): # For each square
                if ply1[i][j] > 0: # If player 1 counter at square
                    self.board[i][j] = ("ply1", ply1[i][j])
                elif ply2[i][j] > 0: # If player 2 counter at square
                    self.board[i][j] = ("ply2", ply2[i][j])
                else:
                    self.board[i][j] = 0


class Player:
    N_MEN: int = 15
    N_KING: int = 0 # Defines initial number of counters and king counters as constants

    def __init__(
        self,
        num: int,
        n_men: Optional[int] = None,
        n_kings: Optional[int] = None,
    ) -> None: # Initialise a Player object
        self.n_men = Player.N_MEN if n_men is None else n_men
        self.n_kings = Player.N_KING if n_kings is None else n_kings
        self.n_eaten = 0 # How many counters the player has taken
        self.ply = num # Player number
        self.init_pos() # Initialise player's starting position on the board

    def init_pos(self) -> None:
        self.pos_pieces = np.zeros(shape=(10, 10), dtype=int) # Initialise 10 x 10 board
        tot_pieces = self.n_men + self.n_kings
        n_men = 0
        n_kings = 0
        for y1 in range(tot_pieces // 5): # Loop through rows and columns to place pieces
            for x in range(0, 10, 2):
                if n_men < self.n_men: # Place regular counterss
                    n_men += 1
                    val = 1
                elif n_kings < self.n_kings: # Place king counters
                    n_kings += 1
                    val = 2
                else:
                    return # Return once limit reached
                if self.ply == 1:
                    self.pos_pieces[x + (y1 % 2), y1] = val
                elif self.ply == 2:
                    y2 = 9 - y1
                    self.pos_pieces[x + (y2 % 2), y2] = val

    def move(
        self, selected: PosType, moveto: PosType, board: BoardType, taken: bool, lastmove: PosType,movedfrom: PosType, makemove: bool
    ) -> bool:
        moves = self.check_forced_move(board) # Check if there are any forced moves availible
        if ((selected, moveto) in moves) or (len(moves) == 0): 
            dead = self.check_eating_move(selected, moveto, board) # Checking if the move involves eating a piece
            if not dead:
                # moves without eating pieces
                if self.check_valid_move(selected, moveto, board):
                    # update position from selected to moveto
                    if makemove:
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
                if taken == True and lastmove != movedfrom: # Added by James
                    return False # Return invalid move if the eating move is not made by the previously moved piece, given that piece ate on the previous move
                # valid eating move
                if makemove:
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
        moves = [] # Initialise empty list to store forced moves
        for i in range(10):
            for j in range(10): # For each position on the board
                if self.pos_pieces[i, j] == 0: # Check if there is a piece at current position
                    continue
                selected = (i, j) # Store position of found piece
                for k in range(-2, 3, 4):
                    for h in range(-2, 3, 4): # For diagonal moves with distance of 2
                        moveto = (k + i, h + j)
                        if (
                            (moveto[0] < 0) or (moveto[0] >= 10) or
                            (moveto[1] < 0) or (moveto[1] >= 10)
                        ): # Check if found move is within the board's boundaries
                            continue
                        if self.check_eating_move(selected, moveto, board): # If move is an eating move
                            moves.append((selected, moveto)) # Add this found move to the list of forced moves
        return moves # Return list of force moves found
    
    def has_forced_moves(self, board: BoardType) -> bool:
        return len(self.check_forced_move(board)) > 0 # Return True if there is a forced move the player must do
    
    def check_eating_move(
        self, selected: PosType, moveto: PosType, board: BoardType
    ) -> Union[bool, PosType]:
        dir = (
            np.sign(moveto[0] - selected[0]),
            np.sign(moveto[1] - selected[1]) # Determine direction of the move
        )
        if self.ply == 1 and self.pos_pieces[selected] == 1: # Check if player 1s piece can move in specified direction
            if dir[1] < 0:
                return False
        elif self.ply == 2 and self.pos_pieces[selected] == 1: # Check if player 2s piece can move in specified direction
            if dir[1] > 0:
                return False
        if (
            (board[selected[0] + dir[0]][selected[1] + dir[1]] != 0) and
            (board[selected[0] + dir[0]][selected[1] + dir[1]] != (f"ply{self.ply}", 1)) and
            (board[selected[0] + dir[0]][selected[1] + dir[1]] != (f"ply{self.ply}", 2)) # Check if sqaure doesnt contain a counter
        ):
            if (
                (abs(selected[0] - moveto[0]) == 2) and
                (abs(selected[1] - moveto[1]) == 2) and
                (board[moveto[0]][moveto[1]] == 0) # Check if move involves taking a piece (jumping over it)
            ):
                return (selected[0] + dir[0], selected[1] + dir[1]) # If so return position of move
            return False
        return False # Return False if conditions are not met

    def check_valid_move(
        self, selected: PosType, moveto: PosType, board: BoardType
    ) -> bool:
        if board[selected[0]][selected[1]] == 0: # If there is not piece at selected square to move from, move cannot be valid 
            return False
        if board[moveto[0]][moveto[1]] != 0: # If there is a piece at specified square wanting to move to, move cannot be valid
            return False
        _, ply_val = board[selected[0]][selected[1]] # Find piece type at given position
        if ply_val == 2: # If regular piece for player 2
            if (
                (abs(moveto[0] - selected[0]) == 1) and
                (abs(moveto[1] - selected[1]) == 1)
            ):
                return True
        elif ply_val == 1: # If regular piece for player 1
            if abs(moveto[0] - selected[0]) == 1:
                if (self.ply == 1) and ((moveto[1] - selected[1]) == 1):
                    return True
                if (self.ply == 2) and ((moveto[1] - selected[1]) == -1):
                    return True # Return valid if move is of the right magnitude and direction
        return False

    def promote_king(self, pos: PosType) -> None:
        self.pos_pieces[pos] = 2 # Promote piece in position pos to a king piece

    def update_dead(self, dead: PosType) -> None:
        if not (dead is True or dead is False):
            self.pos_pieces[dead] = 0 # Update the position on the board to indicate there is no piece there anymore
