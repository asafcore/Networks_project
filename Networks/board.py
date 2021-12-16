from itertools import groupby, chain

EMPTY = '_'
PLAYER = 'B'
SERVER = 'Y'
NUMCOL = 7
NUMLI = 6

class Board:

    def diagonalsPos(self, cols, rows):
        for di in ([(j, i - j) for j in range(cols)] for i in range(cols + rows - 1)):
            yield [self.gameboard[i][j] for i, j in di if 0 <= i < cols and 0 <= j < rows]


    def diagonalsNeg(self, cols, rows):
        for di in ([(j, i - cols + j + 1) for j in range(cols)] for i in range(cols + rows - 1)):
            yield [self.gameboard[i][j] for i, j in di if 0 <= i < cols and 0 <= j < rows]



    def __init__(self, cols=NUMCOL, rows=NUMLI):
        self.cols = cols
        self.rows = rows
        self.gameboard = [[EMPTY] * rows for _ in range(cols)]

    def insert(self, col, kind):
        col  = int(col)
        if 0 <= col < NUMCOL:
            c = self.gameboard[col-1]
            for i, value in enumerate(c):
                if value == EMPTY:
                    c[i] = kind
                    return True
        print("column is full, pick again!")
        return False

    def theWinner(self):
        lines = (
            self.gameboard,  # columns
            zip(*self.gameboard),  # rows
            self.diagonalsPos(self.cols, self.rows),  # positive diagonals
            self.diagonalsNeg(self.cols, self.rows)  # negative diagonals
        )

        for line in chain(*lines):
            for color, group in groupby(line):
                if color != EMPTY and len(list(group)) >= 4:
                    return color
        return False

    def checkForWin(self):
        w = self.theWinner()
        if w:
            self.printBoard()
            print(f"{w} Won!")
            return w
        return False

    def printBoard(self):
        print('  '.join(map(str, range(self.cols))))
        for y in range(self.rows):
            print('  '.join(str(self.gameboard[x][y]) for x in range(self.cols)))
