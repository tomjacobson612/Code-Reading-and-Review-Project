import pygame
import requests

# Window
width = 1100
height = 1200
displayWindow = pygame.display.set_mode((width, height))
backgroundColor = (251, 247, 245)
pygame.display.set_caption("Sudoku Solver")

class Button():
    def __init__(self, x, y, icon):
        self.icon = icon
        self.rectangle = self.icon.get_rect()
        self.rectangle.topleft = (x, y)
        self.pressedByUser = False

    def draw(self):
        action = False
        mousePosition = pygame.mouse.get_pos()

        #check mouseover and clicked conditions
        if self.rectangle.collidepoint(mousePosition):
            if pygame.mouse.get_pressed()[0] == 1 and self.pressedByUser == False:
                self.pressedByUser = True
                action = True
            if pygame.mouse.get_pressed()[0] == 0:
                self.pressedByUser = False

        displayWindow.blit(self.icon, (self.rectangle.x, self.rectangle.y))
        return action

# Buttons
solve_img = pygame.image.load('images/solve.jpg').convert_alpha()
solve_button = Button(100, 1025, solve_img)

restart_img = pygame.image.load('images/restart.png').convert_alpha()
restart_button = Button(600, 1040, restart_img)

class Game:
    def __init__(self):
        self.gameRunning = True
        self.boardSolved = False

        self.cellColor = (0, 0, 0)
        self.solutionColor = (136, 8, 8)

        self.board = self.generate_board()
        self.unchangingBoard = self.generate_board()

    def on_init(self):
        pygame.init()
        self.gameRunning = True

    def generate_board(self) -> list[list[int]]:
        # self.response = requests.get('https://sugoku.herokuapp.com/board?difficulty=easy')
        default_grid = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9] ]
        return default_grid

    def drawGrid(self, color, borderWidth, innerLineWidth):
        pygame.init()
        displayWindow.fill(backgroundColor)

        for i in range(0, 10):
            if i % 3 == 0:
                pygame.draw.line(displayWindow, color, (100 + 100 * i, 100), (100 + 100 * i, 1000), borderWidth)
                pygame.draw.line(displayWindow, color, (100, 100 + 100 * i), (1000, 100 + 100 * i), borderWidth)

            pygame.draw.line(displayWindow, color, (100 + 100 * i, 100), (100 + 100 * i, 1000), innerLineWidth)
            pygame.draw.line(displayWindow, color, (100, 100 + 100 * i), (1000, 100 + 100 * i), innerLineWidth)

        pygame.display.update()

    def initializeBoard(self):
        font = pygame.font.SysFont('Arial', 70)
        for i in range(len(self.board[0])):
            for j in range(len(self.board[0])):
                if 0 < self.board[i][j] < 10:
                    cellValue = font.render(str(self.board[i][j]), True, self.cellColor)
                    displayWindow.blit(cellValue, ((j + 1) * 100 + 30, (i + 1) * 100 + 15))
        pygame.display.update()

    def checkBoard(self):
        # check rows:
        for row in range(len(self.board)):
            checked = []
            for column in range(len(self.board[0])):
                if self.board[row][column] not in checked and self.board[row][column] != 0:
                    checked.append(self.board[row][column])
                elif self.board[row][column] != 0 and self.board[row][column] in checked:
                    return False

        # check columns:
        for row in range(len(self.board[0])):
            checked = []
            for column in range(len(self.board)):
                if self.board[column][row] not in checked and self.board[column][row] != 0:
                    checked.append(self.board[column][row])
                elif self.board[column][row] != 0 and self.board[column][row] in checked:
                    return False

        # check each 3x3
        row = 0
        column = 0
        while row < 9 and column < 9:
            checked = []
            for row in range(row, row + 3):
                for column in range(column, column + 3):
                    if self.board[row][column] not in checked and self.board[row][column] != 0:
                        checked.append(self.board[row][column])
                    elif self.board[row][column] != 0 and self.board[row][column] in checked:
                        return False
            if column < 9:
                column += 3
                if column == 9:
                    column = 0
                    row += 3

        return True

    def nextEmptyCell(self):
        for row in range(len(self.board)):
            for column in range(len(self.board[0])):
                if self.board[row][column] == 0:
                    return (row, column)
        return None

    def solveBoard(self):
        emptyCell = self.nextEmptyCell()

        if not emptyCell:
            return True
        else:
            for i in range(1, 10):
                self.board[emptyCell[0]][emptyCell[1]] = i
                if self.checkBoard():
                    if self.solveBoard():
                        self.boardSolved = True
                        return self.board
                self.board[emptyCell[0]][emptyCell[1]] = 0
        return False

    def populateSolution(self):
        font = pygame.font.SysFont('Arial', 70)
        for row in range(len(self.board[0])):
            for column in range(len(self.board[0])):
                if 0 < self.board[row][column] < 10 and self.board[row][column] != self.unchangingBoard[row][column]:
                    cellValue = font.render(str(self.board[row][column]), True, self.solutionColor)
                    displayWindow.blit(cellValue, ((column + 1) * 100 + 30, (row + 1) * 100 + 15))
        pygame.display.update()

def main():
    app = Game()
    app.drawGrid((0, 0, 0), 4, 1)
    app.initializeBoard()

    while True:
        if restart_button.draw():
            app = Game()
            app.drawGrid((0, 0, 0), 4, 1)
            app.initializeBoard()
        if solve_button.draw() and not app.boardSolved:
            app.solveBoard()
            app.populateSolution()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        pygame.display.update()

if __name__ == "__main__" :
    main()
