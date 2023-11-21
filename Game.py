import pygame, Button, Solver
from App import WINDOW

class Game:
    def __init__(self, gridColor=(0, 0, 0), solutionColor=(136, 8, 8), backgroundColor=(255, 255, 255), gridOuterWidth=4, gridInnerWidth=1):
        self.gameRunning = True
        self.boardSolved = False
        self.buttons = []

        self.gridColor = gridColor
        self.solutionColor = solutionColor
        self.backgroundColor = backgroundColor
        self.gridOuterWidth = gridOuterWidth
        self.gridInnerWidth = gridInnerWidth

        self.board = self.generate_board()
        self.unchangingBoard = self.generate_board()
        self.solver = Solver.sudokuSolver(self.board)

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
    
    def drawBoard(self):

        WINDOW.screen.fill(self.backgroundColor)
        self.drawGrid(self.gridColor, self.gridOuterWidth, self.gridInnerWidth)
        self.initializeBoard()
        
        if not self.buttons:
            solve_img = pygame.image.load('images/solve.jpg').convert_alpha()
            self.initializeButton(100, 1025, solve_img)
            restart_img = pygame.image.load('images/restart.png').convert_alpha()
            self.initializeButton(600, 1040, restart_img)

        for button in self.buttons:
            button.draw()

    def drawGrid(self, gridColor, borderWidth, innerLineWidth):
        pygame.init()

        for i in range(0, 10):
            if i % 3 == 0:
                pygame.draw.line(WINDOW.screen, gridColor, (100 + 100 * i, 100), (100 + 100 * i, 1000), borderWidth)
                pygame.draw.line(WINDOW.screen, gridColor, (100, 100 + 100 * i), (1000, 100 + 100 * i), borderWidth)

            pygame.draw.line(WINDOW.screen, gridColor, (100 + 100 * i, 100), (100 + 100 * i, 1000), innerLineWidth)
            pygame.draw.line(WINDOW.screen, gridColor, (100, 100 + 100 * i), (1000, 100 + 100 * i), innerLineWidth)

        pygame.display.update()

    def initializeBoard(self):
        font = pygame.font.SysFont('Arial', 70)
        for i in range(len(self.board[0])):
            for j in range(len(self.board[0])):
                if 0 < self.board[i][j] < 10:
                    cellValue = font.render(str(self.board[i][j]), True, self.gridColor)
                    WINDOW.screen.blit(cellValue, ((j + 1) * 100 + 30, (i + 1) * 100 + 15))
        pygame.display.update()

    def initializeButton(self, x, y, icon):
        newButton = Button.ButtonRectangular(x, y, icon)
        self.buttons.append(newButton)

    def populateSolution(self):
        self.board = self.solver.solveBoard()
        font = pygame.font.SysFont('Arial', 70)
        for row in range(len(self.board[0])):
            for column in range(len(self.board[0])):
                if 0 < self.board[row][column] < 10 and self.board[row][column] != self.unchangingBoard[row][column]:
                    cellValue = font.render(str(self.board[row][column]), True, self.solutionColor)
                    WINDOW.screen.blit(cellValue, ((column + 1) * 100 + 30, (row + 1) * 100 + 15))
        pygame.display.update()