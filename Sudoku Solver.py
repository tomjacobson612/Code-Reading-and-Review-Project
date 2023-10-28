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
solve_img = pygame.image.load('solve.jpg').convert_alpha()
solve_button = Button(100, 1025, solve_img)

restart_img = pygame.image.load('restart.png').convert_alpha()
restart_button = Button(600, 1040, restart_img)

class Game:
    def __init__(self):
        self.running = True
        self.solved = False

        #Colors
        self.og_grid_color = (0, 0, 0)
        self.solved_color = (136, 8, 8)

        #Board
        # self.response = requests.get('https://sugoku.herokuapp.com/board?difficulty=easy')
        self.board = self.generate_board()
        self.board_unchanging = self.generate_board()

    def on_init(self):
        pygame.init()
        self.running = True

    def generate_board(self) -> list[list[int]]:
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

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False

    def draw_grid(self):
        pygame.init()
        displayWindow.fill(backgroundColor)

        for i in range(0, 10):
            if i % 3 == 0:
                pygame.draw.line(displayWindow, (0, 0, 0), (100 + 100 * i, 100), (100 + 100 * i, 1000), 4)
                pygame.draw.line(displayWindow, (0, 0, 0), (100, 100 + 100 * i), (1000, 100 + 100 * i), 4)

            pygame.draw.line(displayWindow, (0, 0, 0), (100 + 100 * i, 100), (100 + 100 * i, 1000), 1)
            pygame.draw.line(displayWindow, (0, 0, 0), (100, 100 + 100 * i), (1000, 100 + 100 * i), 1)

        pygame.display.update()

    def populate_grid(self):
        font = pygame.font.SysFont('Arial', 70)
        for i in range(len(self.board[0])):
            for j in range(len(self.board[0])):
                if 0 < self.board[i][j] < 10:
                    value = font.render(str(self.board[i][j]), True, self.og_grid_color)
                    displayWindow.blit(value, ((j + 1) * 100 + 30, (i + 1) * 100 + 15))
        pygame.display.update()

    def check_board(self):
        # check rows:
        for i in range(len(self.board)):
            seen = []
            for j in range(len(self.board[0])):
                if self.board[i][j] not in seen and self.board[i][j] != 0:
                    seen.append(self.board[i][j])
                elif self.board[i][j] != 0 and self.board[i][j] in seen:
                    return False

        # check columns:
        for i in range(len(self.board[0])):
            seen = []
            for j in range(len(self.board)):
                if self.board[j][i] not in seen and self.board[j][i] != 0:
                    seen.append(self.board[j][i])
                elif self.board[j][i] != 0 and self.board[j][i] in seen:
                    return False

        # check each 3x3
        row = 0
        column = 0
        while row < 9 and column < 9:
            seen = []
            for i in range(row, row + 3):
                for j in range(column, column + 3):
                    if self.board[i][j] not in seen and self.board[i][j] != 0:
                        seen.append(self.board[i][j])
                    elif self.board[i][j] != 0 and self.board[i][j] in seen:
                        return False
            if column < 9:
                column += 3
                if column == 9:
                    column = 0
                    row += 3

        return True

    def find_next_empty(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] == 0:
                    return (i, j)  # row and column
        return None

    def solve(self):
        found = self.find_next_empty()

        if not found:  # No empty spaces left
            return True
        else:
            for i in range(1, 10):
                self.board[found[0]][found[1]] = i
                if self.check_board():
                    if self.solve():
                        self.solved = True
                        return self.board
                self.board[found[0]][found[1]] = 0
        return False

    def populate_solved(self):
        font = pygame.font.SysFont('Arial', 70)
        for i in range(len(self.board[0])):
            for j in range(len(self.board[0])):
                if 0 < self.board[i][j] < 10 and self.board[i][j] != self.board_unchanging[i][j]:
                    value = font.render(str(self.board[i][j]), True, self.solved_color)
                    displayWindow.blit(value, ((j + 1) * 100 + 30, (i + 1) * 100 + 15))
        pygame.display.update()

def main():
    app = Game()
    app.draw_grid()
    app.populate_grid()

    while True:
        if restart_button.draw():
            app = Game()
            app.draw_grid()
            app.populate_grid()
        if solve_button.draw() and not app.solved:
            app.solve()
            app.populate_solved()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        pygame.display.update()

if __name__ == "__main__" :
    main()
