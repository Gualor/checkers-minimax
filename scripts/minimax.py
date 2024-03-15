import random


class Minimax:
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
