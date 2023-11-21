class sudokuSolver:
    def __init__(self, board):
        self.boardToSolve = board

    def validateBoard(self):
        if not self.validateRow() or not self.validateColumn() or not self.validate3x3():
            return False
        else:
            return True

    def validateRow(self):
        for row in range(len(self.boardToSolve)):
            checked = []
            for column in range(len(self.boardToSolve[0])):
                if self.boardToSolve[row][column] not in checked and self.boardToSolve[row][column] != 0:
                    checked.append(self.boardToSolve[row][column])
                elif self.boardToSolve[row][column] != 0 and self.boardToSolve[row][column] in checked:
                    return False
        return True
    
    def validateColumn(self):
        for row in range(len(self.boardToSolve[0])):
            checked = []
            for column in range(len(self.boardToSolve)):
                if self.boardToSolve[column][row] not in checked and self.boardToSolve[column][row] != 0:
                    checked.append(self.boardToSolve[column][row])
                elif self.boardToSolve[column][row] != 0 and self.boardToSolve[column][row] in checked:
                    return False
        return True
    
    def validate3x3(self):
        startRow = 0
        startColumn = 0
        while startRow < 9 and startColumn < 9:
            checked = []
            for row in range(startRow, startRow + 3):
                for column in range(startColumn, startColumn + 3):
                    if self.boardToSolve[row][column] not in checked and self.boardToSolve[row][column] != 0:
                        checked.append(self.boardToSolve[row][column])
                    elif self.boardToSolve[row][column] != 0 and self.boardToSolve[row][column] in checked:
                        return False
            if startColumn < 9:
                startColumn += 3
                if startColumn == 9:
                    startColumn = 0
                    startRow += 3
        return True

    def nextEmptyCell(self):
        for row in range(len(self.boardToSolve)):
            for column in range(len(self.boardToSolve[0])):
                if self.boardToSolve[row][column] == 0:
                    return (row, column)
        return None

    def solveBoard(self):
        emptyCell = self.nextEmptyCell()

        if not emptyCell:
            return True
        else:
            for i in range(1, 10):
                self.boardToSolve[emptyCell[0]][emptyCell[1]] = i
                if self.validateBoard():
                    if self.solveBoard():
                        self.boardToSolveSolved = True
                        return self.boardToSolve
                self.boardToSolve[emptyCell[0]][emptyCell[1]] = 0
        return False