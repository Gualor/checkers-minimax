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