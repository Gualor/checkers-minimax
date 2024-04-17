from typing import Optional, List, Tuple
import random

from checkers import BoardType, MoveType


class Minimax:
    PIECE_VAL = 10
    KING_VAL = 50
    SIDE_VAL = 20
    WALL_VAL = 10 # Constants for piece values

    def __init__(self, ply_num: int) -> None:
        self.ply = ply_num # Initialize Minimax algorithm with the given player number

    def find_moves(self, board: BoardType) -> List[MoveType]:
        moves = [] # Initialize emtpy list to store possible moves
        for (i, j) in [(i, j) for i in range(10) for j in range(10)]: #  For each position on the board
            if not isinstance(board[i][j], tuple): # Check if position contains a piece belonging to current player
                continue
            ply_str, ply_val = board[i][j]
            if not ply_str == f"ply{self.ply}":
                continue
            for k, h in [(x, y) for x in [-1, 1] for y in [-1, 1]]: # For possible directions to move
                if (
                    (i + k < 0) or (i + k >= 10) or
                    (j + h < 0) or (j + h >= 10) # If move is within bounds of the board
                ):
                    continue
                if ( 
                    (ply_val == 2) or
                    ((h > 0) and (self.ply == 1)) or
                    ((h < 0) and (self.ply == 2)) # Check if move is valid for the current player
                ):
                    if board[i + k][j + h] == 0: # If desired square to move to is empty
                        moves.append(((i, j), (i + k, j + h)))
                        continue
                    dst_str, _ = board[i + k][j + h]
                    if dst_str == f"ply{self.ply}": 
                        continue
                    if (
                        (i + 2 * k < 0) or (i + 2 * k >= 10) or
                        (j + 2 * h < 0) or (j + 2 * h >= 10) # Check if jump is valid
                    ):
                        continue
                    if board[i + 2 * k][j + 2 * h] == 0:
                        moves.append(
                            ((i, j), (i + 2 * k, j + 2 * h))
                        )
        random.shuffle(moves) # Shuffle list of moves to randomise selection
        return moves

    def evaluate_state(self, board: BoardType) -> int:
        value = 0
        n1 = 0
        n2 = 0
        for (i, j) in [(i, j) for i in range(10) for j in range(10)]:
            if not isinstance(board[i][j], tuple):
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
        # - Initializes value, n1, and n2 to zero. value is the score of the state, and n1 and n2 are counters for pieces belonging to two different players
        # - Iterates over each position (i, j) on the board
        # - Checks if the piece at (i, j) on the board belongs to the current player (ply_str == f"ply{self.ply}"). If not, it assumes it belongs to the opponent. If it doesn't belong to any player (isinstance(board[i][j], tuple) evaluates to False), it skips to the next iteration
        # - Depending on the player who owns the piece, it updates the value variable. For the current player (n1), it adds certain values based on the position of the piece and its type (ply_val). For the opponent (n2), it subtracts similar values
        # - If all pieces of the opponent (n2) are captured (n2 == 0) and the current player (n1) has at least one piece on the board, it sets the value to a high positive value (10000). Similarly, if all pieces of the current player (n1) are captured (n1 == 0) and the opponent (n2) has at least one piece on the board, it sets the value to a high negative value (-10000)
        # - Then returns value
    def update_board(self, board: BoardType, move: MoveType) -> BoardType:
        selected = move[0]
        moveto = move[1] # Find selected counter and desired spot to move
        if (
            (abs(selected[0] - moveto[0]) == 2) and
            (abs(selected[1] - moveto[1]) == 2)
        ): # Check if move involves a capture
            dir = (moveto[0] - selected[0], moveto[1] - selected[1]) # Direction of the capture
            board[selected[0] + dir[0]][selected[1] + dir[1]] = 0 # Remove captured piece from the board
        piece = board[selected[0]][selected[1]] # Note piece being moved
        board[moveto[0]][moveto[1]] = piece # Move piece to new location
        board[selected[0]][selected[1]] = 0 # Clear moved piece's original position
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

''' 
General explanation for the Minimax algoithm:
The minimax algorithm is a decision-making approach commonly used in two-player games like chess or tic-tac-toe.
 It works by recursively exploring the game tree, evaluating each possible move and counter-move up to a certain depth or terminal state.
 At each level of the tree, the algorithm alternates between maximizing the score for the current player and minimizing the score for the opponent, assuming optimal play from both sides. 
 The scores are propagated back up the tree, and ultimately, the algorithm selects the move that leads to the best possible outcome based on the computed scores.'''